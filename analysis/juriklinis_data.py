"""Letak dan pembacaan rilis VeriFact-BHC v1.1.0 (PhysioNet credentialed) untuk skrip JuriKlinis.

Data berada di luar repo, di folder $VERIFACT_BHC (bawaan data/verifact-bhc). Hanya kolom kunci yang dibaca; kolom teks
(proposisi, BHC, komentar dokter, alasan juri) tidak pernah dimuat.
"""
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

FOLDER_DATA_BAKU = Path(os.environ.get("VERIFACT_BHC", "data/verifact-bhc"))
BERKAS_PROPOSISI = "propositions/propositions.csv.gz"
BERKAS_KEBENARAN = "propositions/human_verdicts.csv.gz"
BERKAS_VALIDITAS = "propositions/proposition_validity.csv.gz"
BERKAS_VONIS = "verifact/verdicts.parquet"
BERKAS_KONFIGURASI = "verifact/rater_configurations.csv"
STRATA = ["author_type", "proposition_type"]
KOLOM_SETELAN = ["model", "fact_type", "top_n", "rater_alias"]
LABEL_DIDUKUNG = "Supported"
JENIS_KLAIM = "claim"
KOLOM_DOKTER_PUTARAN_1 = ["verdict1", "verdict2", "verdict3"]


def cari_folder_rilis():
    folder_data = Path(sys.argv[1]) if len(sys.argv) > 1 else FOLDER_DATA_BAKU
    calon = [berkas.parent for berkas in folder_data.rglob("SHA256SUMS.txt")]
    if len(calon) != 1:
        raise SystemExit(f"Harus ada tepat satu SHA256SUMS.txt di bawah {folder_data}, ditemukan {len(calon)}")
    return calon[0]


def baca_proposisi(folder_rilis):
    proposisi = pd.read_csv(folder_rilis / BERKAS_PROPOSISI,
                            usecols=["proposition_id", *STRATA, "subject_id"])
    kebenaran = pd.read_csv(folder_rilis / BERKAS_KEBENARAN, usecols=["proposition_id", "human_gt"])
    validitas = pd.read_csv(folder_rilis / BERKAS_VALIDITAS, usecols=["proposition_id", "invalid"])
    return (proposisi
            .merge(kebenaran, on="proposition_id", validate="one_to_one")
            .merge(validitas, on="proposition_id", validate="one_to_one"))


def baca_dokter_acak(folder_rilis, acak):
    label = pd.read_csv(folder_rilis / BERKAS_KEBENARAN, usecols=["proposition_id", *KOLOM_DOKTER_PUTARAN_1])
    pilihan = acak.integers(0, len(KOLOM_DOKTER_PUTARAN_1), len(label))
    terpilih = label[KOLOM_DOKTER_PUTARAN_1].to_numpy()[np.arange(len(label)), pilihan]
    return pd.DataFrame({"proposition_id": label["proposition_id"], "dokter_acak": terpilih})


def baca_vonis(folder_rilis, proposisi, jenis_proposisi):
    terpilih = proposisi.loc[proposisi["proposition_type"] == jenis_proposisi].drop(columns="proposition_type")
    vonis = pd.read_parquet(folder_rilis / BERKAS_VONIS, columns=["proposition_id", "rater_alias", "verdict"])
    vonis = vonis.merge(terpilih, on="proposition_id", validate="many_to_one")
    if vonis.duplicated(["rater_alias", "proposition_id"]).any():
        raise SystemExit("Ada proposisi yang divonis lebih dari sekali oleh alias yang sama")
    sumber_per_alias = vonis.groupby("rater_alias")["author_type"].nunique()
    alias_lengkap = sumber_per_alias.index[sumber_per_alias == vonis["author_type"].nunique()]
    konfigurasi = pd.read_csv(folder_rilis / BERKAS_KONFIGURASI,
                              usecols=["rater_alias", "model", "fact_type", "top_n"])
    return (vonis[vonis["rater_alias"].isin(alias_lengkap)]
            .merge(konfigurasi, on="rater_alias", validate="many_to_one"))


def tandai(vonis, kolom_kebenaran="human_gt", label_positif=None):
    if label_positif is None:
        return vonis.assign(benar=vonis[kolom_kebenaran] != LABEL_DIDUKUNG, juri=vonis["verdict"] != LABEL_DIDUKUNG)
    return vonis.assign(benar=vonis[kolom_kebenaran] == label_positif, juri=vonis["verdict"] == label_positif)


def baca_vonis_klaim(folder_rilis):
    return tandai(baca_vonis(folder_rilis, baca_proposisi(folder_rilis), JENIS_KLAIM))


def hitung_per_pasien(vonis):
    return (vonis.assign(benar_juri=vonis["benar"] & vonis["juri"])
            .groupby([*KOLOM_SETELAN, "author_type", "subject_id"], dropna=False)
            .agg(n=("proposition_id", "size"), benar=("benar", "sum"), juri=("juri", "sum"),
                 benar_juri=("benar_juri", "sum"))
            .reset_index())
