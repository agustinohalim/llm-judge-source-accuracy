# Hasil JuriKlinis 6 — simulasi superpopulasi (rencana bagian K, post hoc)

> Dihasilkan 21 Nov 2026 oleh `juriklinis_superpopulasi.py` (benih 20261124, 1000 ambilan dengan pengembalian per m,
> tanpa koreksi populasi hingga). Rancangan dicatat di `Artikel_JuriKlinis_Rencana.md` bagian K sebelum dijalankan.
> Data dibaca lokal; yang dicetak hanya agregat atas setelan juri, hitungan 1–10 disamarkan. Menurut bagian K, angka
> anggaran dan lebar di naskah (Abstrak, Tabel 2) diambil dari berkas ini; tahap 2 (`Hasil_JuriKlinis_2.md`) menjadi
> kasus audit tetap atas 100 pasien.

## Ringkasan

1. **Analisis utama.** PPI per sumber tak bias, cakupan median 0,937–0,956 atas m (setelan terendah 0,911 pada
   m = 10, ≥ 0,926 dari m = 30). Anggaran PPI: median **30** pasien (126/126 setelan, maks 50); label saja **50**
   (126/126; lebar 0,099 pada m = 50, tipis di bawah 0,10). Lebar median pada m = 20: PPI 0,102, label saja 0,160,
   RG bersama 0,111; pada m = 30: PPI 0,082, label saja 0,130. Cakupan label saja 0,923–0,951 (0,924 pada m = 20).
   RG bersama: bias +0,188 (m = 5) sampai +0,167 (m = 200), cakupan 0 dari m = 10, tak pernah mencapai anggaran.
   RG per sumber: mencapai anggaran di 92/126 setelan, median m = 150; ambilan gagal sampai 62 % pada m = 5.
   PPI++ (satu bobot / per sumber): median 30, tetapi cakupan median 0,88–0,89 pada m = 5.
2. **Per model (PPI).** Median 20 untuk Llama 3.1 70B dan R1-Distill 70B; 25 untuk Qwen 3 32B, Qwen 3 30B-A3B
   instruct, R1-Distill 8B; 30 untuk Gemma 3 12B/27B dan Qwen 3 30B-A3B thinking; 45 untuk Llama 3.1 8B. Label saja
   50 untuk semua.
3. **Varian.** Satu dokter acak: PPI 30, label saja 50. Not Supported saja: label saja 20, PPI 30 (juri tidak
   menghemat). Not Addressed saja: PPI 30, label saja 40. Kalimat BHC LLM (tingkat LLM): label saja 20, PPI 30.
   Cakupan PPI median ≥ 0,933 di semua varian.
4. **Sebaran klaim unverified atas pasien.** Dokter: 1869 klaim di 99 pasien, median 14 per pasien, maks 68, lima
   pasien teratas 16,2 %. LLM: 173 klaim di 66 pasien, median < 11, maks 14, lima pasien teratas 23,1 %.

5. **Galat tingkat per sumber juri saja** (butir K4, dari tabel per setelan `Hasil_JuriKlinis_1.md`, 126 setelan).
   Dokter (p = 0,331): q − p median +0,036, rentang −0,235 sampai +0,306; |q − p| ≥ 0,05 di 75, ≥ 0,10 di 55; rasio
   q/p median 1,11 (0,29–1,92). LLM (p = 0,050): q − p median +0,049, rentang −0,043 sampai +0,372; ≥ 0,05 di 63,
   ≥ 0,10 di 38; rasio q/p median 1,98 (0,14–8,44). Median q − p LLM per model: Gemma 3 12B −0,007, Gemma 3 27B
   −0,028, Llama 3.1 70B +0,046, Llama 3.1 8B +0,126, Qwen 3 30B-A3B instruct +0,004, Qwen 3 30B-A3B thinking
   +0,154, Qwen 3 32B +0,042, R1-Distill 70B +0,038, R1-Distill 8B +0,066. Median q − p dokter per model: Gemma 3
   12B −0,105, Gemma 3 27B −0,156, Llama 3.1 70B +0,052, Llama 3.1 8B +0,048, Qwen 3 30B-A3B instruct −0,034, Qwen 3
   30B-A3B thinking +0,172, Qwen 3 32B +0,043, R1-Distill 70B +0,052, R1-Distill 8B +0,020. Median q LLM Qwen 3
   30B-A3B thinking 0,205.

Bandingkan tahap 2 dengan koreksi populasi hingga (tanpa pengembalian): PPI 20, label saja 50; tanpa koreksi atas
ambilan tanpa pengembalian (`Hasil_JuriKlinis_4.md`): PPI 30, label saja tak tercapai (lebar 0,100 pada 50).

## Log mentah


### Superpopulasi, varian utama (klaim, biner, human_gt): ringkasan atas 126 setelan (1000 ambilan dengan pengembalian per m)

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| PPI | 5 | 126 | -0.001 | 0.942 | 0.913 | 0.250 | 0.000 | 0.000 |
| PPI | 10 | 126 | -0.001 | 0.937 | 0.911 | 0.151 | 0.000 | 0.000 |
| PPI | 20 | 126 | -0.000 | 0.937 | 0.916 | 0.102 | 0.000 | 0.000 |
| PPI | 30 | 126 | 0.000 | 0.948 | 0.926 | 0.082 | 0.000 | 0.000 |
| PPI | 40 | 126 | -0.000 | 0.944 | 0.927 | 0.071 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.950 | 0.932 | 0.063 | 0.000 | 0.000 |
| PPI | 75 | 126 | 0.000 | 0.952 | 0.940 | 0.051 | 0.000 | 0.000 |
| PPI | 100 | 126 | 0.000 | 0.946 | 0.929 | 0.044 | 0.000 | 0.000 |
| PPI | 150 | 126 | -0.000 | 0.956 | 0.940 | 0.036 | 0.000 | 0.000 |
| PPI | 200 | 126 | -0.000 | 0.950 | 0.929 | 0.031 | 0.000 | 0.000 |
| PPI++ bersama | 5 | 126 | -0.001 | 0.881 | 0.826 | 0.212 | 0.000 | 0.000 |
| PPI++ bersama | 10 | 126 | -0.001 | 0.905 | 0.866 | 0.138 | 0.000 | 0.000 |
| PPI++ bersama | 20 | 126 | -0.000 | 0.919 | 0.889 | 0.095 | 0.000 | 0.000 |
| PPI++ bersama | 30 | 126 | 0.000 | 0.940 | 0.915 | 0.078 | 0.000 | 0.000 |
| PPI++ bersama | 40 | 126 | -0.001 | 0.937 | 0.918 | 0.067 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | -0.000 | 0.942 | 0.929 | 0.060 | 0.000 | 0.000 |
| PPI++ bersama | 75 | 126 | 0.000 | 0.945 | 0.933 | 0.049 | 0.000 | 0.000 |
| PPI++ bersama | 100 | 126 | -0.000 | 0.942 | 0.926 | 0.043 | 0.000 | 0.000 |
| PPI++ bersama | 150 | 126 | -0.000 | 0.952 | 0.936 | 0.035 | 0.000 | 0.000 |
| PPI++ bersama | 200 | 126 | -0.000 | 0.949 | 0.934 | 0.030 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.000 | 0.887 | 0.843 | 0.201 | 0.000 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.001 | 0.903 | 0.867 | 0.130 | 0.000 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.001 | 0.918 | 0.884 | 0.091 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.001 | 0.936 | 0.918 | 0.073 | 0.000 | 0.000 |
| PPI++ berstrata | 40 | 126 | 0.000 | 0.933 | 0.917 | 0.064 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.939 | 0.923 | 0.057 | 0.000 | 0.000 |
| PPI++ berstrata | 75 | 126 | 0.000 | 0.942 | 0.928 | 0.046 | 0.000 | 0.000 |
| PPI++ berstrata | 100 | 126 | 0.000 | 0.941 | 0.925 | 0.040 | 0.000 | 0.000 |
| PPI++ berstrata | 150 | 126 | -0.000 | 0.953 | 0.937 | 0.033 | 0.000 | 0.000 |
| PPI++ berstrata | 200 | 126 | 0.000 | 0.945 | 0.928 | 0.029 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.188 | 0.230 | 0.000 | 0.296 | 0.000 | 0.001 |
| RG bersama | 10 | 126 | 0.176 | 0.001 | 0.000 | 0.169 | 0.000 | 0.000 |
| RG bersama | 20 | 126 | 0.173 | 0.000 | 0.000 | 0.111 | 0.000 | 0.000 |
| RG bersama | 30 | 126 | 0.170 | 0.000 | 0.000 | 0.088 | 0.000 | 0.000 |
| RG bersama | 40 | 126 | 0.170 | 0.000 | 0.000 | 0.075 | 0.000 | 0.000 |
| RG bersama | 50 | 126 | 0.170 | 0.000 | 0.000 | 0.067 | 0.000 | 0.000 |
| RG bersama | 75 | 126 | 0.168 | 0.000 | 0.000 | 0.054 | 0.000 | 0.000 |
| RG bersama | 100 | 126 | 0.168 | 0.000 | 0.000 | 0.047 | 0.000 | 0.000 |
| RG bersama | 150 | 126 | 0.167 | 0.000 | 0.000 | 0.038 | 0.000 | 0.000 |
| RG bersama | 200 | 126 | 0.167 | 0.000 | 0.000 | 0.033 | 0.000 | 0.000 |
| RG per sumber | 5 | 126 | -0.008 | 0.866 | 0.355 | 4.189 | 0.165 | 0.624 |
| RG per sumber | 10 | 126 | -0.020 | 0.942 | 0.581 | 2.422 | 0.194 | 0.403 |
| RG per sumber | 20 | 126 | -0.010 | 0.954 | 0.773 | 0.419 | 0.181 | 0.215 |
| RG per sumber | 30 | 126 | -0.007 | 0.957 | 0.853 | 0.249 | 0.162 | 0.140 |
| RG per sumber | 40 | 126 | -0.004 | 0.955 | 0.877 | 0.197 | 0.146 | 0.112 |
| RG per sumber | 50 | 126 | -0.002 | 0.956 | 0.893 | 0.167 | 0.145 | 0.095 |
| RG per sumber | 75 | 126 | -0.003 | 0.956 | 0.935 | 0.133 | 0.120 | 0.047 |
| RG per sumber | 100 | 126 | -0.002 | 0.957 | 0.936 | 0.113 | 0.086 | 0.017 |
| RG per sumber | 150 | 126 | -0.001 | 0.956 | 0.938 | 0.091 | 0.055 | 0.013 |
| RG per sumber | 200 | 126 | -0.001 | 0.952 | 0.911 | 0.079 | 0.042 | 0.007 |
| klasik | 5 | 126 | -0.002 | 0.923 | 0.923 | 0.383 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.002 | 0.931 | 0.931 | 0.237 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.000 | 0.924 | 0.924 | 0.160 | 0.000 | 0.000 |
| klasik | 30 | 126 | 0.001 | 0.944 | 0.943 | 0.130 | 0.000 | 0.000 |
| klasik | 40 | 126 | -0.001 | 0.945 | 0.945 | 0.111 | 0.000 | 0.000 |
| klasik | 50 | 126 | -0.001 | 0.943 | 0.943 | 0.099 | 0.000 | 0.000 |
| klasik | 75 | 126 | 0.001 | 0.941 | 0.941 | 0.081 | 0.000 | 0.000 |
| klasik | 100 | 126 | 0.000 | 0.936 | 0.936 | 0.070 | 0.000 | 0.000 |
| klasik | 150 | 126 | -0.000 | 0.943 | 0.943 | 0.057 | 0.000 | 0.000 |
| klasik | 200 | 126 | 0.000 | 0.951 | 0.948 | 0.049 | 0.000 | 0.000 |

### Superpopulasi, varian utama (klaim, biner, human_gt): anggaran label (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai sampai m = 200)

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| PPI | 126 | 30.000 | 50.000 |
| PPI++ bersama | 126 | 30.000 | 50.000 |
| PPI++ berstrata | 126 | 30.000 | 75.000 |
| RG bersama | 0 | inf | inf |
| RG per sumber | 92 | 150.000 | inf |
| klasik | 126 | 50.000 | 50.000 |

### Superpopulasi, varian utama (klaim, biner, human_gt): anggaran label per model

| model | penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|---|
| Gemma-3-12B | PPI | 14 | 30.000 | 30.000 |
| Gemma-3-12B | PPI++ bersama | 14 | 30.000 | 30.000 |
| Gemma-3-12B | PPI++ berstrata | 14 | 30.000 | 30.000 |
| Gemma-3-12B | RG bersama | 0 | inf | inf |
| Gemma-3-12B | RG per sumber | 6 | inf | inf |
| Gemma-3-12B | klasik | 14 | 50.000 | 50.000 |
| Gemma-3-27B | PPI | 14 | 30.000 | 30.000 |
| Gemma-3-27B | PPI++ bersama | 14 | 30.000 | 30.000 |
| Gemma-3-27B | PPI++ berstrata | 14 | 30.000 | 30.000 |
| Gemma-3-27B | RG bersama | 0 | inf | inf |
| Gemma-3-27B | RG per sumber | 5 | inf | inf |
| Gemma-3-27B | klasik | 14 | 50.000 | 50.000 |
| Llama-70B | PPI | 14 | 20.000 | 40.000 |
| Llama-70B | PPI++ bersama | 14 | 30.000 | 40.000 |
| Llama-70B | PPI++ berstrata | 14 | 30.000 | 40.000 |
| Llama-70B | RG bersama | 0 | inf | inf |
| Llama-70B | RG per sumber | 14 | 100.000 | 200.000 |
| Llama-70B | klasik | 14 | 50.000 | 50.000 |
| Llama-8B | PPI | 14 | 45.000 | 50.000 |
| Llama-8B | PPI++ bersama | 14 | 40.000 | 50.000 |
| Llama-8B | PPI++ berstrata | 14 | 40.000 | 75.000 |
| Llama-8B | RG bersama | 0 | inf | inf |
| Llama-8B | RG per sumber | 0 | inf | inf |
| Llama-8B | klasik | 14 | 50.000 | 50.000 |
| Qwen-3-30B-A3B-Instruct | PPI | 14 | 25.000 | 50.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ bersama | 14 | 30.000 | 30.000 |
| Qwen-3-30B-A3B-Instruct | PPI++ berstrata | 14 | 30.000 | 40.000 |
| Qwen-3-30B-A3B-Instruct | RG bersama | 0 | inf | inf |
| Qwen-3-30B-A3B-Instruct | RG per sumber | 13 | 150.000 | inf |
| Qwen-3-30B-A3B-Instruct | klasik | 14 | 50.000 | 50.000 |
| Qwen-3-30B-A3B-Thinking | PPI | 14 | 30.000 | 50.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ bersama | 14 | 30.000 | 50.000 |
| Qwen-3-30B-A3B-Thinking | PPI++ berstrata | 14 | 30.000 | 75.000 |
| Qwen-3-30B-A3B-Thinking | RG bersama | 0 | inf | inf |
| Qwen-3-30B-A3B-Thinking | RG per sumber | 14 | 100.000 | 200.000 |
| Qwen-3-30B-A3B-Thinking | klasik | 14 | 50.000 | 50.000 |
| Qwen-3-32B | PPI | 14 | 25.000 | 30.000 |
| Qwen-3-32B | PPI++ bersama | 14 | 30.000 | 50.000 |
| Qwen-3-32B | PPI++ berstrata | 14 | 30.000 | 75.000 |
| Qwen-3-32B | RG bersama | 0 | inf | inf |
| Qwen-3-32B | RG per sumber | 14 | 150.000 | 200.000 |
| Qwen-3-32B | klasik | 14 | 50.000 | 50.000 |
| R1-70B | PPI | 14 | 20.000 | 30.000 |
| R1-70B | PPI++ bersama | 14 | 30.000 | 50.000 |
| R1-70B | PPI++ berstrata | 14 | 40.000 | 50.000 |
| R1-70B | RG bersama | 0 | inf | inf |
| R1-70B | RG per sumber | 14 | 75.000 | 150.000 |
| R1-70B | klasik | 14 | 50.000 | 50.000 |
| R1-8B | PPI | 14 | 25.000 | 40.000 |
| R1-8B | PPI++ bersama | 14 | 30.000 | 40.000 |
| R1-8B | PPI++ berstrata | 14 | 30.000 | 30.000 |
| R1-8B | RG bersama | 0 | inf | inf |
| R1-8B | RG per sumber | 12 | 150.000 | inf |
| R1-8B | klasik | 14 | 50.000 | 50.000 |

### Superpopulasi, varian satu dokter acak sebagai kebenaran: ringkasan atas 126 setelan (1000 ambilan dengan pengembalian per m)

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| PPI | 5 | 126 | -0.000 | 0.940 | 0.898 | 0.253 | 0.001 | 0.000 |
| PPI | 10 | 126 | -0.001 | 0.935 | 0.908 | 0.153 | 0.000 | 0.000 |
| PPI | 20 | 126 | -0.001 | 0.942 | 0.915 | 0.103 | 0.000 | 0.000 |
| PPI | 30 | 126 | -0.001 | 0.942 | 0.918 | 0.083 | 0.000 | 0.000 |
| PPI | 40 | 126 | -0.001 | 0.944 | 0.926 | 0.071 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.945 | 0.929 | 0.063 | 0.000 | 0.000 |
| PPI | 75 | 126 | -0.000 | 0.953 | 0.942 | 0.051 | 0.000 | 0.000 |
| PPI | 100 | 126 | 0.000 | 0.946 | 0.933 | 0.045 | 0.000 | 0.000 |
| PPI | 150 | 126 | -0.000 | 0.953 | 0.937 | 0.036 | 0.000 | 0.000 |
| PPI | 200 | 126 | -0.000 | 0.946 | 0.929 | 0.031 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.001 | 0.933 | 0.933 | 0.373 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.002 | 0.937 | 0.936 | 0.232 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.933 | 0.929 | 0.156 | 0.000 | 0.000 |
| klasik | 30 | 126 | 0.000 | 0.946 | 0.946 | 0.127 | 0.000 | 0.000 |
| klasik | 40 | 126 | -0.002 | 0.946 | 0.944 | 0.108 | 0.000 | 0.000 |
| klasik | 50 | 126 | -0.001 | 0.938 | 0.936 | 0.096 | 0.000 | 0.000 |
| klasik | 75 | 126 | 0.000 | 0.945 | 0.945 | 0.079 | 0.000 | 0.000 |
| klasik | 100 | 126 | 0.000 | 0.946 | 0.945 | 0.068 | 0.000 | 0.000 |
| klasik | 150 | 126 | -0.000 | 0.938 | 0.938 | 0.056 | 0.000 | 0.000 |
| klasik | 200 | 126 | 0.000 | 0.941 | 0.941 | 0.048 | 0.000 | 0.000 |

### Superpopulasi, varian satu dokter acak sebagai kebenaran: anggaran label (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai sampai m = 200)

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| PPI | 126 | 30.000 | 50 |
| klasik | 126 | 50.000 | 50 |

### Superpopulasi, varian Not Supported saja: ringkasan atas 126 setelan (1000 ambilan dengan pengembalian per m)

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| PPI | 5 | 126 | -0.000 | 0.937 | 0.913 | 0.245 | 0.160 | 0.000 |
| PPI | 10 | 126 | -0.001 | 0.936 | 0.907 | 0.150 | 0.083 | 0.000 |
| PPI | 20 | 126 | -0.000 | 0.942 | 0.918 | 0.103 | 0.020 | 0.000 |
| PPI | 30 | 126 | 0.000 | 0.942 | 0.925 | 0.083 | 0.008 | 0.000 |
| PPI | 40 | 126 | 0.000 | 0.944 | 0.918 | 0.071 | 0.004 | 0.000 |
| PPI | 50 | 126 | 0.000 | 0.946 | 0.931 | 0.063 | 0.002 | 0.000 |
| PPI | 75 | 126 | 0.000 | 0.950 | 0.937 | 0.051 | 0.000 | 0.000 |
| PPI | 100 | 126 | 0.000 | 0.944 | 0.926 | 0.044 | 0.000 | 0.000 |
| PPI | 150 | 126 | -0.001 | 0.945 | 0.931 | 0.036 | 0.000 | 0.000 |
| PPI | 200 | 126 | -0.000 | 0.953 | 0.941 | 0.031 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.002 | 0.932 | 0.932 | 0.182 | 0.040 | 0.000 |
| klasik | 10 | 126 | -0.002 | 0.925 | 0.925 | 0.114 | 0.008 | 0.000 |
| klasik | 20 | 126 | -0.000 | 0.939 | 0.939 | 0.080 | 0.000 | 0.000 |
| klasik | 30 | 126 | 0.001 | 0.954 | 0.949 | 0.065 | 0.000 | 0.000 |
| klasik | 40 | 126 | -0.000 | 0.951 | 0.951 | 0.057 | 0.000 | 0.000 |
| klasik | 50 | 126 | -0.000 | 0.938 | 0.938 | 0.050 | 0.000 | 0.000 |
| klasik | 75 | 126 | 0.000 | 0.953 | 0.950 | 0.041 | 0.000 | 0.000 |
| klasik | 100 | 126 | 0.000 | 0.941 | 0.941 | 0.036 | 0.000 | 0.000 |
| klasik | 150 | 126 | -0.001 | 0.955 | 0.952 | 0.029 | 0.000 | 0.000 |
| klasik | 200 | 126 | 0.000 | 0.950 | 0.949 | 0.025 | 0.000 | 0.000 |

### Superpopulasi, varian Not Supported saja: anggaran label (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai sampai m = 200)

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| PPI | 126 | 30.000 | 50 |
| klasik | 126 | 20.000 | 20 |

### Superpopulasi, varian Not Addressed saja: ringkasan atas 126 setelan (1000 ambilan dengan pengembalian per m)

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| PPI | 5 | 126 | -0.000 | 0.939 | 0.917 | 0.252 | 0.004 | 0.000 |
| PPI | 10 | 126 | -0.000 | 0.933 | 0.913 | 0.152 | 0.000 | 0.000 |
| PPI | 20 | 126 | 0.000 | 0.942 | 0.925 | 0.102 | 0.000 | 0.000 |
| PPI | 30 | 126 | 0.000 | 0.945 | 0.932 | 0.082 | 0.000 | 0.000 |
| PPI | 40 | 126 | -0.000 | 0.943 | 0.920 | 0.070 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.945 | 0.934 | 0.063 | 0.000 | 0.000 |
| PPI | 75 | 126 | -0.000 | 0.948 | 0.937 | 0.051 | 0.000 | 0.000 |
| PPI | 100 | 126 | -0.000 | 0.941 | 0.927 | 0.044 | 0.000 | 0.000 |
| PPI | 150 | 126 | 0.001 | 0.949 | 0.940 | 0.036 | 0.000 | 0.000 |
| PPI | 200 | 126 | 0.000 | 0.951 | 0.935 | 0.031 | 0.000 | 0.000 |
| klasik | 5 | 126 | 0.000 | 0.924 | 0.921 | 0.340 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.000 | 0.925 | 0.923 | 0.212 | 0.000 | 0.000 |
| klasik | 20 | 126 | 0.000 | 0.926 | 0.920 | 0.143 | 0.000 | 0.000 |
| klasik | 30 | 126 | 0.000 | 0.940 | 0.937 | 0.116 | 0.000 | 0.000 |
| klasik | 40 | 126 | -0.001 | 0.940 | 0.937 | 0.098 | 0.000 | 0.000 |
| klasik | 50 | 126 | -0.001 | 0.938 | 0.936 | 0.088 | 0.000 | 0.000 |
| klasik | 75 | 126 | 0.000 | 0.943 | 0.943 | 0.072 | 0.000 | 0.000 |
| klasik | 100 | 126 | -0.000 | 0.941 | 0.936 | 0.062 | 0.000 | 0.000 |
| klasik | 150 | 126 | 0.001 | 0.949 | 0.949 | 0.051 | 0.000 | 0.000 |
| klasik | 200 | 126 | 0.000 | 0.945 | 0.945 | 0.044 | 0.000 | 0.000 |

### Superpopulasi, varian Not Addressed saja: anggaran label (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai sampai m = 200)

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| PPI | 126 | 30.000 | 40 |
| klasik | 126 | 40.000 | 40 |

### Superpopulasi, varian kalimat BHC LLM (tingkat LLM, bukan Δ): ringkasan atas 126 setelan (1000 ambilan dengan pengembalian per m)

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| PPI | 5 | 126 | 0.003 | 0.922 | 0.854 | 0.278 | 0.275 | 0.000 |
| PPI | 10 | 126 | 0.001 | 0.936 | 0.903 | 0.168 | 0.213 | 0.000 |
| PPI | 20 | 126 | 0.000 | 0.940 | 0.916 | 0.112 | 0.141 | 0.000 |
| PPI | 30 | 126 | 0.000 | 0.941 | 0.911 | 0.090 | 0.081 | 0.000 |
| PPI | 40 | 126 | 0.000 | 0.950 | 0.925 | 0.078 | 0.054 | 0.000 |
| PPI | 50 | 126 | 0.000 | 0.946 | 0.925 | 0.069 | 0.036 | 0.000 |
| PPI | 75 | 126 | 0.000 | 0.950 | 0.924 | 0.056 | 0.010 | 0.000 |
| PPI | 100 | 126 | -0.000 | 0.947 | 0.933 | 0.049 | 0.005 | 0.000 |
| PPI | 150 | 126 | -0.000 | 0.949 | 0.935 | 0.040 | 0.002 | 0.000 |
| PPI | 200 | 126 | 0.000 | 0.952 | 0.940 | 0.034 | 0.000 | 0.000 |
| klasik | 5 | 126 | 0.002 | 0.909 | 0.909 | 0.165 | 0.082 | 0.000 |
| klasik | 10 | 126 | 0.000 | 0.923 | 0.923 | 0.098 | 0.013 | 0.000 |
| klasik | 20 | 126 | 0.000 | 0.940 | 0.940 | 0.065 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.000 | 0.934 | 0.934 | 0.052 | 0.000 | 0.000 |
| klasik | 40 | 126 | 0.000 | 0.957 | 0.957 | 0.045 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.945 | 0.945 | 0.040 | 0.000 | 0.000 |
| klasik | 75 | 126 | 0.000 | 0.952 | 0.952 | 0.032 | 0.000 | 0.000 |
| klasik | 100 | 126 | -0.000 | 0.952 | 0.952 | 0.028 | 0.000 | 0.000 |
| klasik | 150 | 126 | 0.000 | 0.939 | 0.939 | 0.023 | 0.000 | 0.000 |
| klasik | 200 | 126 | -0.000 | 0.951 | 0.951 | 0.020 | 0.000 | 0.000 |

### Superpopulasi, varian kalimat BHC LLM (tingkat LLM, bukan Δ): anggaran label (cakupan >= 0,93, lebar <= 0,10; inf = tak tercapai sampai m = 200)

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| PPI | 126 | 30.000 | 75 |
| klasik | 126 | 20.000 | 20 |

### Sebaran klaim unverified (label akhir dokter) atas pasien, per sumber

| sumber | pasien | pasien_dengan_unverified | unverified_total | median_per_pasien | maks_per_pasien | bagian_5_pasien_teratas |
|---|---|---|---|---|---|---|
| human | 100 | 99 | 1869 | 14 | 68 | 0.162 |
| llm | 100 | 66 | 173 | <11 | 14 | 0.231 |
