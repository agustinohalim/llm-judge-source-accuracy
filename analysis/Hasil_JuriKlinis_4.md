# Hasil JuriKlinis 4 — analisis pasca-panel (*post hoc*)

Sumber angka: `juriklinis_pascapanel.py` dan `juriklinis_pilot.py` (venv-gpu, 21 Nov 2026; ambilan tahap 2 benih
20261122, dokter acak benih 20261123, urutan pilot benih 20261124; 1000 ulangan). Semua butir dicatat di rencana
bagian I **sebelum** dijalankan, sesudah panel 1 (`Telaah/2026-11-21/`) dan sesudah Hasil 1–3 terlihat; karena itu
semuanya *post hoc* dan harus disebut begitu di naskah. Keputusan bagian A tidak berubah. Hanya agregat atas setelan
juri; data tidak dibuka di sesi asisten.

## Ringkasan

1. **Tanpa koreksi populasi hingga** (tim yang melabel m dari N ≫ m): lebar PPI median 0,103 pada m = 20, 0,083
   pada m = 30; anggaran median PPI **30** (126/126 setelan tercapai), label saja **tak tercapai** sampai m = 50
   (lebar median 0,100 pada m = 50). PPI++ per sumber anggaran median 20 tanpa koreksi, tetapi tetap kurang cakupan
   pada m = 5 (0,889) dan m = 10 (0,924). Angka "±20 pasien" di naskah hanya berlaku untuk 20 dari 100 pasien.
2. **Rasio varians label saja / PPI** per setelan (bebas skala dan bebas koreksi): median 2,49 pada m = 20
   (rentang 1,05–4,23), stabil 2,35–2,50 atas m. PPI setara ±2,5 kali pasien berlabel.
3. **Sensitivitas per sumber di dalam jenis galat**: dokter > LLM pada **126/126 setelan** baik di Not Supported
   (median beda 0,227) maupun Not Addressed (median beda 0,387). Asimetri sumber bukan efek campuran jenis galat.
4. **Bias batas RG bersama** (100 pasien berlabel): median 0,167; korelasi dengan bias simulasi m = 20 = 0,999, median
   |selisih| 0,002. Biasnya hampir seluruhnya bias batas, bukan galat sampel kecil.
5. **Varians klaim bebas** (klaster pasien diabaikan, dengan koreksi populasi hingga): cakupan PPI median 0,845–0,859,
   terendah 0,638–0,661 — varians tingkat pasien diperlukan.
6. **Aturan pilot** (10 pasien, ramal m per penaksir, pilih yang lebih kecil): varian utama memilih PPI pada median
   95 % ulangan, m akhir median 20, cakupan median 0,924 (terendah 0,888), lebar median 0,092. Not Supported saja:
   PPI dipilih 36 %, m akhir median 10 (rata 14,4), cakupan 0,921. Kalimat LLM: PPI dipilih 15 %, m akhir median
   10, cakupan 0,928 (terendah 0,879). Cakupan ±0,02–0,03 di bawah nominal karena σ² dari 10 pasien kadang terlalu
   kecil. Ramalan m untuk N ≫ m dari pilot (z, tanpa koreksi): PPI 17, label saja 43 (utama).
7. **Δ sebenarnya**: utama 0,2807 (setelan Qwen thinking dengan 5574 klaim dokter: 0,2826); satu dokter acak 0,2590
   (0,2614); Not Supported 0,0732 (0,0721); Not Addressed 0,2075 (0,2105).

Galat Monte Carlo cakupan pada 0,95 dengan 1000 ulangan: √(0,95 · 0,05 / 1000) = 0,007.

## Keluaran `juriklinis_pascapanel.py`

### Tanpa koreksi populasi hingga (kecuali baris klaim bebas): ringkasan atas 126 setelan

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| PPI | 5 | 126 | -0.002 | 0.945 | 0.902 | 0.249 | 0.000 | 0.000 |
| PPI | 10 | 126 | -0.002 | 0.953 | 0.931 | 0.152 | 0.000 | 0.000 |
| PPI | 20 | 126 | -0.000 | 0.967 | 0.945 | 0.103 | 0.000 | 0.000 |
| PPI | 30 | 126 | -0.000 | 0.978 | 0.961 | 0.083 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.992 | 0.985 | 0.064 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.002 | 0.889 | 0.851 | 0.201 | 0.001 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.002 | 0.924 | 0.889 | 0.131 | 0.000 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.000 | 0.952 | 0.928 | 0.092 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.000 | 0.974 | 0.954 | 0.075 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.990 | 0.981 | 0.058 | 0.000 | 0.000 |
| PPI, varians klaim bebas | 5 | 126 | -0.002 | 0.859 | 0.661 | 0.145 | 0.000 | 0.000 |
| PPI, varians klaim bebas | 10 | 126 | -0.002 | 0.855 | 0.651 | 0.099 | 0.000 | 0.000 |
| PPI, varians klaim bebas | 20 | 126 | -0.000 | 0.853 | 0.638 | 0.065 | 0.000 | 0.000 |
| PPI, varians klaim bebas | 30 | 126 | -0.000 | 0.852 | 0.655 | 0.050 | 0.000 | 0.000 |
| PPI, varians klaim bebas | 50 | 126 | -0.000 | 0.845 | 0.644 | 0.032 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.189 | 0.238 | 0.002 | 0.296 | 0.000 | 0.001 |
| RG bersama | 10 | 126 | 0.177 | 0.000 | 0.000 | 0.169 | 0.000 | 0.000 |
| RG bersama | 20 | 126 | 0.171 | 0.000 | 0.000 | 0.110 | 0.000 | 0.000 |
| RG bersama | 30 | 126 | 0.170 | 0.000 | 0.000 | 0.088 | 0.000 | 0.000 |
| RG bersama | 50 | 126 | 0.168 | 0.000 | 0.000 | 0.067 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.003 | 0.923 | 0.923 | 0.382 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.003 | 0.948 | 0.948 | 0.237 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.965 | 0.964 | 0.162 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.000 | 0.981 | 0.981 | 0.131 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.995 | 0.993 | 0.100 | 0.000 | 0.000 |

### Anggaran label tanpa koreksi populasi hingga (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai)

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| PPI | 126 | 30.000 | 50.000 |
| PPI++ berstrata | 126 | 20.000 | 50.000 |
| RG bersama | 0 | inf | inf |
| klasik | 0 | inf | inf |

### Anggaran label tanpa koreksi, per model

| model | penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|---|
| Gemma-3-12B | PPI | 14 | 30.000 | 50.000 |
| Gemma-3-12B | PPI++ berstrata | 14 | 30.000 | 30.000 |
| Gemma-3-12B | RG bersama | 0 | inf | inf |
| Gemma-3-12B | klasik | 0 | inf | inf |
| Gemma-3-27B | PPI | 14 | 30.000 | 30.000 |
| Gemma-3-27B | PPI++ berstrata | 14 | 25.000 | 30.000 |
| Gemma-3-27B | RG bersama | 0 | inf | inf |
| Gemma-3-27B | klasik | 0 | inf | inf |
| Llama-70B | PPI | 14 | 20.000 | 50.000 |
| Llama-70B | PPI++ berstrata | 14 | 20.000 | 20.000 |
| Llama-70B | RG bersama | 0 | inf | inf |
| Llama-70B | klasik | 0 | inf | inf |
| Llama-8B | PPI | 14 | 50.000 | 50.000 |
| Llama-8B | PPI++ berstrata | 14 | 50.000 | 50.000 |
| Llama-8B | RG bersama | 0 | inf | inf |
| Llama-8B | klasik | 0 | inf | inf |
| Qwen-3-30B-A3B-Instruct | PPI | 14 | 25.000 | 50.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 14 | 20.000 | 30.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 0 | inf | inf |
| Qwen-3-30B-A3B-Instruct | klasik | 0 | inf | inf |
| Qwen-3-30B-A3B-Thinking | PPI | 14 | 30.000 | 50.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 14 | 20.000 | 30.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 0 | inf | inf |
| Qwen-3-30B-A3B-Thinking | klasik | 0 | inf | inf |
| Qwen-3-32B | PPI | 14 | 20.000 | 30.000 |
| Qwen-3-32B | PPI++ berstrata | 14 | 20.000 | 20.000 |
| Qwen-3-32B | RG bersama | 0 | inf | inf |
| Qwen-3-32B | klasik | 0 | inf | inf |
| R1-70B | PPI | 14 | 20.000 | 30.000 |
| R1-70B | PPI++ berstrata | 14 | 20.000 | 20.000 |
| R1-70B | RG bersama | 0 | inf | inf |
| R1-70B | klasik | 0 | inf | inf |
| R1-8B | PPI | 14 | 25.000 | 50.000 |
| R1-8B | PPI++ berstrata | 14 | 20.000 | 30.000 |
| R1-8B | RG bersama | 0 | inf | inf |
| R1-8B | klasik | 0 | inf | inf |

### Rasio varians label saja / PPI per setelan (= kelipatan pasien berlabel yang setara)

| banyak_label | min | 50% | max |
|---|---|---|---|
| 5 | 1.036 | 2.353 | 4.503 |
| 10 | 0.992 | 2.428 | 4.218 |
| 20 | 1.048 | 2.489 | 4.233 |
| 30 | 1.026 | 2.496 | 4.195 |
| 50 | 1.021 | 2.478 | 4.100 |

### Rogan–Gladen bersama: bias batas (100 pasien berlabel) lawan bias simulasi m = 20, median per model

| model | bias_batas | bias_m20 |
|---|---|---|
| Gemma-3-12B | 0.167 | 0.172 |
| Gemma-3-27B | 0.140 | 0.146 |
| Llama-70B | 0.204 | 0.207 |
| Llama-8B | 0.273 | 0.285 |
| Qwen-3-30B-A3B-Instruct | 0.178 | 0.182 |
| Qwen-3-30B-A3B-Thinking | 0.150 | 0.151 |
| Qwen-3-32B | 0.173 | 0.175 |
| R1-70B | 0.159 | 0.161 |
| R1-8B | 0.160 | 0.162 |

Korelasi Pearson atas 126 setelan: 0.999; median |batas − m20| = 0.002; median bias batas = 0.167

### Sensitivitas juri di dalam Not Supported: dokter lawan LLM, per model (14 setelan)

| model | sens_dokter | sens_llm | beda_median | dokter_lebih_tinggi |
|---|---|---|---|---|
| Gemma-3-12B | 0.452 | 0.201 | 0.249 | 14 |
| Gemma-3-27B | 0.317 | 0.089 | 0.215 | 14 |
| Llama-70B | 0.727 | 0.519 | 0.212 | 14 |
| Llama-8B | 0.514 | 0.327 | 0.188 | 14 |
| Qwen-3-30B-A3B-Instruct | 0.587 | 0.336 | 0.277 | 14 |
| Qwen-3-30B-A3B-Thinking | 0.866 | 0.757 | 0.110 | 14 |
| Qwen-3-32B | 0.687 | 0.439 | 0.241 | 14 |
| R1-70B | 0.729 | 0.519 | 0.205 | 14 |
| R1-8B | 0.614 | 0.369 | 0.237 | 14 |

Semua setelan: median beda 0.227; dokter lebih tinggi pada 126 dari 126

### Sensitivitas juri di dalam Not Addressed: dokter lawan LLM, per model (14 setelan)

| model | sens_dokter | sens_llm | beda_median | dokter_lebih_tinggi |
|---|---|---|---|---|
| Gemma-3-12B | 0.531 | 0.182 | 0.364 | 14 |
| Gemma-3-27B | 0.482 | 0.129 | 0.354 | 14 |
| Llama-70B | 0.792 | 0.303 | 0.490 | 14 |
| Llama-8B | 0.633 | 0.258 | 0.335 | 14 |
| Qwen-3-30B-A3B-Instruct | 0.690 | 0.197 | 0.491 | 14 |
| Qwen-3-30B-A3B-Thinking | 0.939 | 0.614 | 0.318 | 14 |
| Qwen-3-32B | 0.809 | 0.280 | 0.522 | 14 |
| R1-70B | 0.845 | 0.379 | 0.442 | 14 |
| R1-8B | 0.738 | 0.379 | 0.338 | 14 |

Semua setelan: median beda 0.387; dokter lebih tinggi pada 126 dari 126

### Δ sebenarnya, varian utama

min 0.2807, median 0.2807, maks 0.2826; setelan dengan klaim dokter paling sedikit (5574): Δ = 0.2826

### Δ sebenarnya, varian satu dokter acak

min 0.2590, median 0.2590, maks 0.2614; setelan dengan klaim dokter paling sedikit (5574): Δ = 0.2614

### Δ sebenarnya, varian Not Supported saja

min 0.0721, median 0.0732, maks 0.0732; setelan dengan klaim dokter paling sedikit (5574): Δ = 0.0721

### Δ sebenarnya, varian Not Addressed saja

min 0.2075, median 0.2075, maks 0.2105; setelan dengan klaim dokter paling sedikit (5574): Δ = 0.2105

## Keluaran `juriklinis_pilot.py`

### Aturan pilot (10 pasien), varian utama: semua setelan

| semua | setelan | cakupan_median | cakupan_min | lebar_median | m_median | m_rata_median | bagian_ppi_median | m_besar_ppi | m_besar_klasik |
|---|---|---|---|---|---|---|---|---|---|
| semua | 126 | 0.924 | 0.888 | 0.092 | 20.000 | 19.532 | 0.948 | 17.000 | 43.000 |

### Aturan pilot, varian utama: per model

| model | setelan | cakupan_median | cakupan_min | lebar_median | m_median | m_rata_median | bagian_ppi_median | m_besar_ppi | m_besar_klasik |
|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 14 | 0.930 | 0.908 | 0.091 | 20.000 | 19.995 | 0.968 | 17.500 | 43.000 |
| Gemma-3-27B | 14 | 0.922 | 0.915 | 0.092 | 20.000 | 20.845 | 0.962 | 19.500 | 43.000 |
| Llama-70B | 14 | 0.921 | 0.901 | 0.089 | 15.000 | 17.483 | 0.965 | 14.500 | 43.000 |
| Llama-8B | 14 | 0.928 | 0.916 | 0.105 | 25.000 | 27.417 | 0.710 | 35.000 | 43.000 |
| Qwen-3-30B-A3B-Instruct | 14 | 0.929 | 0.914 | 0.090 | 18.750 | 18.828 | 0.936 | 15.500 | 43.000 |
| Qwen-3-30B-A3B-Thinking | 14 | 0.910 | 0.888 | 0.097 | 20.000 | 21.570 | 0.867 | 21.000 | 43.000 |
| Qwen-3-32B | 14 | 0.923 | 0.913 | 0.088 | 15.000 | 17.218 | 0.962 | 14.000 | 43.000 |
| R1-70B | 14 | 0.919 | 0.897 | 0.087 | 15.000 | 16.363 | 0.968 | 13.000 | 43.000 |
| R1-8B | 14 | 0.932 | 0.906 | 0.091 | 20.000 | 19.170 | 0.949 | 16.000 | 43.000 |

### Aturan pilot (10 pasien), varian Not Supported saja: semua setelan

| semua | setelan | cakupan_median | cakupan_min | lebar_median | m_median | m_rata_median | bagian_ppi_median | m_besar_ppi | m_besar_klasik |
|---|---|---|---|---|---|---|---|---|---|
| semua | 126 | 0.921 | 0.896 | 0.083 | 10.000 | 14.365 | 0.364 | 18.000 | 9.000 |

### Aturan pilot, varian Not Supported saja: per model

| model | setelan | cakupan_median | cakupan_min | lebar_median | m_median | m_rata_median | bagian_ppi_median | m_besar_ppi | m_besar_klasik |
|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 14 | 0.913 | 0.896 | 0.083 | 10.000 | 13.988 | 0.512 | 14.000 | 9.000 |
| Gemma-3-27B | 14 | 0.939 | 0.912 | 0.081 | 10.000 | 14.438 | 0.740 | 11.000 | 9.000 |
| Llama-70B | 14 | 0.925 | 0.912 | 0.083 | 15.000 | 14.442 | 0.232 | 23.500 | 9.000 |
| Llama-8B | 14 | 0.928 | 0.911 | 0.083 | 15.000 | 14.565 | 0.273 | 20.000 | 9.000 |
| Qwen-3-30B-A3B-Instruct | 14 | 0.917 | 0.901 | 0.083 | 10.000 | 13.860 | 0.470 | 15.000 | 9.000 |
| Qwen-3-30B-A3B-Thinking | 14 | 0.921 | 0.896 | 0.083 | 15.000 | 14.590 | 0.223 | 23.500 | 9.000 |
| Qwen-3-32B | 14 | 0.913 | 0.903 | 0.083 | 10.000 | 13.518 | 0.442 | 16.000 | 9.000 |
| R1-70B | 14 | 0.921 | 0.904 | 0.084 | 10.000 | 14.363 | 0.338 | 19.000 | 9.000 |
| R1-8B | 14 | 0.921 | 0.906 | 0.083 | 15.000 | 14.555 | 0.332 | 18.000 | 9.000 |

### Aturan pilot (10 pasien), varian kalimat BHC LLM (tingkat LLM): semua setelan

| semua | setelan | cakupan_median | cakupan_min | lebar_median | m_median | m_rata_median | bagian_ppi_median | m_besar_ppi | m_besar_klasik |
|---|---|---|---|---|---|---|---|---|---|
| semua | 126 | 0.928 | 0.879 | 0.079 | 10.000 | 12.475 | 0.149 | 22.000 | 8.000 |

### Aturan pilot, varian kalimat BHC LLM (tingkat LLM): per model

| model | setelan | cakupan_median | cakupan_min | lebar_median | m_median | m_rata_median | bagian_ppi_median | m_besar_ppi | m_besar_klasik |
|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 14 | 0.935 | 0.896 | 0.081 | 10.000 | 12.422 | 0.597 | 10.500 | 8.000 |
| Gemma-3-27B | 14 | 0.929 | 0.906 | 0.077 | 10.000 | 12.430 | 0.871 | 8.500 | 8.000 |
| Llama-70B | 14 | 0.929 | 0.899 | 0.080 | 10.000 | 12.235 | 0.521 | 11.000 | 8.000 |
| Llama-8B | 14 | 0.927 | 0.916 | 0.077 | 10.000 | 12.588 | 0.025 | 37.000 | 8.000 |
| Qwen-3-30B-A3B-Instruct | 14 | 0.929 | 0.899 | 0.081 | 10.000 | 11.988 | 0.582 | 10.000 | 8.000 |
| Qwen-3-30B-A3B-Thinking | 14 | 0.926 | 0.913 | 0.078 | 10.000 | 12.560 | 0.049 | 31.500 | 8.000 |
| Qwen-3-32B | 14 | 0.924 | 0.893 | 0.079 | 10.000 | 12.462 | 0.119 | 24.000 | 8.000 |
| R1-70B | 14 | 0.925 | 0.879 | 0.079 | 10.000 | 12.425 | 0.142 | 23.000 | 8.000 |
| R1-8B | 14 | 0.921 | 0.905 | 0.078 | 10.000 | 12.525 | 0.101 | 24.000 | 8.000 |
