"""Ambilan berlabel dan fungsi pengaruh per pasien untuk penaksir JuriKlinis.

Matriks pasien punya satu baris per pasien dan, untuk tiap sumber (dokter, LLM), kolom banyak klaim `n`, klaim bukan
Supported menurut dokter `benar`, menurut juri `juri`, dan menurut keduanya `benar_juri`. Pengaruh per pasien ditulis
sebagai koefisien atas kolom-kolom itu (ulangan x kolom), sehingga varians klaster-pasien semua ulangan dihitung dari
jumlah dan matriks Gram pasien berlabel, tanpa perulangan per ulangan. Taksiran - sasaran ~ rata-rata pengaruh atas
m pasien berlabel. `tanda` menentukan sasaran: {dokter: +1, LLM: −1} untuk Δ, {LLM: +1} untuk tingkat LLM saja.
"""
from dataclasses import dataclass

import numpy as np

SUMBER = ["human", "llm"]
KOLOM = ["n", "benar", "juri", "benar_juri"]
TANDA_SELISIH = {"human": 1.0, "llm": -1.0}


@dataclass(frozen=True)
class Ambilan:
    jumlah: np.ndarray
    gram: np.ndarray
    sensus: np.ndarray
    banyak_label: int
    banyak_pasien: int
    tanda: dict


def buat_ambilan(matriks, topeng, tanda):
    banyak_kolom = matriks.shape[1]
    silang = (matriks[:, :, None] * matriks[:, None, :]).reshape(len(matriks), -1)
    return Ambilan(
        jumlah=topeng @ matriks,
        gram=(topeng @ silang).reshape(len(topeng), banyak_kolom, banyak_kolom),
        sensus=matriks.sum(axis=0),
        banyak_label=int(topeng[0].sum()),
        banyak_pasien=len(matriks),
        tanda=tanda,
    )


def vektor_kolom(sumber, bobot):
    vektor = np.zeros(len(SUMBER) * len(KOLOM))
    for satu_sumber in sumber:
        for nama, nilai in bobot.items():
            vektor[SUMBER.index(satu_sumber) * len(KOLOM) + KOLOM.index(nama)] = nilai
    return vektor


def rasio(ambilan, sumber, pembilang, penyebut):
    atas, bawah = vektor_kolom(sumber, pembilang), vektor_kolom(sumber, penyebut)
    jumlah_bawah = ambilan.jumlah @ bawah
    nilai = (ambilan.jumlah @ atas) / jumlah_bawah
    skala = ambilan.banyak_label / jumlah_bawah
    return nilai, skala[:, None] * (atas[None, :] - nilai[:, None] * bawah[None, :])


def laju_sensus(ambilan, sumber, pembilang):
    return (ambilan.sensus @ vektor_kolom([sumber], pembilang)) / (ambilan.sensus @ vektor_kolom([sumber], {"n": 1}))


def kuadrat(ambilan, kiri, kanan):
    silang = np.einsum("rk,rkl,rl->r", kiri, ambilan.gram, kanan)
    jumlah_kiri = np.einsum("rk,rk->r", kiri, ambilan.jumlah)
    jumlah_kanan = np.einsum("rk,rk->r", kanan, ambilan.jumlah)
    return silang - jumlah_kiri * jumlah_kanan / ambilan.banyak_label


def galat_baku(ambilan, pengaruh, koreksi_populasi=True):
    banyak = ambilan.banyak_label
    faktor = 1 - banyak / ambilan.banyak_pasien if koreksi_populasi else 1.0
    varians = faktor * kuadrat(ambilan, pengaruh, pengaruh) / (banyak * (banyak - 1))
    return np.sqrt(np.clip(varians, 0, None))
