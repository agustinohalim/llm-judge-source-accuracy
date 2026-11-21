"""Selang anggaran tinjauan JuriKlinis (rencana bagian M butir 2, post hoc).

Bootstrap luar 500 ulangan atas 100 pasien (bobot multinomial, benih 20261125); baris pertama adalah data asli. Pada
tiap ulangan dan setelan, varians pengaruh per pasien (fungsi pengaruh yang sama dengan simulasi) memberi
m* = (2 · 1,96 · SD / 0,10)² untuk label saja dan PPI. Per ulangan dicatat median m* atas setelan untuk tiap penaksir
dan rasio PPI / label saja; dilaporkan nilai data asli dan selang persentil 95 %. Hanya agregat yang dicetak.

Pakai:
    python analysis/juriklinis_selang_anggaran.py [folder_data]
"""
import numpy as np
import pandas as pd

from juriklinis_data import JENIS_KLAIM, KOLOM_SETELAN, baca_proposisi, baca_vonis, cari_folder_rilis, \
    hitung_per_pasien, tandai
from juriklinis_kepekaan import JENIS_KALIMAT, TANDA_LLM_SAJA
from juriklinis_markdown import cetak_judul, cetak_markdown
from juriklinis_penaksir import PENAKSIR
from juriklinis_pengaruh import TANDA_SELISIH, buat_ambilan, kuadrat
from juriklinis_tahap2 import matriks_pasien

ULANGAN_LUAR = 500
BENIH_LUAR = 20261125
KUANTIL_NORMAL = 1.96
LEBAR_SASARAN = 0.10
PENAKSIR_BANDING = ["PPI", "klasik"]
PERSENTIL = [2.5, 97.5]


def topeng_luar(banyak_pasien):
    acak = np.random.default_rng(BENIH_LUAR)
    ulangan = acak.multinomial(banyak_pasien, np.full(banyak_pasien, 1 / banyak_pasien), size=ULANGAN_LUAR)
    return np.vstack([np.ones(banyak_pasien), ulangan]).astype(float)


def anggaran_setelan(matriks, topeng, tanda, nama_penaksir):
    ambilan = buat_ambilan(matriks, topeng, tanda)
    _, pengaruh = PENAKSIR[nama_penaksir](ambilan)
    varians = kuadrat(ambilan, pengaruh, pengaruh) / (ambilan.banyak_label - 1)
    return (2 * KUANTIL_NORMAL / LEBAR_SASARAN) ** 2 * varians


def anggaran_per_ulangan(per_pasien, tanda):
    pasien = np.sort(per_pasien["subject_id"].unique())
    topeng = topeng_luar(len(pasien))
    per_setelan = {nama: [] for nama in PENAKSIR_BANDING}
    for _, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False):
        matriks = matriks_pasien(kelompok, pasien)
        for nama in PENAKSIR_BANDING:
            per_setelan[nama].append(anggaran_setelan(matriks, topeng, tanda, nama))
    median = {nama: np.median(np.vstack(nilai), axis=0) for nama, nilai in per_setelan.items()}
    return {"m_PPI": median["PPI"], "m_label": median["klasik"], "rasio": median["PPI"] / median["klasik"]}


def ringkas(nama_varian, anggaran):
    baris = []
    for ukuran, nilai in anggaran.items():
        bawah, atas = np.percentile(nilai[1:], PERSENTIL)
        baris.append({"varian": nama_varian, "ukuran": ukuran, "data_asli": float(nilai[0]),
                      "median_bootstrap": float(np.median(nilai[1:])), "bawah_95": float(bawah),
                      "atas_95": float(atas)})
    return baris


def varian_dihitung(folder_rilis):
    proposisi = baca_proposisi(folder_rilis)
    klaim = baca_vonis(folder_rilis, proposisi, JENIS_KLAIM)
    return {
        "utama (klaim, biner, human_gt)": (tandai(klaim), TANDA_SELISIH),
        "Not Supported saja": (tandai(klaim, label_positif="Not Supported"), TANDA_SELISIH),
        "kalimat BHC LLM (tingkat LLM)": (tandai(baca_vonis(folder_rilis, proposisi, JENIS_KALIMAT)), TANDA_LLM_SAJA),
    }


def main():
    baris = []
    with np.errstate(divide="ignore", invalid="ignore"):
        for nama, (vonis, tanda) in varian_dihitung(cari_folder_rilis()).items():
            baris += ringkas(nama, anggaran_per_ulangan(hitung_per_pasien(vonis), tanda))
    cetak_judul(f"Anggaran m* = (2 · {KUANTIL_NORMAL} · SD / {LEBAR_SASARAN})², median atas setelan; selang persentil "
                f"95 % dari {ULANGAN_LUAR} bootstrap pasien (benih {BENIH_LUAR})")
    cetak_markdown(pd.DataFrame(baris))


if __name__ == "__main__":
    main()
