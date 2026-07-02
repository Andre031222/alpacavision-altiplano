# AlpacaVision AI — Estado del Paper (actualizado 2026-06-28)

## Sesión 2026-06-28 — limpieza, verificación y diagnóstico
- **Limpieza de basura (−7 GB, de 18 GB → 11 GB):** borrado `venv/` de Windows (6.2 GB, rutas `C:\`, inservible en Linux), `__pycache__`, `.pytest_cache`, y checkpoints intermedios `epochN.pt` de `runs/` (los `best.pt` definitivos ya están copiados en `models/`, MD5 verificado). El entorno real es `.venv-linux/`.
- **Seguridad:** se quitaron claves API en texto plano (Groq/Roboflow) y credenciales de `docs/ARRANCAR_SESION.md`. No estaban en el historial de git. Recomendado rotarlas.
- **Verificado funcional:** `.venv-linux` (Python 3.12, torch 2.6+cu124, CUDA OK, ultralytics 8.4.63). Manuscrito compila con `mdpi.cls` real (presente) → `manuscript.pdf` (15 pág.). Números del `.tex` confirmados honestos y consistentes con los JSON de `outputs/figures/`.
- **Diagnóstico:** Paper 1 (detector + dataset + integridad de datos) está **listo para enviar tras revisión humana**. Lo único "por entrenar/modelar" pendiente es el clasificador ocular, que **requiere ground truth veterinario real** (no fabricable) — ver `PLAN_SIGUIENTE_NIVEL.md`, Frente 2, y el protocolo clínico en `docs/CLASIFICACION_OCULAR_VET.md`.

### Mejoras al manuscrito (2026-06-28)
- **Números verificados en vivo:** reproduje el detector con `scripts/eval_detector.py` en esta máquina (RTX 3050): YOLOv11n mAP@0.5=0.8598≈**0.860** (P 0.913, R 0.731) y YOLOv11s **0.863** (P 0.903, R 0.766). Coinciden exactamente con el manuscrito.
- **Correcciones de consistencia:** tabla de crops `448→371` normales (448 era cifra de la era inflada; 371 es lo real y concuerda con las figuras y el split honesto); referencia de config `train_stage1.yaml → train_stage1_clean.yaml` (citaba el config CON fuga).
- **Tabla del detector mejorada:** ahora es ablación **YOLOv11n vs YOLOv11s** con todos los números verificados (n: 2.58M/6.3 GFLOPs; s: 9.43M/21.5 GFLOPs).
- **Compilación arreglada:** faltaba `soul.sty` (lo requiere `mdpi.cls`); vendoré `soul.sty`, `soul-ori.sty`, `soulutf8.sty` en `paper/manuscript/`. **Compila limpio: 15 pág., bibtex OK, 0 refs/citas indefinidas.** PDF regenerado con los cambios.
- **README reescrito** honesto (Linux, sin secretos, números corregidos, alineado al paper).

### Hallazgo de resolución (2026-07-01) — techo físico de los crops
Pre-cribado del lote `batch_01` (462 crops) reveló que los recortes de ojo son **demasiado pequeños** para diagnosticar: **mediana del lado menor ≈31 px** (verificado midiendo los 462 crops), **<8% con lado ≥100 px**, 73% <50 px. Es un techo físico del recorte, independiente del modelo o del etiquetador — **ni un veterinario sacaría anomalías de estas miniaturas**. Añadido al manuscrito como limitación citable (Limitaciones + Discusión + Future Work). El auto-etiquetado Groq marcó 91 "anomaly"; un cribado VLM cuidadoso confirma 1 (acuerdo inter-VLM 60.7%, casi azar) — evidencia extra de la tesis. **Acción correcta = aguas arriba:** re-extraer crops a mayor resolución (lado ≥~128 px) desde `data/raw` ANTES de mandar a un veterinario. Reporte: `docs/PRECRIBADO_IA_batch01.md`. El lote `00_POR_REVISAR/` quedó intacto.

### ⚠️ Para que decida el equipo (no lo resolví yo)
- **Discrepancia de autores:** el manuscrito lista a Vilca-Solorzano R.A., Ccora-Acero C.D., Yana-Yucra D.M., Alemán-Gonzales L. El README viejo listaba otro equipo (Jaguer Ladera, Limachi Quispe, Mares — equipo del póster CONASEIN 2025). Hay que confirmar la autoría definitiva. Dejé el README sin lista de autores (solo asesor) hasta que se confirme.
- Rotar claves Groq/Roboflow y la contraseña de admin/Postgres que estaban en texto plano en README/ARRANCAR_SESION (ya redactadas).

---



## Limpieza y orden del repo (2026-06-17)
Se ordenó la raíz y se eliminó lo redundante (sin tocar git; el equipo commitea aparte):
- **Raíz:** borrados `new.png`, `__pycache__/`, `.pytest_cache/`. Movidos `bases3xpoinvesti.pdf` y este `ESTADO_PAPER.md` a `docs/`.
- **Webapp consolidada:** `src/webapp/` es la única app (entrada `python run_webapp.py`). Borrado el legacy de `src/app/`: `flask_app.py`, `main.py` (FastAPI), `templates/`, `static/`. Conservados `vision_analyzer.py`, `report_generator.py` (los usa la webapp) e `inference.py` (lo usan los tests). `INICIAR.bat` ahora lanza `run_webapp.py`. Quitado `streamlit` de `requirements.txt`.
- **Paper:** borrados `paper/mdpi_acs_extracted/`, `paper/templates/`, los 3 `MDPI_template_*.zip` y `fig5_gradcam_placeholder.*`. Conservados los duplicados internos de `manuscript/` (la compilación los necesita).
- **.gitignore:** ahora ignora `.venv-linux/`, `.pytest_cache/` y artefactos LaTeX (`*.aux/.bbl/.blg/.log/.out`).
- **Conservados (NO eran huérfanos):** `src/data/split_dataset.py` y `src/data/crop_regions.py` (los usa `scripts/run_training.sh`).

## Objetivo
Publicar en **MDPI Agriculture** (Q1, Scopus, APC pagado por UNAP).
Backup: MDPI Animals.

## 🔴 SANEAMIENTO DE INTEGRIDAD DE DATOS (2026-06-17) — los números viejos NO eran válidos

Auditoría que reveló **fuga de datos (data leakage) sistémica** que inflaba ambos modelos:

**Detector:** `data/annotated` tenía 3.088 archivos pero solo **2.051 imágenes únicas** (1.037 duplicados exactos por MD5). Además 186 imágenes idénticas estaban a la vez en train y test (40% del test visto en entrenamiento). → el mAP=0.913 estaba inflado.

**Clasificador de ojos:** dos fugas combinadas:
1. **Conflicto de etiquetas:** 75 de 97 anomalías eran el MISMO archivo (MD5 idéntico) que una "normal" — el script `label_crops_with_vision.py` copiaba en vez de mover. 79% de la clase positiva con etiqueta contradictoria.
2. **Leakage de augmentación:** crops augmentados (`aug_NN_*`) de la misma imagen original caían en train y test (110/197 del test eran augmentados). → el AUC=0.824 estaba inflado.

**Correcciones aplicadas:** dataset del detector deduplicado y re-split honesto (`scripts/clean_detector_dataset.py` → `data/annotated_clean`); split group-aware sin fuga para el clasificador (`src/data/group_split.py`, test/val solo con originales); resolución de los 75 conflictos con Vision doble pasada (`scripts/resolve_label_conflicts.py`); bug del script de etiquetado corregido (ahora mueve).

## Resultados HONESTOS (re-entrenamiento sobre datos saneados, 2026-06-17)

| Modelo | Métrica | Honesto | Antes (inflado) |
|---|---|---|---|
| YOLOv11n detector (test limpio) | mAP@0.5 | **0.860** | 0.913 |
| YOLOv11**s** detector (test, POTENCIADO) | mAP@0.5 | **0.863** | — |
| YOLOv11s detector | mAP@0.5:0.95 | **0.711** | 0.777 (inflado) |
| YOLOv11s detector | Precision / Recall | **0.903 / 0.766** | 0.934 / 0.847 |
| EfficientNet-B2 ojos | AUC-ROC | **0.506** [0.37,0.65] (≈azar) | 0.824 inválido |
| EfficientNet-B2 ojos | F1 anomalía / Accuracy | **0.061 / 0.586** | 0.846 / 0.792 inválido |
| Dataset detector | Imágenes ÚNICAS | **2.051** | "3.088" (con duplicados) |
| Dataset ojos | Anomalías reales | **~81** (tras resolver conflictos) | "97" (75 en conflicto) |

Modelo limpio: `models/detector/best_clean.pt`. Métricas: `outputs/figures/detector_clean_test_metrics.json`.

### ⚠️ Tabla vieja del manuscrito (INVÁLIDA — reemplazar antes de enviar)
mAP=0.913, AUC=0.824, F1=0.846, "3.088 imágenes" — todos inflados por fuga de datos.

## Manuscrito actualizado y compilado (2026-06-18)
- `paper/manuscript/manuscript.tex` **reescrito con números honestos** y reenfocado: detector + dataset + **metodología de integridad de datos** + estudio de viabilidad (clasificador como resultado honesto negativo).
- **Compila limpio: 15 páginas, bibtex OK, sin refs rotas** (se arregló metadata MDPI faltante: `\datereceived/\daterevised/\dateaccepted/\datepublished`).
- Figuras regeneradas con datos honestos: fig3 (detector 0.860), fig4/fig7/fig9 (clasificador AUC 0.506, ROC en diagonal, confusión [[40,16],[13,1]]), fig11 (dataset 2.051/91/371). fig1 y fig6 corregidas. Eliminadas huérfanas fig2, fig5 (gradcam), fig10.
- Título nuevo (provisional, revisar): *"A Curated Dataset and Compact Detector for Altiplano Alpacas, with a Feasibility Study on Automatic Ocular Anomaly Classification"*.
- Scripts nuevos de figuras: `scripts/gen_honest_classifier_figs.py`, `scripts/gen_honest_summary_figs.py`.
- Modelos detector: `best_clean.pt` (n, mAP 0.860, el del manuscrito), `best_clean_s.pt` (s, mAP 0.863). `best.pt` es el viejo con fuga (no usar para el paper).

### Pendiente humano antes de enviar
- Ajustar título y revisar narrativa final.
- **Conseguir ground truth veterinario** (~150-200 anomalías reales) si se quiere un clasificador publicable — ver `PLAN_SIGUIENTE_NIVEL.md`.
- Regenerar fig8 (detecciones YOLO) con el modelo limpio (opcional; visualmente similar).

## Entorno Linux (entrenamiento y evaluacion)

```bash
source .venv-linux/bin/activate

# Re-entrenar clasificador (objetivo: mejorar AUC y recall normal)
# Opcion A: entrenamiento estandar (gamma=2.0)
python scripts/train_two_stage.py

# Opcion B: gamma reducido para mejor recall en clase normal
python scripts/train_two_stage.py --gamma 1.0

# Evaluar (actualiza outputs/figures/classifier_eyes_metrics.json)
python scripts/evaluate_classifiers.py --task eyes

# Generar Fig 5 Grad-CAM (ejecutar DESPUES del evaluador)
python scripts/generate_gradcam_examples.py

# Compilar PDF
cd paper/manuscript
pdflatex preview.tex && bibtex preview && pdflatex preview.tex && pdflatex preview.tex
```

## Archivos clave del paper

| Archivo | Estado | Descripcion |
|---|---|---|
| `paper/manuscript/preview.tex` | **Actualizado** | Fuente LaTeX, citas ampliadas (44 refs), Fig 5 apunta a fig5_gradcam |
| `paper/manuscript/manuscript.tex` | **Actualizado** | Version MDPI (mismos cambios) |
| `paper/manuscript/references.bib` | **44 entradas** | Ampliado de 22 a 44 refs |
| `paper/manuscript/preview.pdf` | PENDIENTE recompilacion | Ultima version: 12 pags con placeholder fig5 |
| `paper/manuscript/manuscript.tex` | PENDIENTE mdpi.cls | Necesita plantilla oficial de mdpi.com |
| `paper/figures/fig5_gradcam.png` | **PENDIENTE** | Ejecutar generate_gradcam_examples.py |
| `paper/figures/fig{1-4}_*.png/pdf` | Listas | Generadas, 300 DPI |
| `paper/cover_letter/cover_letter.tex` | Lista | Carta de presentacion |
| `paper/planning/INVESTIGACION_ARTICULO.md` | Documento maestro | |
| `scripts/generate_gradcam_examples.py` | **NUEVO** | Genera Fig 5 con Grad-CAM real |
| `scripts/train_two_stage.py` | **Actualizado** | Argumento --gamma para mejorar recall normal |
| `outputs/figures/classifier_eyes_metrics.json` | Metricas actuales | AUC=0.819, F1=0.851 |

## Checklist de pendientes (en orden de prioridad)

### Lo que yo (Claude) ya hice:
- [x] Crear `scripts/generate_gradcam_examples.py` (Fig 5 real)
- [x] Ampliar `references.bib`: de 22 a 44 entradas
- [x] Actualizar `preview.tex`: Fig 5 → fig5_gradcam, nuevas citas, eliminar refs con TODO
- [x] Actualizar `manuscript.tex`: mismos cambios para version MDPI
- [x] Agregar `--gamma` a `scripts/train_two_stage.py`
- [x] Actualizar `README.md` con estado real del clasificador
- [x] Actualizar este `ESTADO_PAPER.md`

### Pendiente (requiere Linux + GPU):
- [x] Re-entrenar clasificador con `--gamma 1.0` (completado 2026-06-10)
- [x] Re-evaluar: AUC=0.824, F1=0.846, recall_normal=0.642
- [x] Actualizar numeros en preview.tex y manuscript.tex
- [x] Generar Fig 5 Grad-CAM: paper/figures/fig5_gradcam.png + .pdf
- [x] Recompilar PDF: preview.pdf (15 paginas, sin errores)

### Pendiente (requiere mdpi.cls — accion manual):
- [ ] Descargar plantilla MDPI oficial: https://www.mdpi.com/authors/latex (login requerido)
- [ ] Extraer `mdpi.cls` + auxiliares a `paper/manuscript/`
- [ ] Compilar `manuscript.tex` con la clase real (no el HTML redirect actual)

### Pendiente (acciones del usuario):
- [ ] Confirmar grant number con UNAP → reemplazar "TBD" en manuscript.tex linea ~584
- [ ] Depositar dataset en Zenodo → obtener DOI → reemplazar "TBD" en linea ~588
- [ ] Crear repo GitHub publico `AlpacaVisionAI/alpacavision-ai` → actualizar URL
- [ ] Registrar en susy.mdpi.com con email institucional UNAP
- [ ] Enviar con asesor Aleman Gonzales como corresponding author
- [ ] APC ~2,600 CHF coordinar con administracion UNAP

## Notas sobre las referencias (44 entradas)
- Entradas marcadas `[TODO-verify]` deben verificarse antes del envio: `neethirajan2020`, `ting2017`
- Entradas de proceedings sin paginas exactas (simonyan2015, yosinski2014, loshchilov2019) son estandar en conferencias que no asignan paginas en arXiv-first publication
- Todas las nuevas entradas son papers de alto impacto y altamente citados en sus areas

## Informacion de la revista

| Campo | Valor |
|---|---|
| Revista | MDPI Agriculture |
| ISSN | 2077-0472 |
| Indexacion | Scopus Q1, SCIE |
| IF 2024 | ~3.0 |
| APC | ~2,600 CHF (UNAP paga) |
| Portal envio | https://susy.mdpi.com |
| Tiempo decision | ~6-8 semanas |
| Backup | MDPI Animals (mismo APC) |

---
*AlpacaVision AI · Semillero "John J. Hopfield — IIICCD" · UNA Puno · 2025-2026*
*Asesor: Aleman Gonzales, Leonid · Equipo: Vilca-Solorzano RA, Ccora-Acero CD, Yana-Yucra DM*
*Actualizado: 2026-06-10 — Windows (Claude Code)*
