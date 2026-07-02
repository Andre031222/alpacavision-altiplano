# AlpacaVision AI — Instrucciones de arranque

> ⚠️ **DOCUMENTO PARCIALMENTE DESACTUALIZADO (rutas Windows + métricas viejas con fuga de datos).**
> La **fuente de verdad** del estado del proyecto es [`docs/ESTADO_PAPER.md`](ESTADO_PAPER.md).
> Las métricas honestas son: detector mAP@0.5 = **0.860/0.863**, clasificador AUC = **0.506 (azar)**.
> El antiguo "mAP=0.913" de abajo era **fuga de datos** — NO usar.
> Entorno actual: Linux, `.venv-linux/` (Python 3.12 + torch 2.6 + CUDA). Entrada webapp: `python run_webapp.py`.

## ANTES DE EMPEZAR

1. **Cerrar Ollama** — clic derecho en ícono de la barra de tareas → Quit
2. Verificar GPU libre:
   ```
   nvidia-smi
   ```
   Debe mostrar < 1000MB usados antes de activar el venv.

---

## ESTADO ACTUAL (2026-05-10)

| Componente | Estado |
|------------|--------|
| Stage 1 — Detector YOLOv11n | **COMPLETO** mAP50=0.913 en test |
| Auto-labeling Stage 2 | **COMPLETO** 300/300 imágenes |
| Upload Roboflow Stage 2 | **COMPLETO** 300 imágenes subidas |
| Crops ojos/patas | **COMPLETO** 449 ojos + 446 patas extraídos |
| Modelo ONNX exportado | **COMPLETO** `models/detector/best.onnx` |
| **Aplicación web Flask** | **COMPLETO** — ver detalles abajo |
| **Autenticación + roles** | **COMPLETO** — Flask-Login, BCrypt, CSRF |
| **Panel admin white-label** | **COMPLETO** — 6 tabs, config en DB |
| **Tema oscuro/claro** | **COMPLETO** — toggle, sin FOUC |
| Stage 2 — Detector 5 clases | PENDIENTE (esperando revisión semillero en Roboflow) |
| EfficientNet clasificadores | PENDIENTE (necesitan datos anomaly del semillero) |

---

## SIGUIENTE PASO — Revisión Roboflow (acción humana requerida)

El semillero debe revisar y corregir los 300 pseudo-labels en:
```
https://app.roboflow.com/andre-nftgn/alpacavision-stage2/annotate
```
Con >= 200 imágenes aprobadas, entrenar Stage 2:
```bash
cd D:\Research-Dev\AUP_Articulos_Inves\alpacavision-ai
venv\Scripts\activate
venv\Scripts\python.exe scripts/run_pipeline.py --skip-autolabel --skip-upload
```
(pero primero descargar el dataset revisado de Roboflow)

---

## CUANDO LLEGUEN DATOS ANOMALY — Clasificadores

El semillero debe clasificar las imágenes en `data/crops/`:
- Mover imágenes con anomalías a `data/crops/eyes/anomaly/` y `data/crops/legs/anomaly/`
- Con >= 50 ejemplos anomaly por clase, correr:
```bash
venv\Scripts\python.exe src/training/train_classifier.py
```

---

## Levantar la aplicación web Flask

```bash
cd D:\Research-Dev\AUP_Articulos_Inves\alpacavision-ai
venv\Scripts\activate
venv\Scripts\python.exe src/webapp/run.py
```
Abre: http://localhost:5050

El detector Stage 1 ya está cargado en `models/detector/best.pt`.
Los clasificadores mostrarán "N/A" hasta que se entrenen.

### Credenciales super admin
- Ver `.env` local / gestor de contraseñas (NO documentar credenciales en texto plano).
- Panel admin: http://localhost:5050/admin/

### Flujo de la app web
1. Landing pública → `/`
2. Registro/Login → `/auth/register` y `/auth/login`
3. Dashboard → `/dashboard/` (subir imagen, análisis YOLO + Groq)
4. Animales → `/dashboard/animals` (registrar rebaño, ver historial por animal)
5. Historial → `/dashboard/history` (todos los análisis con filtros)
6. Perfil → `/dashboard/profile`
7. Admin (super_admin only) → `/admin/` (configurar marca, textos, logos, footer)

### Variables de entorno necesarias (.env)
```
DATABASE_URL=postgresql://postgres:221203@localhost:5432/alpacavision
SECRET_KEY=dev-secret-key-cambiar-en-produccion
GROQ_API_KEY=gsk_...
```

### Si la DB no está inicializada (primera vez)
```bash
set FLASK_APP=src/webapp/__init__.py
venv\Scripts\flask.exe db upgrade
venv\Scripts\python.exe scripts/create_admin.py
```

---

## Archivos clave del proyecto

| Archivo | Qué hace |
|---------|----------|
| `models/detector/best.pt` | Detector alpaca body (mAP50=0.913) |
| `models/detector/best.onnx` | Versión ONNX para deployment |
| `scripts/create_admin.py` | Crea usuario super_admin en la DB |
| `scripts/auto_label.py` | Auto-etiquetado con Grounding DINO (con resume) |
| `scripts/upload_labels_roboflow.py` | Sube labels a Roboflow |
| `scripts/run_pipeline.py` | Pipeline completo configurable |
| `scripts/extract_crops_from_labels.py` | Extrae crops de ojos/patas desde labels |
| `scripts/evaluate_stage1.py` | Evaluación completa + ONNX export |
| `src/webapp/run.py` | Arranque de la app web Flask (puerto 5050) |
| `src/webapp/__init__.py` | Application Factory Flask |
| `src/webapp/blueprints/` | Blueprints: public, auth, dashboard, api, admin |
| `src/webapp/models/` | Modelos: User, Animal, Analysis, SystemConfig |
| `src/webapp/templates/` | Templates Jinja2 (base, dashboard, auth, admin) |
| `outputs/figures/stage1_eval_report.txt` | Reporte métricas para el paper |
| `outputs/figures/stage1_training_curves.png` | Curvas entrenamiento |

---

## APIs (en .env — NUNCA en texto plano aquí ni en git)

```
GROQ_API_KEY=<en .env local>
ROBOFLOW_API_KEY=<en .env local>
```
> 🔐 Estas claves estuvieron en texto plano en este doc. Si el repo fue compartido, **rotarlas**
> (Groq → console.groq.com, Roboflow → app.roboflow.com/settings/api).

---

*AlpacaVision AI · Semillero "John J. Hopfield - IIICCD" · UNA Puno · 2025*
