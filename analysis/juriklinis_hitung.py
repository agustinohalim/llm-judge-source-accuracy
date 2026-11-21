"""Hitungan dasar VeriFact-BHC v1.1.0 untuk JuriKlinis: struktur data dan cakupan vonis juri.

Mencetak tabel Markdown agregat untuk Hasil_JuriKlinis_0.md: proposisi dan pasien per sumber dan jenis,
sebaran proposisi per pasien, sebaran label kebenaran dokter per sumber, dan cakupan vonis tiap
konfigurasi juri. Kesepakatan juri dengan dokter sengaja tidak dihitung di sini: angka itu sudah
memperlihatkan bias, jadi baru dihitung sesudah ambang aturan henti dikunci di rencana. Tidak ada data
tingkat baris atau teks yang dicetak.

Pakai:
    python analysis/juriklinis_hitung.py [folder_data]
"""
import pandas as pd

from juriklinis_data import (BERKAS_KONFIGURASI, BERKAS_VONIS, LABEL_DIDUKUNG, STRATA, baca_proposisi,
                             cari_folder_rilis)
from juriklinis_markdown import cetak_judul, cetak_markdown

BERKAS_MATRIKS = "verifact/experiment_matrix.csv"
KOLOM_KONFIGURASI = ["fact_type", "retrieval_method", "top_n", "reference_format",
                     "reference_only_admission", "deduplicate_text"]


def main():
    folder_rilis = cari_folder_rilis()
    proposisi = baca_proposisi(folder_rilis)
    cetak_jumlah_per_strata(proposisi)
    cetak_proposisi_per_pasien(proposisi)
    cetak_kebenaran_per_strata(proposisi)
    cakupan = hitung_cakupan_juri(folder_rilis, proposisi)
    cetak_cakupan_per_model(cakupan)
    cetak_alias_dua_sumber(cakupan, proposisi)


def cetak_jumlah_per_strata(proposisi):
    jumlah = proposisi.groupby(STRATA).agg(
        proposisi=("proposition_id", "size"),
        pasien=("subject_id", "nunique"),
        tidak_sah=("invalid", "sum"),
    )
    cetak_judul("Proposisi dan pasien per sumber dan jenis")
    cetak_markdown(jumlah.reset_index())


def cetak_proposisi_per_pasien(proposisi):
    per_pasien = proposisi.groupby([*STRATA, "subject_id"]).size()
    ringkasan = per_pasien.groupby(level=STRATA).describe()[["count", "min", "25%", "50%", "75%", "max"]]
    cetak_judul("Proposisi per pasien (count = banyak pasien)")
    cetak_markdown(ringkasan.reset_index())


def cetak_kebenaran_per_strata(proposisi):
    sebaran = pd.crosstab([proposisi[kolom] for kolom in STRATA], proposisi["human_gt"])
    total = sebaran.sum(axis=1)
    sebaran["bukan_supported"] = total - sebaran[LABEL_DIDUKUNG]
    sebaran["proporsi_bukan_supported"] = sebaran["bukan_supported"] / total
    cetak_judul("Label kebenaran dokter (`human_gt`) per sumber dan jenis")
    cetak_markdown(sebaran.reset_index())


def hitung_cakupan_juri(folder_rilis, proposisi):
    vonis = pd.read_parquet(folder_rilis / BERKAS_VONIS, columns=["proposition_id", "rater_alias"])
    vonis = vonis.merge(proposisi[["proposition_id", *STRATA]], on="proposition_id",
                        validate="many_to_one")
    cakupan = vonis.groupby(["rater_alias", *STRATA]).size().rename("vonis").reset_index()
    konfigurasi = pd.read_csv(folder_rilis / BERKAS_KONFIGURASI)
    matriks = pd.read_csv(folder_rilis / BERKAS_MATRIKS)
    return (cakupan
            .merge(konfigurasi, on="rater_alias", validate="many_to_one")
            .merge(matriks, on=[*STRATA, *KOLOM_KONFIGURASI], how="left", validate="many_to_one"))


def cetak_cakupan_per_model(cakupan):
    ringkasan = cakupan.groupby(["model", *STRATA, "publication_role"], dropna=False).agg(
        alias=("rater_alias", "nunique"),
        vonis=("vonis", "sum"),
    )
    cetak_judul("Cakupan vonis juri per model, sumber, jenis, dan peran publikasi")
    cetak_markdown(ringkasan.reset_index())


def cetak_alias_dua_sumber(cakupan, proposisi):
    klaim = cakupan[cakupan["proposition_type"] == "claim"]
    per_alias = klaim.pivot_table(index=["model", "rater_alias", *KOLOM_KONFIGURASI],
                                  columns="author_type", values="vonis", aggfunc="sum").dropna()
    jumlah_klaim = proposisi[proposisi["proposition_type"] == "claim"].groupby("author_type").size()
    per_alias["lengkap"] = (per_alias[jumlah_klaim.index] == jumlah_klaim).all(axis=1)
    ringkasan = per_alias.reset_index().groupby(["model", "fact_type", "top_n"]).agg(
        alias=("rater_alias", "nunique"),
        vonis_dokter=("human", "sum"),
        vonis_llm=("llm", "sum"),
        alias_lengkap=("lengkap", "sum"),
    )
    cetak_judul(f"Alias yang menilai klaim kedua sumber (klaim dokter {jumlah_klaim['human']}, "
                f"LLM {jumlah_klaim['llm']})")
    cetak_markdown(ringkasan.reset_index())


if __name__ == "__main__":
    main()
