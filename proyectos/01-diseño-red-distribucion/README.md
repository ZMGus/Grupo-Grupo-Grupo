# 01 — Diseño de la Red de Distribución

Este proyecto resuelve la localización de plantas (tipo pequeña/grande) y la asignación de flujos a 6 regiones durante 3 años, minimizando costos de apertura, fijos, variables y de transporte. Se modela en **PuLP** y se visualiza la solución en un **mapa interactivo (Folium)**.

## Contexto
Funnys Company enfrenta un aumento de demanda y debe rediseñar su red con posibles plantas en Antofagasta, Valparaíso, Santiago, **Rancagua**, Concepción y Puerto Montt. Tres alternativas de transporte (AT1, AT2, AT3) con costos unitarios por ciudad-región.

## Formulación 

## Conjuntos

* $I$: ciudades candidatas.
* $J$: tipos de planta $\{\text{Pequeña, Grande}\}$.
* $K$: regiones de demanda.
* $F$: modos de transporte $\{\text{AT1, AT2, AT3}\}$.
* $T$: años del horizonte $\{1,2,3\}$.
* $|T|$: número de años del horizonte.

---

## Función objetivo (minimizar)

$$
\begin{aligned}
\min\; z \;=\;&
\underbrace{\sum_{i\in I}\sum_{j\in J} x_{ij}\,\big(C_{ij}+CF_{ij}\cdot|T|\big)}_{\text{apertura + fijos de todo el horizonte}}
\\[4pt]
&+\;\underbrace{\sum_{i\in I}\sum_{j\in J} CV_{ij}\left(\sum_{k\in K}\sum_{f\in F}\sum_{t\in T} y_{ikft}\right)}_{\text{costos variables de producción}}
\\[4pt]
&+\;\underbrace{\sum_{i\in I}\sum_{k\in K}\sum_{f\in F} CT_{ikf}\left(\sum_{t\in T} y_{ikft}\right)}_{\text{costos de transporte}} \,.
\end{aligned}
$$

---

## Parámetros

* $C_{ij}$: costo de **apertura** de una planta tipo $j$ en la ciudad $i$.
* $CF_{ij}$: costo **fijo anual** de operación de una planta tipo $j$ en $i$.
* $CT_{ikf}$: costo de **transporte por unidad** desde $i$ a la región $k$ por el modo $f$.
* $CV_{ij}$: costo **variable de producción por unidad** de una planta tipo $j$ en $i$.
* $D_{kt}$: **demanda** de la región $k$ en el año $t$.
* $P_{jt}$: **capacidad anual** de una planta tipo $j$ en el año $t$.

---

## Variables de decisión

* $x_{ij}\in\{0,1\}$: vale 1 si se instala una planta tipo $j$ en la ciudad $i$.
* $y_{ikft}\ge 0$: unidades enviadas desde la ciudad $i$ a la región $k$ por el modo $f$ en el año $t$.

---

## Restricciones

### 1) Satisfacción de demanda (por región y año)

$$
\sum_{i\in I}\sum_{f\in F} y_{ikft}\;\ge\; D_{kt}
\qquad \forall\, k\in K,\; t\in T.
$$

### 2) Capacidad de producción (por ciudad y año)

$$
\sum_{k\in K}\sum_{f\in F} y_{ikft}
\;\le\; \sum_{j\in J} P_{jt}\,x_{ij}
\qquad \forall\, i\in I,\; t\in T.
$$

### 3) A lo más una planta por ciudad

$$
\sum_{j\in J} x_{ij}\;\le\;1
\qquad \forall\, i\in I.
$$

### 4) Naturaleza de variables

$$
x_{ij}\in\{0,1\},\qquad y_{ikft}\ge 0.
$$





#(RELLENAR POSTERIORMENTE, DEJO EJEMPLO)
## Cómo ejecutar
1. `pip install -r requirements.txt`
2. `python src/solve.py` → genera `outputs/solution.json` y `outputs/resumen.txt`
3. `python src/visualize_map.py` → genera `outputs/mapa.html` con la mejor combinación (plantas abiertas y flujos principales).

## Archivos de salida
- **solution.json:** selección de plantas y flujos por año/modo (para trazabilidad).  
- **resumen.txt:** costos totales y chequeos de demanda/capacidad.  
- **mapa.html:** visualización (marcadores de plantas y líneas > umbral).

## Video
En `reports/video.md` está el enlace al video explicativo (5–7 min).

