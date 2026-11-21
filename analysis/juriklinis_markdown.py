"""Cetak tabel agregat sebagai Markdown untuk disalin ke Hasil_JuriKlinis_*.md.

Hitungan 1-10 dicetak "<11" karena keluaran dibaca asisten AI dan DUA PhysioNet melarang sel kecil keluar.
"""

SEL_KECIL = 11


def samarkan_sel_kecil(n):
    return f"<{SEL_KECIL}" if 0 < n < SEL_KECIL else str(n)


def cetak_judul(judul):
    print(f"\n### {judul}\n")


def cetak_markdown(tabel):
    print("| " + " | ".join(str(kolom) for kolom in tabel.columns) + " |")
    print("|" + "---|" * tabel.shape[1])
    for baris in tabel.itertuples(index=False):
        print("| " + " | ".join(format_sel(nilai) for nilai in baris) + " |")


def format_sel(nilai):
    return f"{nilai:.3f}" if isinstance(nilai, float) else str(nilai)
