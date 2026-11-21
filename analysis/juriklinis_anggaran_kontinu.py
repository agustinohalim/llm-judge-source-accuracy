"""Anggaran tinjauan kontinu dari lebar selang superpopulasi (rencana bagian L, post hoc, tanpa data baru).

Seperti juriklinis_gambar.py, skrip ini tidak membaca data PhysioNet; ia mengurai tabel ringkasan Hasil_JuriKlinis_6.md
(median lebar atas 126 setelan). Lebar menyusut kira-kira dengan 1/√m, jadi m kontinu untuk lebar 0,10 adalah
m · (w_m / 0,10)²; acuan utama m = 50, dengan m = 20 dan m = 100 sebagai pemeriksaan. Rasio efisiensi
(w_PPI / w_label)² pada m = 50 adalah bagian pasien yang dibutuhkan PPI dibanding label saja untuk lebar yang sama.

Pakai:
    python analysis/juriklinis_anggaran_kontinu.py > keluaran.md
"""
import pandas as pd

from juriklinis_gambar import tabel_markdown
from juriklinis_markdown import cetak_judul, cetak_markdown

LEBAR_SASARAN = 0.10
M_ACUAN = 50
M_PEMERIKSAAN = [20, 100]
PENAKSIR_BANDING = ["PPI", "klasik"]
VARIAN = {
    "utama": "Superpopulasi, varian utama (klaim, biner, human_gt): ringkasan",
    "satu dokter acak": "Superpopulasi, varian satu dokter acak sebagai kebenaran: ringkasan",
    "Not Supported saja": "Superpopulasi, varian Not Supported saja: ringkasan",
    "Not Addressed saja": "Superpopulasi, varian Not Addressed saja: ringkasan",
    "kalimat BHC LLM (tingkat)": "Superpopulasi, varian kalimat BHC LLM (tingkat LLM, bukan Δ): ringkasan",
}


def lebar_per_m(ringkasan, penaksir):
    baris = ringkasan[ringkasan["penaksir"] == penaksir]
    return dict(zip(baris["banyak_label"].astype(int), baris["lebar_median"].astype(float)))


def m_kontinu(lebar, m):
    return m * (lebar[m] / LEBAR_SASARAN) ** 2


def baris_varian(nama, judul):
    ringkasan = tabel_markdown("Hasil_JuriKlinis_6.md", judul)
    lebar = {penaksir: lebar_per_m(ringkasan, penaksir) for penaksir in PENAKSIR_BANDING}
    baris = {"varian": nama}
    for penaksir in PENAKSIR_BANDING:
        baris[f"m_{penaksir}_acuan50"] = m_kontinu(lebar[penaksir], M_ACUAN)
        for m in M_PEMERIKSAAN:
            baris[f"m_{penaksir}_acuan{m}"] = m_kontinu(lebar[penaksir], m)
    baris["rasio_PPI_per_label_m50"] = (lebar["PPI"][M_ACUAN] / lebar["klasik"][M_ACUAN]) ** 2
    return baris


def main():
    tabel = pd.DataFrame([baris_varian(nama, judul) for nama, judul in VARIAN.items()])
    cetak_judul("Anggaran kontinu untuk lebar 0,10 (m · (w_m / 0,10)², median lebar atas 126 setelan) dan rasio "
                "efisiensi (w_PPI / w_label)² pada m = 50")
    cetak_markdown(tabel)


if __name__ == "__main__":
    main()
