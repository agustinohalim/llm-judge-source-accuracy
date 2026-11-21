"""Tahap 2 JuriKlinis: simulasi anggaran label atas vonis juri terbit VeriFact-BHC v1.1.0.

Rancangan dikunci 21 Nov 2026 sebelum skrip ini pertama dijalankan (Artikel_JuriKlinis_Rencana.md, bagian A):
untuk tiap setelan juri yang menilai klaim atomik kedua sumber, m pasien (5, 10, 20, 30, 50) diambil acak tanpa
pengembalian dari 100 dan diberi label dokter untuk kedua BHC-nya, 1000 ambilan per m dan ambilan yang sama untuk
semua setelan. Tiap penaksir (`juriklinis_penaksir.py`) menaksir Δ dokter − LLM dengan selang 95 % (kuantil t,
m − 1 derajat bebas, pasien sebagai klaster, koreksi populasi hingga); naif memakai vonis juri saja atas 100 pasien.
Sasaran: Δ sebenarnya atas 100 pasien. Dicetak per penaksir dan m: bias, cakupan, lebar selang, tanda terbalik,
bagian ambilan gagal; lalu m terkecil dengan cakupan >= 0,93 dan lebar <= 0,10. Hanya agregat atas setelan juri.

Pakai:
    python analysis/juriklinis_tahap2.py [folder_data]
"""
import numpy as np
import pandas as pd
from scipy import stats

from juriklinis_bootstrap import TINGKAT_SELANG
from juriklinis_data import KOLOM_SETELAN, baca_vonis_klaim, cari_folder_rilis, hitung_per_pasien
from juriklinis_markdown import cetak_judul, cetak_markdown
from juriklinis_penaksir import BUKAN_SUPPORTED_DOKTER, PENAKSIR, naif
from juriklinis_pengaruh import KOLOM, SUMBER, TANDA_SELISIH, buat_ambilan, galat_baku, laju_sensus

BANYAK_LABEL = [5, 10, 20, 30, 50]
ULANGAN_SIMULASI = 1000
BENIH_SIMULASI = 20261122
CAKUPAN_MINIMUM = 0.93
LEBAR_MAKSIMUM = 0.10
MODEL_UTAMA = ["Llama-8B", "Llama-70B", "R1-8B", "R1-70B"]
URUTAN_PENAKSIR = ["naif", *PENAKSIR]
AGREGAT_RINGKASAN = {
    "setelan": ("rater_alias", "size"),
    "bias_median": ("bias", "median"),
    "cakupan_median": ("cakupan", "median"),
    "cakupan_min": ("cakupan", "min"),
    "lebar_median": ("lebar", "median"),
    "terbalik_maks": ("terbalik", "max"),
    "gagal_maks": ("gagal", "max"),
}


def main():
    folder_rilis = cari_folder_rilis()
    hasil = simulasikan(hitung_per_pasien(baca_vonis_klaim(folder_rilis)), TANDA_SELISIH)
    cetak_ringkasan(hasil)
    cetak_anggaran(hasil)


def simulasikan(per_pasien, tanda):
    pasien = np.sort(per_pasien["subject_id"].unique())
    acak = np.random.default_rng(BENIH_SIMULASI)
    topeng = {banyak: topeng_label(len(pasien), banyak, acak) for banyak in BANYAK_LABEL}
    with np.errstate(divide="ignore", invalid="ignore"):
        hasil = pd.DataFrame([baris
                              for setelan, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False)
                              for baris in simulasikan_setelan(setelan, matriks_pasien(kelompok, pasien),
                                                               topeng, tanda)])
    hasil["penaksir"] = pd.Categorical(hasil["penaksir"], categories=URUTAN_PENAKSIR, ordered=True)
    return hasil


def topeng_label(banyak_pasien, banyak_label, acak):
    terpilih = np.argsort(acak.random((ULANGAN_SIMULASI, banyak_pasien)), axis=1)[:, :banyak_label]
    topeng = np.zeros((ULANGAN_SIMULASI, banyak_pasien))
    np.put_along_axis(topeng, terpilih, 1.0, axis=1)
    return topeng


def matriks_pasien(kelompok, pasien):
    return np.column_stack([kelompok.loc[kelompok["author_type"] == sumber]
                            .set_index("subject_id")[kolom]
                            .reindex(pasien, fill_value=0)
                            .to_numpy(dtype=float)
                            for sumber in SUMBER for kolom in KOLOM])


def nilai_penaksir(fungsi, ambilan, delta, koreksi_populasi=True):
    taksiran, pengaruh = fungsi(ambilan)
    setengah = stats.t.ppf((1 + TINGKAT_SELANG) / 2, ambilan.banyak_label - 1) * galat_baku(
        ambilan, pengaruh, koreksi_populasi)
    sah = np.isfinite(taksiran) & np.isfinite(setengah)
    return {
        "bias": np.nanmean(np.where(sah, taksiran - delta, np.nan)),
        "cakupan": np.mean(sah & (np.abs(taksiran - delta) <= setengah)),
        "lebar": np.nanmean(np.where(sah, 2 * setengah, np.nan)),
        "terbalik": np.mean(sah & (taksiran * delta <= 0)),
        "gagal": np.mean(~sah),
    }


def simulasikan_setelan(setelan, matriks, topeng, tanda):
    identitas = dict(zip(KOLOM_SETELAN, setelan))
    ambilan_penuh = buat_ambilan(matriks, np.ones((1, len(matriks))), tanda)
    delta = sum(nilai * laju_sensus(ambilan_penuh, sumber, BUKAN_SUPPORTED_DOKTER) for sumber, nilai in tanda.items())
    baris = [{**identitas, "penaksir": "naif", "banyak_label": 0,
              **nilai_penaksir(naif, ambilan_penuh, delta, koreksi_populasi=False)}]
    for banyak, topeng_banyak in topeng.items():
        ambilan = buat_ambilan(matriks, topeng_banyak, tanda)
        baris += [{**identitas, "penaksir": nama, "banyak_label": banyak, **nilai_penaksir(fungsi, ambilan, delta)}
                  for nama, fungsi in PENAKSIR.items()]
    return baris


def cetak_ringkasan(hasil):
    agregat = AGREGAT_RINGKASAN
    cetak_judul(f"Semua setelan juri (median/min/maks atas setelan; {ULANGAN_SIMULASI} ambilan per m)")
    cetak_markdown(hasil.groupby(["penaksir", "banyak_label"], observed=True).agg(**agregat).reset_index())
    utama = hasil[hasil["model"].isin(MODEL_UTAMA)]
    cetak_judul(f"Model teks utama ({', '.join(MODEL_UTAMA)}), 14 setelan per model")
    cetak_markdown(utama.groupby(["model", "penaksir", "banyak_label"], observed=True).agg(**agregat).reset_index())
    lain = hasil[~hasil["model"].isin(MODEL_UTAMA)]
    cetak_judul("Model lain (suplemen), 14 setelan per model")
    cetak_markdown(lain.groupby(["model", "penaksir", "banyak_label"], observed=True).agg(**agregat).reset_index())
    naif_saja = hasil[hasil["penaksir"] == "naif"]
    cetak_judul("Naif: banyak setelan yang selangnya mencakup Δ sebenarnya")
    cetak_markdown(naif_saja.groupby("model")["cakupan"].agg(setelan="size", mencakup="sum").reset_index())
    print(f"\nSemua model: {int(naif_saja['cakupan'].sum())} dari {len(naif_saja)} setelan")


def anggaran_per_setelan(hasil):
    berlabel = hasil[hasil["banyak_label"] > 0]
    memenuhi = berlabel[(berlabel["cakupan"] >= CAKUPAN_MINIMUM) & (berlabel["lebar"] <= LEBAR_MAKSIMUM)]
    terkecil = (memenuhi.groupby([*KOLOM_SETELAN, "penaksir"], observed=True, dropna=False)["banyak_label"].min()
                .reindex(pd.MultiIndex.from_frame(berlabel[[*KOLOM_SETELAN, "penaksir"]].drop_duplicates())))
    return terkecil.rename("m").reset_index()


def ringkas_anggaran(anggaran, kelompok):
    return anggaran.groupby(kelompok, observed=True)["m"].agg(
        setelan_tercapai="count",
        m_median=lambda nilai: nilai.fillna(np.inf).median(),
        m_maks=lambda nilai: nilai.fillna(np.inf).max(),
    ).reset_index()


def cetak_anggaran(hasil):
    per_model = ringkas_anggaran(anggaran_per_setelan(hasil), ["model", "penaksir"])
    cetak_judul(f"Anggaran label: m terkecil dengan cakupan >= {CAKUPAN_MINIMUM} dan lebar <= {LEBAR_MAKSIMUM} "
                f"(inf = tidak tercapai sampai m = {max(BANYAK_LABEL)})")
    cetak_markdown(per_model)


if __name__ == "__main__":
    main()
