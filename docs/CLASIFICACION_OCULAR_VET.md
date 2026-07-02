# Clasificación clínica de anomalías oculares en alpacas — Protocolo de anotación

> **Propósito.** Convertir el clasificador ocular (hoy AUC = 0.506, azar, por etiquetas de LLM-vision)
> en algo publicable, dándole un **ground truth veterinario real**. Este documento es (a) la base
> clínica investigada con literatura, y (b) el **protocolo de etiquetado** que debe seguir el
> veterinario/asesor para marcar los crops de `data/crops/eyes/`.
> Redactado actuando como veterinario; los hechos epidemiológicos están citados. El juicio clínico
> sobre "qué se ve en una foto" está marcado como tal.

---

## 1. Por qué importa esto (y por qué el modelo actual falla)

El clasificador no falla por la arquitectura (EfficientNet-B2 está bien). Falla porque sus
etiquetas las puso un modelo de visión-lenguaje (Groq), no un clínico. **La patología ocular fina
no es etiquetable de forma fiable sin criterio veterinario.** Este documento fija qué signos
*sí* son reconocibles en una foto de campo y cuáles no, para etiquetar solo lo que es real.

## 2. Base clínica (literatura veterinaria real)

Hechos sobre oftalmología de camélidos sudamericanos (CSA: alpaca, llama, vicuña, guanaco):

- **La enfermedad corneal es la afección ocular más común en camélidos del Nuevo Mundo.** En la
  base VMDB, el **41 % de las llamas** con enfermedad ocular tenían enfermedad corneal, y **más de
  la mitad eran úlceras**; la causa más frecuente es **traumática**. (Gionfriddo, *Ophthalmology of
  South American Camelids*).
- **Queratitis micótica (fúngica):** relativamente común en poblaciones de alpacas; comparte rasgos
  clínicos con la keratomicosis equina.
- **Uveítis:** es la manifestación ocular más común de enfermedades infecciosas sistémicas en CSA
  (p. ej. EHV-1, aspergilosis sistémica → coriorretinitis).
- **Cataratas:** documentadas en CSA (llamas, alpacas, vicuñas, guanacos); en un estudio de afecciones
  oculares en camélidos representaron ~16 % de los casos. Existen también **defectos oculares
  congénitos/hereditarios** descritos en alpacas emparentadas.
- **Entropión:** el entropión severo puede progresar a úlcera corneal, perforación y panoftalmitis.

**Contexto regional (altiplano de Puno — la zona de este paper):**

- La **queratoconjuntivitis** está reconocida entre las ~10 enfermedades infecciosas de camélidos
  domésticos en comunidades altoandinas de Puno (Cangalli, Ilave, El Collao). Agentes asociados en
  CSA: *Staphylococcus aureus* y *Moraxella liquefaciens*.
- Un estudio clínico en Perú documentó **conjuntivitis y blefaritis en 3.25 % (39/1 200)** de
  camélidos, con mayor frecuencia en adultos (69 %) que en juveniles (31 %).

> **Implicación para el dataset:** lo más prevalente y fotografiable en campo en el altiplano es el
> **complejo queratoconjuntival/corneal** (secreción, opacidad corneal, ojo rojo, blefaroespasmo),
> NO las cataratas finas ni la patología de fondo de ojo. La taxonomía de abajo prioriza eso.

## 3. Qué SE VE en una foto externa de campo (juicio clínico) vs. qué NO

El dataset son crops de ojos de fotos de campo (sin lámpara de hendidura, sin fluoresceína, sin
oftalmoscopio, sin tonómetro). Eso limita drásticamente lo etiquetable:

| Signo / condición | ¿Visible en foto externa? | Nota clínica |
|---|---|---|
| Secreción ocular (epífora / mucopurulenta) | ✅ Sí | Costras, lagrimeo, pelo húmedo periocular |
| Opacidad corneal (edema, cicatriz, úlcera con edema) | ✅ Sí | Córnea "azulada"/blanquecina, pierde brillo |
| Vascularización corneal (pannus) | ✅ Sí | Vasos rojos cruzando la córnea |
| Ojo rojo / hiperemia conjuntival | ✅ Sí | Conjuntiva/esclera enrojecida |
| Blefaroespasmo (ojo entrecerrado) | ✅ Sí | Dolor; signo indirecto muy útil |
| Tumefacción / blefaritis (párpado inflamado) | ✅ Sí | Párpados hinchados, alopecia |
| Catarata **madura** (leucocoria) | ⚠️ A veces | Pupila blanca; solo si es madura y bien iluminada |
| Hifema / masa / cuerpo extraño evidente | ✅ Sí | Sangre en cámara anterior, espina, etc. |
| Entropión (párpado invertido) | ⚠️ A veces | Difícil en foto frontal |
| Catarata **incipiente**, uveítis, glaucoma | ❌ No | Necesitan lámpara/tonómetro/midriasis |
| Patología de retina/fondo (coriorretinitis) | ❌ No | Imposible sin oftalmoscopia |

**Regla de oro del protocolo:** si un signo no está en la mitad superior de la tabla, **no se
etiqueta como anomalía a partir de la foto** — se marca `no_evaluable`. Etiquetar lo que no se ve =
reintroducir el ruido que hundió al modelo.

## 4. Taxonomía de etiquetado (la que debe usar el veterinario)

Esquema en **dos niveles**. El nivel 1 es el que el clasificador puede aprender de verdad con los
datos actuales; el nivel 2 es para investigación futura / un detector multi-clase.

**Nivel 1 — binario (objetivo inmediato del clasificador):**
- `normal` — ojo sano: córnea transparente y brillante, sin secreción, sin enrojecimiento, párpados
  normales, ojo bien abierto.
- `anomaly` — cualquier signo fotografiable de la mitad superior de la tabla §3.
- `no_evaluable` — **descartar del entrenamiento**: foto borrosa, ojo cerrado/ocluido, reflejo o
  iluminación que impide juzgar, crop mal recortado, resolución insuficiente.

**Nivel 2 — categorías clínicas (etiqueta fina, opcional, para futuro):**
1. `secrecion_conjuntivitis` — secreción/epífora + ojo rojo (complejo queratoconjuntival; lo más
   prevalente en Puno).
2. `opacidad_corneal` — edema/cicatriz/úlcera con opacidad (la afección corneal más común en CSA).
3. `catarata` — leucocoria/pupila blanca (solo cataratas maduras).
4. `inflamacion_parpado` — blefaritis/tumefacción/entropión.
5. `trauma_otro` — hifema, cuerpo extraño, masa, perforación.

> Mapeo: cualquier categoría de Nivel 2 ⇒ `anomaly` en Nivel 1. Esto permite entrenar el binario ya
> y conservar la etiqueta fina para un Paper 3.

## 5. Protocolo operativo de anotación (para el asesor/veterinario)

1. **Material:** carpeta `data/crops/eyes/` (revisar los **91 crops originales** de anomalía y los
   **371 normales**; ignorar los `aug_*`, son aumentos sintéticos que causaron fuga de datos).
2. **Por cada crop, decisión en árbol:**
   - ¿Se ve el ojo con calidad suficiente para juzgar? **No →** `no_evaluable`.
   - ¿Hay algún signo de la mitad superior de §3? **No →** `normal`. **Sí →** `anomaly`
     (+ categoría Nivel 2 si se quiere la fina).
3. **Doble lectura:** idealmente 2 evaluadores independientes; conservar solo los crops con
   **consenso**. Reportar el acuerdo inter-observador (κ de Cohen) — esto fortalece el paper.
4. **Meta de tamaño:** ≥ **150–200 anomalías** validadas y un número comparable de normales para un
   clasificador creíble. Con los ~91 actuales no alcanza; hay que **extraer más crops** de
   `data/raw` (15 k imágenes) con el detector y volver a revisar.
5. **Re-entrenar honesto:** `scripts/train_two_stage.py` con split *group-aware* (sin fuga; ya
   implementado en `src/data/group_split.py`) y evaluar con `scripts/evaluate_classifiers.py`.

## 6. Qué significa esto para el paper (honesto)

- **Si SE consigue el ground truth** (≥150–200 anomalías reales con consenso): el clasificador pasa
  de "estudio de viabilidad / resultado negativo" a un **resultado positivo real** → posible Paper 3,
  o fortalece el actual.
- **Si NO se consigue a tiempo:** el encuadre actual del manuscrito es correcto y honesto — "el
  auto-etiquetado con LLM-vision no basta para anomalías oculares finas de campo"; este documento
  *explica clínicamente por qué* (la mayoría de la patología ocular fina no es fotografiable sin
  equipamiento), lo que **refuerza** la sección de limitaciones con base veterinaria citada.

## Fuentes

- Gionfriddo JR. *Ophthalmology of South American Camelids* — https://www.semanticscholar.org/paper/Ophthalmology-of-South-american-camelids.-Gionfriddo/7ede1839e41391b0be5e5393f60ed614fe1adb29
- *Ophthalmology of Tylopoda: Camels, Alpacas, Llamas, Vicuñas, and Guanacos* (Springer) — https://link.springer.com/chapter/10.1007/978-3-030-81273-7_8
- *Ophthalmology* — Medicine and Surgery of Camelids (Wiley) — https://onlinelibrary.wiley.com/doi/abs/10.1002/9781119583295.ch18
- Knickelbein et al. (2018) *Multiple ocular developmental defects in four closely related alpacas*, Vet Ophthalmol — https://onlinelibrary.wiley.com/doi/abs/10.1111/vop.12540
- *Cataracts in New World camelids* — https://www.researchgate.net/publication/11215672
- *Diagnosis and treatment of common ophthalmic disorders in South American camelids*, UK Vet Livestock — https://www.magonlinelibrary.com/doi/abs/10.12968/live.2020.25.3.156
- *Phacoemulsification surgery in alpacas* (PubMed) — https://pubmed.ncbi.nlm.nih.gov/32510743/
- *Bilateral bullous keratopathy secondary to melting keratitis in a Suri alpaca* — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5889221/
- *A Literature Review of Selected Bacterial Diseases in Alpacas and Llamas* (PMC) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10778254/
- *La Sabiduría Andina en la sanidad de Alpacas y Llamas — Cangalli, Ilave, El Collao, Puno* — https://repositorioslatinoamericanos.uchile.cl/handle/2250/3274702
- FAO, *Sanidad y salud animal en camélidos* — https://openknowledge.fao.org/server/api/core/bitstreams/360f94ef-9659-41e8-bd2f-d6acb5de134e/content
