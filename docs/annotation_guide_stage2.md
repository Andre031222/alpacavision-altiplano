# Guía de Etiquetado — Etapa 2: Regiones Anatómicas
## AlpacaVision AI · Semillero "John J. Hopfield - IIICCD" · UNA Puno

---

## 1. Acceso a la herramienta

**URL:** https://app.roboflow.com/andre-nftgn/alpacavision-stage2/annotate

Solicitar acceso al coordinador del semillero. La herramienta es gratuita y funciona en el navegador, sin instalar nada.

---

## 2. Las 5 clases que debes etiquetar

### Clase 0 — `alpaca_body`
**Qué es:** El cuerpo completo de la alpaca, desde el cuello hasta la cola. **No incluye** la cabeza ni las patas por debajo de la rodilla.

**Cuándo etiquetar:** Siempre que el cuerpo sea visible (incluso si está parcialmente oculto).

**Criterio del bounding box:** Ajustar justo al torso. Límite superior: base del cuello. Límite inferior: articulación de rodilla/corvejón.

---

### Clase 1 — `alpaca_head`
**Qué es:** La cabeza completa incluyendo el hocico, orejas y cuello superior.

**Cuándo etiquetar:** Si se ve claramente la cabeza (al menos 60% visible).

**Criterio:** Incluir las orejas. El límite inferior es la base del cuello (donde empieza el vellón del cuerpo).

---

### Clase 2 — `alpaca_eye`
**Qué es:** La región del ojo — incluyendo el párpado, la esclerótica y área periocular inmediata.

**Cuándo etiquetar:** Solo si el ojo es claramente visible. Tamaño mínimo en la imagen: 20×20 píxeles.

**Criterio:** Bounding box muy ajustado al ojo. No incluir la oreja ni el hocico.

**Importante:** Etiquetar cada ojo visible por separado (pueden aparecer 1 o 2 por imagen).

---

### Clase 3 — `alpaca_leg_front`
**Qué es:** Extremidad delantera desde la articulación del carpo (rodilla delantera) hacia abajo, incluyendo la pezuña.

**Cuándo etiquetar:** Si la pata delantera es visible al menos desde el carpo hacia abajo.

**Criterio:** Límite superior: articulación del carpo. Límite inferior: punta de la pezuña.

**Importante:** Etiquetar cada pata visible por separado.

---

### Clase 4 — `alpaca_leg_rear`
**Qué es:** Extremidad trasera desde el corvejón (tarso) hacia abajo, incluyendo la pezuña.

**Cuándo etiquetar:** Si la pata trasera es visible al menos desde el corvejón hacia abajo.

**Criterio:** igual que `alpaca_leg_front` pero para las patas traseras.

---

## 3. Reglas generales

| Regla | Detalle |
|-------|---------|
| Oclusión > 50% | NO etiquetar la región |
| Imagen borrosa | Etiquetar igual — anotar como "difícil" en Roboflow |
| Alpaca de espaldas | Etiquetar lo que sea visible |
| Múltiples alpacas | Etiquetar TODAS las visibles |
| Duda entre clases | Etiquetar como la más conservadora y marcar para revisión |

---

## 4. Protocolo de calidad

- **Mínimo 2 anotadores** revisan la misma imagen en casos ambiguos.
- Las etiquetas de `alpaca_eye` requieren **validación del MVZ asesor** antes de usarse para entrenamiento.
- Usar el campo "notas" de Roboflow para señalar imágenes que requieren revisión veterinaria.
- **Meta semanal:** 50 imágenes por anotador.

---

## 5. Flujo de trabajo en Roboflow

```
1. Ir a la URL del proyecto
2. Clic en "Start Annotating"
3. Seleccionar herramienta "Bounding Box" (tecla B)
4. Dibujar bbox → seleccionar clase → Enter
5. Repetir para todas las regiones visibles
6. Clic "Save" antes de pasar a la siguiente imagen
7. Marcar "Approve" solo si el anotador está seguro al 100%
```

---

## 6. Ejemplos de casos difíciles

**Alpaca de perfil:** etiquetar el ojo visible (solo 1), las patas visibles (puede ser 2 de un mismo lado), cabeza y cuerpo normalmente.

**Cría junto a adulto:** etiquetar cada animal por separado con todas sus regiones.

**Vellón muy largo que oculta patas:** si no se distingue la articulación, NO etiquetar las patas.

**Ojo con secreción:** etiquetar `alpaca_eye` normalmente — la anomalía la clasifica el modelo, no el anotador.

---

## 7. Métricas de calidad esperadas

Para proceder con el entrenamiento de Etapa 2 se requiere:
- ≥ 200 imágenes aprobadas
- ≥ 150 con `alpaca_eye` etiquetado
- ≥ 150 con al menos una `alpaca_leg_front` o `alpaca_leg_rear`
- Inter-annotator agreement (IoU) ≥ 0.75 en muestra de revisión

---

*AlpacaVision AI · Semillero "John J. Hopfield - IIICCD" · UNA Puno · 2025*
