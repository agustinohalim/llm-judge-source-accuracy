"""Simulasi superpopulasi JuriKlinis (rencana bagian K, dicatat 21 Nov 2026 sebelum dijalankan; post hoc).

100 pasien dianggap sebaran empiris dari populasi tak hingga: m pasien diambil dengan pengembalian (bobot
multinomial, pasien yang terambil dua kali dihitung dua klaster), 1000 ambilan per m, ambilan sama untuk semua
setelan. Sasaran Δ atas 100 pasien; suku juri = tingkat juri atas 100 pasien; selang tanpa koreksi populasi hingga,
kuantil t pada m − 1 derajat bebas; anggaran memakai kriteria tahap 2. Analisis utama memakai keenam penaksir, varian
kepekaan hanya label saja dan PPI. Butir 3: sebaran klaim unverified per pasien menurut sumber. Hanya agregat yang
dicetak; hitungan 1–10 disamarkan.

Pakai:
    python analysis/juriklinis_superpopulasi.py [folder_data]
"""
import numpy as np
import pandas as pd

from juriklinis_data import (JENIS_KLAIM, KOLOM_SETELAN, baca_dokter_acak, baca_proposisi, baca_vonis,
                             cari_folder_rilis, hitung_per_pasien, tandai)
from juriklinis_kepekaan import BENIH_DOKTER_ACAK, JENIS_KALIMAT, TANDA_LLM_SAJA
from juriklinis_markdown import cetak_judul, cetak_markdown, samarkan_sel_kecil
from juriklinis_penaksir import BUKAN_SUPPORTED_DOKTER, PENAKSIR
from juriklinis_pengaruh import TANDA_SELISIH, buat_ambilan, laju_sensus
from juriklinis_tahap2 import (AGREGAT_RINGKASAN, ULANGAN_SIMULASI, anggaran_per_setelan, matriks_pasien,
                               nilai_penaksir, ringkas_anggaran)

BANYAK_LABEL_SUPER = [5, 10, 20, 30, 40, 50, 75, 100, 150, 200]
BENIH_SUPER = 20261124
PENAKSIR_VARIAN = ["klasik", "PPI"]
PASIEN_TERATAS = 5


def main():
    folder_rilis = cari_folder_rilis()
    dokter_acak = baca_dokter_acak(folder_rilis, np.random.default_rng(BENIH_DOKTER_ACAK))
    proposisi = baca_proposisi(folder_rilis).merge(dokter_acak, on="proposition_id", validate="one_to_one")
    klaim = baca_vonis(folder_rilis, proposisi, JENIS_KLAIM)
    utama = simulasikan_super(hitung_per_pasien(tandai(klaim)), {"tanda": TANDA_SELISIH, "penaksir": list(PENAKSIR)})
    cetak_hasil("utama (klaim, biner, human_gt)", utama, per_model=True)
    for nama, (vonis, tanda) in varian_kepekaan(folder_rilis, proposisi, klaim).items():
        hasil = simulasikan_super(hitung_per_pasien(vonis), {"tanda": tanda, "penaksir": PENAKSIR_VARIAN})
        cetak_hasil(nama, hasil, per_model=False)
    cetak_sebaran_pasien(tandai(klaim))


def varian_kepekaan(folder_rilis, proposisi, klaim):
    return {
        "satu dokter acak sebagai kebenaran": (tandai(klaim, kolom_kebenaran="dokter_acak"), TANDA_SELISIH),
        "Not Supported saja": (tandai(klaim, label_positif="Not Supported"), TANDA_SELISIH),
        "Not Addressed saja": (tandai(klaim, label_positif="Not Addressed"), TANDA_SELISIH),
        "kalimat BHC LLM (tingkat LLM, bukan Δ)": (tandai(baca_vonis(folder_rilis, proposisi, JENIS_KALIMAT)),
                                                   TANDA_LLM_SAJA),
    }


def topeng_dengan_pengembalian(banyak_pasien, banyak_label, acak):
    peluang = np.full(banyak_pasien, 1 / banyak_pasien)
    return acak.multinomial(banyak_label, peluang, size=ULANGAN_SIMULASI).astype(float)


def simulasikan_super(per_pasien, rancangan):
    pasien = np.sort(per_pasien["subject_id"].unique())
    acak = np.random.default_rng(BENIH_SUPER)
    topeng = {banyak: topeng_dengan_pengembalian(len(pasien), banyak, acak) for banyak in BANYAK_LABEL_SUPER}
    baris = []
    with np.errstate(divide="ignore", invalid="ignore"):
        for setelan, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False):
            identitas = dict(zip(KOLOM_SETELAN, setelan))
            baris += baris_setelan(identitas, matriks_pasien(kelompok, pasien), topeng, rancangan)
    return pd.DataFrame(baris)


def baris_setelan(identitas, matriks, topeng, rancangan):
    tanda = rancangan["tanda"]
    ambilan_penuh = buat_ambilan(matriks, np.ones((1, len(matriks))), tanda)
    delta = sum(nilai * laju_sensus(ambilan_penuh, sumber, BUKAN_SUPPORTED_DOKTER) for sumber, nilai in tanda.items())
    baris = []
    for banyak, topeng_banyak in topeng.items():
        ambilan = buat_ambilan(matriks, topeng_banyak, tanda)
        baris += [{**identitas, "penaksir": nama, "banyak_label": banyak,
                   **nilai_penaksir(PENAKSIR[nama], ambilan, delta, koreksi_populasi=False)}
                  for nama in rancangan["penaksir"]]
    return baris


def cetak_hasil(nama, hasil, per_model):
    cetak_judul(f"Superpopulasi, varian {nama}: ringkasan atas {hasil['rater_alias'].nunique()} setelan "
                f"({ULANGAN_SIMULASI} ambilan dengan pengembalian per m)")
    cetak_markdown(hasil.groupby(["penaksir", "banyak_label"]).agg(**AGREGAT_RINGKASAN).reset_index())
    anggaran = anggaran_per_setelan(hasil)
    cetak_judul(f"Superpopulasi, varian {nama}: anggaran label (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai "
                f"sampai m = {max(BANYAK_LABEL_SUPER)})")
    cetak_markdown(ringkas_anggaran(anggaran, ["penaksir"]))
    if per_model:
        cetak_judul(f"Superpopulasi, varian {nama}: anggaran label per model")
        cetak_markdown(ringkas_anggaran(anggaran, ["model", "penaksir"]))


def cetak_sebaran_pasien(vonis):
    klaim_unik = vonis.drop_duplicates("proposition_id")
    pasien = np.sort(klaim_unik["subject_id"].unique())
    baris = []
    for sumber, kelompok in klaim_unik.groupby("author_type"):
        per_pasien = kelompok.groupby("subject_id")["benar"].sum().reindex(pasien, fill_value=0)
        teratas = per_pasien.sort_values(ascending=False).head(PASIEN_TERATAS).sum()
        baris.append({"sumber": sumber, "pasien": len(pasien),
                      "pasien_dengan_unverified": samarkan_sel_kecil(int((per_pasien > 0).sum())),
                      "unverified_total": samarkan_sel_kecil(int(per_pasien.sum())),
                      "median_per_pasien": samarkan_sel_kecil(int(per_pasien.median())),
                      "maks_per_pasien": samarkan_sel_kecil(int(per_pasien.max())),
                      f"bagian_{PASIEN_TERATAS}_pasien_teratas": round(float(teratas / per_pasien.sum()), 3)})
    cetak_judul("Sebaran klaim unverified (label akhir dokter) atas pasien, per sumber")
    cetak_markdown(pd.DataFrame(baris))


if __name__ == "__main__":
    main()
