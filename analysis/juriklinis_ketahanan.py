"""Analisis ketahanan JuriKlinis (rencana bagian J, dicatat 21 Nov 2026 sebelum dijalankan; post hoc).

Butir 1: per setelan juri, beda sensitivitas dan beda spesifisitas (dokter − LLM) dengan selang bootstrap
persentil 95 % atas pasien, memakai bobot dan benih tahap 1. Butir 2: asimetri sensitivitas pada klaim yang ketiga
label putaran pertamanya sama. Hanya kolom label dibaca; yang dicetak hanya agregat per model, sel 1–10 disamarkan.

Pakai:
    python analysis/juriklinis_ketahanan.py [folder_data] > log
"""
import numpy as np
import pandas as pd

from juriklinis_bootstrap import bobot_bootstrap, selang_persentil, timbang
from juriklinis_data import (BERKAS_KEBENARAN, KOLOM_DOKTER_PUTARAN_1, KOLOM_SETELAN, baca_vonis_klaim,
                             cari_folder_rilis, hitung_per_pasien)
from juriklinis_gambar import tabel_markdown
from juriklinis_markdown import cetak_judul, cetak_markdown, samarkan_sel_kecil
from juriklinis_tahap1 import hitungan_per_sumber, ketepatan


def main():
    folder_rilis = cari_folder_rilis()
    vonis = baca_vonis_klaim(folder_rilis)
    cetak_selang(ringkas_selang(hitung_per_pasien(vonis)))
    cetak_bulat(vonis[vonis["proposition_id"].isin(klaim_bulat(folder_rilis))])
    cetak_bias_konfigurasi(tabel_markdown("Hasil_JuriKlinis_1.md", "Bias Δ naif per setelan"))


def beda_ketepatan(setelan, kelompok, pasien, bobot):
    hitungan = hitungan_per_sumber(kelompok, pasien)
    titik = ketepatan(timbang(hitungan, np.ones(len(pasien))))
    ulangan = ketepatan(timbang(hitungan, bobot))
    hasil = dict(zip(KOLOM_SETELAN, setelan))
    for ukuran in ("sens", "spek"):
        bawah, atas = selang_persentil(ulangan[f"{ukuran}_dokter"] - ulangan[f"{ukuran}_llm"])
        hasil.update({f"{ukuran}_beda": float(titik[f"{ukuran}_dokter"] - titik[f"{ukuran}_llm"]),
                      f"{ukuran}_bawah": float(bawah), f"{ukuran}_atas": float(atas)})
    return hasil


def ringkas_selang(per_pasien):
    pasien = np.sort(per_pasien["subject_id"].unique())
    bobot = bobot_bootstrap(len(pasien))
    return pd.DataFrame([beda_ketepatan(setelan, kelompok, pasien, bobot)
                         for setelan, kelompok in per_pasien.groupby(KOLOM_SETELAN, dropna=False)])


def cetak_selang(ringkasan):
    per_model = ringkasan.groupby("model").agg(
        setelan=("rater_alias", "size"),
        sens_beda_median=("sens_beda", "median"),
        sens_bawah_min=("sens_bawah", "min"),
        sens_selang_di_atas_0=("sens_bawah", lambda kolom: int((kolom > 0).sum())),
        spek_beda_median=("spek_beda", "median"),
        spek_atas_maks=("spek_atas", "max"),
        spek_selang_di_bawah_0=("spek_atas", lambda kolom: int((kolom < 0).sum())),
    ).reset_index()
    cetak_judul("Beda sensitivitas dan spesifisitas dokter − LLM per setelan, selang bootstrap pasien 95 %")
    print(f"- Setelan: {len(ringkasan)}; selang beda sensitivitas di atas 0: {int((ringkasan['sens_bawah'] > 0).sum())};"
          f" selang beda spesifisitas di bawah 0: {int((ringkasan['spek_atas'] < 0).sum())}")
    print(f"- Median beda sensitivitas {ringkasan['sens_beda'].median():.3f}, batas bawah selang terkecil "
          f"{ringkasan['sens_bawah'].min():.3f}; median beda spesifisitas {ringkasan['spek_beda'].median():.3f}")
    cetak_markdown(per_model)


def klaim_bulat(folder_rilis):
    label = pd.read_csv(folder_rilis / BERKAS_KEBENARAN, usecols=["proposition_id", *KOLOM_DOKTER_PUTARAN_1])
    lengkap = label[KOLOM_DOKTER_PUTARAN_1].notna().all(axis=1)
    sama = label[KOLOM_DOKTER_PUTARAN_1].nunique(axis=1) == 1
    return label.loc[lengkap & sama, "proposition_id"]


def cetak_bulat(vonis_bulat):
    klaim = vonis_bulat.drop_duplicates("proposition_id")
    per_sumber = klaim.groupby("author_type").agg(klaim=("proposition_id", "size"), unverified=("benar", "sum"),
                                                  bagian_unverified=("benar", "mean")).reset_index()
    per_sumber[["klaim", "unverified"]] = per_sumber[["klaim", "unverified"]].map(samarkan_sel_kecil)
    cetak_judul("Klaim dengan label putaran pertama bulat (ketiga dokter sama)")
    cetak_markdown(per_sumber)
    jumlah = (vonis_bulat.assign(benar_juri=vonis_bulat["benar"] & vonis_bulat["juri"])
              .groupby([*KOLOM_SETELAN, "author_type"], dropna=False)[["benar", "benar_juri"]].sum()
              .unstack("author_type"))
    sens = jumlah["benar_juri"] / jumlah["benar"]
    setelan = pd.DataFrame({"model": sens.index.get_level_values("model"), "sens_dokter": sens["human"].to_numpy(),
                            "sens_llm": sens["llm"].to_numpy()})
    setelan["dokter_lebih_tinggi"] = setelan["sens_dokter"] > setelan["sens_llm"]
    per_model = setelan.groupby("model").agg(sens_dokter=("sens_dokter", "median"), sens_llm=("sens_llm", "median"),
                                             dokter_lebih_tinggi=("dokter_lebih_tinggi", "sum")).reset_index()
    per_model["dokter_lebih_tinggi"] = per_model["dokter_lebih_tinggi"].astype(int)
    cetak_judul("Sensitivitas juri per sumber pada klaim bulat (median atas setelan per model)")
    print(f"- Setelan dengan sensitivitas dokter > LLM: {int(setelan['dokter_lebih_tinggi'].sum())} dari {len(setelan)}")
    cetak_markdown(per_model)


def cetak_bias_konfigurasi(per_setelan):
    tandai = per_setelan.assign(besar=per_setelan["bias"].abs() >= 0.05, sangat_besar=per_setelan["bias"].abs() >= 0.10,
                                selang_atas_0=per_setelan["bias_bawah"] > 0, selang_bawah_0=per_setelan["bias_atas"] < 0)
    cetak_judul("Bias Δ juri saja menurut model dan konfigurasi temu-kembali (dari tabel per setelan Hasil_JuriKlinis_1)")
    print(f"- Setelan: {len(tandai)}; |bias| >= 0,05: {int(tandai['besar'].sum())}; |bias| >= 0,10: "
          f"{int(tandai['sangat_besar'].sum())}; selang di atas 0: {int(tandai['selang_atas_0'].sum())}; selang di "
          f"bawah 0: {int(tandai['selang_bawah_0'].sum())}")
    for kunci in ("model", "fact_type"):
        cetak_markdown(tandai.groupby(kunci).agg(
            setelan=("bias", "size"), bias_median=("bias", "median"), bias_min=("bias", "min"),
            bias_maks=("bias", "max"), besar=("besar", "sum"), selang_atas_0=("selang_atas_0", "sum"),
            selang_bawah_0=("selang_bawah_0", "sum")).reset_index())
        print()


if __name__ == "__main__":
    main()
