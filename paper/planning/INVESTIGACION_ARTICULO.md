# AlpacaVision AI — Documento Maestro de Investigación v1.0

**Proyecto:** Detección automática de anomalías morfológicas en alpacas del altiplano
**Institución:** Universidad Nacional del Altiplano (UNAP), Puno — E.P. Ingeniería Estadística e Informática
**Semillero:** "John J. Hopfield — IIICCD"
**Revista objetivo:** MDPI *Agriculture* (Q1, IF~3.0, APC~2600 CHF — financiado por UNAP)
**Backup:** MDPI *Animals* (Q1, IF~3.0)
**Idioma:** Inglés
**Antecedente:** 3er lugar CONASEIN 2025, poster/categoría B

---

## 1. Tipo y paradigma de investigación

- **Tipo:** Aplicada / Tecnológica
- **Paradigma:** Cuantitativo, hipotético-deductivo
- **Metodología:** CRISP-DM adaptada a visión computacional
- **Diseño:** Experimental (entrenamiento y evaluación de modelos con datos reales y baselines)

---

## 2. Título

**Título oficial actual:**
"Automatic Detection of Morphological Anomalies in Altiplano Alpacas Using a Multi-Stage
Computer Vision System"

**Alternativas:**
1. "AlpacaVision: A Multi-Stage Deep Learning Pipeline for Morphological Anomaly Detection
   in *Vicugna pacos* from the Peruvian Altiplano"
2. "Precision Livestock Farming in the Andean Altiplano: Deep Learning-Based Morphological
   Anomaly Screening for South American Camelids"

**Running title (≤60 chars):**
"Deep Learning Anomaly Detection in Alpacas, Altiplano"

---

## 3. Objetivo general

Develop and evaluate the first open computer-vision system for early, automated detection
of morphological anomalies in alpacas (*Vicugna pacos*) from the Peruvian Altiplano, including
body detection, ocular anomaly classification, and a deployed web-based diagnostic tool.

---

## 4. Objetivos específicos (uno por sección del paper)

| # | Objetivo | Sección en el paper |
|---|---|---|
| OE1 | Consolidate and curate the first publicly available labeled CV dataset of Peruvian alpacas (detección + crops anatómicos) | §3.1 Dataset |
| OE2 | Train and evaluate a robust alpaca body detector (YOLOv11n) with standard CV metrics (mAP@0.5, P, R) | §3.3 + §4.1 |
| OE3 | Develop a two-stage transfer-learning classifier for ocular anomalies (EfficientNet-B2), evaluated with AUC-ROC + 95% bootstrap CI + McNemar | §3.4 + §4.2 |
| OE4 | Provide Grad-CAM visual interpretability maps to validate model focus on clinically relevant regions | §3.5 + §4.3 |
| OE5 | Deploy an end-to-end web system (Flask) with role-based access and automated veterinary report generation | §3.6 + §4.4 |
| OE6 | Release dataset under Creative Commons and code under MIT on GitHub + Zenodo DOI | §Availability |

---

## 5. Hipótesis

| ID | Hipótesis | Estado | Resultado |
|---|---|---|---|
| H1 | A fine-tuned YOLOv11n detector achieves mAP@0.5 ≥ 0.85 on a held-out test set of Peruvian alpaca images | ✅ Confirmada | mAP@0.5 = **0.913** |
| H2 | Two-stage transfer learning (human fundus → alpaca crops) yields AUC-ROC ≥ 0.80 for ocular anomaly detection | ⏳ Pendiente evaluación honesta | TBD (eval bugfix requerido) |
| H3 | The deployed system provides actionable diagnostic support superior to a majority-class baseline (McNemar p < 0.05) | ⏳ Pendiente | TBD |

---

## 6. Preguntas de investigación

1. Can a compact (nano-scale) YOLO model reliably detect alpaca bodies in varied Andean field conditions?
2. Does pre-training on human fundus images improve ocular anomaly detection in alpacas compared to random initialization?
3. What image regions does the classifier focus on (Grad-CAM), and do they correspond to clinically relevant features?
4. Can an automated web system reduce the time and expertise barrier for morphological screening in remote altiplano communities?

---

## 7. Palabras clave

**Inglés (MDPI Agriculture):**
computer vision; precision livestock farming; *Vicugna pacos*; alpaca; anomaly detection;
YOLOv11; EfficientNet; transfer learning; Grad-CAM; Peruvian Altiplano

**Español (CONASEIN / CONCYTEC):**
visión computacional; ganadería de precisión; vicugna pacos; alpaca; detección de anomalías;
aprendizaje profundo; altiplano peruano

---

## 8. Fuentes de datos

| Dataset | Fuente | Imágenes | Etiquetas | Licencia | Uso |
|---|---|---|---|---|---|
| Roboflow Universe (9 proyectos) | roboflow.com | 3,088 | YOLO 1-clase | CC BY 4.0 | Stage 1 detector |
| iNaturalist (*Vicugna pacos*, Peru) | inaturalist.org | 2,367 | Ninguna | CC BY-NC | Auto-etiquetado Stage 2 |
| Eye Disease (fundus humano) | Kaggle/público | 1,896 (937+959) | anomaly/normal | TBD — verificar | Pre-entrenamiento transfer |
| Crops alpaca ojos | Extraídos del detector | 1,321 (873+448) | Auto-label Groq Vision | Derivado Roboflow+iNat | Fine-tuning clasificador |
| Campo propio (Puno) | Pendiente | TBD | TBD | UNAP | Stage 2 / versión futura |

---

## 9. Pipeline metodológico (CRISP-DM)

```
FASE 1 — Comprensión del negocio
  - Definición de anomalías con asesor (Dr. Aleman Gonzales)
  - Regiones anatómicas prioritarias: ojos y extremidades
  - Limitación identificada: sin dataset CV de alpacas peruanas

FASE 2 — Comprensión de los datos
  → scripts/consolidate_dataset.py
  → src/data/download_roboflow.py + download_inaturalist.py
  Inventario: 9 datasets Roboflow + 2,367 iNaturalist
  Deduplicación: hash MD5
  Análisis de calidad: MIN_BOX_AREA = 0.01 (dataset zehtv excluido)

FASE 3 — Preparación de datos
  → src/data/preprocess.py (CLAHE para alta UV altiplano)
  → src/data/split_dataset.py (70/15/15, semilla=42)
  → scripts/auto_label.py (Grounding DINO SwinT, 2.3 img/s)
  → scripts/extract_crops_from_labels.py (crops anatómicos)
  → scripts/label_crops_with_vision.py (Groq llama-4-scout-17b)

FASE 4 — Modelado
  Stage 1: YOLOv11n — detección cuerpo (1 clase)
    → scripts/run_pipeline.py / src/training/train_detector.py
    → config/train_stage1.yaml (80 epochs, batch 8, AdamW, lr=0.001)
  Clasificador ojos: EfficientNet-B2 (transfer learning 2 etapas)
    → scripts/train_two_stage.py
    → Etapa 1: pre-entrenamiento en eye_disease (fundus humano)
    → Etapa 2: fine-tuning en crops de alpaca (data/crops/eyes/)

FASE 5 — Evaluación
  → scripts/evaluate_stage1.py    → outputs/figures/stage1_eval_report.txt
  → scripts/evaluate_classifiers.py → outputs/figures/classifier_eyes_metrics.json
  → src/evaluation/gradcam.py     → paper/figures/gradcam_examples.png

FASE 6 — Despliegue
  → src/webapp/ (Flask, puerto 5050)
  → Groq llama-3.3-70b-versatile (reporte veterinario automático)
  → Exportación ONNX para producción
```

---

## 10. Estructura del paper (sección → contenido → estado → script)

| Sección | Contenido | Estado | Script/Archivo fuente |
|---|---|---|---|
| Abstract | 200 palabras, resultados al frente: mAP=0.913, AUC-ROC TBD | ⏳ | — |
| 1 Introduction | Contexto Puno 87% alpacas, brecha CV, 4 contribuciones | ⏳ | — |
| 2 Related Work | CV ganado, YOLO veterinaria, EfficientNet diagnóstico, transfer learning | ⏳ | — |
| 3.1 Dataset | Tabla fuentes, dedup MD5, CLAHE, splits, mapa Puno | ⏳ | download_*.py, split_dataset.py |
| 3.2 Region Extraction | Crops desde YOLO boxes, clases anatómicas | ⏳ | extract_crops_from_labels.py |
| 3.3 Detector | YOLOv11n, config, hardware, Grounding DINO auto-label | ⏳ | train_stage1.yaml |
| 3.4 Classifier | EfficientNet-B2, 2-stage transfer, FocalLoss, WeightedSampler | ⏳ | train_two_stage.py |
| 3.5 Eval Protocol | mAP, AUC, bootstrap CI, McNemar, Grad-CAM | ⏳ | evaluate_classifiers.py, metrics.py, gradcam.py |
| 3.6 System | Flask, ONNX, Groq report, auth, roles | ⏳ | src/webapp/ |
| 4.1 Detector Results | Tabla métricas, curvas P/R/F1, matriz confusión | ✅ datos | stage1_eval_report.txt |
| 4.2 Classifier Results | Tabla métricas + CI, ROC + PR, matriz confusión | ⏳ eval bugfix | classifier_eyes_metrics.json |
| 4.3 Grad-CAM | Heatmaps 4 casos (TP/TN/FP/FN) | ⏳ | gradcam.py |
| 4.4 Deployed System | Screenshot webapp, tiempo inferencia, reporte Groq | ⏳ | src/webapp/ |
| 5 Discussion | Comparación literatura, limitaciones (5), impacto socioeconómico | ⏳ | — |
| 6 Conclusions | 5-6 ítems, no resultados nuevos | ⏳ | — |
| Availability | GitHub MIT + Zenodo DOI dataset | ⏳ | — |
| References | ≥40 refs (clásicos + 2020-2026) | ⏳ | references.bib |

---

## 11. Contribuciones científicas principales

1. **Primera base de datos pública CV de alpacas peruanas**: 3,088 imágenes etiquetadas en
   formato YOLO, curadas con deduplicación MD5 y preprocesamiento CLAHE para condiciones
   del altiplano (UV alta, niebla).

2. **Detector robusto de cuerpo de alpaca** (YOLOv11n): mAP@0.5 = 0.913, evaluado en
   466 imágenes de test nunca vistas. Exportado a ONNX para producción.

3. **Clasificador de anomalías oculares con transfer learning de dos etapas**: primera
   aplicación documentada de pre-entrenamiento en fundus humano (*eye_disease*) y fine-tuning
   en crops de alpaca para detección de anomalías oculares en camélidos sudamericanos.

4. **Sistema desplegado end-to-end**: aplicación web Flask con autenticación, gestión de
   rebaño, historial de análisis y reporte veterinario automático en español (Groq LLM), lista
   para prueba en campo.

---

## 12. Resultados clave (para el abstract)

| Componente | Métrica | Valor | IC 95% | Estado |
|---|---|---|---|---|
| Detector YOLOv11n | mAP@0.5 | **0.913** | — | ✅ Confirmado |
| Detector YOLOv11n | mAP@0.5:0.95 | 0.777 | — | ✅ Confirmado |
| Detector YOLOv11n | Precision | 0.934 | — | ✅ Confirmado |
| Detector YOLOv11n | Recall | 0.847 | — | ✅ Confirmado |
| Clasificador ojos | AUC-ROC | TBD | TBD | ⏳ eval bugfix |
| Clasificador ojos | F1 (anomaly) | TBD | TBD | ⏳ eval bugfix |
| Dataset | Imágenes etiquetadas | 3,088 | — | ✅ Confirmado |
| Dataset | Total imágenes | 5,455 | — | ✅ Confirmado |

---

## 13. Limitaciones declaradas en el paper

1. **Baja n de anomalías reales de alpaca**: los 873 crops de anomalía ocular provienen de
   auto-etiquetado (Groq Vision); solo ~77 son verificados manualmente. Sin validación
   veterinaria formal del conjunto de test.
2. **Transferencia cross-especie**: el pre-entrenamiento usa ojos humanos (fundus); la
   relevancia directa a fisiología ocular de alpacas no está validada clínicamente.
3. **Sin datos de extremidades patológicas**: el clasificador de patas no se entrena por
   falta de datos (n=3 anomalías reales); se reporta como trabajo futuro.
4. **Dominio geográfico limitado**: el dataset público de entrenamiento no incluye imágenes
   propias de campo del altiplano; el set de iNaturalist es global no regional.
5. **Ambiente controlado no real**: las predicciones no han sido validadas por veterinarios
   especialistas en camélidos sudamericanos en escenarios de campo real.

---

## 14. Trabajo futuro

1. Colecta de campo en zonas de Azángaro, Melgar, Lampa y Carabaya (≥100 alpacas con y
   sin anomalías) para validar y re-entrenar clasificadores.
2. Entrenamiento de clasificador de extremidades con datos de campo propios.
3. Validación clínica con médicos veterinarios especialistas en camélidos.
4. Extensión a análisis de video (marcha / micro-cojeras): 3D CNN + LSTM.
5. Prueba de concepto en campo: distribución del sistema en comunidades altoandinas.

---

## 15. Estado del proyecto y pasos pendientes

### Pendiente técnico (Fase 1)
- [x] Arreglar `scripts/evaluate_classifiers.py` (bug B0→B2, split honesto)
- [ ] Extender `src/evaluation/metrics.py` (bootstrap CI, McNemar)  ← HECHO
- [ ] Ejecutar evaluación limpia: `python scripts/evaluate_classifiers.py --task eyes`
- [ ] Generar mapas Grad-CAM desde `src/evaluation/gradcam.py`
- [ ] Regenerar figuras del detector: `python scripts/evaluate_stage1.py`

### Pendiente figuras (Fase 2)
- [ ] Crear `paper/figures/generate_figures.py` (5 figuras publicación, 300 DPI)
- [ ] Fig 1: Arquitectura del sistema pipeline
- [ ] Fig 2: Resumen del dataset (multipanel + mapa Puno)
- [ ] Fig 3: Desempeño detector (curvas + matriz confusión)
- [ ] Fig 4: Desempeño clasificador (ROC + PR + IC)
- [ ] Fig 5: Grad-CAM interpretabilidad (TP/TN/FP/FN)

### Pendiente manuscrito (Fase 3)
- [ ] Descargar plantilla LaTeX MDPI Agriculture → `paper/templates/`
- [ ] Escribir `paper/manuscript/manuscript.tex` (secciones 1-6)
- [ ] Escribir `paper/manuscript/references.bib` (≥40 refs)
- [ ] Verificar compilación LaTeX sin errores
- [ ] Revisar límite de páginas MDPI (max 20 pp para Agriculture)

### Pendiente envío (Fase 4)
- [ ] Escribir cover letter: `paper/cover_letter/cover_letter.tex`
- [ ] Preparar dataset para Zenodo (formato ZIP, README, licencia CC BY 4.0)
- [ ] Obtener DOI Zenodo y añadir a referencias
- [ ] Subir código a GitHub (asegurar .env NO trackeado)
- [ ] Registro MDPI + envío por Editorial Manager

---

## 16. Información de la revista objetivo

| Campo | Valor |
|---|---|
| Revista | MDPI *Agriculture* |
| ISSN | 2077-0472 |
| Indexación | Scopus Q1, SCIE |
| IF 2024 | ~3.0 |
| APC | ~2,600 CHF (USD ~2,900) |
| Financiamiento APC | Universidad Nacional del Altiplano (UNAP) |
| Idioma | Inglés |
| Formato | Plantilla LaTeX MDPI (descarga en: mdpi.com/authors/latex) |
| Alcance | Crop/livestock science, precision agriculture, technology in farming |
| Criterio de encaje | "Computer vision and AI for livestock health monitoring and precision farming" |
| Portal de envío | susy.mdpi.com |
| Backup | MDPI *Animals* (Q1, IF~3.0, APC similar) |

---

## 17. Referencias clave (base del .bib)

| Referencia | Por qué es importante |
|---|---|
| Jocher et al. — Ultralytics YOLO (2023) | Citar YOLOv8/v11, base de nuestro detector |
| Tan & Le — EfficientNet (ICML 2019) | Arquitectura del clasificador |
| Liu et al. — Grounding DINO (2023) | Auto-etiquetado zero-shot |
| Selvaraju et al. — Grad-CAM (ICCV 2017) | Interpretabilidad |
| Giraldo et al. — CV livestock (2021) | Revisión general CV ganado |
| Li et al. — DL livestock face (2022) | DL en identificación animal |
| Ali et al. — DL livestock behavior (2023) | Revisión sistemática DL comportamiento |
| Xiao et al. — DL veterinary diagnostics (2025) | Revisión más reciente, usar para gap |
| Ramírez & Condori — mejora genética alpacas (2020) | Contexto regional Puno |
| Smith et al. — cattle lameness detection (2025) | Comparación directa (extremidades) |
| MDPI Animals — canine cataracts DL (2025) | Comparación directa (ojos) |
| Kong et al. — sheep disease detection (2022) | Benchmark de referencia |
| Doğan & Yıldırım — animal ocular CV (2024) | Trabajo más cercano en ojos animales |
| He et al. — deep residual learning (2016) | ResNet, baseline implícito |
| Everingham et al. — VOC challenge (2010) | Definición mAP |
| Lin et al. — focal loss (2017) | FocalLoss que usamos en entrenamiento |
| Kingma & Ba — Adam (2015) | Optimizador base |
| INEI-Peru — estadística alpaquera (2024) | Dato 87% alpacas mundiales en Perú |
| SENASA — sistema pecuario Puno | Contexto ganadería regional |

---

*AlpacaVision AI · Semillero "John J. Hopfield — IIICCD" · UNA Puno · 2025-2026*
*Asesor: Alemán Gonzales, Leonid · Equipo: Vilca Solorzano RA, Ccopa Acero CD, Yana Yucra DM*
