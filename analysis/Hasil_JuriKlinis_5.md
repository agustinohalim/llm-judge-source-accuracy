# Hasil JuriKlinis 5 — ketahanan asimetri (post hoc, rencana bagian J)

> Dijalankan 21 Nov 2026 dengan `juriklinis_ketahanan.py` atas VeriFact-BHC v1.1.0 di laptop lokal; data tidak dibuka
> di sesi asisten, yang tercetak hanya agregat (sel 1–10 disamarkan). Analisis dicatat di rencana bagian J sebelum
> dijalankan. Bootstrap: 2000 ulangan atas pasien, benih dan bobot tahap 1.

## Ringkasan

- **Butir 1.** Beda sensitivitas dokter − LLM: selang bootstrap pasien 95 % di atas 0 pada **126 dari 126** setelan
  (median beda 0,332; batas bawah terkecil 0,043, Qwen 3 30B-A3B thinking). Beda spesifisitas dokter − LLM: selang di
  bawah 0 pada **126 dari 126** (median −0,083). Asimetri tidak bergantung pada hitungan setelan saja.
- **Butir 2.** Klaim dengan label putaran pertama bulat: 3501 klaim dokter (bagian unverified 0,172) dan 2877 klaim
  LLM (0,014, yakni 41 klaim). Sensitivitas dokter > LLM pada **126 dari 126** setelan; median per model 0,524–0,955
  (dokter) lawan 0,146–0,866 (LLM). Asimetri bertahan pada label rujukan yang paling andal, walau sisi LLM bertumpu
  pada 41 klaim unverified.
- Keputusan bagian J: asimetri tidak melemah; klaim tetap, dengan selang dan batas jumlah klaim disebut.

- **Butir pelengkap (tanpa data baru, dari tabel per setelan Hasil_1).** Bias Δ juri saja |bias| ≥ 0,05 (18 % dari
  Δ = 0,281) pada **52 dari 126** setelan, ≥ 0,10 pada 20; selang bootstrap tak memuat 0 pada 85 (15 di atas, 70 di
  bawah). Per model: Gemma 3 12B (median −0,095), Gemma 3 27B (−0,128), Llama 3.1 8B (−0,093), R1-Distill 8B
  (−0,051) jauh; Llama 3.1 70B (+0,010; juga model pembuat BHC LLM), R1-Distill 70B (+0,004), Qwen 3 32B (−0,013),
  Qwen thinking (+0,013) dekat. Qwen 3 30B-A3B instruct −0,079 sampai +0,174 menurut konfigurasi. Fakta kalimat
  median −0,055 lawan fakta klaim −0,017.

## Log mentah

### Beda sensitivitas dan spesifisitas dokter − LLM per setelan, selang bootstrap pasien 95 %

- Setelan: 126; selang beda sensitivitas di atas 0: 126; selang beda spesifisitas di bawah 0: 126
- Median beda sensitivitas 0.332, batas bawah selang terkecil 0.043; median beda spesifisitas -0.083
| model | setelan | sens_beda_median | sens_bawah_min | sens_selang_di_atas_0 | spek_beda_median | spek_atas_maks | spek_selang_di_bawah_0 |
|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 14 | 0.324 | 0.181 | 14 | -0.056 | -0.027 | 14 |
| Gemma-3-27B | 14 | 0.319 | 0.132 | 14 | -0.034 | -0.007 | 14 |
| Llama-70B | 14 | 0.339 | 0.147 | 14 | -0.117 | -0.057 | 14 |
| Llama-8B | 14 | 0.284 | 0.124 | 14 | -0.087 | -0.002 | 14 |
| Qwen-3-30B-A3B-Instruct | 14 | 0.379 | 0.245 | 14 | -0.080 | -0.005 | 14 |
| Qwen-3-30B-A3B-Thinking | 14 | 0.216 | 0.043 | 14 | -0.103 | -0.012 | 14 |
| Qwen-3-32B | 14 | 0.378 | 0.209 | 14 | -0.094 | -0.023 | 14 |
| R1-70B | 14 | 0.346 | 0.107 | 14 | -0.096 | -0.030 | 14 |
| R1-8B | 14 | 0.324 | 0.164 | 14 | -0.070 | -0.005 | 14 |

### Klaim dengan label putaran pertama bulat (ketiga dokter sama)

| author_type | klaim | unverified | bagian_unverified |
|---|---|---|---|
| human | 3501 | 602 | 0.172 |
| llm | 2877 | 41 | 0.014 |

### Sensitivitas juri per sumber pada klaim bulat (median atas setelan per model)

- Setelan dengan sensitivitas dokter > LLM: 126 dari 126
| model | sens_dokter | sens_llm | dokter_lebih_tinggi |
|---|---|---|---|
| Gemma-3-12B | 0.559 | 0.244 | 14 |
| Gemma-3-27B | 0.524 | 0.146 | 14 |
| Llama-70B | 0.820 | 0.610 | 14 |
| Llama-8B | 0.648 | 0.329 | 14 |
| Qwen-3-30B-A3B-Instruct | 0.747 | 0.427 | 14 |
| Qwen-3-30B-A3B-Thinking | 0.955 | 0.866 | 14 |
| Qwen-3-32B | 0.846 | 0.573 | 14 |
| R1-70B | 0.874 | 0.622 | 14 |
| R1-8B | 0.777 | 0.439 | 14 |

### Bias Δ juri saja menurut model dan konfigurasi temu-kembali (dari tabel per setelan Hasil_JuriKlinis_1)

- Setelan: 126; |bias| >= 0,05: 52; |bias| >= 0,10: 20; selang di atas 0: 15; selang di bawah 0: 70
| model | setelan | bias_median | bias_min | bias_maks | besar | selang_atas_0 | selang_bawah_0 |
|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 14 | -0.095 | -0.144 | -0.029 | 11 | 0 | 14 |
| Gemma-3-27B | 14 | -0.128 | -0.192 | -0.002 | 10 | 0 | 12 |
| Llama-70B | 14 | 0.010 | -0.028 | 0.033 | 0 | 4 | 0 |
| Llama-8B | 14 | -0.093 | -0.148 | -0.016 | 11 | 0 | 12 |
| Qwen-3-30B-A3B-Instruct | 14 | -0.043 | -0.079 | 0.174 | 9 | 4 | 10 |
| Qwen-3-30B-A3B-Thinking | 14 | 0.013 | -0.085 | 0.035 | 2 | 4 | 3 |
| Qwen-3-32B | 14 | -0.013 | -0.055 | 0.006 | 1 | 0 | 3 |
| R1-70B | 14 | 0.004 | -0.051 | 0.022 | 1 | 3 | 2 |
| R1-8B | 14 | -0.051 | -0.098 | -0.042 | 7 | 0 | 14 |

| fact_type | setelan | bias_median | bias_min | bias_maks | besar | selang_atas_0 | selang_bawah_0 |
|---|---|---|---|---|---|---|---|
| claim | 72 | -0.017 | -0.192 | 0.174 | 24 | 14 | 35 |
| sentence | 54 | -0.055 | -0.169 | 0.025 | 28 | 1 | 35 |

