"""Penaksir JuriKlinis untuk Δ (tingkat klaim bukan Supported, dokter − LLM) atau tingkat satu sumber; rencana
bagian A butir 6 dan rancangan simulasi yang dikunci 21 Nov 2026.

Tiap penaksir menerima `Ambilan` dan mengembalikan taksiran per ulangan serta koefisien pengaruh per pasien;
sumber dan tandanya diambil dari `ambilan.tanda`.
- naif: tingkat vonis juri saja (dipanggil dengan semua pasien sebagai ambilan).
- klasik (pembanding, λ = 0): label dokter saja. PPI: λ = 1. PPI++ bersama: satu λ yang meminimalkan varians
  sasaran. PPI++ berstrata: λ per sumber. λ dipotong ke [0, 1]. Vonis juri ada untuk semua pasien, jadi suku juri
  adalah sensus tanpa varians, dan PPI sama dengan penaksir selisih survei.
- Rogan–Gladen: tingkat juri sensus dikoreksi sensitivitas/spesifisitas dari klaim berlabel, dihitung bersama dari
  semua sumber atau per sumber; NaN bila sensitivitas tak terdefinisi atau sens + spek − 1 <= 0.
"""
from functools import partial

import numpy as np

from juriklinis_pengaruh import kuadrat, laju_sensus, rasio

BUKAN_SUPPORTED_DOKTER = {"benar": 1}
BUKAN_SUPPORTED_JURI = {"juri": 1}
SEMUA_KLAIM = {"n": 1}
POSITIF_BENAR = {"benar_juri": 1}
NEGATIF_BENAR = {"n": 1, "benar": -1, "juri": -1, "benar_juri": 1}
SUPPORTED_DOKTER = {"n": 1, "benar": -1}


def naif(ambilan):
    taksiran, pengaruh = 0.0, 0.0
    for sumber, tanda in ambilan.tanda.items():
        laju_juri, pengaruh_juri = rasio(ambilan, [sumber], BUKAN_SUPPORTED_JURI, SEMUA_KLAIM)
        taksiran = taksiran + tanda * laju_juri
        pengaruh = pengaruh + tanda * pengaruh_juri
    return taksiran, pengaruh


def ppi_lambda(ambilan, bobot_juri):
    taksiran, pengaruh = 0.0, 0.0
    for sumber, tanda in ambilan.tanda.items():
        bobot_sumber = bobot_juri[sumber] if isinstance(bobot_juri, dict) else bobot_juri
        bobot = np.broadcast_to(bobot_sumber, ambilan.jumlah.shape[:1])
        laju_dokter, pengaruh_dokter = rasio(ambilan, [sumber], BUKAN_SUPPORTED_DOKTER, SEMUA_KLAIM)
        laju_juri, pengaruh_juri = rasio(ambilan, [sumber], BUKAN_SUPPORTED_JURI, SEMUA_KLAIM)
        sensus_juri = laju_sensus(ambilan, sumber, BUKAN_SUPPORTED_JURI)
        taksiran = taksiran + tanda * (laju_dokter + bobot * (sensus_juri - laju_juri))
        pengaruh = pengaruh + tanda * (pengaruh_dokter - bobot[:, None] * pengaruh_juri)
    return taksiran, pengaruh


def pengaruh_dokter_juri(ambilan, sumber):
    return (rasio(ambilan, [sumber], BUKAN_SUPPORTED_DOKTER, SEMUA_KLAIM)[1],
            rasio(ambilan, [sumber], BUKAN_SUPPORTED_JURI, SEMUA_KLAIM)[1])


def lambda_optimal(ambilan, pengaruh_dokter, pengaruh_juri):
    with np.errstate(divide="ignore", invalid="ignore"):
        bobot = kuadrat(ambilan, pengaruh_dokter, pengaruh_juri) / kuadrat(ambilan, pengaruh_juri, pengaruh_juri)
    return np.clip(np.nan_to_num(bobot), 0.0, 1.0)


def ppi_pp_berstrata(ambilan):
    return ppi_lambda(ambilan, {sumber: lambda_optimal(ambilan, *pengaruh_dokter_juri(ambilan, sumber))
                                for sumber in ambilan.tanda})


def ppi_pp_bersama(ambilan):
    pasangan = {sumber: pengaruh_dokter_juri(ambilan, sumber) for sumber in ambilan.tanda}
    gabungan_dokter = sum(tanda * pasangan[sumber][0] for sumber, tanda in ambilan.tanda.items())
    gabungan_juri = sum(tanda * pasangan[sumber][1] for sumber, tanda in ambilan.tanda.items())
    bobot = lambda_optimal(ambilan, gabungan_dokter, gabungan_juri)
    return ppi_lambda(ambilan, {sumber: bobot for sumber in ambilan.tanda})


def rogan_gladen(ambilan, kalibrasi_bersama):
    taksiran, pengaruh = 0.0, 0.0
    for sumber, tanda in ambilan.tanda.items():
        kalibrasi = list(ambilan.tanda) if kalibrasi_bersama else [sumber]
        sensitivitas, pengaruh_sens = rasio(ambilan, kalibrasi, POSITIF_BENAR, BUKAN_SUPPORTED_DOKTER)
        spesifisitas, pengaruh_spek = rasio(ambilan, kalibrasi, NEGATIF_BENAR, SUPPORTED_DOKTER)
        penyebut = sensitivitas + spesifisitas - 1
        penyebut = np.where(penyebut > 0, penyebut, np.nan)
        laju = (laju_sensus(ambilan, sumber, BUKAN_SUPPORTED_JURI) + spesifisitas - 1) / penyebut
        taksiran = taksiran + tanda * laju
        pengaruh = pengaruh + tanda * (
            (1 - laju)[:, None] * pengaruh_spek - laju[:, None] * pengaruh_sens) / penyebut[:, None]
    return taksiran, pengaruh


PENAKSIR = {
    "klasik": partial(ppi_lambda, bobot_juri=0.0),
    "PPI": partial(ppi_lambda, bobot_juri=1.0),
    "PPI++ bersama": ppi_pp_bersama,
    "PPI++ berstrata": ppi_pp_berstrata,
    "RG bersama": partial(rogan_gladen, kalibrasi_bersama=True),
    "RG per sumber": partial(rogan_gladen, kalibrasi_bersama=False),
}
