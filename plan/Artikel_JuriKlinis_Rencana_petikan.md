# Analysis plan (excerpt)

Sections A (decisions locked before results), C (data rules) and I–K (analyses added after internal review rounds,
each recorded here before it was run) of the authors' working plan, in Indonesian. Sections on journal choice,
manuscript outline and work steps are omitted, and sentences describing the internal review rounds were shortened.
File names `Hasil_JuriKlinis_N.md` refer to `analysis/`.

## A. Keputusan (disetujui 20 Nov 2026)

**Keputusan pengguna 20 Nov 2026 ("approve all ★"), dikunci sebelum hasil apa pun dilihat:**
1. Cakupan: ketiga pertanyaan — bias perbandingan naif, penaksir yang cakupannya sah, anggaran label.
2. Data: VeriFact-BHC saja. ann-pt-summ ditunda ke revisi.
3. Label: biner utama (Supported lawan bukan); tiga label sebagai kepekaan.
4. Jenis proposisi: klaim atomik utama (9095); kalimat (3975) sebagai kepekaan.
5. Juri: semua 54 konfigurasi di suplemen; teks utama membandingkan 8B lawan 70B dalam keluarga yang sama.
6. Penaksir: keenamnya — naif, Rogan–Gladen bersama, Rogan–Gladen per sumber, PPI, PPI++, PPI++ berstrata menurut
   sumber.
7. Kebenaran: label konsensus akhir dokter; satu dokter acak sebagai kepekaan. Bootstrap dan pengambilan label per
   pasien.
8. Juri lokal baru (tahap 2) hanya bila tahap 1 menunjukkan bias nyata.

**Penyesuaian dari skema data, disetujui pengguna 20 Nov ("ok"), sebelum hasil apa pun** (`Hasil_JuriKlinis_0.md`):
- 4a. Kalimat BHC dokter (2977) tidak punya vonis juri. Δ dokter lawan LLM hanya pada klaim atomik dan hanya pada
  konfigurasi juri yang menilai kedua sumber; kepekaan kalimat hanya untuk tingkat per sumber LLM.
- 9. Proposisi `invalid` (456) tetap dihitung di analisis utama (seperti NEJM AI); dikeluarkan sebagai kepekaan.

**Aturan henti (dikunci):** bila bias perbandingan naif kecil — CI bias memuat 0 pada sebagian besar juri — naskah
menjadi catatan pendek "perbandingan naif aman di sini", dan slot metode AI pindah ke topik lain. Ambang dikunci
pengguna 21 Nov 2026 ("go"), sesudah `Hasil_JuriKlinis_0.md` (hanya struktur dan kebenaran, belum ada vonis juri
lawan dokter) dan sebelum skrip tahap 1 dijalankan:
- bias = Δ naif (vonis juri) − Δ sebenarnya (`human_gt`), biner, klaim atomik, semua proposisi, pada klaim yang
  divonis setelan itu;
- bias kecil: |bias| < 0,02 **dan** selang bootstrap persentil 95 % (2000 kali ambil ulang pasien) memuat 0;
- sebagian besar: ≥ 2/3 setelan juri yang menilai kedua sumber, yaitu ≥ 84 dari 126;
- keduanya terpenuhi → berhenti (catatan pendek); selain itu lanjut ke penaksir terkoreksi dan anggaran label.
- Dicatat sebelum hasil: dengan Δ sebenarnya 0,281, tanda terbalik kemungkinan jarang; bobot naskah lalu pada besar
  bias, cakupan selang, dan anggaran label.
- Hasil tahap 1 (`Hasil_JuriKlinis_1.md`): 38 dari 126 → LANJUT.

**Rancangan simulasi anggaran label (dikunci pengguna 21 Nov 2026, "Ok", sebelum simulasi dijalankan):**
- Unit label: m pasien diambil acak tanpa pengembalian dari 100; kedua BHC mereka diberi label dokter, sisanya hanya
  vonis juri. m = 5, 10, 20, 30, 50. 1000 ambilan per m, sama untuk semua setelan juri.
- Penaksir: keenam penaksir butir 6; selang 95 % dengan pasien sebagai klaster, tanpa bootstrap di dalam ambilan.
- Sasaran: Δ sebenarnya atas 100 pasien (pada klaim yang divonis setelan itu).
- Metrik: bias, cakupan, lebar selang, tanda terbalik; m terkecil dengan cakupan ≥ 0,93 dan lebar ≤ 0,10.
- Juri: 126 setelan di suplemen; teks utama Llama-8B, Llama-70B, R1-8B, R1-70B (median dan rentang atas 14 setelan).
- Rincian yang ditetapkan saat menulis skrip, sebelum dijalankan: vonis juri ada untuk semua pasien, jadi suku juri
  adalah sensus dan varians memakai koreksi populasi hingga (1 − m/100); kuantil t dengan m − 1 derajat bebas;
  λ PPI++ dipotong ke [0, 1] (bersama = satu λ untuk Δ, berstrata = λ per sumber); Rogan–Gladen gagal bila
  sensitivitas tak terdefinisi atau sens + spek − 1 ≤ 0, dan ambilan gagal dihitung tidak mencakup; pembanding
  "klasik" (label dokter saja, tanpa juri) ditambahkan sebagai rujukan anggaran label, bukan penaksir ketujuh;
  selang naif memakai varians klaster atas 100 pasien tanpa koreksi populasi.

**Pertanyaan.** Bila juri LLM lokal kecil menaksir bagian klaim yang tidak didukung rekam medis pada ringkasan
perawatan (Brief Hospital Course, BHC) tulisan dokter lawan tulisan LLM, (1) seberapa bias perbandingan naif yang
hanya memakai vonis juri, dan seberapa sering tandanya terbalik; (2) penaksir mana (koreksi sensitivitas/spesifisitas
bersama atau per sumber, PPI, PPI++, PPI++ berstrata menurut sumber) memberi selang kepercayaan yang cakupannya benar;
(3) berapa label dokter per sumber yang dibutuhkan untuk lebar selang tertentu?

**Mengapa bisa diuji di sini, tidak di makalah lain.** VeriFact-BHC merilis label dokter untuk *semua* proposisi
(tiga dokter per proposisi + adjudikasi) dan vonis 54 konfigurasi juri. Jadi kebenaran penuh diketahui: anggaran label
bisa disimulasikan dengan mengambil n proposisi berlabel per sumber, sisanya divonis juri, lalu cakupan selang diukur
terhadap selisih sebenarnya. Fiedler 2026 hanya bisa melakukannya pada MMLU-Pro.

**Sumbangan dalam satu kalimat (dikunci pengguna 21 Nov 2026, pilihan A, dari `Hasil_JuriKlinis_1..3.md`):**
"Correcting LLM-judge error rates with one shared adjustment for both sources (doctor-written and LLM-written text) is
dangerous. Prediction-powered inference (PPI) gives valid intervals with about 20 doctor-labelled patients instead of
50, but the saving depends on how informative the judge is; there is none for rare or weakly detected errors."
Judul, abstrak, pendahuluan, dan simpulan naskah mengikuti kalimat ini. Bentuk lama yang dituju (bias/terbalik, PPI
berstrata) tidak dipakai: tanda tak pernah terbalik, dan PPI++ berstrata kurang cakupan pada m kecil.

**Pendahulu terdekat (bacaan 20 Nov lewat agen; ⬜ = belum teks penuh):**
- VeriFact (Chung dkk., NEJM AI 2026, doi 10.1056/AIdbp2500418; teks utama dibaca penuh, lampiran ⬜). Analisis
  utama hanya BHC tulisan LLM; juri terbaik 93,2 % sepakat tetapi MCC 0,31; kinerja pada BHC dokter "significantly
  decreased" (lampiran). Tabel 1: kesepakatan antar-dokter BHC dokter 73,3 % lawan LLM 88,5 % (klaim atomik). Mereka
  mengusulkan persentase "supported" dari juri sebagai ambang kendali mutu, tanpa koreksi dan tanpa CI tingkat per
  sumber. Perancu dari arXiv v1: pipa LLM "aggressively compresses the BHC" (median 164 lawan 334 kata). Rincian:
  `Kebaruan_JuriKlinis_2026-11-20.md`.
- Pakull dkk., npj Digit Med 2026 (teks penuh dibaca): semua juri terbuka condong ke teks LLM; tanpa koreksi.
- Fiedler 2026, *Bias and Uncertainty in LLM-as-a-Judge Estimation* (arXiv 2605.06939; §1–6.2 dibaca): kalibrasi juri
  bersama lintas model "can introduce severe bias, including cases where the comparison estimate points in the wrong
  direction"; PPI++ memulihkan tanda pada MMLU-Pro biologi. Batasan: soal MMLU-Pro saja, keluaran biner, hasil
  "finite-sample and benchmark-specific" (⬜ §8 ringkasan).
- PrecepTron (arXiv 2609.12822), preferensi diri juri medis (arXiv 2611.18616), MedVAL (arXiv 2507.03152) — ⬜ abstrak.

**Rancangan (draf).**
- Data utama: MIMIC-III-Ext-VeriFact-BHC v1.1.0 (PhysioNet, 27 Agu 2026; 100 pasien, tiap pasien punya BHC dokter
  dan BHC LLM; 13.070 proposisi = 8625 dokter + 4445 LLM, 9095 atomik + 3975 kalimat menurut NEJM AI; 13.290 di arXiv
  v1 adalah versi lama). Berkas: `human_verdicts` (label tiap dokter, adjudikasi, kebenaran
  akhir), `verifact_verdicts`/`verdicts.parquet` (54 konfigurasi, juri Gemma 3 12B/27B, Qwen 3 30B-A3B/32B,
  R1-Distill-Llama 8B/70B, Llama 3.1 8B/70B), `experiment_matrix.csv`, `reference_payloads.parquet` (konteks rekam
  medis yang diambil).
- Data kedua (uji generalisasi, bukan lengan ketiga): ann-pt-summ v1.0.1 (Hegselmann; 100 ringkasan dokter + 100 LLM,
  rentang "unsupported") ⬜ cek bentuk labelnya cocok.
- Estimand: tingkat proposisi tak didukung per sumber (dokter, LLM) dan selisihnya Δ. Biner utama
  (Supported lawan bukan); tiga label sebagai kepekaan.
- Penaksir: naif (vonis juri), Rogan–Gladen sensitivitas/spesifisitas bersama, Rogan–Gladen per sumber, PPI, PPI++,
  PPI++ berstrata menurut sumber.
- Unit: proposisi bersarang di pasien dan BHC → anggaran label dan bootstrap diambil per pasien, bukan per proposisi.
  Perancu panjang BHC: stratifikasi menurut jenis proposisi (atomik/kalimat); perbandingan berpasangan dalam pasien
  (kedua sumber ada untuk tiap pasien — NEJM AI).
- Metrik: bias, cakupan nominal 95 %, lebar selang, frekuensi tanda terbalik, label minimum untuk lebar w — per juri,
  dibandingkan antara juri kecil (8B) dan besar (70B).
- Tahap 1 tanpa LLM: hanya vonis terbit. Tahap 2 opsional: juri lokal baru (Qwen3-8B, Gemma-3-4B, MedVAL-4B) atas
  `reference_payloads` di RTX 5060 — hanya bila tahap 1 menunjukkan efek dan ada alasan juri baru menambah sesuatu.
- Ketidakpastian kebenaran sendiri: label tiap dokter tersedia → kepekaan dengan kebenaran dari satu dokter acak.

## C. Aturan data (PhysioNet DUA)

- Lisensi PhysioNet Credentialed Health Data 1.5.0 + DUA 1.5.0, turunan MIMIC-III; ⬜ pengguna menandatangani DUA
  VeriFact-BHC (CITI sudah ada). Data di `C:\Data\VeriFact-BHC\` (terenkripsi, di luar repo).
- Asisten tidak membuka berkas data atau teks BHC/proposisi di sesi; skrip lokal hanya mencetak agregat. README dan
  kamus data boleh dibaca bila pengguna mengizinkan.
- Juri tahap 2 hanya lokal (pedoman LLM PhysioNet 24 Sep 2025). Klausul "Llama" di laman dataset berlaku bila keluaran
  dipakai melatih model — rencana ini tidak melatih model.

## I. Analisis pasca-panel (dicatat 21 Nov 2026 sebelum dijalankan; semuanya *post hoc*)

Sesudah telaah internal pertama (21 Nov). Keputusan terkunci bagian A (estimand Δ atas 100 pasien, penaksir, grid m, ambang 0,93/0,10, aturan henti,
varian kepekaan) **tidak diubah**; hasil Hasil_JuriKlinis_1–3 tetap hasil utama. Yang ditambahkan, semuanya disebut
*post hoc* di naskah, ditulis di sini sebelum skripnya dijalankan:

1. **Anggaran tanpa koreksi populasi hingga (kritis panel).** Simulasi tahap 2 diulang, ambilan sama, selang tanpa
   faktor 1 − m/100: lebar yang didapat tim yang melabel m dari N ≫ m pasien. Dicetak juga rasio varians PPI/label
   saja per setelan (penghematan relatif, bebas skala) dan rumus lebar ≈ 2 t √((1 − m/N) σ²/m).
2. **Sensitivitas juri per sumber di dalam tiap jenis galat** (Not Supported, Not Addressed): juri menandai bukan
   Supported; median beda dokter − LLM per model dan banyak setelan dengan dokter > LLM. Menguji apakah asimetri
   sumber hanya efek campuran jenis galat.
3. **Bias batas Rogan–Gladen bersama** (semua 100 pasien berlabel, rumus tertutup dari sensitivitas/spesifisitas
   gabungan) per setelan, dibandingkan dengan bias simulasi m = 20.
4. **Aturan pilot**: label m₀ = 10 pasien; dari pilot taksir σ² per pasien untuk PPI dan label saja; pilih penaksir
   dengan m ramalan lebih kecil; m ramalan = m terkecil di {10, 15, …, 100} dengan lebar ramalan ≤ 0,10 (dengan
   faktor 1 − m/100); lanjutkan label sampai m itu (pilot termasuk); catat cakupan, lebar, m akhir, dan penaksir
   terpilih. Dijalankan pada varian utama, Not Supported saja, dan kalimat LLM.
5. **Varians klaim bebas** (mengabaikan klaster pasien) untuk PPI pada ambilan pasien yang sama: cakupannya, untuk
   menunjukkan perlunya varians tingkat pasien.
6. Dicetak pelengkap: Δ sebenarnya per varian (termasuk satu dokter acak) dan untuk setelan Qwen thinking yang
   kehilangan 74 vonis; galat Monte Carlo cakupan √(0,95 · 0,05 / 1000) = 0,007 dinyatakan di Metode.

Skrip: `juriklinis_pascapanel.py` (butir 1–3, 5–6) dan `juriklinis_pilot.py` (butir 4) → `Hasil_JuriKlinis_4.md`.
Bila butir 1 menggeser anggaran median PPI dari 20, judul dan abstrak memakai angka tanpa koreksi atau rasio, bukan
"20".

## J. Analisis ketahanan (dicatat 21 Nov 2026 sebelum dijalankan; semuanya *post hoc*)

Sesudah telaah internal ketiga (21 Nov), naskah dibangun di sekitar satu temuan terapan (seberapa jauh
perbandingan juri saja meleset, per juri dan konfigurasi temu-kembali), PPI per sumber satu-satunya rekomendasi,
perbandingan penaksir lain ke suplemen. Keputusan bagian A tetap. Dua analisis baru, ditulis sebelum dijalankan:

1. **Selang ketidakpastian asimetri.** Per setelan, beda sensitivitas (dokter − LLM) dan beda spesifisitas
   (dokter − LLM) dengan selang bootstrap persentil 95 % atas pasien (2000 ulangan, benih dan bobot tahap 1). Dicetak
   per model: median beda, banyak setelan yang selang beda sensitivitasnya di atas 0, dan yang selang beda
   spesifisitasnya di bawah 0.
2. **Asimetri pada label rujukan yang bulat.** Hanya klaim yang ketiga label putaran pertamanya sama (`verdict1` =
   `verdict2` = `verdict3`, tak kosong). Dicetak banyak klaim tersisa per sumber dan bagian unverified-nya, lalu per
   model median sensitivitas per sumber dan banyak setelan dengan dokter > LLM. Menguji apakah asimetri berasal dari
   label rujukan yang lebih bising pada klaim dokter (kesepakatan 73,3 % lawan 88,5 %).

Butir pelengkap tanpa data baru: bias juri saja per setelan menurut model dan konfigurasi (`fact_type`, `top_n`)
dari tabel per setelan `Hasil_JuriKlinis_1.md`, untuk gambar temuan terapan. Skrip: `juriklinis_ketahanan.py` →
`Hasil_JuriKlinis_5.md`. Bila butir 1 atau 2 melemahkan asimetri (sebagian besar selang memuat 0, atau dokter > LLM
tidak lagi pada mayoritas setelan), naskah menyatakannya dan klaim asimetri diturunkan.

## K. Simulasi superpopulasi (dicatat 21 Nov 2026 sebelum dijalankan; *post hoc*)

Isu dari telaah internal keempat: lebar 0,092 dan anggaran 20 pasien memakai koreksi populasi hingga
atas 100 pasien, padahal tim yang mengaudit alat yang berjalan mengambil sedikit pasien dari banyak. Pengguna memilih
opsi (a) 21 Nov: tambah simulasi superpopulasi. Keputusan bagian A tetap; analisis ini tidak menggantikan tahap 2,
tetapi menjadi sumber utama angka anggaran dan lebar di naskah (Abstrak, Tabel 2), apa pun hasilnya. Hasil tahap 2
dengan koreksi populasi hingga dilaporkan sebagai kasus audit tetap atas 100 pasien ini.

1. **Rancangan.** 100 pasien dianggap sebaran empiris dari populasi tak hingga: m pasien diambil **dengan
   pengembalian** (bobot multinomial; pasien terambil dua kali dihitung dua klaster), m ∈ {5, 10, 20, 30, 40, 50,
   75, 100, 150, 200}, 1000 ambilan per m, benih 20261124, ambilan sama untuk semua setelan. Sasaran: Δ atas 100
   pasien (= Δ superpopulasi sebaran empiris). Suku juri: tingkat juri atas 100 pasien (juri menilai seluruh
   populasi). Selang: varians pengaruh per pasien tanpa koreksi populasi hingga, kuantil t pada m − 1 derajat bebas.
   Anggaran: m terkecil pada kisi dengan cakupan ≥ 0,93 dan lebar rata-rata ≤ 0,10 (kriteria tahap 2).
2. **Penaksir dan varian.** Analisis utama: keenam penaksir. Varian kepekaan (satu dokter acak, benih 20261123; Not
   Supported saja; Not Addressed saja, juri memakai label yang sama; kalimat BHC LLM, tingkat LLM saja): label saja
   dan PPI.
3. **Sebaran klaim unverified LLM atas pasien** (pertanyaan devil's advocate dan methods): banyak pasien dengan ≥ 1
   klaim unverified LLM, median dan maksimum per pasien, dan bagian yang disumbang lima pasien teratas; sel 1–10
   disamarkan.
4. **Galat tingkat per sumber juri saja** (editor X3; tanpa data baru): dari tabel per setelan
   `Hasil_JuriKlinis_1.md`, q − p per sumber: median, rentang, banyak setelan dengan |q − p| ≥ 0,05, dan rasio
   q_llm / p_llm. Dicatat sebelum dihitung; dicetak ke `Hasil_JuriKlinis_6.md`.

Skrip: `juriklinis_superpopulasi.py` → `Hasil_JuriKlinis_6.md`. Bila PPI tak mencapai anggaran sampai m = 200,
naskah menyatakan bahwa juri tidak mengurangi tinjauan sampai lebar 0,10 untuk tim yang mengaudit dari populasi besar,
dan rekomendasi menyebut lebar yang tercapai pada m yang wajar, bukan anggaran.
