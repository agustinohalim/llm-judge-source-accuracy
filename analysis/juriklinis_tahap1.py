"""Tahap 1 JuriKlinis: bias perbandingan naif dokter lawan LLM dari vonis juri terbit VeriFact-BHC v1.1.0.

Untuk tiap setelan juri yang menilai klaim atomik kedua sumber (rencana: 126 = 9 model x 14 alias), pada klaim
yang divonis setelan itu: tingkat klaim bukan Supported per sumber menurut label konsensus dokter (`human_gt`)
dan menurut juri; Δ sebenarnya dan Δ naif (dokter − LLM); bias = Δ naif − Δ; selang bootstrap persentil 95 %
dengan pasien sebagai unit ambil ulang; peluang tanda Δ naif terbalik; sensitivitas dan spesifisitas juri per
sumber. Biner, semua proposisi termasuk `invalid` (rencana A, butir 3 dan 9).

Ambang aturan henti dikunci 21 Nov 2026 sebelum skrip ini pertama dijalankan (Artikel_JuriKlinis_Rencana.md,
bagian A): bias kecil bila |bias| < 0,02 dan selangnya memuat 0; berhenti bila itu berlaku pada >= 2/3 setelan.
Penaksir terkoreksi dan anggaran label belum di sini. Yang dicetak hanya agregat per setelan juri.

Pakai:
    python analysis/juriklinis_tahap1.py [folder_data]
"""
import math
from fractions import Fraction

import numpy as np
import pandas as pd

from juriklinis_bootstrap import bobot_bootstrap, selang_persentil, timbang
from juriklinis_data import KOLOM_SETELAN, baca_vonis_klaim, cari_folder_rilis, hitung_per_pasien
from juriklinis_markdown import cetak_judul, cetak_markdown

NAMA_SUMBER = {"human": "dokter", "llm": "llm"}
KOLOM_HITUNG = ["n", "benar", "juri", "benar_juri"]
BATAS_BIAS_KECIL = 0.02
BAGIAN_SETELAN_HENTI = Fraction(2, 3)


def main():
    folder_rilis = cari_folder_rilis()
    per_pasien = hitung_per_pasien(baca_vonis_klaim(folder_rilis))
    pasien = np.sort(per_pasien["subject_id"].unique())
    bobot = bobot_bootstrap(len(pasien))
    ringkasan = pd.DataFrame([ringkas_setelan(setelan, kelompok, pasien, bobot)
                              for setelan, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False)])
    cetak_aturan_henti(ringkasan)
    cetak_per_model(ringkasan)
    cetak_per_setelan(ringkasan)


def hitungan_per_sumber(kelompok, pasien):
    return {sumber: {kolom: (kelompok.loc[kelompok["author_type"] == sumber]
                             .set_index("subject_id")[kolom]
                             .reindex(pasien, fill_value=0)
                             .to_numpy(dtype=float))
                     for kolom in KOLOM_HITUNG}
            for sumber in NAMA_SUMBER}


def selisih(jumlah, kolom):
    return jumlah["human"][kolom] / jumlah["human"]["n"] - jumlah["llm"][kolom] / jumlah["llm"]["n"]


def ketepatan(jumlah):
    hasil = {}
    for sumber, nama in NAMA_SUMBER.items():
        per = jumlah[sumber]
        bukan_benar = per["n"] - per["benar"]
        hasil[f"p_{nama}"] = per["benar"] / per["n"]
        hasil[f"q_{nama}"] = per["juri"] / per["n"]
        hasil[f"sens_{nama}"] = per["benar_juri"] / per["benar"]
        hasil[f"spek_{nama}"] = (bukan_benar - per["juri"] + per["benar_juri"]) / bukan_benar
    return hasil


def ringkas_setelan(setelan, kelompok, pasien, bobot):
    hitungan = hitungan_per_sumber(kelompok, pasien)
    titik = timbang(hitungan, np.ones(len(pasien)))
    ulangan = timbang(hitungan, bobot)
    delta, delta_naif = selisih(titik, "benar"), selisih(titik, "juri")
    delta_ulangan, naif_ulangan = selisih(ulangan, "benar"), selisih(ulangan, "juri")
    bias = delta_naif - delta
    bias_bawah, bias_atas = selang_persentil(naif_ulangan - delta_ulangan)
    return {
        **dict(zip(KOLOM_SETELAN, setelan)),
        "n_dokter": int(titik["human"]["n"]),
        "n_llm": int(titik["llm"]["n"]),
        "delta": delta,
        "delta_naif": delta_naif,
        "bias": bias,
        "bias_bawah": bias_bawah,
        "bias_atas": bias_atas,
        "kecil": bool(abs(bias) < BATAS_BIAS_KECIL and bias_bawah <= 0 <= bias_atas),
        "terbalik": bool(delta_naif * delta <= 0),
        "p_terbalik": float(np.mean(naif_ulangan * delta_ulangan <= 0)),
        **ketepatan(titik),
    }


def cetak_aturan_henti(ringkasan):
    banyak = len(ringkasan)
    ambang = math.ceil(BAGIAN_SETELAN_HENTI * banyak)
    kecil = int(ringkasan["kecil"].sum())
    keputusan = "BERHENTI (catatan pendek)" if kecil >= ambang else "LANJUT (penaksir terkoreksi, anggaran label)"
    cetak_judul("Aturan henti (ambang dikunci 21 Nov 2026)")
    print(f"- Setelan juri yang menilai klaim kedua sumber: {banyak}")
    print(f"- Bias kecil (|bias| < {BATAS_BIAS_KECIL} dan selang 95 % memuat 0): {kecil}; ambang henti >= {ambang}")
    print(f"- Tanda Δ naif terbalik pada taksiran titik: {int(ringkasan['terbalik'].sum())}")
    print(f"- Keputusan: {keputusan}")


def cetak_per_model(ringkasan):
    per_model = ringkasan.groupby("model").agg(
        setelan=("rater_alias", "size"),
        bias_median=("bias", "median"),
        bias_min=("bias", "min"),
        bias_maks=("bias", "max"),
        kecil=("kecil", "sum"),
        terbalik=("terbalik", "sum"),
        sens_dokter=("sens_dokter", "median"),
        spek_dokter=("spek_dokter", "median"),
        sens_llm=("sens_llm", "median"),
        spek_llm=("spek_llm", "median"),
    )
    cetak_judul("Per model (median atas setelan; sens/spek = juri mengenali klaim bukan Supported)")
    cetak_markdown(per_model.reset_index())


def cetak_per_setelan(ringkasan):
    urut = ringkasan.sort_values(KOLOM_SETELAN)
    cetak_judul("Bias Δ naif per setelan juri (selang bootstrap persentil 95 %, pasien sebagai unit)")
    cetak_markdown(urut[[*KOLOM_SETELAN, "n_dokter", "n_llm", "delta", "delta_naif", "bias", "bias_bawah",
                         "bias_atas", "kecil", "terbalik", "p_terbalik"]])
    cetak_judul("Tingkat per sumber dan ketepatan juri per setelan (p = dokter berlabel, q = juri)")
    cetak_markdown(urut[[*KOLOM_SETELAN[:3], "p_dokter", "q_dokter", "sens_dokter", "spek_dokter",
                         "p_llm", "q_llm", "sens_llm", "spek_llm"]])


if __name__ == "__main__":
    main()
