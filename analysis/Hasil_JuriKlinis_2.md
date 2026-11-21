# Hasil JuriKlinis 2 — tahap 2: penaksir terkoreksi dan anggaran label

Sumber angka: `juriklinis_tahap2.py` (venv-gpu, 21 Nov 2026; benih 20261122; 1000 ambilan pasien per m, sama untuk
semua setelan) dengan penaksir `juriklinis_penaksir.py` dan `juriklinis_pengaruh.py`, atas `C:\Data\VeriFact-BHC\`.
Rancangan dikunci di `Artikel_JuriKlinis_Rencana.md` bagian A sebelum skrip ini pertama dijalankan. Penaksir diuji
dulu pada data sintetis (scratchpad, bukan data PhysioNet): tepat bila semua pasien berlabel, cakupan 0,92–0,95 pada
m = 10 dan 30, dan RG bersama bias bila sensitivitas berbeda per sumber. Hanya agregat atas setelan juri.

Catatan baca: "naif" tidak memakai label; cakupannya 0 atau 1 per setelan (satu selang), jadi median atas setelan
juga 0 atau 1. "klasik" tidak memakai juri, jadi hampir sama untuk semua setelan (beda hanya pada setelan Qwen
Thinking top_n 100 yang kehilangan 74 klaim). m terkecil dipilih dari kisi 5, 10, 20, 30, 50 saja. Rata-rata klaim
per pasien: 56,5 dokter dan 34,5 LLM, jadi m = 20 pasien ≈ 1800 klaim berlabel.

## Ringkasan (semua 126 setelan; median atas setelan)

- **Naif**: bias median −0,040; selang naif (lebar median 0,066) mencakup Δ sebenarnya pada mayoritas setelan
  Llama-70B, R1-70B, Qwen-3-32B, dan Qwen-3-30B-A3B-Thinking (median 1), tetapi tidak pada mayoritas setelan lima
  model lain (median 0); median atas 126 setelan 0. Selang naif mencakup Δ pada 56 dari 126 setelan (Llama-70B, Qwen-3-32B, R1-70B 13 dari 14; Qwen Thinking 11; lima model lain 0–2; ditambahkan 21 Nov, keluaran lain tidak berubah).
- **RG bersama** (satu sensitivitas/spesifisitas untuk kedua sumber): bias **+0,17 sampai +0,19** di semua m,
  cakupan 0 dari m = 10. Koreksi bersama membalik arah galat naif (−0,04) menjadi galat yang lebih besar ke arah
  sebaliknya. Sesuai dugaan dari `Hasil_JuriKlinis_1.md` (sensitivitas juri berbeda per sumber).
- **RG per sumber**: hampir tak bias (median −0,004 sampai −0,021), tetapi tidak stabil pada m kecil: gagal sampai
  64 % ambilan pada m = 5 (sensitivitas sisi LLM tak terdefinisi atau sens + spek − 1 ≤ 0), selang sangat lebar
  (median 4,9 pada m = 5; 0,115 pada m = 50), dan cakupan minimum 0,34–0,92.
- **PPI**: tak bias; cakupan median 0,940–0,948 di semua m, minimum 0,90 (m = 5) sampai 0,93. Lebar median 0,092
  pada m = 20, lawan 0,145 untuk klasik pada m yang sama.
- **PPI++ bersama / berstrata**: tak bias dan sedikit lebih sempit dari PPI (0,086 / 0,082 pada m = 20), tetapi
  cakupannya kurang pada m kecil (median 0,876 / 0,883 pada m = 5; 0,913 / 0,911 pada m = 10; minimum 0,83–0,84).
  Pada m ≥ 30 cakupan median 0,937–0,942.
- **Anggaran label** (cakupan ≥ 0,93 dan lebar ≤ 0,10): klasik butuh m = 50 di semua setelan. PPI butuh median
  m = 20 (Gemma-3 12B/27B, Llama-70B, Qwen-3-30B-A3B-Instruct, Qwen-3-32B, R1-70B, R1-8B) atau 30 (Llama-8B,
  Qwen-3-30B-A3B-Thinking), dan mencapainya di 126 dari 126 setelan. PPI++ berstrata gagal mencapainya pada 9 setelan
  (Qwen-3-32B 3, R1-70B 4, Qwen Thinking 2). RG bersama tidak pernah; RG per sumber pada 35 setelan saja.
- **8B lawan 70B, PPI, m = 20** (median lebar): Llama-8B 0,129 lawan Llama-70B 0,083; R1-8B 0,089 lawan R1-70B 0,080.
  Juri besar mempersempit selang, tetapi PPI dengan juri kecil tetap sah.

## Pengamatan untuk rencana (dicatat sesudah hasil; belum klaim naskah)

1. Dugaan rencana "PPI++ berstrata memulihkan selang sah" hanya sebagian benar: PPI biasa (λ = 1) sudah menghitung
   koreksi per sumber, dan pada 100 pasien ia lebih aman daripada PPI++ (λ ditaksir dari sedikit klaster). Sumbangan
   lebih tepat dirumuskan sebagai: koreksi bersama (RG bersama) berbahaya, koreksi per sumber perlu, dan PPI memberi
   selang sah dengan ±20 pasien berlabel lawan 50 untuk label saja.
2. Galat terbesar bukan dari juri naif, melainkan dari koreksi bersama — temuan yang sejalan dengan Fiedler 2026
   (kalibrasi bersama bisa memperburuk perbandingan), kini pada teks klinis nyata dengan kebenaran penuh.
3. Batasan: sasaran adalah Δ atas 100 pasien ini (populasi hingga), bukan populasi rumah sakit; kisi m kasar;
   kepekaan (tiga label, satu dokter acak, tanpa `invalid`, kalimat LLM) belum dijalankan.

## Keluaran skrip

Disalin utuh dari keluaran `juriklinis_tahap2.py`.

### Semua setelan juri (median/min/maks atas setelan; 1000 ambilan per m)

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| naif | 0 | 126 | -0.040 | 0.000 | 0.000 | 0.066 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.003 | 0.935 | 0.934 | 0.225 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.943 | 0.938 | 0.145 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| PPI | 5 | 126 | -0.002 | 0.940 | 0.901 | 0.242 | 0.000 | 0.000 |
| PPI | 10 | 126 | -0.002 | 0.943 | 0.919 | 0.144 | 0.000 | 0.000 |
| PPI | 20 | 126 | -0.000 | 0.948 | 0.920 | 0.092 | 0.000 | 0.000 |
| PPI | 30 | 126 | -0.000 | 0.947 | 0.932 | 0.069 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.946 | 0.925 | 0.045 | 0.000 | 0.000 |
| PPI++ bersama | 5 | 126 | -0.002 | 0.876 | 0.833 | 0.206 | 0.000 | 0.000 |
| PPI++ bersama | 10 | 126 | -0.003 | 0.913 | 0.889 | 0.131 | 0.000 | 0.000 |
| PPI++ bersama | 20 | 126 | -0.000 | 0.932 | 0.899 | 0.086 | 0.000 | 0.000 |
| PPI++ bersama | 30 | 126 | -0.000 | 0.942 | 0.922 | 0.066 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | -0.000 | 0.941 | 0.920 | 0.044 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.002 | 0.883 | 0.841 | 0.195 | 0.001 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.002 | 0.911 | 0.878 | 0.125 | 0.000 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.000 | 0.930 | 0.903 | 0.082 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.000 | 0.938 | 0.911 | 0.063 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.937 | 0.920 | 0.041 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.189 | 0.218 | 0.001 | 0.289 | 0.000 | 0.001 |
| RG bersama | 10 | 126 | 0.177 | 0.000 | 0.000 | 0.160 | 0.000 | 0.000 |
| RG bersama | 20 | 126 | 0.171 | 0.000 | 0.000 | 0.099 | 0.000 | 0.000 |
| RG bersama | 30 | 126 | 0.170 | 0.000 | 0.000 | 0.074 | 0.000 | 0.000 |
| RG bersama | 50 | 126 | 0.168 | 0.000 | 0.000 | 0.047 | 0.000 | 0.000 |
| RG per sumber | 5 | 126 | -0.008 | 0.875 | 0.344 | 4.924 | 0.185 | 0.636 |
| RG per sumber | 10 | 126 | -0.021 | 0.949 | 0.587 | 1.072 | 0.187 | 0.392 |
| RG per sumber | 20 | 126 | -0.006 | 0.957 | 0.816 | 0.287 | 0.151 | 0.179 |
| RG per sumber | 30 | 126 | -0.005 | 0.954 | 0.864 | 0.190 | 0.163 | 0.123 |
| RG per sumber | 50 | 126 | -0.004 | 0.949 | 0.920 | 0.115 | 0.100 | 0.040 |

### Model teks utama (Llama-8B, Llama-70B, R1-8B, R1-70B), 14 setelan per model

| model | penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|---|
| Llama-70B | naif | 0 | 14 | 0.010 | 1.000 | 0.000 | 0.066 | 0.000 | 0.000 |
| Llama-70B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Llama-70B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| Llama-70B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| Llama-70B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Llama-70B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Llama-70B | PPI | 5 | 14 | -0.001 | 0.940 | 0.921 | 0.220 | 0.000 | 0.000 |
| Llama-70B | PPI | 10 | 14 | -0.003 | 0.938 | 0.924 | 0.131 | 0.000 | 0.000 |
| Llama-70B | PPI | 20 | 14 | 0.000 | 0.944 | 0.932 | 0.083 | 0.000 | 0.000 |
| Llama-70B | PPI | 30 | 14 | -0.000 | 0.948 | 0.941 | 0.063 | 0.000 | 0.000 |
| Llama-70B | PPI | 50 | 14 | -0.001 | 0.940 | 0.933 | 0.041 | 0.000 | 0.000 |
| Llama-70B | PPI++ bersama | 5 | 14 | -0.003 | 0.871 | 0.854 | 0.189 | 0.000 | 0.000 |
| Llama-70B | PPI++ bersama | 10 | 14 | -0.003 | 0.905 | 0.893 | 0.120 | 0.000 | 0.000 |
| Llama-70B | PPI++ bersama | 20 | 14 | -0.001 | 0.933 | 0.918 | 0.079 | 0.000 | 0.000 |
| Llama-70B | PPI++ bersama | 30 | 14 | -0.001 | 0.944 | 0.930 | 0.061 | 0.000 | 0.000 |
| Llama-70B | PPI++ bersama | 50 | 14 | -0.001 | 0.937 | 0.929 | 0.040 | 0.000 | 0.000 |
| Llama-70B | PPI++ berstrata | 5 | 14 | -0.003 | 0.882 | 0.864 | 0.180 | 0.000 | 0.000 |
| Llama-70B | PPI++ berstrata | 10 | 14 | -0.002 | 0.900 | 0.890 | 0.114 | 0.000 | 0.000 |
| Llama-70B | PPI++ berstrata | 20 | 14 | 0.000 | 0.928 | 0.920 | 0.075 | 0.000 | 0.000 |
| Llama-70B | PPI++ berstrata | 30 | 14 | 0.000 | 0.941 | 0.931 | 0.057 | 0.000 | 0.000 |
| Llama-70B | PPI++ berstrata | 50 | 14 | -0.000 | 0.935 | 0.928 | 0.037 | 0.000 | 0.000 |
| Llama-70B | RG bersama | 5 | 14 | 0.220 | 0.097 | 0.024 | 0.276 | 0.000 | 0.000 |
| Llama-70B | RG bersama | 10 | 14 | 0.211 | 0.000 | 0.000 | 0.159 | 0.000 | 0.000 |
| Llama-70B | RG bersama | 20 | 14 | 0.207 | 0.000 | 0.000 | 0.097 | 0.000 | 0.000 |
| Llama-70B | RG bersama | 30 | 14 | 0.206 | 0.000 | 0.000 | 0.073 | 0.000 | 0.000 |
| Llama-70B | RG bersama | 50 | 14 | 0.205 | 0.000 | 0.000 | 0.047 | 0.000 | 0.000 |
| Llama-70B | RG per sumber | 5 | 14 | -0.007 | 0.901 | 0.872 | 5.943 | 0.078 | 0.109 |
| Llama-70B | RG per sumber | 10 | 14 | -0.023 | 0.958 | 0.947 | 1.198 | 0.030 | 0.020 |
| Llama-70B | RG per sumber | 20 | 14 | -0.004 | 0.964 | 0.946 | 0.228 | 0.007 | 0.000 |
| Llama-70B | RG per sumber | 30 | 14 | -0.004 | 0.950 | 0.941 | 0.154 | 0.000 | 0.000 |
| Llama-70B | RG per sumber | 50 | 14 | -0.003 | 0.946 | 0.930 | 0.095 | 0.000 | 0.000 |
| Llama-8B | naif | 0 | 14 | -0.093 | 0.000 | 0.000 | 0.059 | 0.000 | 0.000 |
| Llama-8B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Llama-8B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| Llama-8B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| Llama-8B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Llama-8B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Llama-8B | PPI | 5 | 14 | 0.002 | 0.942 | 0.923 | 0.335 | 0.000 | 0.000 |
| Llama-8B | PPI | 10 | 14 | -0.003 | 0.940 | 0.936 | 0.205 | 0.000 | 0.000 |
| Llama-8B | PPI | 20 | 14 | -0.000 | 0.950 | 0.938 | 0.129 | 0.000 | 0.000 |
| Llama-8B | PPI | 30 | 14 | -0.000 | 0.948 | 0.935 | 0.097 | 0.000 | 0.000 |
| Llama-8B | PPI | 50 | 14 | -0.000 | 0.952 | 0.945 | 0.063 | 0.000 | 0.000 |
| Llama-8B | PPI++ bersama | 5 | 14 | -0.006 | 0.877 | 0.859 | 0.278 | 0.000 | 0.000 |
| Llama-8B | PPI++ bersama | 10 | 14 | -0.005 | 0.908 | 0.901 | 0.181 | 0.000 | 0.000 |
| Llama-8B | PPI++ bersama | 20 | 14 | -0.002 | 0.935 | 0.920 | 0.118 | 0.000 | 0.000 |
| Llama-8B | PPI++ bersama | 30 | 14 | -0.001 | 0.943 | 0.932 | 0.090 | 0.000 | 0.000 |
| Llama-8B | PPI++ bersama | 50 | 14 | -0.001 | 0.946 | 0.935 | 0.059 | 0.000 | 0.000 |
| Llama-8B | PPI++ berstrata | 5 | 14 | -0.004 | 0.869 | 0.863 | 0.287 | 0.001 | 0.000 |
| Llama-8B | PPI++ berstrata | 10 | 14 | -0.005 | 0.906 | 0.897 | 0.187 | 0.000 | 0.000 |
| Llama-8B | PPI++ berstrata | 20 | 14 | -0.002 | 0.923 | 0.911 | 0.124 | 0.000 | 0.000 |
| Llama-8B | PPI++ berstrata | 30 | 14 | -0.001 | 0.937 | 0.931 | 0.095 | 0.000 | 0.000 |
| Llama-8B | PPI++ berstrata | 50 | 14 | -0.000 | 0.944 | 0.939 | 0.063 | 0.000 | 0.000 |
| Llama-8B | RG bersama | 5 | 14 | 0.340 | 0.657 | 0.069 | 0.806 | 0.000 | 0.001 |
| Llama-8B | RG bersama | 10 | 14 | 0.311 | 0.084 | 0.000 | 0.423 | 0.000 | 0.000 |
| Llama-8B | RG bersama | 20 | 14 | 0.285 | 0.000 | 0.000 | 0.264 | 0.000 | 0.000 |
| Llama-8B | RG bersama | 30 | 14 | 0.283 | 0.000 | 0.000 | 0.198 | 0.000 | 0.000 |
| Llama-8B | RG bersama | 50 | 14 | 0.278 | 0.000 | 0.000 | 0.129 | 0.000 | 0.000 |
| Llama-8B | RG per sumber | 5 | 14 | -0.015 | 0.724 | 0.607 | 75.473 | 0.185 | 0.383 |
| Llama-8B | RG per sumber | 10 | 14 | -0.050 | 0.834 | 0.691 | 62.727 | 0.187 | 0.300 |
| Llama-8B | RG per sumber | 20 | 14 | -0.040 | 0.943 | 0.816 | 14.037 | 0.151 | 0.179 |
| Llama-8B | RG per sumber | 30 | 14 | -0.006 | 0.961 | 0.864 | 4.484 | 0.163 | 0.123 |
| Llama-8B | RG per sumber | 50 | 14 | -0.006 | 0.966 | 0.955 | 0.414 | 0.100 | 0.040 |
| R1-70B | naif | 0 | 14 | 0.004 | 1.000 | 0.000 | 0.071 | 0.000 | 0.000 |
| R1-70B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| R1-70B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| R1-70B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| R1-70B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| R1-70B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| R1-70B | PPI | 5 | 14 | -0.002 | 0.933 | 0.910 | 0.201 | 0.000 | 0.000 |
| R1-70B | PPI | 10 | 14 | -0.002 | 0.936 | 0.919 | 0.124 | 0.000 | 0.000 |
| R1-70B | PPI | 20 | 14 | 0.000 | 0.938 | 0.931 | 0.080 | 0.000 | 0.000 |
| R1-70B | PPI | 30 | 14 | -0.000 | 0.942 | 0.932 | 0.060 | 0.000 | 0.000 |
| R1-70B | PPI | 50 | 14 | -0.000 | 0.939 | 0.925 | 0.040 | 0.000 | 0.000 |
| R1-70B | PPI++ bersama | 5 | 14 | -0.003 | 0.865 | 0.849 | 0.171 | 0.000 | 0.000 |
| R1-70B | PPI++ bersama | 10 | 14 | -0.002 | 0.901 | 0.895 | 0.112 | 0.000 | 0.000 |
| R1-70B | PPI++ bersama | 20 | 14 | -0.000 | 0.922 | 0.908 | 0.075 | 0.000 | 0.000 |
| R1-70B | PPI++ bersama | 30 | 14 | -0.000 | 0.936 | 0.928 | 0.057 | 0.000 | 0.000 |
| R1-70B | PPI++ bersama | 50 | 14 | -0.000 | 0.934 | 0.927 | 0.038 | 0.000 | 0.000 |
| R1-70B | PPI++ berstrata | 5 | 14 | -0.002 | 0.875 | 0.855 | 0.166 | 0.000 | 0.000 |
| R1-70B | PPI++ berstrata | 10 | 14 | -0.001 | 0.905 | 0.887 | 0.107 | 0.000 | 0.000 |
| R1-70B | PPI++ berstrata | 20 | 14 | 0.001 | 0.925 | 0.908 | 0.071 | 0.000 | 0.000 |
| R1-70B | PPI++ berstrata | 30 | 14 | 0.000 | 0.933 | 0.922 | 0.055 | 0.000 | 0.000 |
| R1-70B | PPI++ berstrata | 50 | 14 | 0.000 | 0.927 | 0.921 | 0.036 | 0.000 | 0.000 |
| R1-70B | RG bersama | 5 | 14 | 0.169 | 0.084 | 0.029 | 0.209 | 0.000 | 0.000 |
| R1-70B | RG bersama | 10 | 14 | 0.163 | 0.000 | 0.000 | 0.116 | 0.000 | 0.000 |
| R1-70B | RG bersama | 20 | 14 | 0.161 | 0.000 | 0.000 | 0.071 | 0.000 | 0.000 |
| R1-70B | RG bersama | 30 | 14 | 0.160 | 0.000 | 0.000 | 0.054 | 0.000 | 0.000 |
| R1-70B | RG bersama | 50 | 14 | 0.159 | 0.000 | 0.000 | 0.034 | 0.000 | 0.000 |
| R1-70B | RG per sumber | 5 | 14 | -0.018 | 0.917 | 0.862 | 0.792 | 0.055 | 0.096 |
| R1-70B | RG per sumber | 10 | 14 | -0.017 | 0.958 | 0.940 | 0.489 | 0.025 | 0.013 |
| R1-70B | RG per sumber | 20 | 14 | -0.004 | 0.952 | 0.940 | 0.176 | 0.002 | 0.000 |
| R1-70B | RG per sumber | 30 | 14 | -0.004 | 0.943 | 0.932 | 0.126 | 0.000 | 0.000 |
| R1-70B | RG per sumber | 50 | 14 | -0.003 | 0.933 | 0.920 | 0.080 | 0.000 | 0.000 |
| R1-8B | naif | 0 | 14 | -0.051 | 0.000 | 0.000 | 0.063 | 0.000 | 0.000 |
| R1-8B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| R1-8B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| R1-8B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| R1-8B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| R1-8B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| R1-8B | PPI | 5 | 14 | -0.002 | 0.942 | 0.927 | 0.238 | 0.000 | 0.000 |
| R1-8B | PPI | 10 | 14 | -0.003 | 0.950 | 0.929 | 0.140 | 0.000 | 0.000 |
| R1-8B | PPI | 20 | 14 | -0.000 | 0.952 | 0.931 | 0.089 | 0.000 | 0.000 |
| R1-8B | PPI | 30 | 14 | -0.000 | 0.956 | 0.939 | 0.068 | 0.000 | 0.000 |
| R1-8B | PPI | 50 | 14 | -0.000 | 0.948 | 0.927 | 0.044 | 0.000 | 0.000 |
| R1-8B | PPI++ bersama | 5 | 14 | -0.003 | 0.876 | 0.860 | 0.210 | 0.000 | 0.000 |
| R1-8B | PPI++ bersama | 10 | 14 | -0.003 | 0.920 | 0.896 | 0.132 | 0.000 | 0.000 |
| R1-8B | PPI++ bersama | 20 | 14 | -0.000 | 0.935 | 0.916 | 0.086 | 0.000 | 0.000 |
| R1-8B | PPI++ bersama | 30 | 14 | -0.001 | 0.945 | 0.940 | 0.066 | 0.000 | 0.000 |
| R1-8B | PPI++ bersama | 50 | 14 | -0.000 | 0.944 | 0.920 | 0.043 | 0.000 | 0.000 |
| R1-8B | PPI++ berstrata | 5 | 14 | -0.002 | 0.887 | 0.870 | 0.202 | 0.000 | 0.000 |
| R1-8B | PPI++ berstrata | 10 | 14 | -0.002 | 0.919 | 0.909 | 0.126 | 0.000 | 0.000 |
| R1-8B | PPI++ berstrata | 20 | 14 | 0.000 | 0.939 | 0.930 | 0.083 | 0.000 | 0.000 |
| R1-8B | PPI++ berstrata | 30 | 14 | -0.000 | 0.944 | 0.936 | 0.063 | 0.000 | 0.000 |
| R1-8B | PPI++ berstrata | 50 | 14 | 0.000 | 0.938 | 0.920 | 0.041 | 0.000 | 0.000 |
| R1-8B | RG bersama | 5 | 14 | 0.173 | 0.236 | 0.185 | 0.275 | 0.000 | 0.000 |
| R1-8B | RG bersama | 10 | 14 | 0.167 | 0.000 | 0.000 | 0.153 | 0.000 | 0.000 |
| R1-8B | RG bersama | 20 | 14 | 0.162 | 0.000 | 0.000 | 0.094 | 0.000 | 0.000 |
| R1-8B | RG bersama | 30 | 14 | 0.162 | 0.000 | 0.000 | 0.071 | 0.000 | 0.000 |
| R1-8B | RG bersama | 50 | 14 | 0.161 | 0.000 | 0.000 | 0.046 | 0.000 | 0.000 |
| R1-8B | RG per sumber | 5 | 14 | -0.025 | 0.875 | 0.847 | 7.049 | 0.095 | 0.137 |
| R1-8B | RG per sumber | 10 | 14 | -0.041 | 0.950 | 0.933 | 2.960 | 0.079 | 0.039 |
| R1-8B | RG per sumber | 20 | 14 | -0.005 | 0.964 | 0.948 | 0.357 | 0.013 | 0.002 |
| R1-8B | RG per sumber | 30 | 14 | -0.004 | 0.961 | 0.947 | 0.207 | 0.005 | 0.001 |
| R1-8B | RG per sumber | 50 | 14 | -0.002 | 0.952 | 0.939 | 0.123 | 0.000 | 0.000 |

### Model lain (suplemen), 14 setelan per model

| model | penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | naif | 0 | 14 | -0.095 | 0.000 | 0.000 | 0.051 | 0.000 | 0.000 |
| Gemma-3-12B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Gemma-3-12B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| Gemma-3-12B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| Gemma-3-12B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Gemma-3-12B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Gemma-3-12B | PPI | 5 | 14 | -0.001 | 0.941 | 0.925 | 0.249 | 0.000 | 0.000 |
| Gemma-3-12B | PPI | 10 | 14 | -0.002 | 0.944 | 0.936 | 0.146 | 0.000 | 0.000 |
| Gemma-3-12B | PPI | 20 | 14 | -0.000 | 0.951 | 0.940 | 0.092 | 0.000 | 0.000 |
| Gemma-3-12B | PPI | 30 | 14 | -0.000 | 0.952 | 0.932 | 0.070 | 0.000 | 0.000 |
| Gemma-3-12B | PPI | 50 | 14 | -0.000 | 0.950 | 0.942 | 0.045 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ bersama | 5 | 14 | -0.002 | 0.891 | 0.874 | 0.231 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ bersama | 10 | 14 | -0.002 | 0.925 | 0.917 | 0.142 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ bersama | 20 | 14 | -0.000 | 0.942 | 0.930 | 0.092 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ bersama | 30 | 14 | -0.000 | 0.948 | 0.932 | 0.070 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ bersama | 50 | 14 | -0.000 | 0.948 | 0.938 | 0.045 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ berstrata | 5 | 14 | -0.002 | 0.897 | 0.883 | 0.228 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ berstrata | 10 | 14 | -0.002 | 0.927 | 0.911 | 0.140 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ berstrata | 20 | 14 | -0.001 | 0.943 | 0.934 | 0.091 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ berstrata | 30 | 14 | 0.000 | 0.948 | 0.933 | 0.069 | 0.000 | 0.000 |
| Gemma-3-12B | PPI++ berstrata | 50 | 14 | 0.000 | 0.948 | 0.936 | 0.045 | 0.000 | 0.000 |
| Gemma-3-12B | RG bersama | 5 | 14 | 0.202 | 0.553 | 0.214 | 0.412 | 0.000 | 0.000 |
| Gemma-3-12B | RG bersama | 10 | 14 | 0.180 | 0.055 | 0.000 | 0.233 | 0.000 | 0.000 |
| Gemma-3-12B | RG bersama | 20 | 14 | 0.172 | 0.000 | 0.000 | 0.146 | 0.000 | 0.000 |
| Gemma-3-12B | RG bersama | 30 | 14 | 0.171 | 0.000 | 0.000 | 0.111 | 0.000 | 0.000 |
| Gemma-3-12B | RG bersama | 50 | 14 | 0.169 | 0.000 | 0.000 | 0.072 | 0.000 | 0.000 |
| Gemma-3-12B | RG per sumber | 5 | 14 | 0.052 | 0.675 | 0.589 | 14.804 | 0.110 | 0.391 |
| Gemma-3-12B | RG per sumber | 10 | 14 | -0.023 | 0.897 | 0.834 | 2.774 | 0.101 | 0.149 |
| Gemma-3-12B | RG per sumber | 20 | 14 | -0.028 | 0.960 | 0.935 | 2.111 | 0.065 | 0.038 |
| Gemma-3-12B | RG per sumber | 30 | 14 | -0.009 | 0.965 | 0.950 | 0.342 | 0.037 | 0.010 |
| Gemma-3-12B | RG per sumber | 50 | 14 | -0.005 | 0.960 | 0.949 | 0.160 | 0.004 | 0.000 |
| Gemma-3-27B | naif | 0 | 14 | -0.127 | 0.000 | 0.000 | 0.049 | 0.000 | 0.000 |
| Gemma-3-27B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Gemma-3-27B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| Gemma-3-27B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| Gemma-3-27B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Gemma-3-27B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Gemma-3-27B | PPI | 5 | 14 | -0.002 | 0.940 | 0.918 | 0.258 | 0.000 | 0.000 |
| Gemma-3-27B | PPI | 10 | 14 | -0.002 | 0.939 | 0.930 | 0.151 | 0.000 | 0.000 |
| Gemma-3-27B | PPI | 20 | 14 | -0.001 | 0.952 | 0.944 | 0.096 | 0.000 | 0.000 |
| Gemma-3-27B | PPI | 30 | 14 | -0.001 | 0.952 | 0.938 | 0.072 | 0.000 | 0.000 |
| Gemma-3-27B | PPI | 50 | 14 | -0.000 | 0.950 | 0.936 | 0.047 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ bersama | 5 | 14 | -0.001 | 0.901 | 0.856 | 0.234 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ bersama | 10 | 14 | -0.002 | 0.923 | 0.911 | 0.142 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ bersama | 20 | 14 | -0.000 | 0.945 | 0.929 | 0.092 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ bersama | 30 | 14 | -0.000 | 0.952 | 0.930 | 0.070 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ bersama | 50 | 14 | -0.000 | 0.950 | 0.935 | 0.046 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ berstrata | 5 | 14 | -0.001 | 0.898 | 0.873 | 0.235 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ berstrata | 10 | 14 | -0.002 | 0.923 | 0.899 | 0.141 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ berstrata | 20 | 14 | -0.000 | 0.945 | 0.918 | 0.092 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ berstrata | 30 | 14 | -0.000 | 0.948 | 0.918 | 0.070 | 0.000 | 0.000 |
| Gemma-3-27B | PPI++ berstrata | 50 | 14 | 0.000 | 0.944 | 0.933 | 0.045 | 0.000 | 0.000 |
| Gemma-3-27B | RG bersama | 5 | 14 | 0.191 | 0.745 | 0.110 | 0.498 | 0.000 | 0.000 |
| Gemma-3-27B | RG bersama | 10 | 14 | 0.158 | 0.406 | 0.000 | 0.266 | 0.000 | 0.000 |
| Gemma-3-27B | RG bersama | 20 | 14 | 0.146 | 0.029 | 0.000 | 0.165 | 0.000 | 0.000 |
| Gemma-3-27B | RG bersama | 30 | 14 | 0.143 | 0.000 | 0.000 | 0.123 | 0.000 | 0.000 |
| Gemma-3-27B | RG bersama | 50 | 14 | 0.142 | 0.000 | 0.000 | 0.079 | 0.000 | 0.000 |
| Gemma-3-27B | RG per sumber | 5 | 14 | 0.075 | 0.565 | 0.344 | 2.551 | 0.116 | 0.636 |
| Gemma-3-27B | RG per sumber | 10 | 14 | 0.011 | 0.808 | 0.587 | 1.046 | 0.087 | 0.392 |
| Gemma-3-27B | RG per sumber | 20 | 14 | -0.006 | 0.947 | 0.857 | 0.513 | 0.086 | 0.112 |
| Gemma-3-27B | RG per sumber | 30 | 14 | -0.017 | 0.962 | 0.934 | 0.366 | 0.061 | 0.056 |
| Gemma-3-27B | RG per sumber | 50 | 14 | -0.006 | 0.966 | 0.954 | 0.168 | 0.023 | 0.006 |
| Qwen-3-30B-A3B-Instruct | naif | 0 | 14 | -0.044 | 0.000 | 0.000 | 0.063 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 5 | 14 | -0.001 | 0.941 | 0.919 | 0.233 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 10 | 14 | -0.002 | 0.945 | 0.930 | 0.139 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 20 | 14 | 0.000 | 0.948 | 0.936 | 0.089 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 30 | 14 | -0.000 | 0.949 | 0.933 | 0.068 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 50 | 14 | -0.000 | 0.940 | 0.930 | 0.044 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 5 | 14 | -0.002 | 0.883 | 0.836 | 0.209 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 10 | 14 | -0.002 | 0.915 | 0.900 | 0.131 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 20 | 14 | -0.000 | 0.935 | 0.916 | 0.086 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 30 | 14 | -0.000 | 0.941 | 0.924 | 0.066 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 50 | 14 | -0.000 | 0.934 | 0.929 | 0.044 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 5 | 14 | -0.002 | 0.887 | 0.841 | 0.198 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 10 | 14 | -0.001 | 0.910 | 0.899 | 0.125 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 20 | 14 | 0.001 | 0.931 | 0.913 | 0.084 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 30 | 14 | 0.001 | 0.938 | 0.918 | 0.064 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 50 | 14 | 0.000 | 0.930 | 0.920 | 0.043 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 5 | 14 | 0.196 | 0.327 | 0.001 | 0.323 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 10 | 14 | 0.185 | 0.002 | 0.000 | 0.181 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 20 | 14 | 0.182 | 0.000 | 0.000 | 0.110 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 30 | 14 | 0.180 | 0.000 | 0.000 | 0.082 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 50 | 14 | 0.179 | 0.000 | 0.000 | 0.052 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 5 | 14 | 0.000 | 0.845 | 0.752 | 2.088 | 0.126 | 0.228 |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 10 | 14 | -0.026 | 0.942 | 0.909 | 0.968 | 0.059 | 0.062 |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 20 | 14 | -0.009 | 0.957 | 0.942 | 0.293 | 0.019 | 0.006 |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 30 | 14 | -0.007 | 0.956 | 0.944 | 0.187 | 0.005 | 0.001 |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 50 | 14 | -0.004 | 0.948 | 0.934 | 0.109 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | naif | 0 | 14 | 0.014 | 1.000 | 0.000 | 0.078 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | klasik | 10 | 14 | -0.003 | 0.935 | 0.934 | 0.225 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | klasik | 20 | 14 | -0.001 | 0.943 | 0.938 | 0.145 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 5 | 14 | -0.002 | 0.937 | 0.925 | 0.266 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 10 | 14 | -0.002 | 0.944 | 0.931 | 0.162 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 20 | 14 | -0.000 | 0.944 | 0.920 | 0.104 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 30 | 14 | -0.000 | 0.943 | 0.935 | 0.078 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 50 | 14 | -0.001 | 0.942 | 0.932 | 0.051 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 5 | 14 | -0.001 | 0.849 | 0.833 | 0.205 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 10 | 14 | -0.001 | 0.899 | 0.889 | 0.137 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 20 | 14 | -0.000 | 0.925 | 0.899 | 0.091 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 30 | 14 | 0.000 | 0.937 | 0.925 | 0.069 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 50 | 14 | -0.000 | 0.940 | 0.934 | 0.046 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 5 | 14 | -0.001 | 0.854 | 0.844 | 0.187 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 10 | 14 | -0.002 | 0.899 | 0.887 | 0.122 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 20 | 14 | 0.000 | 0.919 | 0.903 | 0.081 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 30 | 14 | 0.001 | 0.931 | 0.911 | 0.062 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 50 | 14 | 0.000 | 0.933 | 0.924 | 0.041 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 5 | 14 | 0.156 | 0.025 | 0.001 | 0.177 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 10 | 14 | 0.155 | 0.000 | 0.000 | 0.100 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 20 | 14 | 0.151 | 0.000 | 0.000 | 0.061 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 30 | 14 | 0.151 | 0.000 | 0.000 | 0.046 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 50 | 14 | 0.151 | 0.000 | 0.000 | 0.029 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 5 | 14 | -0.018 | 0.936 | 0.920 | 1.749 | 0.069 | 0.029 |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 10 | 14 | -0.008 | 0.952 | 0.948 | 0.356 | 0.019 | 0.002 |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 20 | 14 | -0.002 | 0.946 | 0.937 | 0.193 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 30 | 14 | -0.002 | 0.944 | 0.938 | 0.144 | 0.000 | 0.000 |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 50 | 14 | -0.002 | 0.938 | 0.926 | 0.093 | 0.000 | 0.000 |
| Qwen-3-32B | naif | 0 | 14 | -0.012 | 1.000 | 0.000 | 0.071 | 0.000 | 0.000 |
| Qwen-3-32B | klasik | 5 | 14 | -0.003 | 0.917 | 0.917 | 0.372 | 0.000 | 0.000 |
| Qwen-3-32B | klasik | 10 | 14 | -0.003 | 0.935 | 0.935 | 0.225 | 0.000 | 0.000 |
| Qwen-3-32B | klasik | 20 | 14 | -0.001 | 0.943 | 0.943 | 0.145 | 0.000 | 0.000 |
| Qwen-3-32B | klasik | 30 | 14 | -0.000 | 0.947 | 0.947 | 0.109 | 0.000 | 0.000 |
| Qwen-3-32B | klasik | 50 | 14 | 0.000 | 0.953 | 0.953 | 0.071 | 0.000 | 0.000 |
| Qwen-3-32B | PPI | 5 | 14 | -0.001 | 0.946 | 0.901 | 0.215 | 0.000 | 0.000 |
| Qwen-3-32B | PPI | 10 | 14 | -0.002 | 0.944 | 0.926 | 0.129 | 0.000 | 0.000 |
| Qwen-3-32B | PPI | 20 | 14 | -0.000 | 0.944 | 0.938 | 0.083 | 0.000 | 0.000 |
| Qwen-3-32B | PPI | 30 | 14 | -0.000 | 0.938 | 0.932 | 0.062 | 0.000 | 0.000 |
| Qwen-3-32B | PPI | 50 | 14 | -0.000 | 0.948 | 0.928 | 0.041 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ bersama | 5 | 14 | -0.002 | 0.877 | 0.845 | 0.186 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ bersama | 10 | 14 | -0.003 | 0.911 | 0.894 | 0.117 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ bersama | 20 | 14 | -0.001 | 0.927 | 0.919 | 0.077 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ bersama | 30 | 14 | -0.001 | 0.933 | 0.922 | 0.059 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ bersama | 50 | 14 | -0.000 | 0.937 | 0.928 | 0.039 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ berstrata | 5 | 14 | -0.002 | 0.881 | 0.860 | 0.175 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ berstrata | 10 | 14 | -0.001 | 0.909 | 0.878 | 0.112 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ berstrata | 20 | 14 | 0.001 | 0.925 | 0.910 | 0.074 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ berstrata | 30 | 14 | 0.001 | 0.931 | 0.920 | 0.056 | 0.000 | 0.000 |
| Qwen-3-32B | PPI++ berstrata | 50 | 14 | 0.000 | 0.929 | 0.922 | 0.037 | 0.000 | 0.000 |
| Qwen-3-32B | RG bersama | 5 | 14 | 0.184 | 0.144 | 0.042 | 0.251 | 0.000 | 0.000 |
| Qwen-3-32B | RG bersama | 10 | 14 | 0.178 | 0.000 | 0.000 | 0.141 | 0.000 | 0.000 |
| Qwen-3-32B | RG bersama | 20 | 14 | 0.175 | 0.000 | 0.000 | 0.086 | 0.000 | 0.000 |
| Qwen-3-32B | RG bersama | 30 | 14 | 0.175 | 0.000 | 0.000 | 0.065 | 0.000 | 0.000 |
| Qwen-3-32B | RG bersama | 50 | 14 | 0.174 | 0.000 | 0.000 | 0.041 | 0.000 | 0.000 |
| Qwen-3-32B | RG per sumber | 5 | 14 | 0.003 | 0.897 | 0.737 | 6.326 | 0.080 | 0.248 |
| Qwen-3-32B | RG per sumber | 10 | 14 | -0.027 | 0.957 | 0.928 | 1.010 | 0.060 | 0.061 |
| Qwen-3-32B | RG per sumber | 20 | 14 | -0.008 | 0.959 | 0.945 | 0.235 | 0.019 | 0.004 |
| Qwen-3-32B | RG per sumber | 30 | 14 | -0.007 | 0.948 | 0.928 | 0.168 | 0.006 | 0.000 |
| Qwen-3-32B | RG per sumber | 50 | 14 | -0.004 | 0.945 | 0.923 | 0.104 | 0.000 | 0.000 |

### Naif: banyak setelan yang selangnya mencakup Δ sebenarnya

| model | setelan | mencakup |
|---|---|---|
| Gemma-3-12B | 14 | 1.000 |
| Gemma-3-27B | 14 | 2.000 |
| Llama-70B | 14 | 13.000 |
| Llama-8B | 14 | 2.000 |
| Qwen-3-30B-A3B-Instruct | 14 | 1.000 |
| Qwen-3-30B-A3B-Thinking | 14 | 11.000 |
| Qwen-3-32B | 14 | 13.000 |
| R1-70B | 14 | 13.000 |
| R1-8B | 14 | 0.000 |

Semua model: 56 dari 126 setelan

### Anggaran label: m terkecil dengan cakupan >= 0.93 dan lebar <= 0.1 (inf = tidak tercapai sampai m = 50)

| model | penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|---|
| Gemma-3-12B | klasik | 14 | 50.000 | 50.000 |
| Gemma-3-12B | PPI | 14 | 20.000 | 30.000 |
| Gemma-3-12B | PPI++ bersama | 14 | 20.000 | 30.000 |
| Gemma-3-12B | PPI++ berstrata | 14 | 20.000 | 30.000 |
| Gemma-3-12B | RG bersama | 0 | inf | inf |
| Gemma-3-12B | RG per sumber | 0 | inf | inf |
| Gemma-3-27B | klasik | 14 | 50.000 | 50.000 |
| Gemma-3-27B | PPI | 14 | 20.000 | 30.000 |
| Gemma-3-27B | PPI++ bersama | 14 | 20.000 | 30.000 |
| Gemma-3-27B | PPI++ berstrata | 14 | 20.000 | 50.000 |
| Gemma-3-27B | RG bersama | 0 | inf | inf |
| Gemma-3-27B | RG per sumber | 0 | inf | inf |
| Llama-70B | klasik | 14 | 50.000 | 50.000 |
| Llama-70B | PPI | 14 | 20.000 | 30.000 |
| Llama-70B | PPI++ bersama | 14 | 20.000 | 30.000 |
| Llama-70B | PPI++ berstrata | 14 | 30.000 | 30.000 |
| Llama-70B | RG bersama | 0 | inf | inf |
| Llama-70B | RG per sumber | 9 | 50.000 | inf |
| Llama-8B | klasik | 14 | 50.000 | 50.000 |
| Llama-8B | PPI | 14 | 30.000 | 50.000 |
| Llama-8B | PPI++ bersama | 14 | 30.000 | 30.000 |
| Llama-8B | PPI++ berstrata | 14 | 30.000 | 50.000 |
| Llama-8B | RG bersama | 0 | inf | inf |
| Llama-8B | RG per sumber | 0 | inf | inf |
| Qwen-3-30B-A3B-Instruct | klasik | 14 | 50.000 | 50.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 14 | 20.000 | 30.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 14 | 20.000 | 50.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 14 | 20.000 | 50.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 0 | inf | inf |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 2 | inf | inf |
| Qwen-3-30B-A3B-Thinking | klasik | 14 | 50.000 | 50.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 14 | 30.000 | 30.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 14 | 30.000 | 50.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 12 | 30.000 | inf |
| Qwen-3-30B-A3B-Thinking | RG bersama | 0 | inf | inf |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 9 | 50.000 | inf |
| Qwen-3-32B | klasik | 14 | 50.000 | 50.000 |
| Qwen-3-32B | PPI | 14 | 20.000 | 20.000 |
| Qwen-3-32B | PPI++ bersama | 14 | 30.000 | 50.000 |
| Qwen-3-32B | PPI++ berstrata | 11 | 30.000 | inf |
| Qwen-3-32B | RG bersama | 0 | inf | inf |
| Qwen-3-32B | RG per sumber | 4 | inf | inf |
| R1-70B | klasik | 14 | 50.000 | 50.000 |
| R1-70B | PPI | 14 | 20.000 | 30.000 |
| R1-70B | PPI++ bersama | 14 | 30.000 | 50.000 |
| R1-70B | PPI++ berstrata | 10 | 30.000 | inf |
| R1-70B | RG bersama | 0 | inf | inf |
| R1-70B | RG per sumber | 9 | 50.000 | inf |
| R1-8B | klasik | 14 | 50.000 | 50.000 |
| R1-8B | PPI | 14 | 20.000 | 30.000 |
| R1-8B | PPI++ bersama | 14 | 20.000 | 30.000 |
| R1-8B | PPI++ berstrata | 14 | 20.000 | 20.000 |
| R1-8B | RG bersama | 0 | inf | inf |
| R1-8B | RG per sumber | 2 | inf | inf |
