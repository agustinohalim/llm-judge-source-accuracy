"""Skema tabel VeriFact-BHC v1.1.0 (Chung dkk., PhysioNet, lisensi credentialed 1.5.0) untuk JuriKlinis.

Membaca tabel proposisi, label dokter, dan vonis juri dari $VERIFACT_BHC (di luar repo), lalu
mencetak per tabel jumlah baris serta nama, tipe, dan banyaknya nilai unik tiap kolom. Sebaran nilai
hanya dicetak untuk kolom label (paling banyak 12 nilai unik dan bukan teks bebas — kolom komentar dokter
yang jarang terisi juga punya sedikit nilai unik, jadi disaring menurut nama), dengan hitungan 1-10 dicetak
"<11", karena keluaran ini dibaca asisten AI dan DUA PhysioNet melarang teks atau data tingkat pasien
keluar dari laptop. Konteks rujukan EHR hanya dicetak skemanya dari metadata Parquet; tabel EHR mentah
tidak disentuh. Tidak ada analisis.

Pakai:
    python analysis/juriklinis_skema.py [folder_data]
"""
import pandas as pd
import pyarrow.parquet as pq

from juriklinis_data import cari_folder_rilis
from juriklinis_markdown import samarkan_sel_kecil

TABEL_CSV = [
    "propositions/propositions.csv.gz",
    "propositions/human_verdicts.csv.gz",
    "propositions/proposition_validity.csv.gz",
    "verifact/rater_configurations.csv",
    "verifact/experiment_matrix.csv",
    "verifact/model_metadata.csv",
]
TABEL_VONIS = "verifact/verdicts.parquet"
KOLOM_VONIS_DIBACA = ["model", "rater_alias", "verdict"]
TABEL_KONTEKS = "verifact/reference_payloads.parquet"
BATAS_NILAI_UNIK_LABEL = 12
PREFIKS_KOLOM_TEKS_BEBAS = ("comment", "adjudicated_comment", "text", "parent_text_chunk",
                            "brief_hospital_course", "reason", "reference")
PANJANG_NILAI_MAKS = 60


def main():
    folder_rilis = cari_folder_rilis()
    for nama in TABEL_CSV:
        cetak_tabel(nama, pd.read_csv(folder_rilis / nama, low_memory=False))
    vonis = pd.read_parquet(folder_rilis / TABEL_VONIS, columns=KOLOM_VONIS_DIBACA)
    cetak_tabel(f"{TABEL_VONIS} (kolom {', '.join(KOLOM_VONIS_DIBACA)})", vonis)
    cetak_skema_parquet(folder_rilis, TABEL_VONIS)
    cetak_skema_parquet(folder_rilis, TABEL_KONTEKS)


def cetak_tabel(nama, tabel):
    print(f"\n### `{nama}` — {len(tabel)} baris, {tabel.shape[1]} kolom\n")
    print("| Kolom | Tipe | Nilai unik | Sebaran (kolom label saja) |")
    print("|---|---|---|---|")
    for nama_kolom in tabel.columns:
        kolom = tabel[nama_kolom]
        print(f"| `{nama_kolom}` | {kolom.dtype} | {kolom.nunique(dropna=False)} | {ringkas_sebaran(kolom)} |")


def ringkas_sebaran(kolom):
    if adalah_teks_bebas(kolom.name):
        return f"teks bebas, tidak dicetak; terisi {kolom.notna().sum()}"
    if kolom.nunique(dropna=False) > BATAS_NILAI_UNIK_LABEL:
        return ""
    hitungan = kolom.value_counts(dropna=False)
    return "; ".join(f"{potong_nilai(nilai)}: {samarkan_sel_kecil(n)}" for nilai, n in hitungan.items())


def adalah_teks_bebas(nama_kolom):
    return nama_kolom.startswith(PREFIKS_KOLOM_TEKS_BEBAS)


def potong_nilai(nilai):
    return str(nilai)[:PANJANG_NILAI_MAKS].replace("|", "/").replace("\n", " ")


def cetak_skema_parquet(folder_rilis, nama):
    berkas = pq.ParquetFile(folder_rilis / nama)
    print(f"\n### `{nama}` — skema dari metadata, {berkas.metadata.num_rows} baris\n")
    for medan in berkas.schema_arrow:
        print(f"- `{medan.name}`: {medan.type}")


if __name__ == "__main__":
    main()
