"""Analisis pasca-panel JuriKlinis (post hoc, rencana bagian I butir 1–3, 5, 6; dicatat 21 Nov 2026 sebelum dijalankan).

Keputusan terkunci bagian A tidak diubah; skrip ini menambah pembacaan atas ambilan yang sama dengan tahap 2
(`juriklinis_tahap2.py`, benih dan topeng identik):
1. selang tanpa koreksi populasi hingga (lebar untuk tim yang melabel m dari N >> m pasien) untuk label saja, PPI,
   PPI++ per sumber, dan Rogan–Gladen bersama, lalu anggaran label dan rasio varians label saja / PPI per setelan;
3. bias batas Rogan–Gladen bersama (semua 100 pasien berlabel) lawan bias simulasinya pada m = 20;
5. cakupan PPI bila variansnya menganggap klaim bebas (klaster pasien diabaikan), dengan koreksi populasi hingga
   seperti analisis utama;
2. sensitivitas juri (vonis bukan Supported) per sumber di dalam tiap jenis galat dokter;
6. Δ sebenarnya per varian label dan untuk setelan dengan klaim dokter paling sedikit.
Hanya agregat atas setelan juri yang dicetak.

Pakai:
    python analysis/juriklinis_pascapanel.py [folder_data]
"""
import numpy as np
import pandas as pd
from scipy import stats

from juriklinis_bootstrap import TINGKAT_SELANG
from juriklinis_data import (JENIS_KLAIM, KOLOM_SETELAN, LABEL_DIDUKUNG, baca_dokter_acak, baca_proposisi,
                             baca_vonis, cari_folder_rilis, hitung_per_pasien, tandai)
from juriklinis_kepekaan import BENIH_DOKTER_ACAK
from juriklinis_markdown import cetak_judul, cetak_markdown
from juriklinis_penaksir import BUKAN_SUPPORTED_DOKTER, PENAKSIR, rogan_gladen
from juriklinis_pengaruh import TANDA_SELISIH, buat_ambilan, laju_sensus, vektor_kolom
from juriklinis_tahap2 import (AGREGAT_RINGKASAN, BANYAK_LABEL, BENIH_SIMULASI, anggaran_per_setelan, matriks_pasien,
                               nilai_penaksir, ringkas_anggaran, topeng_label)

PENAKSIR_TANPA_KOREKSI = ["klasik", "PPI", "PPI++ berstrata", "RG bersama"]
KLAIM_BEBAS = "PPI, varians klaim bebas"
BATAS_RG = "RG bersama, batas m = 100"
JENIS_GALAT = ["Not Supported", "Not Addressed"]


def main():
    folder_rilis = cari_folder_rilis()
    dokter_acak = baca_dokter_acak(folder_rilis, np.random.default_rng(BENIH_DOKTER_ACAK))
    proposisi = baca_proposisi(folder_rilis).merge(dokter_acak, on="proposition_id", validate="one_to_one")
    klaim = baca_vonis(folder_rilis, proposisi, JENIS_KLAIM)
    hasil = simulasikan_tambahan(hitung_per_pasien(tandai(klaim)))
    cetak_tanpa_koreksi(hasil)
    cetak_batas_rg(hasil)
    cetak_sensitivitas_jenis(klaim)
    cetak_delta({
        "utama": tandai(klaim),
        "satu dokter acak": tandai(klaim, kolom_kebenaran="dokter_acak"),
        "Not Supported saja": tandai(klaim, label_positif="Not Supported"),
        "Not Addressed saja": tandai(klaim, label_positif="Not Addressed"),
    })


def simulasikan_tambahan(per_pasien):
    pasien = np.sort(per_pasien["subject_id"].unique())
    acak = np.random.default_rng(BENIH_SIMULASI)
    topeng = {banyak: topeng_label(len(pasien), banyak, acak) for banyak in BANYAK_LABEL}
    baris = []
    with np.errstate(divide="ignore", invalid="ignore"):
        for setelan, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False):
            baris += baris_setelan(dict(zip(KOLOM_SETELAN, setelan)), matriks_pasien(kelompok, pasien), topeng)
    return pd.DataFrame(baris)


def baris_setelan(identitas, matriks, topeng):
    ambilan_penuh = buat_ambilan(matriks, np.ones((1, len(matriks))), TANDA_SELISIH)
    delta = sum(nilai * laju_sensus(ambilan_penuh, sumber, BUKAN_SUPPORTED_DOKTER)
                for sumber, nilai in TANDA_SELISIH.items())
    batas = rogan_gladen(ambilan_penuh, kalibrasi_bersama=True)[0][0] - delta
    baris = [{**identitas, "penaksir": BATAS_RG, "banyak_label": len(matriks), "bias": batas}]
    for banyak, topeng_banyak in topeng.items():
        ambilan = buat_ambilan(matriks, topeng_banyak, TANDA_SELISIH)
        baris += [{**identitas, "penaksir": nama, "banyak_label": banyak,
                   **nilai_penaksir(PENAKSIR[nama], ambilan, delta, koreksi_populasi=False)}
                  for nama in PENAKSIR_TANPA_KOREKSI]
        baris.append({**identitas, "penaksir": KLAIM_BEBAS, "banyak_label": banyak, **nilai_klaim_bebas(ambilan, delta)})
    return baris


def nilai_klaim_bebas(ambilan, delta):
    taksiran = PENAKSIR["PPI"](ambilan)[0]
    varians = 0.0
    for sumber in ambilan.tanda:
        klaim = ambilan.jumlah @ vektor_kolom([sumber], {"n": 1})
        sisa = ambilan.jumlah @ vektor_kolom([sumber], {"benar": 1, "juri": -1})
        sisa_kuadrat = ambilan.jumlah @ vektor_kolom([sumber], {"benar": 1, "juri": 1, "benar_juri": -2})
        varians = varians + (sisa_kuadrat - sisa ** 2 / klaim) / (klaim - 1) / klaim
    faktor = 1 - ambilan.banyak_label / ambilan.banyak_pasien
    setengah = stats.norm.ppf((1 + TINGKAT_SELANG) / 2) * np.sqrt(faktor * varians)
    return {"bias": np.mean(taksiran - delta), "cakupan": np.mean(np.abs(taksiran - delta) <= setengah),
            "lebar": np.mean(2 * setengah), "terbalik": np.mean(taksiran * delta <= 0), "gagal": 0.0}


def cetak_tanpa_koreksi(hasil):
    simulasi = hasil[hasil["penaksir"] != BATAS_RG]
    cetak_judul("Tanpa koreksi populasi hingga (kecuali baris klaim bebas): ringkasan atas 126 setelan")
    cetak_markdown(simulasi.groupby(["penaksir", "banyak_label"]).agg(**AGREGAT_RINGKASAN).reset_index())
    tanpa_koreksi = simulasi[simulasi["penaksir"].isin(PENAKSIR_TANPA_KOREKSI)]
    anggaran = anggaran_per_setelan(tanpa_koreksi)
    cetak_judul("Anggaran label tanpa koreksi populasi hingga (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai)")
    cetak_markdown(ringkas_anggaran(anggaran, ["penaksir"]))
    cetak_judul("Anggaran label tanpa koreksi, per model")
    cetak_markdown(ringkas_anggaran(anggaran, ["model", "penaksir"]))
    lebar = simulasi.pivot_table(index=["rater_alias", "banyak_label"], columns="penaksir", values="lebar")
    rasio = ((lebar["klasik"] / lebar["PPI"]) ** 2).rename("rasio").reset_index()
    cetak_judul("Rasio varians label saja / PPI per setelan (= kelipatan pasien berlabel yang setara)")
    cetak_markdown(rasio.groupby("banyak_label")["rasio"].describe(percentiles=[0.5])[["min", "50%", "max"]]
                   .reset_index())


def cetak_batas_rg(hasil):
    batas = hasil[hasil["penaksir"] == BATAS_RG].set_index("rater_alias")
    simulasi = hasil[(hasil["penaksir"] == "RG bersama") & (hasil["banyak_label"] == 20)].set_index("rater_alias")
    gabung = pd.DataFrame({"model": batas["model"], "bias_batas": batas["bias"], "bias_m20": simulasi["bias"]})
    cetak_judul("Rogan–Gladen bersama: bias batas (100 pasien berlabel) lawan bias simulasi m = 20, median per model")
    cetak_markdown(gabung.groupby("model")[["bias_batas", "bias_m20"]].median().reset_index())
    print(f"\nKorelasi Pearson atas {len(gabung)} setelan: {gabung['bias_batas'].corr(gabung['bias_m20']):.3f}; "
          f"median |batas − m20| = {(gabung['bias_batas'] - gabung['bias_m20']).abs().median():.3f}; "
          f"median bias batas = {gabung['bias_batas'].median():.3f}")


def cetak_sensitivitas_jenis(klaim):
    for jenis in JENIS_GALAT:
        galat = klaim[klaim["human_gt"] == jenis].assign(tandai=lambda tabel: tabel["verdict"] != LABEL_DIDUKUNG)
        peka = (galat.groupby([*KOLOM_SETELAN, "author_type"], dropna=False)["tandai"].mean()
                .unstack("author_type").reset_index())
        peka["beda"] = peka["human"] - peka["llm"]
        cetak_judul(f"Sensitivitas juri di dalam {jenis}: dokter lawan LLM, per model (14 setelan)")
        ringkas = peka.groupby("model").agg(sens_dokter=("human", "median"), sens_llm=("llm", "median"),
                                            beda_median=("beda", "median"),
                                            dokter_lebih_tinggi=("beda", lambda beda: int((beda > 0).sum())))
        cetak_markdown(ringkas.reset_index())
        print(f"\nSemua setelan: median beda {peka['beda'].median():.3f}; dokter lebih tinggi pada "
              f"{int((peka['beda'] > 0).sum())} dari {len(peka)}")


def cetak_delta(varian):
    for nama, vonis in varian.items():
        jumlah = vonis.groupby([*KOLOM_SETELAN, "author_type"], dropna=False)[["benar"]].agg(["sum", "size"])
        laju = (jumlah[("benar", "sum")] / jumlah[("benar", "size")]).unstack("author_type")
        klaim_dokter = jumlah[("benar", "size")].unstack("author_type")["human"]
        delta = laju["human"] - laju["llm"]
        cetak_judul(f"Δ sebenarnya, varian {nama}")
        print(f"min {delta.min():.4f}, median {delta.median():.4f}, maks {delta.max():.4f}; setelan dengan klaim "
              f"dokter paling sedikit ({int(klaim_dokter.min())}): Δ = {delta[klaim_dokter.idxmin()]:.4f}")


if __name__ == "__main__":
    main()
