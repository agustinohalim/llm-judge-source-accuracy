# Hasil JuriKlinis 1 — tahap 1: bias perbandingan naif dari vonis juri terbit

Sumber angka: `juriklinis_tahap1.py` (venv-gpu, 21 Nov 2026; bootstrap 2000 kali ambil ulang pasien, benih 20261121,
`juriklinis_bootstrap.py`) atas `C:\Data\VeriFact-BHC\`. Ambang aturan henti dikunci di
`Artikel_JuriKlinis_Rencana.md` bagian A sebelum skrip ini pertama dijalankan. Biner (Supported lawan bukan), klaim
atomik, semua proposisi termasuk `invalid`, pada klaim yang divonis tiap setelan. Hanya agregat per setelan juri.
Penaksir terkoreksi dan anggaran label belum dihitung.

## Ringkasan

- Aturan henti: bias kecil (|bias| < 0,02 dan selang 95 % memuat 0) pada **38 dari 126** setelan; ambang henti ≥ 84
  → **LANJUT** ke penaksir terkoreksi dan anggaran label.
- Tanda Δ naif tidak pernah terbalik: 0 dari 126 setelan pada taksiran titik, dan peluang bootstrap terbalik 0,000
  di semua setelan (seperti diduga sebelum hasil, karena Δ sebenarnya 0,281).
- Bias negatif (juri mengecilkan selisih dokter lawan LLM) pada 90 dari 126 setelan.

## Pengamatan (dicatat sesudah hasil; bahan rencana, belum klaim naskah)

1. Arah dan besar bias bergantung pada model dan setelan pengambilan konteks. Gemma-3 12B/27B, Llama-8B, dan R1-8B
   mengecilkan Δ (median −0,05 sampai −0,13; terburuk −0,19). Qwen-3-30B-A3B-Instruct fakta klaim top_n 5–25
   membesarkannya +0,17, tetapi top_n 75–150 mengecilkannya −0,03 sampai −0,05. Llama-70B, R1-70B, Qwen-3-32B,
   dan Qwen-3-30B-A3B-Thinking paling dekat ke 0 (median −0,012 sampai +0,014), dan dari keempat model inilah
   34 dari 38 setelan "kecil" berasal.
2. Juri jauh lebih peka terhadap klaim bermasalah di BHC dokter daripada di BHC LLM. Median sensitivitas per model:
   dokter 0,43–0,92, LLM 0,11–0,70. Jadi salah klasifikasinya berbeda menurut sumber. Akibat yang diuji di tahap
   berikut (belum disimpulkan): koreksi sensitivitas/spesifisitas bersama bisa bias; koreksi per sumber atau PPI
   berstrata seharusnya tidak.
3. Bias Δ kecil tidak berarti tingkat per sumber benar. Contoh: Llama-70B fakta klaim top_n 5 punya bias Δ +0,018,
   tetapi juri memberi 0,567 untuk dokter (sebenarnya 0,331) dan 0,268 untuk LLM (sebenarnya 0,050). Galat kedua
   sumber saling menghapus. Ini menyentuh usul VeriFact memakai persentase "supported" dari juri sebagai ambang mutu.
4. Batasan angka ini: sensitivitas/spesifisitas belum diberi selang; sisi LLM hanya punya 173 klaim bukan Supported.
   Setelan Qwen-3-30B-A3B-Thinking fakta klaim top_n 100 dihitung pada 5574 klaim dokter, sehingga Δ-nya 0,283.

## Keluaran skrip

Disalin utuh dari keluaran `juriklinis_tahap1.py`.

### Aturan henti (ambang dikunci 21 Nov 2026)

- Setelan juri yang menilai klaim kedua sumber: 126
- Bias kecil (|bias| < 0.02 dan selang 95 % memuat 0): 38; ambang henti >= 84
- Tanda Δ naif terbalik pada taksiran titik: 0
- Keputusan: LANJUT (penaksir terkoreksi, anggaran label)

### Per model (median atas setelan; sens/spek = juri mengenali klaim bukan Supported)

| model | setelan | bias_median | bias_min | bias_maks | kecil | terbalik | sens_dokter | spek_dokter | sens_llm | spek_llm |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 14 | -0.095 | -0.144 | -0.029 | 0 | 0 | 0.506 | 0.911 | 0.191 | 0.964 |
| Gemma-3-27B | 14 | -0.127 | -0.192 | -0.002 | 2 | 0 | 0.429 | 0.948 | 0.113 | 0.981 |
| Llama-70B | 14 | 0.010 | -0.028 | 0.033 | 9 | 0 | 0.772 | 0.803 | 0.413 | 0.921 |
| Llama-8B | 14 | -0.093 | -0.148 | -0.016 | 2 | 0 | 0.594 | 0.727 | 0.295 | 0.830 |
| Qwen-3-30B-A3B-Instruct | 14 | -0.044 | -0.079 | 0.174 | 0 | 0 | 0.663 | 0.880 | 0.289 | 0.960 |
| Qwen-3-30B-A3B-Thinking | 14 | 0.014 | -0.085 | 0.035 | 6 | 0 | 0.916 | 0.699 | 0.699 | 0.823 |
| Qwen-3-32B | 14 | -0.012 | -0.055 | 0.006 | 10 | 0 | 0.771 | 0.822 | 0.399 | 0.924 |
| R1-70B | 14 | 0.004 | -0.051 | 0.022 | 9 | 0 | 0.808 | 0.827 | 0.462 | 0.930 |
| R1-8B | 14 | -0.051 | -0.098 | -0.042 | 0 | 0 | 0.697 | 0.823 | 0.376 | 0.898 |

### Bias Δ naif per setelan juri (selang bootstrap persentil 95 %, pasien sebagai unit)

| model | fact_type | top_n | rater_alias | n_dokter | n_llm | delta | delta_naif | bias | bias_bawah | bias_atas | kecil | terbalik | p_terbalik |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | claim | 5 | v1.1.0-rater-001 | 5648 | 3447 | 0.281 | 0.252 | -0.029 | -0.049 | -0.006 | False | False | 0.000 |
| Gemma-3-12B | claim | 10 | v1.1.0-rater-002 | 5648 | 3447 | 0.281 | 0.249 | -0.031 | -0.053 | -0.009 | False | False | 0.000 |
| Gemma-3-12B | claim | 25 | v1.1.0-rater-003 | 5648 | 3447 | 0.281 | 0.243 | -0.038 | -0.056 | -0.018 | False | False | 0.000 |
| Gemma-3-12B | claim | 50 | v1.1.0-rater-004 | 5648 | 3447 | 0.281 | 0.191 | -0.089 | -0.111 | -0.068 | False | False | 0.000 |
| Gemma-3-12B | claim | 75 | v1.1.0-rater-005 | 5648 | 3447 | 0.281 | 0.182 | -0.099 | -0.122 | -0.077 | False | False | 0.000 |
| Gemma-3-12B | claim | 100 | v1.1.0-rater-006 | 5648 | 3447 | 0.281 | 0.185 | -0.095 | -0.117 | -0.074 | False | False | 0.000 |
| Gemma-3-12B | claim | 125 | v1.1.0-rater-007 | 5648 | 3447 | 0.281 | 0.173 | -0.108 | -0.130 | -0.086 | False | False | 0.000 |
| Gemma-3-12B | claim | 150 | v1.1.0-rater-008 | 5648 | 3447 | 0.281 | 0.182 | -0.099 | -0.122 | -0.076 | False | False | 0.000 |
| Gemma-3-12B | sentence | 5 | v1.1.0-rater-009 | 5648 | 3447 | 0.281 | 0.197 | -0.083 | -0.107 | -0.059 | False | False | 0.000 |
| Gemma-3-12B | sentence | 10 | v1.1.0-rater-010 | 5648 | 3447 | 0.281 | 0.204 | -0.076 | -0.094 | -0.056 | False | False | 0.000 |
| Gemma-3-12B | sentence | 25 | v1.1.0-rater-011 | 5648 | 3447 | 0.281 | 0.186 | -0.095 | -0.117 | -0.072 | False | False | 0.000 |
| Gemma-3-12B | sentence | 50 | v1.1.0-rater-012 | 5648 | 3447 | 0.281 | 0.149 | -0.131 | -0.154 | -0.108 | False | False | 0.000 |
| Gemma-3-12B | sentence | 75 | v1.1.0-rater-013 | 5648 | 3447 | 0.281 | 0.149 | -0.132 | -0.155 | -0.108 | False | False | 0.000 |
| Gemma-3-12B | sentence | 100 | v1.1.0-rater-014 | 5648 | 3447 | 0.281 | 0.137 | -0.144 | -0.171 | -0.117 | False | False | 0.000 |
| Gemma-3-27B | claim | 5 | v1.1.0-rater-015 | 5648 | 3447 | 0.281 | 0.279 | -0.002 | -0.021 | 0.019 | True | False | 0.000 |
| Gemma-3-27B | claim | 10 | v1.1.0-rater-016 | 5648 | 3447 | 0.281 | 0.272 | -0.009 | -0.029 | 0.014 | True | False | 0.000 |
| Gemma-3-27B | claim | 25 | v1.1.0-rater-017 | 5648 | 3447 | 0.281 | 0.235 | -0.046 | -0.065 | -0.025 | False | False | 0.000 |
| Gemma-3-27B | claim | 50 | v1.1.0-rater-018 | 5648 | 3447 | 0.281 | 0.175 | -0.106 | -0.127 | -0.085 | False | False | 0.000 |
| Gemma-3-27B | claim | 75 | v1.1.0-rater-019 | 5648 | 3447 | 0.281 | 0.130 | -0.150 | -0.174 | -0.128 | False | False | 0.000 |
| Gemma-3-27B | claim | 100 | v1.1.0-rater-020 | 5648 | 3447 | 0.281 | 0.100 | -0.180 | -0.204 | -0.156 | False | False | 0.000 |
| Gemma-3-27B | claim | 125 | v1.1.0-rater-021 | 5648 | 3447 | 0.281 | 0.092 | -0.189 | -0.212 | -0.163 | False | False | 0.000 |
| Gemma-3-27B | claim | 150 | v1.1.0-rater-022 | 5648 | 3447 | 0.281 | 0.088 | -0.192 | -0.217 | -0.168 | False | False | 0.000 |
| Gemma-3-27B | sentence | 5 | v1.1.0-rater-023 | 5648 | 3447 | 0.281 | 0.226 | -0.055 | -0.078 | -0.030 | False | False | 0.000 |
| Gemma-3-27B | sentence | 10 | v1.1.0-rater-024 | 5648 | 3447 | 0.281 | 0.232 | -0.049 | -0.071 | -0.027 | False | False | 0.000 |
| Gemma-3-27B | sentence | 25 | v1.1.0-rater-025 | 5648 | 3447 | 0.281 | 0.188 | -0.092 | -0.113 | -0.070 | False | False | 0.000 |
| Gemma-3-27B | sentence | 50 | v1.1.0-rater-026 | 5648 | 3447 | 0.281 | 0.132 | -0.149 | -0.172 | -0.125 | False | False | 0.000 |
| Gemma-3-27B | sentence | 75 | v1.1.0-rater-027 | 5648 | 3447 | 0.281 | 0.112 | -0.169 | -0.193 | -0.144 | False | False | 0.000 |
| Gemma-3-27B | sentence | 100 | v1.1.0-rater-028 | 5648 | 3447 | 0.281 | 0.123 | -0.157 | -0.182 | -0.133 | False | False | 0.000 |
| Llama-70B | claim | 5 | v1.1.0-rater-151 | 5648 | 3447 | 0.281 | 0.299 | 0.018 | -0.003 | 0.040 | True | False | 0.000 |
| Llama-70B | claim | 10 | v1.1.0-rater-152 | 5648 | 3447 | 0.281 | 0.309 | 0.028 | 0.006 | 0.051 | False | False | 0.000 |
| Llama-70B | claim | 25 | v1.1.0-rater-153 | 5648 | 3447 | 0.281 | 0.306 | 0.025 | 0.005 | 0.046 | False | False | 0.000 |
| Llama-70B | claim | 50 | v1.1.0-rater-155 | 5648 | 3447 | 0.281 | 0.291 | 0.010 | -0.008 | 0.030 | True | False | 0.000 |
| Llama-70B | claim | 75 | v1.1.0-rater-158 | 5648 | 3447 | 0.281 | 0.292 | 0.011 | -0.006 | 0.030 | True | False | 0.000 |
| Llama-70B | claim | 100 | v1.1.0-rater-159 | 5648 | 3447 | 0.281 | 0.301 | 0.021 | 0.001 | 0.042 | False | False | 0.000 |
| Llama-70B | claim | 125 | v1.1.0-rater-160 | 5648 | 3447 | 0.281 | 0.314 | 0.033 | 0.015 | 0.053 | False | False | 0.000 |
| Llama-70B | claim | 150 | v1.1.0-rater-161 | 5648 | 3447 | 0.281 | 0.291 | 0.010 | -0.008 | 0.031 | True | False | 0.000 |
| Llama-70B | sentence | 5 | v1.1.0-rater-165 | 5648 | 3447 | 0.281 | 0.253 | -0.028 | -0.055 | 0.002 | False | False | 0.000 |
| Llama-70B | sentence | 10 | v1.1.0-rater-166 | 5648 | 3447 | 0.281 | 0.284 | 0.003 | -0.018 | 0.028 | True | False | 0.000 |
| Llama-70B | sentence | 25 | v1.1.0-rater-167 | 5648 | 3447 | 0.281 | 0.281 | 0.000 | -0.019 | 0.021 | True | False | 0.000 |
| Llama-70B | sentence | 50 | v1.1.0-rater-169 | 5648 | 3447 | 0.281 | 0.267 | -0.014 | -0.033 | 0.006 | True | False | 0.000 |
| Llama-70B | sentence | 75 | v1.1.0-rater-172 | 5648 | 3447 | 0.281 | 0.275 | -0.006 | -0.024 | 0.013 | True | False | 0.000 |
| Llama-70B | sentence | 100 | v1.1.0-rater-173 | 5648 | 3447 | 0.281 | 0.278 | -0.002 | -0.022 | 0.019 | True | False | 0.000 |
| Llama-8B | claim | 5 | v1.1.0-rater-125 | 5648 | 3447 | 0.281 | 0.264 | -0.017 | -0.044 | 0.011 | True | False | 0.000 |
| Llama-8B | claim | 10 | v1.1.0-rater-126 | 5648 | 3447 | 0.281 | 0.235 | -0.046 | -0.076 | -0.013 | False | False | 0.000 |
| Llama-8B | claim | 25 | v1.1.0-rater-127 | 5648 | 3447 | 0.281 | 0.265 | -0.016 | -0.049 | 0.018 | True | False | 0.000 |
| Llama-8B | claim | 50 | v1.1.0-rater-129 | 5648 | 3447 | 0.281 | 0.215 | -0.066 | -0.098 | -0.035 | False | False | 0.000 |
| Llama-8B | claim | 75 | v1.1.0-rater-132 | 5648 | 3447 | 0.281 | 0.195 | -0.085 | -0.116 | -0.054 | False | False | 0.000 |
| Llama-8B | claim | 100 | v1.1.0-rater-133 | 5648 | 3447 | 0.281 | 0.186 | -0.095 | -0.125 | -0.063 | False | False | 0.000 |
| Llama-8B | claim | 125 | v1.1.0-rater-134 | 5648 | 3447 | 0.281 | 0.190 | -0.091 | -0.118 | -0.063 | False | False | 0.000 |
| Llama-8B | claim | 150 | v1.1.0-rater-135 | 5648 | 3447 | 0.281 | 0.192 | -0.089 | -0.117 | -0.062 | False | False | 0.000 |
| Llama-8B | sentence | 5 | v1.1.0-rater-139 | 5648 | 3447 | 0.281 | 0.173 | -0.108 | -0.132 | -0.085 | False | False | 0.000 |
| Llama-8B | sentence | 10 | v1.1.0-rater-140 | 5648 | 3447 | 0.281 | 0.171 | -0.110 | -0.136 | -0.082 | False | False | 0.000 |
| Llama-8B | sentence | 25 | v1.1.0-rater-141 | 5648 | 3447 | 0.281 | 0.183 | -0.098 | -0.129 | -0.063 | False | False | 0.000 |
| Llama-8B | sentence | 50 | v1.1.0-rater-143 | 5648 | 3447 | 0.281 | 0.153 | -0.127 | -0.160 | -0.090 | False | False | 0.000 |
| Llama-8B | sentence | 75 | v1.1.0-rater-146 | 5648 | 3447 | 0.281 | 0.132 | -0.148 | -0.183 | -0.115 | False | False | 0.000 |
| Llama-8B | sentence | 100 | v1.1.0-rater-147 | 5648 | 3447 | 0.281 | 0.141 | -0.140 | -0.174 | -0.104 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 5 | v1.1.0-rater-029 | 5648 | 3447 | 0.281 | 0.455 | 0.174 | 0.149 | 0.200 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 10 | v1.1.0-rater-030 | 5648 | 3447 | 0.281 | 0.455 | 0.174 | 0.151 | 0.200 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 25 | v1.1.0-rater-031 | 5648 | 3447 | 0.281 | 0.454 | 0.173 | 0.152 | 0.197 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 50 | v1.1.0-rater-032 | 5648 | 3447 | 0.281 | 0.377 | 0.096 | 0.066 | 0.127 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 75 | v1.1.0-rater-033 | 5648 | 3447 | 0.281 | 0.251 | -0.030 | -0.050 | -0.010 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 100 | v1.1.0-rater-034 | 5648 | 3447 | 0.281 | 0.239 | -0.042 | -0.061 | -0.021 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 125 | v1.1.0-rater-035 | 5648 | 3447 | 0.281 | 0.239 | -0.042 | -0.061 | -0.023 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | claim | 150 | v1.1.0-rater-036 | 5648 | 3447 | 0.281 | 0.235 | -0.045 | -0.066 | -0.024 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | sentence | 5 | v1.1.0-rater-037 | 5648 | 3447 | 0.281 | 0.211 | -0.070 | -0.097 | -0.043 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | sentence | 10 | v1.1.0-rater-038 | 5648 | 3447 | 0.281 | 0.225 | -0.055 | -0.078 | -0.033 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | sentence | 25 | v1.1.0-rater-039 | 5648 | 3447 | 0.281 | 0.232 | -0.049 | -0.069 | -0.028 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | sentence | 50 | v1.1.0-rater-040 | 5648 | 3447 | 0.281 | 0.226 | -0.055 | -0.077 | -0.033 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | sentence | 75 | v1.1.0-rater-041 | 5648 | 3447 | 0.281 | 0.209 | -0.072 | -0.094 | -0.049 | False | False | 0.000 |
| Qwen-3-30B-A3B-Instruct | sentence | 100 | v1.1.0-rater-042 | 5648 | 3447 | 0.281 | 0.202 | -0.079 | -0.100 | -0.058 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 5 | v1.1.0-rater-043 | 5648 | 3447 | 0.281 | 0.196 | -0.085 | -0.113 | -0.056 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 10 | v1.1.0-rater-044 | 5648 | 3447 | 0.281 | 0.237 | -0.043 | -0.072 | -0.015 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 25 | v1.1.0-rater-045 | 5648 | 3447 | 0.281 | 0.266 | -0.015 | -0.041 | 0.012 | True | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 50 | v1.1.0-rater-046 | 5648 | 3447 | 0.281 | 0.292 | 0.011 | -0.013 | 0.037 | True | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 75 | v1.1.0-rater-047 | 5648 | 3447 | 0.281 | 0.297 | 0.016 | -0.007 | 0.042 | True | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 100 | v1.1.0-rater-048 | 5574 | 3447 | 0.283 | 0.318 | 0.035 | 0.011 | 0.060 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 125 | v1.1.0-rater-049 | 5648 | 3447 | 0.281 | 0.313 | 0.032 | 0.009 | 0.057 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | claim | 150 | v1.1.0-rater-050 | 5648 | 3447 | 0.281 | 0.310 | 0.029 | 0.006 | 0.053 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | sentence | 5 | v1.1.0-rater-051 | 5648 | 3447 | 0.281 | 0.222 | -0.059 | -0.085 | -0.031 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | sentence | 10 | v1.1.0-rater-052 | 5648 | 3447 | 0.281 | 0.256 | -0.025 | -0.052 | 0.003 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | sentence | 25 | v1.1.0-rater-053 | 5648 | 3447 | 0.281 | 0.286 | 0.005 | -0.019 | 0.031 | True | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | sentence | 50 | v1.1.0-rater-054 | 5648 | 3447 | 0.281 | 0.298 | 0.017 | -0.003 | 0.039 | True | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | sentence | 75 | v1.1.0-rater-055 | 5648 | 3447 | 0.281 | 0.306 | 0.025 | 0.004 | 0.049 | False | False | 0.000 |
| Qwen-3-30B-A3B-Thinking | sentence | 100 | v1.1.0-rater-056 | 5648 | 3447 | 0.281 | 0.298 | 0.017 | -0.004 | 0.040 | True | False | 0.000 |
| Qwen-3-32B | claim | 5 | v1.1.0-rater-057 | 5648 | 3447 | 0.281 | 0.269 | -0.012 | -0.033 | 0.010 | True | False | 0.000 |
| Qwen-3-32B | claim | 10 | v1.1.0-rater-058 | 5648 | 3447 | 0.281 | 0.275 | -0.005 | -0.027 | 0.018 | True | False | 0.000 |
| Qwen-3-32B | claim | 25 | v1.1.0-rater-059 | 5648 | 3447 | 0.281 | 0.287 | 0.006 | -0.013 | 0.027 | True | False | 0.000 |
| Qwen-3-32B | claim | 50 | v1.1.0-rater-060 | 5648 | 3447 | 0.281 | 0.284 | 0.004 | -0.016 | 0.024 | True | False | 0.000 |
| Qwen-3-32B | claim | 75 | v1.1.0-rater-061 | 5648 | 3447 | 0.281 | 0.279 | -0.002 | -0.020 | 0.018 | True | False | 0.000 |
| Qwen-3-32B | claim | 100 | v1.1.0-rater-062 | 5648 | 3447 | 0.281 | 0.284 | 0.004 | -0.014 | 0.023 | True | False | 0.000 |
| Qwen-3-32B | claim | 125 | v1.1.0-rater-063 | 5648 | 3447 | 0.281 | 0.282 | 0.001 | -0.016 | 0.021 | True | False | 0.000 |
| Qwen-3-32B | claim | 150 | v1.1.0-rater-064 | 5648 | 3447 | 0.281 | 0.268 | -0.013 | -0.031 | 0.008 | True | False | 0.000 |
| Qwen-3-32B | sentence | 5 | v1.1.0-rater-065 | 5648 | 3447 | 0.281 | 0.226 | -0.055 | -0.077 | -0.030 | False | False | 0.000 |
| Qwen-3-32B | sentence | 10 | v1.1.0-rater-066 | 5648 | 3447 | 0.281 | 0.258 | -0.023 | -0.043 | 0.002 | False | False | 0.000 |
| Qwen-3-32B | sentence | 25 | v1.1.0-rater-067 | 5648 | 3447 | 0.281 | 0.265 | -0.016 | -0.034 | 0.006 | True | False | 0.000 |
| Qwen-3-32B | sentence | 50 | v1.1.0-rater-068 | 5648 | 3447 | 0.281 | 0.254 | -0.027 | -0.047 | -0.005 | False | False | 0.000 |
| Qwen-3-32B | sentence | 75 | v1.1.0-rater-069 | 5648 | 3447 | 0.281 | 0.265 | -0.016 | -0.034 | 0.003 | True | False | 0.000 |
| Qwen-3-32B | sentence | 100 | v1.1.0-rater-070 | 5648 | 3447 | 0.281 | 0.257 | -0.024 | -0.044 | -0.003 | False | False | 0.000 |
| R1-70B | claim | 5 | v1.1.0-rater-099 | 5648 | 3447 | 0.281 | 0.230 | -0.051 | -0.074 | -0.026 | False | False | 0.000 |
| R1-70B | claim | 10 | v1.1.0-rater-100 | 5648 | 3447 | 0.281 | 0.269 | -0.011 | -0.035 | 0.013 | True | False | 0.000 |
| R1-70B | claim | 25 | v1.1.0-rater-101 | 5648 | 3447 | 0.281 | 0.303 | 0.022 | 0.003 | 0.043 | False | False | 0.000 |
| R1-70B | claim | 50 | v1.1.0-rater-103 | 5648 | 3447 | 0.281 | 0.300 | 0.019 | 0.001 | 0.038 | False | False | 0.000 |
| R1-70B | claim | 75 | v1.1.0-rater-106 | 5648 | 3447 | 0.281 | 0.302 | 0.021 | 0.003 | 0.041 | False | False | 0.000 |
| R1-70B | claim | 100 | v1.1.0-rater-107 | 5648 | 3447 | 0.281 | 0.283 | 0.002 | -0.017 | 0.022 | True | False | 0.000 |
| R1-70B | claim | 125 | v1.1.0-rater-108 | 5648 | 3447 | 0.281 | 0.290 | 0.009 | -0.008 | 0.026 | True | False | 0.000 |
| R1-70B | claim | 150 | v1.1.0-rater-109 | 5648 | 3447 | 0.281 | 0.285 | 0.005 | -0.014 | 0.024 | True | False | 0.000 |
| R1-70B | sentence | 5 | v1.1.0-rater-113 | 5648 | 3447 | 0.281 | 0.246 | -0.035 | -0.059 | -0.008 | False | False | 0.000 |
| R1-70B | sentence | 10 | v1.1.0-rater-114 | 5648 | 3447 | 0.281 | 0.279 | -0.002 | -0.024 | 0.021 | True | False | 0.000 |
| R1-70B | sentence | 25 | v1.1.0-rater-115 | 5648 | 3447 | 0.281 | 0.288 | 0.007 | -0.012 | 0.027 | True | False | 0.000 |
| R1-70B | sentence | 50 | v1.1.0-rater-117 | 5648 | 3447 | 0.281 | 0.288 | 0.007 | -0.010 | 0.026 | True | False | 0.000 |
| R1-70B | sentence | 75 | v1.1.0-rater-120 | 5648 | 3447 | 0.281 | 0.283 | 0.002 | -0.016 | 0.021 | True | False | 0.000 |
| R1-70B | sentence | 100 | v1.1.0-rater-121 | 5648 | 3447 | 0.281 | 0.277 | -0.004 | -0.021 | 0.015 | True | False | 0.000 |
| R1-8B | claim | 5 | v1.1.0-rater-073 | 5648 | 3447 | 0.281 | 0.200 | -0.081 | -0.103 | -0.057 | False | False | 0.000 |
| R1-8B | claim | 10 | v1.1.0-rater-074 | 5648 | 3447 | 0.281 | 0.228 | -0.053 | -0.073 | -0.032 | False | False | 0.000 |
| R1-8B | claim | 25 | v1.1.0-rater-075 | 5648 | 3447 | 0.281 | 0.239 | -0.042 | -0.064 | -0.020 | False | False | 0.000 |
| R1-8B | claim | 50 | v1.1.0-rater-077 | 5648 | 3447 | 0.281 | 0.236 | -0.045 | -0.064 | -0.025 | False | False | 0.000 |
| R1-8B | claim | 75 | v1.1.0-rater-080 | 5648 | 3447 | 0.281 | 0.237 | -0.044 | -0.063 | -0.024 | False | False | 0.000 |
| R1-8B | claim | 100 | v1.1.0-rater-081 | 5648 | 3447 | 0.281 | 0.232 | -0.049 | -0.069 | -0.028 | False | False | 0.000 |
| R1-8B | claim | 125 | v1.1.0-rater-082 | 5648 | 3447 | 0.281 | 0.234 | -0.047 | -0.069 | -0.025 | False | False | 0.000 |
| R1-8B | claim | 150 | v1.1.0-rater-083 | 5648 | 3447 | 0.281 | 0.220 | -0.061 | -0.084 | -0.038 | False | False | 0.000 |
| R1-8B | sentence | 5 | v1.1.0-rater-087 | 5648 | 3447 | 0.281 | 0.183 | -0.098 | -0.126 | -0.070 | False | False | 0.000 |
| R1-8B | sentence | 10 | v1.1.0-rater-088 | 5648 | 3447 | 0.281 | 0.217 | -0.063 | -0.088 | -0.038 | False | False | 0.000 |
| R1-8B | sentence | 25 | v1.1.0-rater-089 | 5648 | 3447 | 0.281 | 0.234 | -0.046 | -0.067 | -0.025 | False | False | 0.000 |
| R1-8B | sentence | 50 | v1.1.0-rater-091 | 5648 | 3447 | 0.281 | 0.237 | -0.044 | -0.065 | -0.021 | False | False | 0.000 |
| R1-8B | sentence | 75 | v1.1.0-rater-094 | 5648 | 3447 | 0.281 | 0.224 | -0.057 | -0.078 | -0.035 | False | False | 0.000 |
| R1-8B | sentence | 100 | v1.1.0-rater-095 | 5648 | 3447 | 0.281 | 0.215 | -0.066 | -0.088 | -0.042 | False | False | 0.000 |

### Tingkat per sumber dan ketepatan juri per setelan (p = dokter berlabel, q = juri)

| model | fact_type | top_n | p_dokter | q_dokter | sens_dokter | spek_dokter | p_llm | q_llm | sens_llm | spek_llm |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | claim | 5 | 0.331 | 0.358 | 0.685 | 0.804 | 0.050 | 0.106 | 0.266 | 0.903 |
| Gemma-3-12B | claim | 10 | 0.331 | 0.328 | 0.655 | 0.833 | 0.050 | 0.079 | 0.237 | 0.929 |
| Gemma-3-12B | claim | 25 | 0.331 | 0.293 | 0.626 | 0.872 | 0.050 | 0.050 | 0.220 | 0.959 |
| Gemma-3-12B | claim | 50 | 0.331 | 0.230 | 0.515 | 0.912 | 0.050 | 0.038 | 0.179 | 0.969 |
| Gemma-3-12B | claim | 75 | 0.331 | 0.218 | 0.485 | 0.915 | 0.050 | 0.035 | 0.173 | 0.972 |
| Gemma-3-12B | claim | 100 | 0.331 | 0.227 | 0.504 | 0.911 | 0.050 | 0.041 | 0.202 | 0.967 |
| Gemma-3-12B | claim | 125 | 0.331 | 0.214 | 0.477 | 0.916 | 0.050 | 0.041 | 0.191 | 0.967 |
| Gemma-3-12B | claim | 150 | 0.331 | 0.226 | 0.489 | 0.905 | 0.050 | 0.044 | 0.191 | 0.964 |
| Gemma-3-12B | sentence | 5 | 0.331 | 0.314 | 0.625 | 0.841 | 0.050 | 0.116 | 0.249 | 0.891 |
| Gemma-3-12B | sentence | 10 | 0.331 | 0.278 | 0.594 | 0.878 | 0.050 | 0.074 | 0.202 | 0.933 |
| Gemma-3-12B | sentence | 25 | 0.331 | 0.226 | 0.507 | 0.914 | 0.050 | 0.040 | 0.127 | 0.965 |
| Gemma-3-12B | sentence | 50 | 0.331 | 0.185 | 0.419 | 0.931 | 0.050 | 0.035 | 0.139 | 0.970 |
| Gemma-3-12B | sentence | 75 | 0.331 | 0.191 | 0.417 | 0.921 | 0.050 | 0.042 | 0.156 | 0.964 |
| Gemma-3-12B | sentence | 100 | 0.331 | 0.182 | 0.390 | 0.920 | 0.050 | 0.046 | 0.150 | 0.960 |
| Gemma-3-27B | claim | 5 | 0.331 | 0.401 | 0.772 | 0.783 | 0.050 | 0.122 | 0.410 | 0.893 |
| Gemma-3-27B | claim | 10 | 0.331 | 0.368 | 0.747 | 0.820 | 0.050 | 0.096 | 0.329 | 0.916 |
| Gemma-3-27B | claim | 25 | 0.331 | 0.284 | 0.630 | 0.887 | 0.050 | 0.049 | 0.191 | 0.958 |
| Gemma-3-27B | claim | 50 | 0.331 | 0.196 | 0.470 | 0.939 | 0.050 | 0.021 | 0.127 | 0.984 |
| Gemma-3-27B | claim | 75 | 0.331 | 0.143 | 0.358 | 0.963 | 0.050 | 0.013 | 0.081 | 0.991 |
| Gemma-3-27B | claim | 100 | 0.331 | 0.110 | 0.286 | 0.977 | 0.050 | 0.010 | 0.075 | 0.994 |
| Gemma-3-27B | claim | 125 | 0.331 | 0.099 | 0.259 | 0.980 | 0.050 | 0.007 | 0.058 | 0.996 |
| Gemma-3-27B | claim | 150 | 0.331 | 0.096 | 0.255 | 0.982 | 0.050 | 0.008 | 0.064 | 0.995 |
| Gemma-3-27B | sentence | 5 | 0.331 | 0.367 | 0.733 | 0.814 | 0.050 | 0.141 | 0.324 | 0.869 |
| Gemma-3-27B | sentence | 10 | 0.331 | 0.315 | 0.676 | 0.863 | 0.050 | 0.084 | 0.231 | 0.924 |
| Gemma-3-27B | sentence | 25 | 0.331 | 0.225 | 0.535 | 0.929 | 0.050 | 0.036 | 0.145 | 0.969 |
| Gemma-3-27B | sentence | 50 | 0.331 | 0.155 | 0.387 | 0.959 | 0.050 | 0.023 | 0.092 | 0.980 |
| Gemma-3-27B | sentence | 75 | 0.331 | 0.132 | 0.332 | 0.968 | 0.050 | 0.020 | 0.098 | 0.984 |
| Gemma-3-27B | sentence | 100 | 0.331 | 0.143 | 0.344 | 0.957 | 0.050 | 0.019 | 0.058 | 0.983 |
| Llama-70B | claim | 5 | 0.331 | 0.567 | 0.920 | 0.608 | 0.050 | 0.268 | 0.642 | 0.752 |
| Llama-70B | claim | 10 | 0.331 | 0.508 | 0.884 | 0.678 | 0.050 | 0.199 | 0.566 | 0.820 |
| Llama-70B | claim | 25 | 0.331 | 0.428 | 0.810 | 0.760 | 0.050 | 0.123 | 0.468 | 0.896 |
| Llama-70B | claim | 50 | 0.331 | 0.380 | 0.766 | 0.811 | 0.050 | 0.088 | 0.393 | 0.928 |
| Llama-70B | claim | 75 | 0.331 | 0.375 | 0.761 | 0.816 | 0.050 | 0.083 | 0.410 | 0.934 |
| Llama-70B | claim | 100 | 0.331 | 0.386 | 0.761 | 0.800 | 0.050 | 0.084 | 0.416 | 0.933 |
| Llama-70B | claim | 125 | 0.331 | 0.403 | 0.781 | 0.784 | 0.050 | 0.089 | 0.405 | 0.928 |
| Llama-70B | claim | 150 | 0.331 | 0.371 | 0.751 | 0.816 | 0.050 | 0.080 | 0.387 | 0.936 |
| Llama-70B | sentence | 5 | 0.331 | 0.506 | 0.879 | 0.678 | 0.050 | 0.253 | 0.630 | 0.767 |
| Llama-70B | sentence | 10 | 0.331 | 0.464 | 0.857 | 0.730 | 0.050 | 0.180 | 0.538 | 0.839 |
| Llama-70B | sentence | 25 | 0.331 | 0.381 | 0.778 | 0.815 | 0.050 | 0.100 | 0.434 | 0.917 |
| Llama-70B | sentence | 50 | 0.331 | 0.352 | 0.727 | 0.833 | 0.050 | 0.085 | 0.393 | 0.931 |
| Llama-70B | sentence | 75 | 0.331 | 0.368 | 0.740 | 0.816 | 0.050 | 0.093 | 0.410 | 0.923 |
| Llama-70B | sentence | 100 | 0.331 | 0.377 | 0.747 | 0.806 | 0.050 | 0.098 | 0.410 | 0.918 |
| Llama-8B | claim | 5 | 0.331 | 0.637 | 0.878 | 0.483 | 0.050 | 0.373 | 0.543 | 0.636 |
| Llama-8B | claim | 10 | 0.331 | 0.620 | 0.857 | 0.497 | 0.050 | 0.385 | 0.572 | 0.625 |
| Llama-8B | claim | 25 | 0.331 | 0.617 | 0.818 | 0.483 | 0.050 | 0.352 | 0.474 | 0.655 |
| Llama-8B | claim | 50 | 0.331 | 0.382 | 0.584 | 0.718 | 0.050 | 0.167 | 0.237 | 0.837 |
| Llama-8B | claim | 75 | 0.331 | 0.354 | 0.568 | 0.752 | 0.050 | 0.159 | 0.231 | 0.845 |
| Llama-8B | claim | 100 | 0.331 | 0.325 | 0.538 | 0.780 | 0.050 | 0.139 | 0.254 | 0.867 |
| Llama-8B | claim | 125 | 0.331 | 0.321 | 0.527 | 0.781 | 0.050 | 0.131 | 0.243 | 0.875 |
| Llama-8B | claim | 150 | 0.331 | 0.376 | 0.604 | 0.736 | 0.050 | 0.185 | 0.335 | 0.823 |
| Llama-8B | sentence | 5 | 0.331 | 0.515 | 0.820 | 0.636 | 0.050 | 0.343 | 0.509 | 0.666 |
| Llama-8B | sentence | 10 | 0.331 | 0.563 | 0.846 | 0.577 | 0.050 | 0.393 | 0.595 | 0.618 |
| Llama-8B | sentence | 25 | 0.331 | 0.433 | 0.677 | 0.687 | 0.050 | 0.251 | 0.410 | 0.758 |
| Llama-8B | sentence | 50 | 0.331 | 0.312 | 0.526 | 0.794 | 0.050 | 0.159 | 0.249 | 0.846 |
| Llama-8B | sentence | 75 | 0.331 | 0.257 | 0.428 | 0.827 | 0.050 | 0.125 | 0.225 | 0.880 |
| Llama-8B | sentence | 100 | 0.331 | 0.291 | 0.455 | 0.790 | 0.050 | 0.150 | 0.220 | 0.854 |
| Qwen-3-30B-A3B-Instruct | claim | 5 | 0.331 | 0.586 | 0.936 | 0.587 | 0.050 | 0.131 | 0.410 | 0.884 |
| Qwen-3-30B-A3B-Instruct | claim | 10 | 0.331 | 0.552 | 0.928 | 0.634 | 0.050 | 0.097 | 0.364 | 0.917 |
| Qwen-3-30B-A3B-Instruct | claim | 25 | 0.331 | 0.521 | 0.917 | 0.675 | 0.050 | 0.067 | 0.341 | 0.947 |
| Qwen-3-30B-A3B-Instruct | claim | 50 | 0.331 | 0.432 | 0.829 | 0.764 | 0.050 | 0.055 | 0.312 | 0.959 |
| Qwen-3-30B-A3B-Instruct | claim | 75 | 0.331 | 0.303 | 0.662 | 0.874 | 0.050 | 0.053 | 0.295 | 0.960 |
| Qwen-3-30B-A3B-Instruct | claim | 100 | 0.331 | 0.284 | 0.628 | 0.886 | 0.050 | 0.045 | 0.277 | 0.967 |
| Qwen-3-30B-A3B-Instruct | claim | 125 | 0.331 | 0.282 | 0.620 | 0.886 | 0.050 | 0.043 | 0.243 | 0.968 |
| Qwen-3-30B-A3B-Instruct | claim | 150 | 0.331 | 0.277 | 0.614 | 0.890 | 0.050 | 0.041 | 0.225 | 0.969 |
| Qwen-3-30B-A3B-Instruct | sentence | 5 | 0.331 | 0.376 | 0.759 | 0.814 | 0.050 | 0.165 | 0.399 | 0.847 |
| Qwen-3-30B-A3B-Instruct | sentence | 10 | 0.331 | 0.326 | 0.699 | 0.858 | 0.050 | 0.101 | 0.324 | 0.911 |
| Qwen-3-30B-A3B-Instruct | sentence | 25 | 0.331 | 0.291 | 0.665 | 0.894 | 0.050 | 0.059 | 0.283 | 0.953 |
| Qwen-3-30B-A3B-Instruct | sentence | 50 | 0.331 | 0.271 | 0.625 | 0.904 | 0.050 | 0.045 | 0.243 | 0.965 |
| Qwen-3-30B-A3B-Instruct | sentence | 75 | 0.331 | 0.248 | 0.574 | 0.914 | 0.050 | 0.039 | 0.208 | 0.970 |
| Qwen-3-30B-A3B-Instruct | sentence | 100 | 0.331 | 0.239 | 0.562 | 0.921 | 0.050 | 0.037 | 0.191 | 0.971 |
| Qwen-3-30B-A3B-Thinking | claim | 5 | 0.331 | 0.618 | 0.953 | 0.547 | 0.050 | 0.422 | 0.844 | 0.600 |
| Qwen-3-30B-A3B-Thinking | claim | 10 | 0.331 | 0.584 | 0.944 | 0.595 | 0.050 | 0.346 | 0.775 | 0.677 |
| Qwen-3-30B-A3B-Thinking | claim | 25 | 0.331 | 0.542 | 0.929 | 0.650 | 0.050 | 0.276 | 0.740 | 0.749 |
| Qwen-3-30B-A3B-Thinking | claim | 50 | 0.331 | 0.521 | 0.923 | 0.678 | 0.050 | 0.229 | 0.699 | 0.796 |
| Qwen-3-30B-A3B-Thinking | claim | 75 | 0.331 | 0.505 | 0.917 | 0.698 | 0.050 | 0.209 | 0.699 | 0.817 |
| Qwen-3-30B-A3B-Thinking | claim | 100 | 0.333 | 0.503 | 0.912 | 0.701 | 0.050 | 0.186 | 0.671 | 0.840 |
| Qwen-3-30B-A3B-Thinking | claim | 125 | 0.331 | 0.488 | 0.903 | 0.717 | 0.050 | 0.175 | 0.688 | 0.852 |
| Qwen-3-30B-A3B-Thinking | claim | 150 | 0.331 | 0.484 | 0.909 | 0.725 | 0.050 | 0.175 | 0.653 | 0.851 |
| Qwen-3-30B-A3B-Thinking | sentence | 5 | 0.331 | 0.590 | 0.951 | 0.589 | 0.050 | 0.368 | 0.815 | 0.656 |
| Qwen-3-30B-A3B-Thinking | sentence | 10 | 0.331 | 0.542 | 0.945 | 0.658 | 0.050 | 0.286 | 0.780 | 0.740 |
| Qwen-3-30B-A3B-Thinking | sentence | 25 | 0.331 | 0.487 | 0.916 | 0.726 | 0.050 | 0.200 | 0.734 | 0.828 |
| Qwen-3-30B-A3B-Thinking | sentence | 50 | 0.331 | 0.463 | 0.912 | 0.759 | 0.050 | 0.165 | 0.694 | 0.863 |
| Qwen-3-30B-A3B-Thinking | sentence | 75 | 0.331 | 0.452 | 0.898 | 0.769 | 0.050 | 0.146 | 0.659 | 0.881 |
| Qwen-3-30B-A3B-Thinking | sentence | 100 | 0.331 | 0.441 | 0.903 | 0.787 | 0.050 | 0.143 | 0.665 | 0.884 |
| Qwen-3-32B | claim | 5 | 0.331 | 0.476 | 0.856 | 0.712 | 0.050 | 0.207 | 0.549 | 0.811 |
| Qwen-3-32B | claim | 10 | 0.331 | 0.450 | 0.842 | 0.743 | 0.050 | 0.175 | 0.532 | 0.844 |
| Qwen-3-32B | claim | 25 | 0.331 | 0.418 | 0.818 | 0.780 | 0.050 | 0.131 | 0.451 | 0.885 |
| Qwen-3-32B | claim | 50 | 0.331 | 0.385 | 0.786 | 0.813 | 0.050 | 0.101 | 0.428 | 0.917 |
| Qwen-3-32B | claim | 75 | 0.331 | 0.376 | 0.764 | 0.815 | 0.050 | 0.097 | 0.428 | 0.920 |
| Qwen-3-32B | claim | 100 | 0.331 | 0.372 | 0.778 | 0.829 | 0.050 | 0.087 | 0.370 | 0.928 |
| Qwen-3-32B | claim | 125 | 0.331 | 0.360 | 0.759 | 0.837 | 0.050 | 0.078 | 0.370 | 0.937 |
| Qwen-3-32B | claim | 150 | 0.331 | 0.346 | 0.737 | 0.847 | 0.050 | 0.078 | 0.347 | 0.936 |
| Qwen-3-32B | sentence | 5 | 0.331 | 0.445 | 0.833 | 0.747 | 0.050 | 0.219 | 0.520 | 0.797 |
| Qwen-3-32B | sentence | 10 | 0.331 | 0.398 | 0.799 | 0.800 | 0.050 | 0.140 | 0.457 | 0.877 |
| Qwen-3-32B | sentence | 25 | 0.331 | 0.348 | 0.755 | 0.853 | 0.050 | 0.083 | 0.347 | 0.931 |
| Qwen-3-32B | sentence | 50 | 0.331 | 0.323 | 0.717 | 0.872 | 0.050 | 0.069 | 0.283 | 0.943 |
| Qwen-3-32B | sentence | 75 | 0.331 | 0.321 | 0.718 | 0.875 | 0.050 | 0.056 | 0.277 | 0.955 |
| Qwen-3-32B | sentence | 100 | 0.331 | 0.312 | 0.713 | 0.886 | 0.050 | 0.056 | 0.266 | 0.955 |
| R1-70B | claim | 5 | 0.331 | 0.545 | 0.920 | 0.641 | 0.050 | 0.315 | 0.728 | 0.707 |
| R1-70B | claim | 10 | 0.331 | 0.507 | 0.895 | 0.685 | 0.050 | 0.238 | 0.653 | 0.784 |
| R1-70B | claim | 25 | 0.331 | 0.444 | 0.866 | 0.764 | 0.050 | 0.141 | 0.549 | 0.881 |
| R1-70B | claim | 50 | 0.331 | 0.397 | 0.820 | 0.812 | 0.050 | 0.098 | 0.462 | 0.922 |
| R1-70B | claim | 75 | 0.331 | 0.382 | 0.807 | 0.828 | 0.050 | 0.080 | 0.439 | 0.939 |
| R1-70B | claim | 100 | 0.331 | 0.362 | 0.785 | 0.847 | 0.050 | 0.080 | 0.468 | 0.941 |
| R1-70B | claim | 125 | 0.331 | 0.356 | 0.764 | 0.846 | 0.050 | 0.066 | 0.405 | 0.951 |
| R1-70B | claim | 150 | 0.331 | 0.351 | 0.773 | 0.858 | 0.050 | 0.066 | 0.428 | 0.954 |
| R1-70B | sentence | 5 | 0.331 | 0.518 | 0.899 | 0.671 | 0.050 | 0.272 | 0.705 | 0.751 |
| R1-70B | sentence | 10 | 0.331 | 0.458 | 0.873 | 0.748 | 0.050 | 0.179 | 0.607 | 0.844 |
| R1-70B | sentence | 25 | 0.331 | 0.385 | 0.810 | 0.825 | 0.050 | 0.097 | 0.462 | 0.922 |
| R1-70B | sentence | 50 | 0.331 | 0.355 | 0.787 | 0.859 | 0.050 | 0.067 | 0.428 | 0.952 |
| R1-70B | sentence | 75 | 0.331 | 0.339 | 0.769 | 0.874 | 0.050 | 0.056 | 0.387 | 0.962 |
| R1-70B | sentence | 100 | 0.331 | 0.330 | 0.747 | 0.876 | 0.050 | 0.053 | 0.393 | 0.965 |
| R1-8B | claim | 5 | 0.331 | 0.437 | 0.754 | 0.720 | 0.050 | 0.238 | 0.480 | 0.775 |
| R1-8B | claim | 10 | 0.331 | 0.408 | 0.753 | 0.763 | 0.050 | 0.180 | 0.428 | 0.833 |
| R1-8B | claim | 25 | 0.331 | 0.380 | 0.738 | 0.798 | 0.050 | 0.140 | 0.399 | 0.873 |
| R1-8B | claim | 50 | 0.331 | 0.351 | 0.690 | 0.817 | 0.050 | 0.115 | 0.364 | 0.898 |
| R1-8B | claim | 75 | 0.331 | 0.353 | 0.703 | 0.821 | 0.050 | 0.116 | 0.387 | 0.899 |
| R1-8B | claim | 100 | 0.331 | 0.336 | 0.681 | 0.835 | 0.050 | 0.104 | 0.382 | 0.911 |
| R1-8B | claim | 125 | 0.331 | 0.327 | 0.659 | 0.837 | 0.050 | 0.093 | 0.364 | 0.921 |
| R1-8B | claim | 150 | 0.331 | 0.314 | 0.638 | 0.846 | 0.050 | 0.095 | 0.312 | 0.917 |
| R1-8B | sentence | 5 | 0.331 | 0.411 | 0.743 | 0.753 | 0.050 | 0.229 | 0.486 | 0.785 |
| R1-8B | sentence | 10 | 0.331 | 0.384 | 0.737 | 0.791 | 0.050 | 0.166 | 0.428 | 0.848 |
| R1-8B | sentence | 25 | 0.331 | 0.351 | 0.710 | 0.826 | 0.050 | 0.117 | 0.329 | 0.894 |
| R1-8B | sentence | 50 | 0.331 | 0.342 | 0.692 | 0.831 | 0.050 | 0.105 | 0.370 | 0.909 |
| R1-8B | sentence | 75 | 0.331 | 0.317 | 0.653 | 0.849 | 0.050 | 0.093 | 0.324 | 0.919 |
| R1-8B | sentence | 100 | 0.331 | 0.320 | 0.640 | 0.839 | 0.050 | 0.105 | 0.289 | 0.905 |
