# Hasil JuriKlinis 3 — kepekaan simulasi anggaran label

Sumber angka: `juriklinis_kepekaan.py` (venv-gpu, 21 Nov 2026; dokter acak benih 20261123; simulasi dan ambilan
pasien sama dengan `juriklinis_tahap2.py`, benih 20261122) atas `C:\Data\VeriFact-BHC\`. Varian kepekaan sudah
ditetapkan di rencana bagian A (butir 3, 4, 4a, 7, 9) sebelum hasil apa pun. Varian "utama" mengulang
`Hasil_JuriKlinis_2.md` dan angkanya sama. Tabel silang label dokter acak memakai penyamaran sel 1–10 ("<11").
Hanya agregat atas setelan juri.

Catatan baca: "anggaran" di bawah adalah median atas semua 126 setelan (bukan per model seperti di Hasil 2), jadi
PPI++ bersama utama tercatat 30, bukan 20–30 per model. Pada varian kalimat LLM sasarannya tingkat LLM (≈0,05),
bukan Δ, sehingga kolom "terbalik" berarti taksiran ≤ 0 dan lebar ≤ 0,10 adalah syarat yang longgar.

## Ringkasan per varian (median atas 126 setelan)

| Varian | Δ naif: bias | RG bersama: bias (m = 20) | PPI: cakupan median (min), m = 5–50 | m anggaran: klasik / PPI / PPI++ berstrata |
|---|---|---|---|---|
| utama | −0,040 | +0,171 | 0,940–0,948 (0,901) | 50 / 20 / 30 (117 dari 126 tercapai) |
| tanpa `invalid` | −0,038 | +0,171 | 0,942–0,948 (0,905) | 50 / 20 / 30 (117) |
| satu dokter acak | −0,018 | +0,252 | 0,936–0,945 (0,898) | 50 / 20 / 30 (87) |
| Not Supported saja | **+0,065** | +0,403 | 0,937–0,948 (0,913) | **20 / 20 / 50** (114) |
| Not Addressed saja | **−0,102** | +0,119 | 0,933–0,957 (0,917) | 30 / 20 / 20 (126) |
| kalimat LLM (tingkat) | +0,061 | gagal (sens tak terdefinisi pada sebagian setelan) | 0,927–0,947 (0,864) | **10 / 30 / 30** |

## Pengamatan (dicatat sesudah hasil; bahan rencana, belum klaim naskah)

1. **Yang bertahan di semua varian Δ:** RG bersama selalu bias besar ke atas (+0,12 sampai +0,40) dan cakupannya 0
   dari m = 20; PPI tak bias dengan cakupan median ≥ 0,933 dan minimum ≥ 0,898; PPI++ kurang cakupan pada m = 5
   (median 0,870–0,911). Mengeluarkan proposisi `invalid` hampir tidak mengubah apa pun.
2. **Dokter acak sebagai kebenaran:** bias naif mengecil ke −0,018, tetapi RG bersama memburuk ke +0,25. Satu
   dokter acak menandai lebih banyak klaim LLM bukan Supported daripada konsensus (tabel silang di bawah). PPI tetap butuh 20 pasien. Pilihan kebenaran (konsensus lawan satu
   dokter) mengubah besar bias naif sampai dua kali lipat.
3. **Tiga label:** arah bias naif berbalik antar-kategori — juri melebihkan selisih Not Supported (+0,065) dan
   mengecilkan selisih Not Addressed (−0,102); bias biner −0,040 menggabungkan dua galat berlawanan. Dugaan yang
   belum diperiksa (butuh matriks kebingungan juri per sumber): juri menukar Not Addressed dengan Not Supported.
4. **PPI tidak selalu menghemat label.** Untuk Not Supported saja, klasik sudah cukup dengan 20 pasien (sama dengan
   PPI); untuk tingkat kalimat LLM (kejadian jarang, sensitivitas juri rendah), klasik butuh 10 pasien dan PPI 30.
   Penghematan label PPI bergantung pada seberapa informatif juri untuk sasaran itu; PPI++ seharusnya melindungi
   kasus ini (λ → 0) tetapi kurang cakupan pada m kecil.
5. RG per sumber tetap tidak praktis: gagal pada sampai 22 % ambilan (dokter acak, m = 50) dan sampai 100 % pada
   setelan yang tidak pernah memberi vonis Not Addressed atau tidak pernah menolak kalimat LLM.

## Keluaran skrip

Disalin utuh dari keluaran `juriklinis_kepekaan.py`.

### Label dokter acak (putaran 1) lawan human_gt, per jenis dan sumber

| proposition_type | author_type | human_gt | dokter_acak | proposisi |
|---|---|---|---|---|
| claim | human | Supported | Supported | 3511 |
| claim | human | Not Addressed | Not Addressed | 996 |
| claim | human | Not Supported | Not Supported | 386 |
| claim | human | Not Addressed | Not Supported | 177 |
| claim | human | Supported | Not Supported | 165 |
| claim | human | Not Supported | Supported | 110 |
| claim | human | Not Addressed | Supported | 107 |
| claim | human | Supported | Not Addressed | 103 |
| claim | human | Not Supported | Not Addressed | 93 |
| claim | llm | Supported | Supported | 3115 |
| claim | llm | Supported | Not Supported | 97 |
| claim | llm | Not Supported | Not Supported | 68 |
| claim | llm | Supported | Not Addressed | 62 |
| claim | llm | Not Addressed | Not Addressed | 40 |
| claim | llm | Not Supported | Supported | 31 |
| claim | llm | Not Addressed | Supported | 22 |
| claim | llm | Not Supported | Not Addressed | <11 |
| claim | llm | Not Addressed | Not Supported | <11 |
| sentence | human | Supported | Supported | 1418 |
| sentence | human | Not Addressed | Not Addressed | 732 |
| sentence | human | Not Supported | Not Supported | 289 |
| sentence | human | Not Addressed | Not Supported | 129 |
| sentence | human | Supported | Not Supported | 117 |
| sentence | human | Not Supported | Not Addressed | 84 |
| sentence | human | Supported | Not Addressed | 82 |
| sentence | human | Not Addressed | Supported | 70 |
| sentence | human | Not Supported | Supported | 56 |
| sentence | llm | Supported | Supported | 892 |
| sentence | llm | Supported | Not Supported | 38 |
| sentence | llm | Not Supported | Not Supported | 17 |
| sentence | llm | Supported | Not Addressed | 17 |
| sentence | llm | Not Addressed | Not Addressed | 12 |
| sentence | llm | Not Supported | Supported | <11 |
| sentence | llm | Not Addressed | Not Supported | <11 |
| sentence | llm | Not Addressed | Supported | <11 |
| sentence | llm | Not Supported | Not Addressed | <11 |

### Varian: utama (klaim, biner, human_gt) — ringkasan atas 126 setelan

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

### Varian: utama (klaim, biner, human_gt) — anggaran label per penaksir

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| klasik | 126 | 50.000 | 50.000 |
| PPI | 126 | 20.000 | 50.000 |
| PPI++ bersama | 126 | 30.000 | 50.000 |
| PPI++ berstrata | 117 | 30.000 | inf |
| RG bersama | 0 | inf | inf |
| RG per sumber | 35 | inf | inf |

### Varian: tanpa proposisi invalid — ringkasan atas 126 setelan

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| naif | 0 | 126 | -0.038 | 0.000 | 0.000 | 0.066 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.003 | 0.915 | 0.915 | 0.375 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.003 | 0.938 | 0.932 | 0.226 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.942 | 0.941 | 0.146 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.000 | 0.948 | 0.948 | 0.110 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.955 | 0.954 | 0.072 | 0.000 | 0.000 |
| PPI | 5 | 126 | -0.001 | 0.942 | 0.905 | 0.242 | 0.000 | 0.000 |
| PPI | 10 | 126 | -0.002 | 0.943 | 0.921 | 0.144 | 0.000 | 0.000 |
| PPI | 20 | 126 | -0.000 | 0.947 | 0.923 | 0.093 | 0.000 | 0.000 |
| PPI | 30 | 126 | -0.000 | 0.948 | 0.931 | 0.070 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.947 | 0.928 | 0.045 | 0.000 | 0.000 |
| PPI++ bersama | 5 | 126 | -0.002 | 0.875 | 0.832 | 0.207 | 0.000 | 0.000 |
| PPI++ bersama | 10 | 126 | -0.003 | 0.913 | 0.892 | 0.132 | 0.000 | 0.000 |
| PPI++ bersama | 20 | 126 | -0.001 | 0.931 | 0.899 | 0.087 | 0.000 | 0.000 |
| PPI++ bersama | 30 | 126 | -0.000 | 0.942 | 0.923 | 0.066 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | -0.000 | 0.941 | 0.918 | 0.044 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.002 | 0.881 | 0.839 | 0.197 | 0.001 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.002 | 0.912 | 0.880 | 0.125 | 0.000 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.000 | 0.929 | 0.903 | 0.082 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.000 | 0.939 | 0.912 | 0.063 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.937 | 0.920 | 0.042 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.189 | 0.212 | 0.001 | 0.287 | 0.000 | 0.001 |
| RG bersama | 10 | 126 | 0.177 | 0.000 | 0.000 | 0.160 | 0.000 | 0.000 |
| RG bersama | 20 | 126 | 0.171 | 0.000 | 0.000 | 0.099 | 0.000 | 0.000 |
| RG bersama | 30 | 126 | 0.170 | 0.000 | 0.000 | 0.074 | 0.000 | 0.000 |
| RG bersama | 50 | 126 | 0.169 | 0.000 | 0.000 | 0.047 | 0.000 | 0.000 |
| RG per sumber | 5 | 126 | -0.010 | 0.874 | 0.344 | 4.649 | 0.183 | 0.636 |
| RG per sumber | 10 | 126 | -0.021 | 0.950 | 0.583 | 1.244 | 0.188 | 0.392 |
| RG per sumber | 20 | 126 | -0.006 | 0.956 | 0.819 | 0.286 | 0.145 | 0.174 |
| RG per sumber | 30 | 126 | -0.005 | 0.954 | 0.868 | 0.193 | 0.167 | 0.119 |
| RG per sumber | 50 | 126 | -0.004 | 0.949 | 0.920 | 0.115 | 0.098 | 0.033 |

### Varian: tanpa proposisi invalid — anggaran label per penaksir

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| klasik | 126 | 50.000 | 50.000 |
| PPI | 126 | 20.000 | 50.000 |
| PPI++ bersama | 125 | 30.000 | inf |
| PPI++ berstrata | 117 | 30.000 | inf |
| RG bersama | 0 | inf | inf |
| RG per sumber | 33 | inf | inf |

### Varian: satu dokter acak sebagai kebenaran — ringkasan atas 126 setelan

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| naif | 0 | 126 | -0.018 | 1.000 | 0.000 | 0.066 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.005 | 0.926 | 0.926 | 0.364 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.002 | 0.934 | 0.930 | 0.219 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.957 | 0.954 | 0.142 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.000 | 0.950 | 0.950 | 0.107 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.951 | 0.947 | 0.069 | 0.000 | 0.000 |
| PPI | 5 | 126 | -0.003 | 0.936 | 0.902 | 0.249 | 0.001 | 0.000 |
| PPI | 10 | 126 | -0.001 | 0.938 | 0.898 | 0.145 | 0.000 | 0.000 |
| PPI | 20 | 126 | 0.000 | 0.945 | 0.926 | 0.093 | 0.000 | 0.000 |
| PPI | 30 | 126 | -0.000 | 0.943 | 0.921 | 0.070 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.945 | 0.925 | 0.045 | 0.000 | 0.000 |
| PPI++ bersama | 5 | 126 | -0.004 | 0.876 | 0.846 | 0.205 | 0.000 | 0.000 |
| PPI++ bersama | 10 | 126 | -0.001 | 0.908 | 0.882 | 0.131 | 0.000 | 0.000 |
| PPI++ bersama | 20 | 126 | -0.000 | 0.931 | 0.909 | 0.086 | 0.000 | 0.000 |
| PPI++ bersama | 30 | 126 | -0.000 | 0.935 | 0.909 | 0.066 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | -0.000 | 0.939 | 0.924 | 0.043 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.004 | 0.877 | 0.850 | 0.195 | 0.001 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.001 | 0.899 | 0.870 | 0.123 | 0.000 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.001 | 0.928 | 0.909 | 0.081 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.000 | 0.926 | 0.902 | 0.062 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.931 | 0.911 | 0.041 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.276 | 0.155 | 0.002 | 0.389 | 0.000 | 0.001 |
| RG bersama | 10 | 126 | 0.260 | 0.000 | 0.000 | 0.217 | 0.000 | 0.000 |
| RG bersama | 20 | 126 | 0.252 | 0.000 | 0.000 | 0.133 | 0.000 | 0.000 |
| RG bersama | 30 | 126 | 0.252 | 0.000 | 0.000 | 0.100 | 0.000 | 0.000 |
| RG bersama | 50 | 126 | 0.250 | 0.000 | 0.000 | 0.064 | 0.000 | 0.000 |
| RG per sumber | 5 | 126 | -0.039 | 0.888 | 0.429 | 16.575 | 0.253 | 0.555 |
| RG per sumber | 10 | 126 | -0.037 | 0.956 | 0.548 | 4.274 | 0.244 | 0.450 |
| RG per sumber | 20 | 126 | -0.008 | 0.961 | 0.671 | 0.396 | 0.229 | 0.329 |
| RG per sumber | 30 | 126 | -0.007 | 0.961 | 0.691 | 0.265 | 0.216 | 0.309 |
| RG per sumber | 50 | 126 | -0.005 | 0.950 | 0.782 | 0.160 | 0.216 | 0.218 |

### Varian: satu dokter acak sebagai kebenaran — anggaran label per penaksir

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| klasik | 126 | 50.000 | 50.000 |
| PPI | 126 | 20.000 | 50.000 |
| PPI++ bersama | 126 | 30.000 | 50.000 |
| PPI++ berstrata | 87 | 30.000 | inf |
| RG bersama | 0 | inf | inf |
| RG per sumber | 1 | inf | inf |

### Varian: Not Supported saja — ringkasan atas 126 setelan

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| naif | 0 | 126 | 0.065 | 0.000 | 0.000 | 0.042 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.002 | 0.924 | 0.924 | 0.181 | 0.040 | 0.000 |
| klasik | 10 | 126 | -0.002 | 0.930 | 0.929 | 0.110 | 0.005 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.933 | 0.927 | 0.073 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.001 | 0.939 | 0.939 | 0.055 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.951 | 0.951 | 0.036 | 0.000 | 0.000 |
| PPI | 5 | 126 | -0.001 | 0.937 | 0.913 | 0.244 | 0.177 | 0.000 |
| PPI | 10 | 126 | -0.001 | 0.937 | 0.915 | 0.145 | 0.073 | 0.000 |
| PPI | 20 | 126 | 0.000 | 0.939 | 0.918 | 0.093 | 0.017 | 0.000 |
| PPI | 30 | 126 | -0.001 | 0.940 | 0.914 | 0.070 | 0.001 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.948 | 0.933 | 0.045 | 0.000 | 0.000 |
| PPI++ bersama | 5 | 126 | -0.001 | 0.872 | 0.842 | 0.147 | 0.043 | 0.000 |
| PPI++ bersama | 10 | 126 | -0.001 | 0.900 | 0.884 | 0.096 | 0.010 | 0.000 |
| PPI++ bersama | 20 | 126 | -0.000 | 0.912 | 0.895 | 0.065 | 0.001 | 0.000 |
| PPI++ bersama | 30 | 126 | -0.000 | 0.928 | 0.912 | 0.050 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | 0.000 | 0.944 | 0.931 | 0.034 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.001 | 0.870 | 0.831 | 0.146 | 0.048 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.000 | 0.899 | 0.874 | 0.094 | 0.012 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.001 | 0.909 | 0.888 | 0.064 | 0.001 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.000 | 0.924 | 0.906 | 0.049 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.937 | 0.924 | 0.033 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.488 | 0.398 | 0.080 | 1.353 | 0.000 | 0.201 |
| RG bersama | 10 | 126 | 0.425 | 0.031 | 0.000 | 0.474 | 0.000 | 0.060 |
| RG bersama | 20 | 126 | 0.403 | 0.000 | 0.000 | 0.271 | 0.000 | 0.007 |
| RG bersama | 30 | 126 | 0.398 | 0.000 | 0.000 | 0.206 | 0.000 | 0.001 |
| RG bersama | 50 | 126 | 0.389 | 0.000 | 0.000 | 0.129 | 0.000 | 0.000 |
| RG per sumber | 5 | 126 | 0.014 | 0.715 | 0.051 | 4.960 | 0.353 | 0.948 |
| RG per sumber | 10 | 126 | -0.009 | 0.896 | 0.174 | 1.362 | 0.365 | 0.826 |
| RG per sumber | 20 | 126 | -0.004 | 0.955 | 0.376 | 0.497 | 0.406 | 0.622 |
| RG per sumber | 30 | 126 | -0.006 | 0.948 | 0.486 | 0.269 | 0.401 | 0.511 |
| RG per sumber | 50 | 126 | -0.004 | 0.950 | 0.730 | 0.150 | 0.319 | 0.265 |

### Varian: Not Supported saja — anggaran label per penaksir

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| klasik | 126 | 20.000 | 30.000 |
| PPI | 126 | 20.000 | 50.000 |
| PPI++ bersama | 126 | 50.000 | 50.000 |
| PPI++ berstrata | 114 | 50.000 | inf |
| RG bersama | 0 | inf | inf |
| RG per sumber | 2 | inf | inf |

### Varian: Not Addressed saja — ringkasan atas 126 setelan

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| naif | 0 | 126 | -0.102 | 0.000 | 0.000 | 0.038 | 0.000 | 0.000 |
| klasik | 5 | 126 | -0.001 | 0.927 | 0.925 | 0.331 | 0.000 | 0.000 |
| klasik | 10 | 126 | -0.001 | 0.917 | 0.916 | 0.200 | 0.000 | 0.000 |
| klasik | 20 | 126 | -0.001 | 0.945 | 0.943 | 0.129 | 0.000 | 0.000 |
| klasik | 30 | 126 | 0.000 | 0.943 | 0.938 | 0.097 | 0.000 | 0.000 |
| klasik | 50 | 126 | 0.000 | 0.959 | 0.959 | 0.063 | 0.000 | 0.000 |
| PPI | 5 | 126 | -0.000 | 0.940 | 0.922 | 0.244 | 0.004 | 0.000 |
| PPI | 10 | 126 | -0.001 | 0.933 | 0.917 | 0.145 | 0.000 | 0.000 |
| PPI | 20 | 126 | -0.000 | 0.945 | 0.924 | 0.092 | 0.000 | 0.000 |
| PPI | 30 | 126 | 0.000 | 0.947 | 0.932 | 0.069 | 0.000 | 0.000 |
| PPI | 50 | 126 | -0.000 | 0.957 | 0.942 | 0.045 | 0.000 | 0.000 |
| PPI++ bersama | 5 | 126 | -0.001 | 0.910 | 0.870 | 0.228 | 0.000 | 0.000 |
| PPI++ bersama | 10 | 126 | -0.001 | 0.915 | 0.895 | 0.142 | 0.000 | 0.000 |
| PPI++ bersama | 20 | 126 | -0.000 | 0.940 | 0.904 | 0.090 | 0.000 | 0.000 |
| PPI++ bersama | 30 | 126 | 0.000 | 0.944 | 0.921 | 0.069 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | -0.000 | 0.955 | 0.936 | 0.045 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | -0.000 | 0.911 | 0.870 | 0.221 | 0.001 | 0.000 |
| PPI++ berstrata | 10 | 126 | -0.001 | 0.915 | 0.887 | 0.137 | 0.000 | 0.000 |
| PPI++ berstrata | 20 | 126 | -0.000 | 0.940 | 0.906 | 0.088 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | 0.000 | 0.946 | 0.927 | 0.067 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | 0.000 | 0.956 | 0.935 | 0.043 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | 0.156 | 0.788 | 0.259 | 0.461 | 0.000 | 0.042 |
| RG bersama | 10 | 126 | 0.129 | 0.390 | 0.004 | 0.234 | 0.000 | 0.004 |
| RG bersama | 20 | 126 | 0.119 | 0.018 | 0.000 | 0.138 | 0.000 | 0.000 |
| RG bersama | 30 | 126 | 0.115 | 0.000 | 0.000 | 0.103 | 0.000 | 0.000 |
| RG bersama | 50 | 126 | 0.112 | 0.000 | 0.000 | 0.066 | 0.000 | 0.000 |
| RG per sumber | 5 | 126 | 0.044 | 0.231 | 0.000 | 0.713 | 0.136 | 1.000 |
| RG per sumber | 10 | 126 | 0.018 | 0.428 | 0.000 | 0.411 | 0.093 | 1.000 |
| RG per sumber | 20 | 126 | 0.009 | 0.685 | 0.000 | 0.324 | 0.107 | 1.000 |
| RG per sumber | 30 | 126 | 0.004 | 0.829 | 0.000 | 0.293 | 0.123 | 1.000 |
| RG per sumber | 50 | 126 | -0.003 | 0.948 | 0.000 | 0.197 | 0.154 | 1.000 |

### Varian: Not Addressed saja — anggaran label per penaksir

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| klasik | 126 | 30.000 | 30.000 |
| PPI | 126 | 20.000 | 30.000 |
| PPI++ bersama | 126 | 20.000 | 50.000 |
| PPI++ berstrata | 126 | 20.000 | 50.000 |
| RG bersama | 0 | inf | inf |
| RG per sumber | 6 | inf | inf |

### Varian: kalimat BHC LLM (tingkat LLM, bukan Δ) — ringkasan atas 126 setelan

| penaksir | banyak_label | setelan | bias_median | cakupan_median | cakupan_min | lebar_median | terbalik_maks | gagal_maks |
|---|---|---|---|---|---|---|---|---|
| naif | 0 | 126 | 0.061 | 0.000 | 0.000 | 0.042 | 1.000 | 0.000 |
| klasik | 5 | 126 | 0.001 | 0.905 | 0.905 | 0.157 | 0.087 | 0.000 |
| klasik | 10 | 126 | 0.000 | 0.934 | 0.934 | 0.093 | 0.004 | 0.000 |
| klasik | 20 | 126 | 0.001 | 0.936 | 0.936 | 0.059 | 0.000 | 0.000 |
| klasik | 30 | 126 | -0.000 | 0.945 | 0.945 | 0.044 | 0.000 | 0.000 |
| klasik | 50 | 126 | -0.000 | 0.950 | 0.950 | 0.028 | 0.000 | 0.000 |
| PPI | 5 | 126 | 0.002 | 0.927 | 0.864 | 0.269 | 0.275 | 0.000 |
| PPI | 10 | 126 | 0.001 | 0.940 | 0.913 | 0.160 | 0.194 | 0.000 |
| PPI | 20 | 126 | 0.001 | 0.941 | 0.914 | 0.102 | 0.116 | 0.000 |
| PPI | 30 | 126 | -0.000 | 0.947 | 0.924 | 0.076 | 0.052 | 0.000 |
| PPI | 50 | 126 | 0.000 | 0.946 | 0.929 | 0.049 | 0.004 | 0.000 |
| PPI++ bersama | 5 | 126 | 0.001 | 0.854 | 0.800 | 0.142 | 0.120 | 0.000 |
| PPI++ bersama | 10 | 126 | 0.001 | 0.913 | 0.878 | 0.089 | 0.008 | 0.000 |
| PPI++ bersama | 20 | 126 | 0.001 | 0.925 | 0.901 | 0.058 | 0.000 | 0.000 |
| PPI++ bersama | 30 | 126 | -0.000 | 0.940 | 0.928 | 0.043 | 0.000 | 0.000 |
| PPI++ bersama | 50 | 126 | -0.000 | 0.946 | 0.929 | 0.028 | 0.000 | 0.000 |
| PPI++ berstrata | 5 | 126 | 0.001 | 0.854 | 0.800 | 0.142 | 0.120 | 0.000 |
| PPI++ berstrata | 10 | 126 | 0.001 | 0.913 | 0.878 | 0.089 | 0.008 | 0.000 |
| PPI++ berstrata | 20 | 126 | 0.001 | 0.925 | 0.901 | 0.058 | 0.000 | 0.000 |
| PPI++ berstrata | 30 | 126 | -0.000 | 0.940 | 0.928 | 0.043 | 0.000 | 0.000 |
| PPI++ berstrata | 50 | 126 | -0.000 | 0.946 | 0.929 | 0.028 | 0.000 | 0.000 |
| RG bersama | 5 | 126 | -0.051 | 0.389 | 0.000 | 5.439 | 0.300 | 1.000 |
| RG bersama | 10 | 126 | -0.039 | 0.579 | 0.000 | 14.515 | 0.356 | 1.000 |
| RG bersama | 20 | 126 | -0.007 | 0.721 | 0.000 | 22.779 | 0.381 | 1.000 |
| RG bersama | 30 | 126 | 0.002 | 0.800 | 0.000 | 23.813 | 0.353 | 1.000 |
| RG bersama | 50 | 126 | 0.008 | 0.927 | 0.000 | 11.786 | 0.380 | 1.000 |
| RG per sumber | 5 | 126 | -0.051 | 0.389 | 0.000 | 5.439 | 0.300 | 1.000 |
| RG per sumber | 10 | 126 | -0.039 | 0.579 | 0.000 | 14.515 | 0.356 | 1.000 |
| RG per sumber | 20 | 126 | -0.007 | 0.721 | 0.000 | 22.779 | 0.381 | 1.000 |
| RG per sumber | 30 | 126 | 0.002 | 0.800 | 0.000 | 23.813 | 0.353 | 1.000 |
| RG per sumber | 50 | 126 | 0.008 | 0.927 | 0.000 | 11.786 | 0.380 | 1.000 |

### Varian: kalimat BHC LLM (tingkat LLM, bukan Δ) — anggaran label per penaksir

| penaksir | setelan_tercapai | m_median | m_maks |
|---|---|---|---|
| klasik | 126 | 10.000 | 10.000 |
| PPI | 125 | 30.000 | inf |
| PPI++ bersama | 126 | 30.000 | 50.000 |
| PPI++ berstrata | 126 | 30.000 | 50.000 |
| RG bersama | 0 | inf | inf |
| RG per sumber | 0 | inf | inf |
