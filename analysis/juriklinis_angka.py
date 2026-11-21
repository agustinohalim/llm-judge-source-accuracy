"""Format angka untuk tabel suplemen JuriKlinis: tiga desimal, tanda plus/minus tipografis, ∞ untuk tak tercapai."""


def angka(nilai, digit=3):
    return "∞" if str(nilai) in ("inf", "nan") else f"{float(nilai):.{digit}f}"


def bertanda(nilai):
    teks = f"{float(nilai):+.3f}"
    return "0.000" if teks in ("+0.000", "-0.000") else teks.replace("-", "−")


def banyak_setelan(nilai):
    return "—" if str(nilai) == "-" else str(int(float(nilai)))
