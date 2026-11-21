"""Gambar naskah JuriKlinis dari tabel agregat di Hasil_JuriKlinis_1.md, _2.md, dan _6.md.

Skrip ini tidak membaca data PhysioNet; ia mengurai tabel Markdown yang sudah dicetak skrip analisis, sehingga
angka di gambar sama dengan angka di berkas hasil. Gambar 1: sensitivitas juri pada klaim dokter lawan LLM per
setelan (abu-abu) dengan median per model (berlabel). Gambar 2: bias Δ juri saja per setelan dengan selang bootstrap.
Gambar 3: lebar selang PPI lawan label saja pada simulasi superpopulasi (median atas 126 setelan). Gambar S1: cakupan
selang lawan banyak pasien berlabel per penaksir pada audit tetap 100 pasien (penanda kosong = setelan terendah). Warna kategoris: palet bawaan skill dataviz, enam slot pertama, lolos validator mode
terang (peringatan kontras dijawab dengan label langsung dan bentuk penanda). Keluaran PNG 300 dpi dan PDF di
`analysis/Gambar/`.

Pakai:
    python analysis/juriklinis_gambar.py
"""
from io import StringIO
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

FOLDER = Path(__file__).resolve().parent
GAYA = {"warna": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"],
        "penanda": ["o", "s", "^", "D", "v", "P"], "tinta": "#3d3d3a", "kisi": "#e4e3df", "abu": "#b9b8b0"}
NAMA_PENAKSIR = {"klasik": "Labels only", "RG bersama": "Rogan–Gladen, shared",
                 "RG per sumber": "Rogan–Gladen, per source", "PPI": "PPI", "PPI++ bersama": "PPI++, one weight",
                 "PPI++ berstrata": "PPI++, weight per source"}
INDEKS_PENAKSIR = {"PPI": 0, "klasik": 1, "RG bersama": 2, "RG per sumber": 3, "PPI++ bersama": 4,
                   "PPI++ berstrata": 5}
NAMA_MODEL = {"Gemma-3-12B": "Gemma 3 12B", "Gemma-3-27B": "Gemma 3 27B", "Llama-8B": "Llama 3.1 8B",
              "Llama-70B": "Llama 3.1 70B", "R1-8B": "R1-Distill 8B", "R1-70B": "R1-Distill 70B",
              "Qwen-3-32B": "Qwen 3 32B", "Qwen-3-30B-A3B-Instruct": "Qwen 3 30B-A3B instruct",
              "Qwen-3-30B-A3B-Thinking": "Qwen 3 30B-A3B thinking"}


def tabel_markdown(berkas, awal_judul):
    baris = (FOLDER / berkas).read_text(encoding="utf-8").splitlines()
    mulai = next(nomor for nomor, isi in enumerate(baris) if isi.startswith(f"### {awal_judul}")) + 1
    sesudah = baris[mulai:]
    akhir = next((nomor for nomor, isi in enumerate(sesudah) if isi.startswith("### ")), len(sesudah))
    isi_tabel = [isi.strip().strip("|") for isi in sesudah[:akhir] if isi.startswith("|") and "---" not in isi]
    tabel = pd.read_csv(StringIO("\n".join(isi_tabel)), sep="|", skipinitialspace=True)
    tabel.columns = tabel.columns.str.strip()
    return tabel.apply(lambda kolom: kolom.str.strip() if kolom.dtype == object else kolom)


def rapikan(sumbu, judul_x, judul_y):
    sumbu.grid(color=GAYA["kisi"], linewidth=0.6)
    sumbu.set_axisbelow(True)
    for sisi in ("top", "right"):
        sumbu.spines[sisi].set_visible(False)
    sumbu.tick_params(colors=GAYA["tinta"], labelsize=8)
    sumbu.set_xlabel(judul_x, color=GAYA["tinta"], fontsize=9)
    sumbu.set_ylabel(judul_y, color=GAYA["tinta"], fontsize=9)


def gambar_sensitivitas():
    setelan = tabel_markdown("Hasil_JuriKlinis_1.md", "Tingkat per sumber")
    median = setelan.groupby("model")[["sens_dokter", "sens_llm"]].median()
    figur, sumbu = plt.subplots(figsize=(5.2, 5.0))
    sumbu.plot([0, 1], [0, 1], linestyle="--", color=GAYA["abu"], linewidth=1)
    sumbu.scatter(setelan["sens_dokter"], setelan["sens_llm"], s=14, color=GAYA["abu"], label="Judge setting")
    sumbu.scatter(median["sens_dokter"], median["sens_llm"], s=40, color=GAYA["warna"][0],
                  edgecolor="white", linewidth=1.5, zorder=3, label="Model median")
    geser_ke_kiri = {"Llama-8B", "Llama-70B", "R1-8B"}
    for model, titik in median.iterrows():
        kiri = model in geser_ke_kiri
        sumbu.annotate(NAMA_MODEL[model], (titik["sens_dokter"], titik["sens_llm"]), xytext=(-6 if kiri else 6, 0),
                       textcoords="offset points", fontsize=7, color=GAYA["tinta"], va="center",
                       ha="right" if kiri else "left")
    sumbu.set_xlim(0, 1)
    sumbu.set_ylim(0, 1)
    sumbu.set_aspect("equal")
    sumbu.legend(frameon=False, fontsize=8, loc="upper left")
    rapikan(sumbu, "Sensitivity on physician claims", "Sensitivity on LLM claims")
    return figur


def gambar_bias_setelan():
    setelan = tabel_markdown("Hasil_JuriKlinis_1.md", "Bias Δ naif per setelan")
    urutan = setelan.groupby("model")["bias"].median().sort_values().index
    figur, sumbu = plt.subplots(figsize=(6.4, 4.8))
    for batas in (-0.05, 0.05):
        sumbu.axvline(batas, linestyle="--", color=GAYA["abu"], linewidth=1)
    sumbu.axvline(0, color=GAYA["tinta"], linewidth=0.8)
    for indeks, (jenis, nama) in zip((2, 4), [("claim", "Facts retrieved as claims"),
                                                ("sentence", "Facts retrieved as sentences")]):
        baris = setelan[setelan["fact_type"] == jenis]
        posisi = (baris["model"].map({model: nomor for nomor, model in enumerate(urutan)})
                  + (baris["top_n"].rank(method="dense") - 4) * 0.07 + (0.12 if jenis == "sentence" else -0.12))
        sumbu.hlines(posisi, baris["bias_bawah"], baris["bias_atas"], color=GAYA["warna"][indeks], linewidth=0.8,
                     alpha=0.6)
        sumbu.scatter(baris["bias"], posisi, s=12, color=GAYA["warna"][indeks], marker=GAYA["penanda"][indeks],
                      zorder=3, label=nama)
    sumbu.set_yticks(range(len(urutan)), [NAMA_MODEL[model] for model in urutan])
    sumbu.legend(frameon=False, fontsize=8, loc="lower right")
    rapikan(sumbu, "Judge-only estimate minus true difference", "")
    return figur


def gambar_cakupan():
    ringkasan = tabel_markdown("Hasil_JuriKlinis_2.md", "Semua setelan juri")
    figur, panel = plt.subplots(1, 2, figsize=(7.0, 3.8))
    for sumbu, batas_y, judul in zip(panel, [(-0.03, 1.03), (0.80, 0.98)], ["(a) All estimators", "(b) Detail"]):
        sumbu.axhline(0.95, linestyle="--", color=GAYA["abu"], linewidth=1)
        for kode, nama in NAMA_PENAKSIR.items():
            baris = ringkasan[ringkasan["penaksir"] == kode]
            warna, penanda = GAYA["warna"][INDEKS_PENAKSIR[kode]], GAYA["penanda"][INDEKS_PENAKSIR[kode]]
            sumbu.plot(baris["banyak_label"], baris["cakupan_median"], color=warna, marker=penanda, markersize=5,
                       linewidth=1.5, label=nama)
            sumbu.scatter(baris["banyak_label"], baris["cakupan_min"], marker=penanda, s=18, facecolor="none",
                          edgecolor=warna, linewidth=1)
        sumbu.set_xticks([5, 10, 20, 30, 50])
        sumbu.set_ylim(*batas_y)
        sumbu.set_title(judul, fontsize=9, color=GAYA["tinta"], loc="left")
        rapikan(sumbu, "Labelled patients (m)", "Coverage of the 95% interval")
    panel[1].set_ylabel("")
    pegangan, nama_seri = panel[0].get_legend_handles_labels()
    figur.legend(pegangan, nama_seri, frameon=False, fontsize=8, loc="lower center", ncol=3)
    figur.tight_layout(rect=(0, 0.14, 1, 1))
    return figur


def gambar_lebar():
    ringkasan = tabel_markdown("Hasil_JuriKlinis_6.md", "Superpopulasi, varian utama (klaim, biner, human_gt): ringkasan")
    figur, sumbu = plt.subplots(figsize=(5.2, 3.8))
    sumbu.axhline(0.10, linestyle="--", color=GAYA["abu"], linewidth=1)
    for kode in ["PPI", "klasik"]:
        baris = ringkasan[ringkasan["penaksir"] == kode]
        sumbu.plot(baris["banyak_label"], baris["lebar_median"], color=GAYA["warna"][INDEKS_PENAKSIR[kode]],
                   marker=GAYA["penanda"][INDEKS_PENAKSIR[kode]], markersize=5, linewidth=1.5,
                   label=NAMA_PENAKSIR[kode])
    sumbu.set_xscale("log")
    sumbu.set_xticks([5, 10, 20, 30, 50, 100, 200], ["5", "10", "20", "30", "50", "100", "200"])
    sumbu.minorticks_off()
    sumbu.legend(frameon=False, fontsize=8)
    rapikan(sumbu, "Reviewed patients (m)", "Interval width")
    return figur


def main():
    keluaran = FOLDER / "Gambar"
    keluaran.mkdir(exist_ok=True)
    for nomor, buat in [("1", gambar_sensitivitas), ("2", gambar_bias_setelan), ("3", gambar_lebar),
                        ("S1", gambar_cakupan)]:
        figur = buat()
        if not figur.legends:
            figur.tight_layout()
        for akhiran in ("png", "pdf"):
            figur.savefig(keluaran / f"JuriKlinis_Gambar{nomor}.{akhiran}", dpi=300)
        plt.close(figur)


if __name__ == "__main__":
    main()
