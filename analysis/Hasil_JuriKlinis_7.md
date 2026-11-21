# Hasil JuriKlinis 7 — anggaran kontinu dari lebar superpopulasi (rencana bagian L, post hoc)

> Dihasilkan 21 Nov 2026 oleh `juriklinis_anggaran_kontinu.py` dari tabel ringkasan `Hasil_JuriKlinis_6.md` (median
> lebar atas 126 setelan); tidak membaca data PhysioNet dan tidak menjalankan ulang simulasi. Rumus dicatat di
> `Artikel_JuriKlinis_Rencana.md` bagian L sebelum dihitung. Tanpa koreksi populasi hingga (superpopulasi).

## Ringkasan

1. **Utama:** untuk lebar 0,10, PPI butuh ±20 pasien (19,8 dari acuan m = 50; 19,4–20,8 dari acuan 100 dan 20), label
   saja ±49 (49,0; 49,0–51,2). Rasio (w_PPI / w_label)² pada m = 50 = 0,405: PPI butuh ±40 % pasien label saja.
2. **Satu dokter acak:** PPI ±20, label saja ±46, rasio 0,431.
3. **Not Supported saja:** PPI ±20, label saja ±13 (12,5; 12,8–13,0), rasio 1,588: PPI butuh ±1,6 kali pasien label
   saja; juri menambah varians.
4. **Not Addressed saja:** PPI ±20, label saja ±39 (38,7; 38,4–40,9), rasio 0,513.
5. **Kalimat BHC LLM (tingkat LLM):** PPI ±24, label saja ±8, rasio 2,976.
6. Lebar PPI hampir sama pada varian utama, Not Supported, dan Not Addressed (0,063 pada m = 50; audit tetap juga
   0,092–0,093 pada m = 20, `Hasil_JuriKlinis_3.md`), sehingga m PPI sama; yang berubah antarvarian adalah lebar label
   saja. Anggaran ini adalah median lebar, bukan median anggaran per setelan, dan tidak memuat ketidakpastian dari
   100 pasien.

## Log mentah

### Anggaran kontinu untuk lebar 0,10 (m · (w_m / 0,10)², median lebar atas 126 setelan) dan rasio efisiensi (w_PPI / w_label)² pada m = 50

| varian | m_PPI_acuan50 | m_PPI_acuan20 | m_PPI_acuan100 | m_klasik_acuan50 | m_klasik_acuan20 | m_klasik_acuan100 | rasio_PPI_per_label_m50 |
|---|---|---|---|---|---|---|---|
| utama | 19.845 | 20.808 | 19.360 | 49.005 | 51.200 | 49.000 | 0.405 |
| satu dokter acak | 19.845 | 21.218 | 20.250 | 46.080 | 48.672 | 46.240 | 0.431 |
| Not Supported saja | 19.845 | 21.218 | 19.360 | 12.500 | 12.800 | 12.960 | 1.588 |
| Not Addressed saja | 19.845 | 20.808 | 19.360 | 38.720 | 40.898 | 38.440 | 0.513 |
| kalimat BHC LLM (tingkat) | 23.805 | 25.088 | 24.010 | 8.000 | 8.450 | 7.840 | 2.976 |
