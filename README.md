# llm-judge-source-accuracy

Analysis code, aggregate results and analysis plan for the manuscript *Source-Dependent Accuracy of LLM Judges When
Comparing Physician-Written and LLM-Written Hospital-Course Summaries* (in preparation).

The study uses the published judge verdicts and complete physician labels of MIMIC-III-Ext-VeriFact-BHC v1.1.0: 100
patients, each with a physician-written and an LLM-written brief hospital course, split into atomic claims that three
physicians labelled Supported, Not Supported or Not Addressed by the patient's notes. For 126 judge settings (nine
open-weight models, 14 retrieval configurations each) it measures judge sensitivity and specificity by source, the
error of judge-only rates and of the judge-only physician-minus-LLM difference, and simulates physician review of m
patients to compare labels alone, Rogan–Gladen correction (shared and per source), prediction-powered inference (PPI)
within each source, and PPI++.

**No data from the dataset are included.** The scripts read the release locally and print aggregate tables only;
counts between 1 and 10 are printed as "<11". The dataset is available to credentialed PhysioNet users who sign its
data use agreement: https://doi.org/10.13026/7cqh-bc36. Set `VERIFACT_BHC` (default `data/verifact-bhc`), or pass the
folder as the first argument, to a folder that holds the extracted release with its `SHA256SUMS.txt`. Text columns
(claims, summaries, physician comments, judge explanations) are never loaded.

## Requirements

Python 3.12.10 with NumPy 2.5.4, pandas 2.3.3, SciPy 1.18.1, pyarrow 26.0.0 and matplotlib 3.11.2
(`requirements.txt`). Seeds are set in the scripts. Run from `analysis/` or with it on the path, without `-I`, because
the scripts import each other; set `PYTHONIOENCODING=utf-8` when redirecting output, as the tables contain Δ.

## Layout

- `analysis/` — scripts, the working notes `Hasil_JuriKlinis_0.md` to `Hasil_JuriKlinis_6.md` in which every number
  of the manuscript was recorded with the copied output, and the figures in `Gambar/`. Order of the analyses:
  - `juriklinis_skema.py`, `juriklinis_hitung.py` — data structure and counts (`Hasil_0`);
  - `juriklinis_tahap1.py` — stage 1: judge accuracy by source and judge-only bias (`Hasil_1`);
  - `juriklinis_tahap2.py` — stage 2: review simulation of a fixed audit of the 100 patients, with the
    finite-population correction (`Hasil_2`); estimators in `juriklinis_penaksir.py`, patient-level influence
    variance in `juriklinis_pengaruh.py`;
  - `juriklinis_kepekaan.py` — planned sensitivity analyses (`Hasil_3`);
  - `juriklinis_pascapanel.py`, `juriklinis_pilot.py` — exploratory analyses of plan section I (`Hasil_4`);
  - `juriklinis_ketahanan.py` — exploratory analyses of plan section J (`Hasil_5`);
  - `juriklinis_superpopulasi.py` — exploratory large-population simulation of plan section K, the source of the
    manuscript's review budgets (`Hasil_6`);
  - `juriklinis_gambar.py`, `juriklinis_suplemen.py` — figures and supplementary tables, parsed from the notes;
  - shared: `juriklinis_data.py` (loading), `juriklinis_bootstrap.py`, `juriklinis_markdown.py` (masking and tables).
- `plan/` — an excerpt of the analysis plan (sections A, C, I, J, K).

Comments, notes and the plan are in Indonesian. Glossary: *juri* judge, *setelan* judge setting, *sumber* source
(*dokter* physician, *LLM*), *klaim* atomic claim, *kalimat* sentence, *kebenaran* reference label, *naif* / *juri
saja* judge only, *klasik* / *label saja* labels only, *RG bersama* / *per sumber* Rogan–Gladen shared / per source,
*penaksir* estimator, *cakupan* coverage, *lebar* interval width, *anggaran* review budget, *ambilan* draw, *benih*
seed, *tahap* stage, *kepekaan* sensitivity analysis, *superpopulasi* large population, *pasien berlabel* reviewed
patients, *disamarkan* masked. Working notes refer to internal review rounds and planning files that are not part of
this repository.

## Licence

Code: MIT. Notes, plan and figures: CC BY 4.0. Aggregate results derived from MIMIC-III-Ext-VeriFact-BHC; cite the
dataset and its paper (Chung et al., NEJM AI 2026) when using them.
