"""Δ juri saja pada beda benar kecil (rencana bagian M butir 1, post hoc, tanpa data baru).

Skrip ini tidak membaca data PhysioNet; ia mengurai tabel per setelan Hasil_JuriKlinis_1.md (sens dan spek juri per
sumber) dan memasukkannya ke q_s = sens_s · p_s + (1 − spek_s)(1 − p_s). Tingkat benar sumber yang lebih rendah
ditetapkan pada acuan (0,050 = tingkat LLM teramati; 0,10 sebagai kepekaan), sumber lainnya acuan + |Δ|; Δ > 0 berarti
dokter lebih tinggi. Asumsi: sens dan spek juri per sumber tidak berubah bila tingkat benar berubah. Pemeriksaan: pada
p teramati rumus mengulang q yang dicetak di tabel.

Pakai:
    python analysis/juriklinis_bias_nol.py > keluaran.md
"""
import numpy as np
import pandas as pd

from juriklinis_gambar import tabel_markdown
from juriklinis_markdown import cetak_judul, cetak_markdown

JUDUL_TABEL = "Tingkat per sumber dan ketepatan juri"
BEDA_BENAR = [-0.10, -0.05, 0.0, 0.05, 0.10]
TINGKAT_ACUAN = [0.050, 0.10]
AMBANG_MELESET = 0.05
KOLOM_ANGKA = ["p_dokter", "q_dokter", "sens_dokter", "spek_dokter", "p_llm", "q_llm", "sens_llm", "spek_llm"]


def baca_setelan():
    tabel = tabel_markdown("Hasil_JuriKlinis_1.md", JUDUL_TABEL)
    return tabel.astype({kolom: float for kolom in KOLOM_ANGKA})


def tingkat_juri(sens, spek, tingkat_benar):
    return sens * tingkat_benar + (1 - spek) * (1 - tingkat_benar)


def selisih_juri(setelan, tingkat_dokter, tingkat_llm):
    return (tingkat_juri(setelan["sens_dokter"], setelan["spek_dokter"], tingkat_dokter)
            - tingkat_juri(setelan["sens_llm"], setelan["spek_llm"], tingkat_llm))


def tingkat_benar(acuan, beda):
    return (acuan + max(beda, 0.0), acuan + max(-beda, 0.0))


def ringkas_beda(setelan, acuan, beda):
    juri = selisih_juri(setelan, *tingkat_benar(acuan, beda))
    nol = not beda
    return {"acuan": acuan, "delta_benar": beda, "median": juri.median(), "min": juri.min(), "maks": juri.max(),
            "tanda_salah": "-" if nol else int((np.sign(juri) != np.sign(beda)).sum()),
            "meleset_0,05": int(((juri - beda).abs() >= AMBANG_MELESET).sum()),
            "palsu_naik": int((juri >= AMBANG_MELESET).sum()) if nol else "-",
            "palsu_turun": int((juri <= -AMBANG_MELESET).sum()) if nol else "-"}


def per_model_nol(setelan, acuan):
    juri = setelan.assign(delta_juri=selisih_juri(setelan, acuan, acuan))
    return (juri.groupby("model")["delta_juri"].agg(median="median", min="min", maks="max")
            .reset_index().sort_values("median"))


def galat_rumus(setelan):
    dokter = tingkat_juri(setelan["sens_dokter"], setelan["spek_dokter"], setelan["p_dokter"]) - setelan["q_dokter"]
    llm = tingkat_juri(setelan["sens_llm"], setelan["spek_llm"], setelan["p_llm"]) - setelan["q_llm"]
    return float(max(dokter.abs().max(), llm.abs().max()))


def main():
    setelan = baca_setelan()
    cetak_judul(f"Pemeriksaan rumus pada p teramati ({len(setelan)} setelan): galat mutlak maksimum q")
    print(f"{galat_rumus(setelan):.4f} (pembulatan tabel tiga desimal)")
    ringkasan = pd.DataFrame([ringkas_beda(setelan, acuan, beda) for acuan in TINGKAT_ACUAN for beda in BEDA_BENAR])
    cetak_judul(f"Δ juri saja menurut beda benar (atas {len(setelan)} setelan; tingkat rendah = acuan)")
    cetak_markdown(ringkasan)
    for acuan in TINGKAT_ACUAN:
        cetak_judul(f"Δ juri saja per model pada beda benar 0 (kedua sumber {acuan:.3f})")
        cetak_markdown(per_model_nol(setelan, acuan))


if __name__ == "__main__":
    main()
