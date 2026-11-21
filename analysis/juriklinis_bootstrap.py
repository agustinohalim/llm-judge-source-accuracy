"""Bootstrap per pasien untuk skrip JuriKlinis.

Proposisi bersarang di pasien, dan tiap pasien punya BHC dokter dan BHC LLM, jadi yang diambil ulang adalah
pasien beserta kedua sumbernya. Bobot yang sama dipakai untuk semua setelan juri agar perbandingan antarjuri
memakai ambilan acak yang sama.
"""
import numpy as np

ULANGAN_BOOTSTRAP = 2000
BENIH = 20261121
TINGKAT_SELANG = 0.95


def bobot_bootstrap(banyak_pasien):
    acak = np.random.default_rng(BENIH)
    ambilan = acak.integers(0, banyak_pasien, size=(ULANGAN_BOOTSTRAP, banyak_pasien))
    bobot = np.zeros((ULANGAN_BOOTSTRAP, banyak_pasien))
    np.add.at(bobot, (np.arange(ULANGAN_BOOTSTRAP)[:, None], ambilan), 1)
    return bobot


def timbang(hitungan, bobot):
    return {sumber: {kolom: bobot @ nilai for kolom, nilai in per_kolom.items()}
            for sumber, per_kolom in hitungan.items()}


def selang_persentil(ulangan):
    return np.quantile(ulangan, [(1 - TINGKAT_SELANG) / 2, (1 + TINGKAT_SELANG) / 2])
