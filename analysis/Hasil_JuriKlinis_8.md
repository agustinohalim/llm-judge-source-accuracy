# Hasil JuriKlinis 8 — bias juri saja pada beda benar kecil dan selang anggaran (rencana bagian M, post hoc)

> Dihasilkan 21 Nov 2026 oleh `juriklinis_bias_nol.py` (butir 1; mengurai tabel per setelan `Hasil_JuriKlinis_1.md`,
> tidak membaca data PhysioNet) dan `juriklinis_selang_anggaran.py` (butir 2; data lokal, hanya agregat, tanpa sel
> hitungan). Rancangan dicatat di `Artikel_JuriKlinis_Rencana.md` bagian M sebelum dijalankan. Persiapan revisi
> (methods X1 dan X2 panel 9); sesudah hasil, pengguna memilih memasukkannya ke naskah sebelum kirim (21 Nov).

## Ringkasan

1. **Pemeriksaan rumus.** q = sens · p + (1 − spek)(1 − p) mengulang tingkat juri tabel pada p teramati (galat
   maksimum 0,0009, pembulatan tiga desimal).
2. **Beda benar 0 (kedua sumber 0,050).** Δ juri saja median +0,096 (rentang +0,022 s.d. +0,308); 115/126 setelan
   memberi kelebihan dokter ≥ 0,05, tak satu pun ≤ −0,05. Per model median +0,049 (Gemma 3 27B) s.d. +0,130 (Llama
   3.1 70B), sesuai hitungan kasar panel (+0,05 s.d. +0,13). Acuan 0,10: median +0,108, 121/126 ≥ 0,05.
3. **LLM benar-benar lebih buruk (Δ −0,05 dan −0,10).** Δ juri saja tetap positif di **126/126** setelan (median
   +0,081 dan +0,065): juri saja akan menyatakan ringkasan dokter lebih buruk padahal ringkasan LLM yang lebih buruk.
   Sama pada acuan 0,10.
4. **Dokter lebih buruk (Δ +0,05 dan +0,10).** Tanda selalu benar (0/126 salah), tetapi besarnya meleset ≥ 0,05 pada
   90/126 dan 63/126 setelan (median +0,120 dan +0,148; dilebih-lebihkan).
5. **Artinya.** Arah yang benar pada data ini (Δ benar 0,281) datang dari beda benar yang besar ditambah bias ke arah
   yang sama (spesifisitas juri lebih rendah pada klaim dokter), bukan dari ketepatan juri. Pada beda kecil atau
   terbalik, juri saja memberi kelebihan dokter palsu di hampir semua setelan. Asumsi: sens dan spek juri per sumber
   tetap bila tingkat benar berubah (ekstrapolasi, bukan pengamatan).
6. **Selang anggaran (utama, lebar 0,10).** PPI 19,6 pasien [14,7; 24,6], label saja 48,8 [34,0; 63,1], rasio 0,40
   [0,28; 0,59]: batas atas rasio < 1, jadi penghematan juri bertahan atas ketidakpastian sampel 100 pasien.
   Nilai data asli dekat `Hasil_JuriKlinis_7.md` (19,8 dan 49,0; rumus z, bukan simulasi).
7. **Not Supported saja.** PPI 19,7 [15,5; 24,0], label saja 12,9 [6,9; 19,7], rasio 1,52 [1,09; 2,58]: juri
   menambah varians dengan pasti di sini.
8. **Kalimat BHC LLM (tingkat).** PPI 23,4 [19,3; 26,6], label saja 7,7 [5,2; 11,0], rasio 3,06 [2,21; 4,06].

Untuk revisi (bagian M rencana): butir 2–5 memenuhi syarat "sebagian besar setelan", jadi abstrak, Simpulan, dan
Diskusi menulis bahwa arahnya benar karena beda benar besar, dan juri saja tak dapat dipakai untuk menyimpulkan
arah bila bedanya kecil. CRS memberi rentang (±15–25 pasien), bukan "about 20".

## Log mentah

### Pemeriksaan rumus pada p teramati (126 setelan): galat mutlak maksimum q

0.0009 (pembulatan tabel tiga desimal)

### Δ juri saja menurut beda benar (atas 126 setelan; tingkat rendah = acuan)

| acuan | delta_benar | median | min | maks | tanda_salah | meleset_0,05 | palsu_naik | palsu_turun |
|---|---|---|---|---|---|---|---|---|
| 0.050 | -0.100 | 0.065 | 0.011 | 0.279 | 126 | 126 | - | - |
| 0.050 | -0.050 | 0.081 | 0.019 | 0.294 | 126 | 126 | - | - |
| 0.050 | 0.000 | 0.096 | 0.022 | 0.308 | - | 115 | 115 | 0 |
| 0.050 | 0.050 | 0.120 | 0.034 | 0.335 | 0 | 90 | - | - |
| 0.050 | 0.100 | 0.148 | 0.046 | 0.361 | 0 | 63 | - | - |
| 0.100 | -0.100 | 0.077 | 0.014 | 0.291 | 126 | 126 | - | - |
| 0.100 | -0.050 | 0.094 | 0.028 | 0.305 | 126 | 126 | - | - |
| 0.100 | 0.000 | 0.108 | 0.031 | 0.320 | - | 121 | 121 | 0 |
| 0.100 | 0.050 | 0.134 | 0.043 | 0.346 | 0 | 105 | - | - |
| 0.100 | 0.100 | 0.161 | 0.055 | 0.372 | 0 | 75 | - | - |

### Δ juri saja per model pada beda benar 0 (kedua sumber 0.050)

| model | median | min | maks |
|---|---|---|---|
| Gemma-3-27B | 0.049 | 0.022 | 0.123 |
| Gemma-3-12B | 0.069 | 0.050 | 0.115 |
| R1-8B | 0.084 | 0.043 | 0.095 |
| Qwen-3-30B-A3B-Instruct | 0.094 | 0.049 | 0.308 |
| Llama-8B | 0.096 | 0.044 | 0.181 |
| R1-70B | 0.106 | 0.072 | 0.127 |
| Qwen-3-32B | 0.107 | 0.063 | 0.118 |
| Qwen-3-30B-A3B-Thinking | 0.108 | 0.056 | 0.144 |
| Llama-70B | 0.130 | 0.097 | 0.156 |

### Δ juri saja per model pada beda benar 0 (kedua sumber 0.100)

| model | median | min | maks |
|---|---|---|---|
| Gemma-3-27B | 0.064 | 0.031 | 0.135 |
| Gemma-3-12B | 0.083 | 0.060 | 0.131 |
| R1-8B | 0.097 | 0.054 | 0.106 |
| Llama-8B | 0.106 | 0.058 | 0.189 |
| Qwen-3-30B-A3B-Instruct | 0.109 | 0.066 | 0.320 |
| Qwen-3-30B-A3B-Thinking | 0.113 | 0.059 | 0.149 |
| R1-70B | 0.118 | 0.079 | 0.137 |
| Qwen-3-32B | 0.119 | 0.076 | 0.131 |
| Llama-70B | 0.142 | 0.105 | 0.167 |

### Anggaran m* = (2 · 1.96 · SD / 0.1)², median atas setelan; selang persentil 95 % dari 500 bootstrap pasien (benih 20261125)

| varian | ukuran | data_asli | median_bootstrap | bawah_95 | atas_95 |
|---|---|---|---|---|---|
| utama (klaim, biner, human_gt) | m_PPI | 19.568 | 19.086 | 14.716 | 24.557 |
| utama (klaim, biner, human_gt) | m_label | 48.751 | 47.473 | 34.025 | 63.065 |
| utama (klaim, biner, human_gt) | rasio | 0.401 | 0.402 | 0.278 | 0.593 |
| Not Supported saja | m_PPI | 19.651 | 19.496 | 15.467 | 24.040 |
| Not Supported saja | m_label | 12.900 | 12.331 | 6.863 | 19.652 |
| Not Supported saja | rasio | 1.523 | 1.581 | 1.090 | 2.579 |
| kalimat BHC LLM (tingkat LLM) | m_PPI | 23.431 | 22.707 | 19.328 | 26.575 |
| kalimat BHC LLM (tingkat LLM) | m_label | 7.670 | 7.599 | 5.232 | 10.965 |
| kalimat BHC LLM (tingkat LLM) | rasio | 3.055 | 2.987 | 2.208 | 4.064 |
