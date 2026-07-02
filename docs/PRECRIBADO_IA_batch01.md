# Pre-cribado IA del lote batch_01 (462 crops oculares) — reporte honesto

> **Qué es esto y qué NO es.** Este documento reporta un **pase de etiquetado por IA de visión**
> (Claude, actuando como cribador oftalmológico con el protocolo de `CLASIFICACION_OCULAR_VET.md`)
> sobre los 462 crops de `data/vet_labeling/batch_01/00_POR_REVISAR/`.
>
> **NO es ground truth veterinario.** El paper documenta que el clasificador se hundió *precisamente*
> porque sus etiquetas las puso una IA de visión (Groq), no un clínico. Usar otra IA como verdad de
> referencia repetiría ese error. Por eso este pase sirve solo para dos cosas legítimas:
> 1. **Triaje** — reducir el trabajo de un veterinario real a los pocos crops que valen la pena.
> 2. **Comparador honesto** — ¿una VLM más cuidadosa mejora al etiquetado Groq viejo? (Resultado
>    reportable para la sección de limitaciones, *sin* llamarlo ground truth.)
>
> El lote original `00_POR_REVISAR/` **no se tocó**; un veterinario real sigue siendo posible.

## 1. Método

- 462 crops, anonimizados y barajados (`eye_0001…eye_0462`).
- **Regla de resolución** (objetiva, previa a la visión): crops con lado menor **< 32 px → `no_evaluable`**
  por resolución insuficiente. Se revisaron igualmente en mosaico para descartar signos groseros
  (pupila blanca, secreción masiva): no se halló ninguno.
- Crops **≥ 32 px**: ampliados con Lanczos y evaluados por 12 cribadores de visión en paralelo con
  rubro clínico idéntico y **sesgo conservador** (ante la duda → `no_evaluable`, nunca anomalía adivinada).
- **Control adversarial:** las anomalías candidatas las reconfirmó el revisor principal a mano.
- Salidas: `data/vet_labeling/batch_01/ai_prescreen.csv` y árbol de copias `ai_prescreen/`.

## 2. El hallazgo que domina todo: los crops son demasiado pequeños

Distribución del **lado menor** de los 462 crops:

| Rango (lado menor) | n | % | Utilidad diagnóstica |
|---|---:|---:|---|
| < 32 px  | 232 | 50.2 % | Inservible |
| 32–63 px | 150 | 32.5 % | Muy dudoso |
| 64–99 px | 42 | 9.1 % | Limitado |
| 100–159 px | 13 | 2.8 % | Evaluable |
| ≥ 160 px | 25 | 5.4 % | Bueno |

**Mediana = 37 px de ancho. Solo 38/462 (8 %) tienen el lado menor ≥ 100 px.** A 37 px no se puede
juzgar patología corneal fina (edema, úlcera, opacidad), que es justo lo más prevalente en el
altiplano. Esto es una **limitación física del pipeline de recorte**, independiente de la
arquitectura del clasificador o de quién etiquete.

## 3. Resultado del cribado IA (n = 462)

| Etiqueta IA | n | % |
|---|---:|---:|
| `no_evaluable` | 434 | 93.9 % |
| `normal` | 27 | 5.8 % |
| `anomalia` (candidata) | 1 | 0.2 % |

- Única anomalía candidata: **`eye_0425`** — posible secreción/lagrimeo seco bajo el canto medial,
  **confianza 0.55** (61×63 px). Reconfirmada a mano: **candidato débil, no diagnóstico firme.**
- Conclusión clínica: en 462 crops de campo hay **≈ 0 anomalías oculares diagnosticables con confianza.**

## 4. Comparación con el etiquetado Groq viejo (el que hundió al modelo)

Matriz IA vs Groq:

|  | groq: anomaly | groq: normal |
|---|---:|---:|
| IA anomaly | 1 | 0 |
| IA normal | 11 | 16 |
| IA no_evaluable | 79 | 355 |

- Groq marcó **91 crops como "anomaly"**. Un cribado IA cuidadoso confirma **1**. El 87 % de esas
  "anomalías" Groq eran de hecho **no evaluables** (borrosas / sin ojo / resolución nula).
- Acuerdo IA–Groq sobre los crops que la IA juzga decidibles (n=28): **60.7 %** — apenas mejor que azar.

Esto es **evidencia independiente y directa** de la tesis del paper: el auto-etiquetado con
LLM-visión no basta para anomalía ocular fina en crops de campo. Ahora respaldado por *dos* VLM
distintas que discrepan casi por completo entre sí.

## 5. Qué significa para el paper (honesto)

1. **El encuadre actual es correcto y ahora está más fundamentado.** La sección de limitaciones puede
   citar: (a) el techo de resolución (mediana 37 px, solo 8 % ≥100 px) y (b) la discordancia
   inter-VLM (Groq 91 vs IA-cuidadosa 1 anomalía; acuerdo 60.7 %).
2. **Este lote NO puede dar el ground truth buscado.** Un veterinario real sobre estos mismos crops
   encontraría casi nada etiquetable — no por falta de patología en el rebaño, sino porque los
   recortes no la contienen a esta resolución.
3. **La acción correcta es aguas arriba, no seguir etiquetando miniaturas:** re-extraer crops
   oculares a **mayor resolución** (bounding boxes más grandes / imágenes fuente de mayor calidad,
   filtrando por lado menor ≥ ~128 px) desde `data/raw`, y recién entonces someterlos a un
   veterinario. Con eso, la meta de ≥150–200 anomalías reales pasa a ser plausible.

## 6. Archivos generados

- `data/vet_labeling/batch_01/ai_prescreen.csv` — 462 filas: `id, ai_label, categoria, confianza, signo, calidad, groq_previa`.
- `data/vet_labeling/batch_01/ai_prescreen/{normal,anomalia_candidata,no_evaluable}/` — **copias** para inspección visual.
- `00_POR_REVISAR/` — intacto (462), listo aún para un evaluador humano.
