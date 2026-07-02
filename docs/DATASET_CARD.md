# AlpacaVision AI — Curated Alpaca Detection Dataset (v1.0)

**A curated, deduplicated, leakage-free object-detection dataset of Peruvian Altiplano
alpacas (*Vicugna pacos*).**

- **Version:** 1.0
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Format:** YOLO (images + `.txt` bounding-box labels), single class `alpaca`
- **Total:** 2,051 unique images · 1 class · train/val/test = 1,435 / 308 / 308

---

## Summary

This dataset consolidates and curates alpaca imagery from nine public Roboflow Universe
projects into a single, **deduplicated and leakage-free** detection benchmark for the
species. It was produced for the AlpacaVision AI study (Universidad Nacional del Altiplano
de Puno, Perú) and accompanies a manuscript submitted to *MDPI Agriculture*.

A data-integrity audit of the raw consolidation (3,088 image files) found **1,037 exact
byte-level (MD5) duplicates**, 186 of which leaked across the original train/test boundary
and had inflated previously reported detection metrics. This release contains only the
**2,051 unique images**, re-split from scratch at the level of unique source images so that
no duplicate or augmentation of a test image appears in training.

## Contents & structure

```
annotated_clean/
├── images/
│   ├── train/   1,435 images
│   ├── val/       308 images
│   └── test/      308 images
└── labels/
    ├── train/   1,435 YOLO .txt files
    ├── val/       308 YOLO .txt files
    └── test/      308 YOLO .txt files
```

- **Classes:** `0: alpaca` (single class).
- **Label format:** YOLO — one `.txt` per image; each line `class cx cy w h` (normalised).
- **Split:** stratified, fixed seed = 42, performed **after** MD5 deduplication.

## Provenance

Consolidated from nine Roboflow Universe projects (single class `alpaca`, YOLO-format
bounding boxes):
`alpaca-5jmfl`, `alpaca-8baig`, `alpaca-epqna`, `alpaca-gkbmi`, `alpaca-ibscl`,
`alpaca-lls3s`, `alpaca-nrzos`, `alpaca-ofxv9`, `alpaca-xqfiw`.
One project (`alpaca-zehtv`) was excluded after quality screening (mean bounding-box area
ratio < 0.01). Supplementary unlabelled imagery was obtained from iNaturalist
(taxon 319688, *Vicugna pacos*, Peruvian observations).

## Curation & preprocessing

1. **MD5 deduplication** — exact byte-level duplicates removed (1,037 of 3,088 files).
2. **CLAHE** (Contrast-Limited Adaptive Histogram Equalisation) — applied to compensate for
   high ultraviolet irradiance and atmospheric haze typical of Andean altiplano photography.
3. **Leakage-free re-split** — at the level of unique source images (seed = 42).

Methodology and code: `scripts/clean_detector_dataset.py` and `src/data/group_split.py` in
the accompanying repository.

## Benchmark (reference)

A compact YOLOv11n detector (2.58M parameters) trained on this dataset reaches
**mAP@0.5 = 0.860** (Precision = 0.913, Recall = 0.731) on the held-out test set; a larger
YOLOv11s reaches mAP@0.5 = 0.863. These are the leakage-free figures reported in the paper.

## Intended use & limitations

- **Intended use:** body-level alpaca detection/localisation; precision-livestock-farming
  research; transfer-learning source for camelid vision tasks.
- **Limitations:** single class (body only — no anatomical-part or anomaly labels); source
  imagery is globally sourced (not exclusively altiplano biome); not intended for clinical
  diagnosis.

## Citation

> Vilca-Solorzano, R.A.; Ccopa-Acero, C.D.; Yana-Yucra, D.M.; Alemán-Gonzales, L.
> *AlpacaVision AI: A Curated Dataset and Compact Detector for Altiplano Alpacas.*
> Universidad Nacional del Altiplano de Puno, 2026. Dataset, CC BY 4.0.

## Contact

Semillero de Investigación "John J. Hopfield — IIICCD", Escuela Profesional de Ingeniería
Estadística e Informática, Universidad Nacional del Altiplano de Puno (UNAP), Puno, Perú.
Corresponding: Leonid Alemán-Gonzales — laleman@unap.edu.pe
