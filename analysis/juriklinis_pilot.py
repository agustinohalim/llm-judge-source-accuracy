"""Aturan pilot JuriKlinis (post hoc, rencana bagian I butir 4; dicatat 21 Nov 2026 sebelum dijalankan).

Tiap ulangan mengambil urutan acak 100 pasien. Sepuluh pasien pertama adalah pilot berlabel; dari pilot itu varians
pengaruh per pasien σ² ditaksir untuk label saja dan PPI, dan untuk masing-masing diramalkan m terkecil di
{10, 15, ..., 100} dengan lebar 2 t √((1 − m/100) σ² / m) <= 0,10. Penaksir dengan m ramalan lebih kecil dipilih
(seri: PPI), label diteruskan sampai m itu (pilot termasuk), lalu selang 95 % akhir dinilai terhadap Δ sebenarnya.
Dicetak juga m ramalan untuk N >> m (tanpa faktor 1 − m/N), sebagai angka yang bisa dibawa ke populasi lain.
Varian: utama, Not Supported saja, kalimat BHC LLM (tingkat saja). Hanya agregat atas setelan juri.

Pakai:
    python analysis/juriklinis_pilot.py [folder_data]
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

from juriklinis_bootstrap import TINGKAT_SELANG
from juriklinis_data import (JENIS_KLAIM, KOLOM_SETELAN, baca_proposisi, baca_vonis, cari_folder_rilis,
                             hitung_per_pasien, tandai)
from juriklinis_kepekaan import JENIS_KALIMAT, TANDA_LLM_SAJA
from juriklinis_markdown import cetak_judul, cetak_markdown
from juriklinis_penaksir import BUKAN_SUPPORTED_DOKTER, PENAKSIR
from juriklinis_pengaruh import TANDA_SELISIH, buat_ambilan, galat_baku, kuadrat, laju_sensus
from juriklinis_tahap2 import LEBAR_MAKSIMUM, ULANGAN_SIMULASI, matriks_pasien

BANYAK_PILOT = 10
GRID_AKHIR = np.arange(10, 101, 5)
BENIH_PILOT = 20261124
PENAKSIR_PILOT = ["klasik", "PPI"]


@dataclass(frozen=True)
class KonteksSetelan:
    matriks: np.ndarray
    urutan: np.ndarray
    tanda: dict
    delta: float


def main():
    folder_rilis = cari_folder_rilis()
    proposisi = baca_proposisi(folder_rilis)
    klaim = baca_vonis(folder_rilis, proposisi, JENIS_KLAIM)
    varian = {
        "utama": (tandai(klaim), TANDA_SELISIH),
        "Not Supported saja": (tandai(klaim, label_positif="Not Supported"), TANDA_SELISIH),
        "kalimat BHC LLM (tingkat LLM)": (tandai(baca_vonis(folder_rilis, proposisi, JENIS_KALIMAT)), TANDA_LLM_SAJA),
    }
    for nama, (vonis, tanda) in varian.items():
        cetak_pilot(nama, jalankan_pilot(hitung_per_pasien(vonis), tanda))


def jalankan_pilot(per_pasien, tanda):
    pasien = np.sort(per_pasien["subject_id"].unique())
    urutan = np.argsort(np.random.default_rng(BENIH_PILOT).random((ULANGAN_SIMULASI, len(pasien))), axis=1)
    baris = []
    with np.errstate(divide="ignore", invalid="ignore"):
        for setelan, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False):
            matriks = matriks_pasien(kelompok, pasien)
            ambilan_penuh = buat_ambilan(matriks, np.ones((1, len(matriks))), tanda)
            delta = sum(nilai * laju_sensus(ambilan_penuh, sumber, BUKAN_SUPPORTED_DOKTER)
                        for sumber, nilai in tanda.items())
            baris.append({**dict(zip(KOLOM_SETELAN, setelan)),
                          **pilot_setelan(KonteksSetelan(matriks, urutan, tanda, float(delta)))})
    return pd.DataFrame(baris)


def topeng_dari_urutan(urutan, banyak):
    topeng = np.zeros(urutan.shape)
    np.put_along_axis(topeng, urutan[:, :banyak], 1.0, axis=1)
    return topeng


def ramalkan_m(ambilan_pilot, fungsi):
    pengaruh = fungsi(ambilan_pilot)[1]
    varians = kuadrat(ambilan_pilot, pengaruh, pengaruh) / (BANYAK_PILOT - 1)
    kuantil = stats.t.ppf((1 + TINGKAT_SELANG) / 2, GRID_AKHIR - 1)
    faktor = 1 - GRID_AKHIR / ambilan_pilot.banyak_pasien
    lebar = 2 * kuantil[None, :] * np.sqrt(faktor[None, :] * varians[:, None] / GRID_AKHIR[None, :])
    m_terhingga = GRID_AKHIR[np.argmax(lebar <= LEBAR_MAKSIMUM, axis=1)]
    m_besar = np.ceil(varians * (2 * stats.norm.ppf((1 + TINGKAT_SELANG) / 2) / LEBAR_MAKSIMUM) ** 2)
    return m_terhingga, m_besar


def nilai_akhir(konteks, baris, banyak, nama):
    ambilan = buat_ambilan(konteks.matriks, topeng_dari_urutan(konteks.urutan[baris], banyak), konteks.tanda)
    taksiran, pengaruh = PENAKSIR[nama](ambilan)
    setengah = stats.t.ppf((1 + TINGKAT_SELANG) / 2, banyak - 1) * galat_baku(ambilan, pengaruh)
    return np.abs(taksiran - konteks.delta) <= setengah + 1e-12, 2 * setengah


def pilot_setelan(konteks):
    ambilan_pilot = buat_ambilan(konteks.matriks, topeng_dari_urutan(konteks.urutan, BANYAK_PILOT), konteks.tanda)
    ramalan = {nama: ramalkan_m(ambilan_pilot, PENAKSIR[nama]) for nama in PENAKSIR_PILOT}
    pilih_ppi = ramalan["PPI"][0] <= ramalan["klasik"][0]
    m_akhir = np.where(pilih_ppi, ramalan["PPI"][0], ramalan["klasik"][0])
    tercakup, lebar = np.zeros(len(m_akhir), dtype=bool), np.zeros(len(m_akhir))
    for banyak in np.unique(m_akhir):
        for nama, pilihan in (("PPI", pilih_ppi), ("klasik", ~pilih_ppi)):
            baris = (m_akhir == banyak) & pilihan
            if baris.any():
                tercakup[baris], lebar[baris] = nilai_akhir(konteks, baris, int(banyak), nama)
    return {"cakupan": tercakup.mean(), "lebar": lebar.mean(), "m_median": np.median(m_akhir),
            "m_rata": m_akhir.mean(), "bagian_ppi": pilih_ppi.mean(),
            "m_besar_ppi": np.median(ramalan["PPI"][1]), "m_besar_klasik": np.median(ramalan["klasik"][1])}


def cetak_pilot(nama, hasil):
    agregat = {"setelan": ("rater_alias", "size"), "cakupan_median": ("cakupan", "median"),
               "cakupan_min": ("cakupan", "min"), "lebar_median": ("lebar", "median"),
               "m_median": ("m_median", "median"), "m_rata_median": ("m_rata", "median"),
               "bagian_ppi_median": ("bagian_ppi", "median"), "m_besar_ppi": ("m_besar_ppi", "median"),
               "m_besar_klasik": ("m_besar_klasik", "median")}
    cetak_judul(f"Aturan pilot ({BANYAK_PILOT} pasien), varian {nama}: semua setelan")
    cetak_markdown(hasil.assign(semua="semua").groupby("semua").agg(**agregat).reset_index())
    cetak_judul(f"Aturan pilot, varian {nama}: per model")
    cetak_markdown(hasil.groupby("model").agg(**agregat).reset_index())


if __name__ == "__main__":
    main()
