"""Kepekaan JuriKlinis: simulasi anggaran label tahap 2 diulang dengan definisi lain (rencana bagian A, butir 3, 4,
4a, 7, 9; dikunci 20 Nov 2026 sebelum hasil).

Varian: utama (pembanding, sama dengan Hasil_JuriKlinis_2); tanpa proposisi `invalid`; kebenaran dari satu dokter
putaran 1 yang dipilih acak per proposisi (benih tetap) lawan vonis juri; tiga label dipecah jadi dua sasaran biner
(Not Supported saja, Not Addressed saja — juri dan dokter memakai label yang sama); kalimat BHC LLM, hanya tingkat
LLM karena kalimat dokter tidak divonis juri (butir 4a). Rancangan simulasi, penaksir, ambilan pasien, dan ambang
anggaran sama dengan `juriklinis_tahap2.py`. Dicetak per varian: ringkasan atas semua setelan dan anggaran label per
penaksir; ditambah sebaran label dokter acak. Hanya agregat.

Pakai:
    python analysis/juriklinis_kepekaan.py [folder_data]
"""
import numpy as np

from juriklinis_data import (JENIS_KLAIM, baca_dokter_acak, baca_proposisi, baca_vonis, cari_folder_rilis,
                             hitung_per_pasien, tandai)
from juriklinis_markdown import cetak_judul, cetak_markdown, samarkan_sel_kecil
from juriklinis_pengaruh import TANDA_SELISIH
from juriklinis_tahap2 import AGREGAT_RINGKASAN, anggaran_per_setelan, ringkas_anggaran, simulasikan

BENIH_DOKTER_ACAK = 20261123
JENIS_KALIMAT = "sentence"
TANDA_LLM_SAJA = {"llm": 1.0}


def main():
    folder_rilis = cari_folder_rilis()
    dokter_acak = baca_dokter_acak(folder_rilis, np.random.default_rng(BENIH_DOKTER_ACAK))
    proposisi = baca_proposisi(folder_rilis).merge(dokter_acak, on="proposition_id", validate="one_to_one")
    cetak_sebaran_label(proposisi)
    klaim = baca_vonis(folder_rilis, proposisi, JENIS_KLAIM)
    kalimat = baca_vonis(folder_rilis, proposisi, JENIS_KALIMAT)
    varian = {
        "utama (klaim, biner, human_gt)": (tandai(klaim), TANDA_SELISIH),
        "tanpa proposisi invalid": (tandai(klaim[~klaim["invalid"].astype(bool)]), TANDA_SELISIH),
        "satu dokter acak sebagai kebenaran": (tandai(klaim, kolom_kebenaran="dokter_acak"), TANDA_SELISIH),
        "Not Supported saja": (tandai(klaim, label_positif="Not Supported"), TANDA_SELISIH),
        "Not Addressed saja": (tandai(klaim, label_positif="Not Addressed"), TANDA_SELISIH),
        "kalimat BHC LLM (tingkat LLM, bukan Δ)": (tandai(kalimat), TANDA_LLM_SAJA),
    }
    for nama, (vonis, tanda) in varian.items():
        cetak_varian(nama, simulasikan(hitung_per_pasien(vonis), tanda))


def cetak_sebaran_label(proposisi):
    sebaran = (proposisi.groupby(["proposition_type", "author_type"])[["human_gt", "dokter_acak"]]
               .value_counts(dropna=False).rename("proposisi").reset_index())
    sebaran["proposisi"] = sebaran["proposisi"].map(samarkan_sel_kecil)
    cetak_judul("Label dokter acak (putaran 1) lawan human_gt, per jenis dan sumber")
    cetak_markdown(sebaran)


def cetak_varian(nama, hasil):
    cetak_judul(f"Varian: {nama} — ringkasan atas {hasil['rater_alias'].nunique()} setelan")
    cetak_markdown(hasil.groupby(["penaksir", "banyak_label"], observed=True).agg(**AGREGAT_RINGKASAN)
                   .reset_index())
    cetak_judul(f"Varian: {nama} — anggaran label per penaksir")
    cetak_markdown(ringkas_anggaran(anggaran_per_setelan(hasil), ["penaksir"]))


if __name__ == "__main__":
    main()
