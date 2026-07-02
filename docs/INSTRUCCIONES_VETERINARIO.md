# Instrucciones para el veterinario — Etiquetado de ojos de alpaca

**Objetivo:** revisar fotos recortadas de ojos de alpaca y marcar cuáles muestran una
**anomalía ocular** y cuáles son **normales**. Tu criterio clínico es el "ground truth"
que hará creíble al modelo (hoy las etiquetas las puso una IA y no sirven).

> **Regla de oro:** marca **solo lo que realmente se ve en la foto.** Si dudas o la
> imagen no permite juzgar, va a `no_evaluable`. Etiquetar lo que no se ve arruina el modelo.

---

## Qué tienes que hacer (5 minutos para entender, ~1–2 s por imagen)

1. Abre la carpeta **`00_POR_REVISAR/`** (tiene 462 imágenes: `eye_0001.jpg`, `eye_0002.jpg`…).
   Están **mezcladas a propósito** para que no te condicione ninguna etiqueta previa.
2. Mira cada imagen y **muévela** a UNA de estas tres carpetas:
   - **`normal/`** → ojo sano.
   - **`anomalia/`** → se ve algún signo anormal (lista abajo).
   - **`no_evaluable/`** → borrosa, ojo cerrado/tapado, reflejo, mal recorte, no se puede juzgar.
3. (Opcional pero valioso) para las que pongas en `anomalia/`, anota la categoría en
   `planilla.csv` (columna `categoria`) o renombrando el archivo, p. ej.
   `eye_0123_secrecion.jpg`.

Eso es todo. Puedes trabajar en tandas; no hace falta terminar de una sola vez.

---

## ¿Qué cuenta como ANOMALÍA? (lo que SÍ se ve en una foto de campo)

| Signo | Cómo se ve |
|---|---|
| **Secreción / conjuntivitis** | Lagrimeo, costras, pelo húmedo periocular, legaña |
| **Opacidad corneal** | Córnea azulada/blanquecina, pierde el brillo/transparencia (edema, úlcera, cicatriz) |
| **Ojo rojo** | Conjuntiva o esclera enrojecida (hiperemia) |
| **Blefaroespasmo** | Ojo entrecerrado por dolor |
| **Inflamación del párpado** | Párpado hinchado, blefaritis, entropión visible |
| **Catarata madura** | Pupila blanca (leucocoria) — solo si es evidente |
| **Trauma / otros** | Sangre en el ojo (hifema), cuerpo extraño, masa, perforación |

## Lo que NO se puede juzgar por foto → `no_evaluable` (NO lo marques como anomalía)

Catarata incipiente, uveítis, glaucoma, o cualquier patología de **fondo de ojo/retina**:
necesitan lámpara de hendidura, oftalmoscopio o tonómetro. Si el signo no está en la tabla
de arriba, **no es evaluable desde la foto**.

*(Base clínica y referencias completas en `docs/CLASIFICACION_OCULAR_VET.md`.)*

---

## Categorías para las anomalías (opcional, columna `categoria`)

`secrecion_conjuntivitis` · `opacidad_corneal` · `catarata` · `inflamacion_parpado` · `trauma_otro`

---

## Meta y calidad

- **Meta:** llegar a **≥ 150–200 ojos con anomalía real** confirmada. Si este lote de 462 no
  alcanza, se te preparará un segundo lote.
- **Ideal:** que **dos** evaluadores revisen por separado y se conserven solo las imágenes
  con **acuerdo** (esto fortalece la publicación; se reporta el índice κ de Cohen).
- Ante la duda entre normal y anomalía leve → es preferible `no_evaluable` que un falso positivo.

## Qué NO hacer

- ❌ No marcar como anomalía algo que no se ve claramente.
- ❌ No adivinar diagnósticos de retina/fondo desde una foto externa.
- ❌ No apurarte: 462 imágenes a ~2 s cada una son ~15–20 minutos por evaluador.

---

Cuando termines, avísanos: leeremos en qué carpeta quedó cada imagen, mediremos cuánto se
equivocó la IA previa, y re-entrenaremos el clasificador con **tus etiquetas reales**.
