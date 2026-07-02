# AlpacaVision AI — Plan "siguiente nivel" (2026-06-17)

Tras el saneamiento de datos (ver `ESTADO_PAPER.md`), esto es lo que hace falta para
llevar el proyecto a un resultado **potente y honesto**, publicable de verdad.

## Diagnóstico en una frase
- ✅ El **detector** funciona honestamente (mAP50 = 0.860, sin fuga). Se está potenciando con YOLOv11s.
- 🔴 El **clasificador de ojos** es azar (AUC 0.51) porque sus etiquetas vienen de un LLM-vision (Groq),
  no de un veterinario. El pipeline de entrenamiento funciona (val-F1 0.957 en fundus humano);
  faltan **etiquetas reales** y **más anomalías**.

## Frente 1 — Detector (lo que ya rinde): exprimirlo
- [en curso] YOLOv11s 100 épocas (`config/train_stage1_clean_s.yaml`).
- Comparar n vs s en test honesto (`scripts/eval_detector.py`) → tabla de ablación para el paper.
- Opcional: imgsz 768 si la VRAM aguanta; TTA en val.

## Frente 2 — Clasificador (lo que falla): conseguir señal real
**Causa raíz:** etiquetas de Vision sin poder predictivo. Soluciones, en orden de impacto:

### 2A. Ground truth veterinario (lo que de verdad lo arregla)
Protocolo de etiquetado para el asesor/veterinario:
1. Extraer crops de ojos limpios (ya hay 91 anomaly + 371 normal + más por extraer de `data/raw`).
2. Un veterinario revisa cada crop y marca: `normal` | `catarata` | `opacidad` | `secreción` | `inflamación` | `no_evaluable`.
3. Descartar `no_evaluable`. Exigir ≥150–200 anomalías reales validadas para un clasificador creíble.
4. Re-entrenar con `scripts/train_eyes_honest.py` (ya hace split sin fuga + eval honesta).

### 2B. Ampliar con Vision + validación humana (puente más rápido)
Bloqueado hoy por cuota de Groq (free tier agotado). Cuando se resetee o con API de pago:
```bash
# 1) extraer más crops de ojos de imágenes sin usar (15k en data/raw)
#    NOTA: el detector actual es 1-clase (alpaca); para ojos se usó Grounding DINO (auto_label.py)
venv/Scripts/python.exe scripts/auto_label.py --source data/raw/inaturalist
venv/Scripts/python.exe scripts/extract_crops_from_labels.py
# 2) etiquetar con Vision (doble pasada, consenso estricto)
venv/Scripts/python.exe scripts/label_crops_with_vision.py --task eyes --min-confidence 0.80
# 3) validar a mano las positivas antes de entrenar (clave: Vision tiene falsos positivos)
```

### 2C. Limitación honesta a reportar
Si no hay ground truth a tiempo: reportar el clasificador como **estudio de viabilidad**
("el auto-etiquetado con LLM-vision no basta para anomalías oculares finas") — hallazgo válido.

## Frente 3 — Paper(s) honestos
1. **Paper 1 (ahora):** detector multi-etapa + dataset del altiplano + **metodología de integridad de
   datos** (detección y corrección de fuga sistémica) + sistema/webapp. Sólido y publicable.
2. **Paper 2 (software):** la webapp desplegable (Flask + Groq + reportes).
3. **Paper 3 (futuro):** clasificador de anomalías CON ground truth veterinario (cuando exista).

## Lo que NO se debe hacer
- ❌ Reportar AUC=0.824 / mAP=0.913 (eran fuga de datos).
- ❌ "Mejorar" el clasificador probando arquitecturas: la señal no está en las etiquetas, sería perseguir ruido.
- ❌ Usar `data/annotated` (sucio); usar `data/annotated_clean`.
