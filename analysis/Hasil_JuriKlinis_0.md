# Hasil JuriKlinis 0 — skema dan hitungan dasar VeriFact-BHC v1.1.0

Sumber angka: `juriklinis_skema.py` (venv-gpu, 20 Nov 2026) atas `C:\Data\VeriFact-BHC\` (SHA256SUMS semua OK).
Hanya agregat; nilai kolom teks tidak dicetak (versi pertama skrip skema membocorkan ±14 potongan komentar dokter,
dilaporkan ke pengguna 20 Nov; skrip diperbaiki). Belum ada analisis juri.

## Tabel dan kolom yang dipakai

| Tabel | Baris | Kolom kunci |
|---|---|---|
| `propositions/propositions.csv.gz` | 13.070 | `proposition_id`, `author_type`, `proposition_type`, `subject_id` (100), `hadm_id` (100), `brief_hospital_course` (200 = 100 pasien × 2 sumber) |
| `propositions/human_verdicts.csv.gz` | 13.070 | `verdict1..3` (putaran 1), `round1_num_raters_agree`, `round1_majority_vote`, `verdict4..5` + `round2_decision` (putaran 2), `adjudicated_verdict`, **`human_gt`** (kebenaran akhir) |
| `propositions/proposition_validity.csv.gz` | 13.070 | `invalid` (456 True), `incomplete`, `vague`, dll. |
| `verifact/verdicts.parquet` | 1.437.100 | `model`, `proposition_id`, `rater_alias`, `verdict` |
| `verifact/rater_configurations.csv` | 174 | `rater_alias`, `model`, `fact_type`, `retrieval_method`, `top_n`, `reference_format`, `reference_only_admission` |
| `verifact/experiment_matrix.csv` | 54 | konfigurasi × `author_type` × `proposition_type`; `publication_role` main 42, preliminary 12 |

## Hitungan

- Sumber: dokter 8625, LLM 4445. Jenis: klaim 9095, kalimat 3975 (sama dengan NEJM AI).
- `human_gt`: Supported 9617, Not Addressed 2297, Not Supported 1156 (biner: Supported 9617 lawan bukan 3453).
- Putaran 1: tiga dokter sepakat 8743, dua 3860, tidak ada mayoritas 467. Putaran 2 untuk 467 itu: Agree 236,
  Disagree 231 (= 231 adjudikasi di NEJM AI).
- Bendera ragu per dokter: 624 / 558 / 444 (rater 1/2/3).
- Vonis juri per model: keluarga Llama/R1 (8B, 70B) 182.666 baris tiap model (26 alias); Gemma-3 12B/27B, Qwen-3
  32B dan 30B-A3B-Instruct 141.302 (14 alias); Qwen-3-30B-A3B-Thinking 141.228 (74 baris hilang).
- Sebaran vonis juri seluruhnya: Supported 1.075.771, Not Supported 252.241, Not Addressed 109.088.
- Konfigurasi matriks: 40 untuk BHC LLM, 14 untuk BHC dokter; semua 14 konfigurasi dokter berjenis klaim
  (README: 2977 kalimat dokter tanpa vonis juri).

## Struktur dan kebenaran per sumber (`juriklinis_hitung.py`, 20 Nov)

Kesepakatan juri dengan dokter belum dihitung — menunggu ambang aturan henti dikunci.

| Sumber | Jenis | Proposisi | Pasien | Tidak sah | Per pasien, median (min–maks) | Kebenaran bukan Supported |
|---|---|---|---|---|---|---|
| dokter | klaim | 5648 | 100 | 24 | 48 (8–182) | 1869 (0,331): NA 1280, NS 589 |
| dokter | kalimat | 2977 | 100 | 426 | 24 (7–99) | 1360 (0,457) |
| LLM | klaim | 3447 | 100 | 6 | 28,5 (13–109) | 173 (0,050): NA 66, NS 107 |
| LLM | kalimat | 998 | 100 | 0 | 8 (4–32) | 51 (0,051) |

NA = Not Addressed, NS = Not Supported.

- Δ sebenarnya (klaim, biner, semua proposisi): 0,331 − 0,050 = 0,281. Sebagian besar selisih dokter datang dari Not
  Addressed (fakta di BHC dokter yang tidak ada di catatan EHR — "information asymmetry" di arXiv v1).
- Cakupan juri: tiap model punya 14 alias utama yang menilai klaim **kedua** sumber (fakta klaim top_n 5–150 = 8,
  fakta kalimat top_n 5–100 = 6) → 9 × 14 = 126 setelan juri untuk Δ. Semua lengkap kecuali Qwen-3-30B-A3B-Thinking
  fakta klaim top_n 100 (5574 dari 5648 klaim dokter; 74 hilang).
- Kalimat LLM: 14 alias per model. Alias pendahuluan (12, keluarga Llama/R1) hanya klaim LLM → tidak untuk Δ.

## Akibat untuk rancangan (dicatat sebelum hasil)

1. Perbandingan dokter lawan LLM hanya mungkin pada klaim atomik dan hanya pada konfigurasi juri yang menilai
   kedua sumber. Skrip berikut harus menghitung dulu alias mana yang punya vonis untuk kedua sumber; pilihan ★4
   (kalimat sebagai kepekaan) hanya bisa untuk tingkat per sumber LLM, bukan untuk Δ. Disetujui 20 Nov (rencana 4a).
2. Biner dari `human_gt`; kepekaan "satu dokter acak" memakai `verdict1..3`.
3. `invalid` (456) tetap dihitung di analisis utama, dikeluarkan sebagai kepekaan. Disetujui 20 Nov (rencana 9).
