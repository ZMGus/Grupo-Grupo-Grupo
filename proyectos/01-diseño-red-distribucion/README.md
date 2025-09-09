# 01 — Diseño de la Red de Distribución

Este proyecto resuelve la localización de plantas (tipo pequeña/grande) y la asignación de flujos a 6 regiones durante 3 años, minimizando costos de apertura, fijos, variables y de transporte. Se modela en **Gurobipy** y se visualiza la solución en un **mapa interactivo (Folium)**.

## Contexto
Funnys Company enfrenta un aumento de demanda y debe rediseñar su red con posibles plantas en Antofagasta, Valparaíso, Santiago, **Rancagua**, Concepción y Puerto Montt. Tres alternativas de transporte (AT1, AT2, AT3) con costos unitarios por ciudad-región.

## Formulación 

---

## Conjuntos

* $I$: ciudades que pueden **producir y despachar**
  $I=\{\text{Antofagasta, Valparaíso, Santiago, Rancagua, Concepción, Puerto Montt}\}$
* $I^{\text{new}}\subset I$: **ciudades nuevas** candidatas a apertura
  $I^{\text{new}}=\{\text{Antofagasta, Valparaíso, Santiago, Concepción, Puerto Montt}\}$
* $J$: tipos de planta $\{\text{Pequeña, Grande}\}$
* $K$: regiones de demanda $\{\text{R1,\dots,R6}\}$
* $F$: modos de transporte $\{\text{AT1, AT2, AT3}\}$
* $T$: años del horizonte $\{1,2,3\}$

Definición: **demanda acumulada 3 años** $\ \bar D_k=\sum_{t\in T} D_{kt}$.

---

## Parámetros

* $C_{ij}$: costo de **apertura** de planta tipo $j$ en ciudad $i$ (solo $i\in I^{\text{new}}$).
* $CF_{ij}$: costo **fijo anual** de planta tipo $j$ en $i$.
* $CV_{ij}$: costo **variable por unidad** de planta tipo $j$ en $i$.
* $CT_{ikf}$: costo **unitario de transporte** desde $i$ a región $k$ por modo $f$.
* $P_{j}$: **capacidad anual** de una planta tipo $j$.
* $D_{kt}$: demanda de la región $k$ en el año $t$.
* $M$: constante “Big-M” suficientemente grande.

> **Planta existente:** en **Rancagua** hay una planta **Pequeña** instalada (costo de apertura $=0$), con costos $CF_{\text{Rancagua},\text{Pequeña}}$, $CV_{\text{Rancagua},\text{Pequeña}}$ y capacidad anual $P_{\text{Pequeña}}$.

---

## Variables de decisión

* $x_{ij}\in\{0,1\}$ $(i\in I^{\text{new}},\, j\in J)$: 1 si se abre una planta tipo $j$ en $i$.
* $z_f\in\{0,1\}$ $(f\in F)$: 1 si se **elige** el modo de transporte $f$ (único para todo el sistema).
* $y_{ikf}\in\mathbb{Z}_{\ge 0}$ $(i\in I,\,k\in K,\,f\in F)$: flujo $i\to k$ por $f$ **acumulado en 3 años**.
* $\mathrm{prod}_i\in\mathbb{R}_{\ge 0}$ $(i\in I)$: producción total de la ciudad $i$ **acumulada en 3 años**.

---

## Función objetivo (minimizar)

$$
\min z =
\sum_{i\in I^{\text{new}}}\sum_{j\in J} C_{ij}\,x_{ij}
+ 3\!\left(\sum_{i\in I^{\text{new}}}\sum_{j\in J} CF_{ij}\,x_{ij}
+ CF_{\text{Rancagua},\text{Pequeña}}\right)
+ CV_{\text{Rancagua},\text{Pequeña}}\,\mathrm{prod}_{\text{Rancagua}}
+ \sum_{i\in I^{\text{new}}}\sum_{j\in J} CV_{ij}\,\mathrm{prod}_i\,x_{ij}
+ \sum_{i\in I}\sum_{k\in K}\sum_{f\in F} CT_{ikf}\, y_{ikf}.
$$

---

## Restricciones

### 1) Satisfacción de la demanda (acumulada 3 años)

$$
\sum_{i\in I}\sum_{f\in F} y_{ikf} \ge \bar D_k
\qquad \forall k\in K.
$$

### 2) Capacidad acumulada por ciudad (3 años)

**Rancagua (planta existente Pequeña):**

$$
\mathrm{prod}_{\text{Rancagua}} \le 3\,P_{\text{Pequeña}}.
$$

**Ciudades nuevas:**

$$
\mathrm{prod}_{i} \le 3\sum_{j\in J} P_{j}\,x_{ij}
\qquad \forall i\in I^{\text{new}}.
$$

### 3) Balance producción–despachos por ciudad

$$
\mathrm{prod}_{i} = \sum_{k\in K}\sum_{f\in F} y_{ikf}
\qquad \forall i\in I.
$$

### 4) A lo más una planta por ciudad nueva

$$
\sum_{j\in J} x_{ij} \le 1
\qquad \forall i\in I^{\text{new}}.
$$

### 5) Elección única del modo de transporte

$$
\sum_{f\in F} z_f = 1.
$$

### 6) Activación de flujos por modo (Big-M)

$$
y_{ikf} \le M\,z_f
\qquad \forall i\in I,\; \forall k\in K,\; \forall f\in F.
$$

### 7) Naturaleza de variables

$$
x_{ij}\in\{0,1\},\quad z_f\in\{0,1\},\quad
y_{ikf}\in\mathbb{Z}_{\ge 0},\quad \mathrm{prod}_i\ge 0.
$$


---




# (RELLENAR POSTERIORMENTE, DEJO EJEMPLO)
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












