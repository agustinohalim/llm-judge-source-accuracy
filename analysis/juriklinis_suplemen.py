"""Suplemen naskah JuriKlinis dari tabel agregat di Hasil_JuriKlinis_2.md sampai _6.md.

Seperti juriklinis_gambar.py, skrip ini tidak membaca data PhysioNet; ia mengurai tabel Markdown yang sudah dicetak
skrip analisis, lalu menulis Naskah_JuriKlinis_Suplemen.md (bahasa Inggris) dengan tabel menurut urutan rujukan di
naskah. Ketepatan juri per model ada di Tabel 2 naskah, bukan di sini. S1: sensitivitas per sumber di dalam tiap jenis
label (_4). S2: selang bootstrap pasien untuk beda sensitivitas dan asimetri pada label bulat (_5). S3: label satu
dokter acak lawan label akhir, sel 1–10 tetap "<11" (_3). S4: keenam penaksir pada simulasi superpopulasi (_6). S5:
ketujuh penaksir pada audit tetap 100 pasien dengan koreksi populasi hingga (_2). S6: anggaran label per model untuk
kedua rancangan (_6, _2). Gambar S1 dibuat juriklinis_gambar.py.

Pakai:
    python analysis/juriklinis_suplemen.py
"""
import pandas as pd

from juriklinis_gambar import FOLDER, NAMA_MODEL, NAMA_PENAKSIR, tabel_markdown

NAMA_SUMBER = {"human": "Physician BHC", "llm": "LLM BHC"}
PENAKSIR_UTAMA = ["PPI", "klasik", "RG bersama"]
JUDUL_SUPERPOPULASI = "Superpopulasi, varian utama (klaim, biner, human_gt)"
KEPALA = """# Supplementary material

Supplement to "Source-Dependent Accuracy of LLM Judges When Comparing Physician-Written and LLM-Written
Hospital-Course Summaries". A claim is unverified if its final physician label is Not Supported or Not Addressed; a
judge flags a claim when its verdict is not Supported (in the label-type analyses, when its verdict is that label). All
values are aggregates over the 100 patients of MIMIC-III-Ext-VeriFact-BHC v1.1.0; counts between 1 and 10 are shown as
"<11", as the data use agreement requires. Medians are over the 14 judge settings of each model unless stated
otherwise. Large population: patients drawn with replacement, no finite-population correction (exploratory). Fixed
audit: patients drawn without replacement from these 100, with the finite-population correction (planned stage 2).
Tables S1, S2 and S4 are exploratory analyses added after the main results.

**Fig. S1.** Coverage of the 95% interval for the difference against the number of physician-reviewed patients in the
fixed audit, all six estimators (file JuriKlinis_GambarS1). Lines and filled markers: median over 126 settings; open
markers: lowest setting. (a) Full range; (b) the same on 0.80–0.98. Dashed line: nominal 0.95.
"""


def angka(nilai, digit=3):
    return "∞" if str(nilai) in ("inf", "nan") else f"{float(nilai):.{digit}f}"


def bertanda(nilai):
    teks = f"{float(nilai):+.3f}"
    return "0.000" if teks in ("+0.000", "-0.000") else teks.replace("-", "−")


def tabel_s1():
    bagian = []
    for jenis in ("Not Supported", "Not Addressed"):
        peka = tabel_markdown("Hasil_JuriKlinis_4.md", f"Sensitivitas juri di dalam {jenis}")
        bagian.append(pd.DataFrame({
            "Judge": peka["model"].map(NAMA_MODEL),
            "Label type": jenis,
            "Sensitivity, physician": peka["sens_dokter"].map(angka),
            "Sensitivity, LLM": peka["sens_llm"].map(angka),
            "Difference, median": peka["beda_median"].map(bertanda),
            "Settings with physician higher (of 14)": peka["dokter_lebih_tinggi"].astype(str),
        }))
    return ("**Table S1.** Exploratory: judge sensitivity by source within each label type of the final physician "
            "label, by model.", pd.concat(bagian))


def tabel_s2():
    selang = tabel_markdown("Hasil_JuriKlinis_5.md", "Beda sensitivitas dan spesifisitas")
    bulat = tabel_markdown("Hasil_JuriKlinis_5.md", "Sensitivitas juri per sumber pada klaim bulat")
    gabung = selang.merge(bulat, on="model", validate="one_to_one")
    keluar = pd.DataFrame({
        "Judge": gabung["model"].map(NAMA_MODEL),
        "Sensitivity difference, median (smallest lower limit)": [
            f"{bertanda(a)} ({bertanda(b)})" for a, b in zip(gabung["sens_beda_median"], gabung["sens_bawah_min"])],
        "Settings with interval above 0 (of 14)": gabung["sens_selang_di_atas_0"].astype(str),
        "Specificity difference, median": gabung["spek_beda_median"].map(bertanda),
        "Unanimous claims: sensitivity, physician": gabung["sens_dokter"].map(angka),
        "Unanimous claims: sensitivity, LLM": gabung["sens_llm"].map(angka),
        "Unanimous claims: settings with physician higher (of 14)": gabung["dokter_lebih_tinggi"].astype(str),
    })
    return ("**Table S2.** Exploratory: physician-minus-LLM differences in judge sensitivity and specificity with 95% "
            "percentile bootstrap intervals over patients (2000 resamples), and judge sensitivity by source on the "
            "3501 physician and 2877 LLM claims whose three first-round physician labels agreed (602 and 41 of them "
            "unverified).", keluar)


def tabel_s3():
    silang = tabel_markdown("Hasil_JuriKlinis_3.md", "Label dokter acak")
    silang = silang[silang["proposition_type"] == "claim"]
    keluar = pd.DataFrame({
        "Source": silang["author_type"].map(NAMA_SUMBER),
        "Final label (consensus)": silang["human_gt"],
        "First-round label, one random physician": silang["dokter_acak"],
        "Claims": silang["proposisi"].astype(str),
    })
    return ("**Table S3.** First-round label of one physician drawn at random per claim against the final label, atomic "
            "claims. Cells with 1–10 claims are masked.", keluar)


def ringkasan_penaksir(semua):
    semua = semua[semua["banyak_label"] > 0]
    return pd.DataFrame({
        "Estimator": semua["penaksir"].map(NAMA_PENAKSIR),
        "Patients reviewed (m)": semua["banyak_label"].astype(str),
        "Bias": semua["bias_median"].map(bertanda),
        "Coverage (lowest setting)": [f"{angka(a)} ({angka(b)})" for a, b in
                                      zip(semua["cakupan_median"], semua["cakupan_min"])],
        "Width": semua["lebar_median"].map(angka),
        "Failed draws, maximum": semua["gagal_maks"].map(angka),
    })


def tabel_s4_s5():
    superpopulasi = tabel_markdown("Hasil_JuriKlinis_6.md", f"{JUDUL_SUPERPOPULASI}: ringkasan")
    audit = tabel_markdown("Hasil_JuriKlinis_2.md", "Semua setelan juri")
    return [("**Table S4.** Exploratory: all six estimators by number of physician-reviewed patients drawn from a large "
             "population (1000 draws with replacement per m, no finite-population correction). Median over 126 "
             "settings; PPI++ is PPI with a variance-minimising weight on the judge term, one weight or one per source.",
             ringkasan_penaksir(superpopulasi)),
            ("**Table S5.** All six estimators by number of physician-reviewed patients in the fixed audit of these 100 "
             "patients (1000 draws without replacement per m, finite-population correction). Median over 126 settings.",
             ringkasan_penaksir(audit))]


def tabel_s6():
    superpopulasi = tabel_markdown("Hasil_JuriKlinis_6.md", f"{JUDUL_SUPERPOPULASI}: anggaran label per model")
    audit = tabel_markdown("Hasil_JuriKlinis_2.md", "Anggaran label")
    gabung = superpopulasi.merge(audit, on=["model", "penaksir"], suffixes=("_super", "_audit"), validate="one_to_one")
    gabung = gabung[gabung["penaksir"].isin(PENAKSIR_UTAMA)]
    keluar = pd.DataFrame({
        "Judge": gabung["model"].map(NAMA_MODEL),
        "Estimator": gabung["penaksir"].map(NAMA_PENAKSIR),
        "Large population: budget m, median (settings reaching it of 14)": [
            f"{angka(a, 0)} ({b})" for a, b in zip(gabung["m_median_super"], gabung["setelan_tercapai_super"])],
        "Fixed audit: budget m, median (settings reaching it of 14)": [
            f"{angka(a, 0)} ({b})" for a, b in zip(gabung["m_median_audit"], gabung["setelan_tercapai_audit"])],
    })
    return ("**Table S6.** Review budget by model: smallest m on the grid with coverage ≥ 0.93 and width ≤ 0.10 (∞ = not "
            "reached by m = 200 in the large population or m = 50 in the fixed audit).", keluar)


def markdown_tabel(judul, tabel):
    baris = ["| " + " | ".join(tabel.columns) + " |", "|" + "---|" * len(tabel.columns)]
    baris += ["| " + " | ".join(str(sel) for sel in rekam) + " |" for rekam in tabel.itertuples(index=False)]
    return judul + "\n\n" + "\n".join(baris) + "\n"


def main():
    tabel = [tabel_s1(), tabel_s2(), tabel_s3(), *tabel_s4_s5(), tabel_s6()]
    bagian = [markdown_tabel(judul, isi) for judul, isi in tabel]
    (FOLDER / "Naskah_JuriKlinis_Suplemen.md").write_text(KEPALA + "\n" + "\n".join(bagian), encoding="utf-8")


if __name__ == "__main__":
    main()
