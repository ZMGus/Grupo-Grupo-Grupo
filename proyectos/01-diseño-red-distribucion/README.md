# 01 — Diseño de la Red de Distribución

Este proyecto resuelve la localización de plantas (tipo pequeña/grande) y la asignación de flujos a 6 regiones durante 3 años, minimizando costos de apertura, fijos, variables y de transporte. Se modela en **Gurobipy** y se visualiza la solución en un **mapa interactivo (Folium)**.

## Contexto
Funnys Company enfrenta un aumento de demanda y debe rediseñar su red con posibles plantas en Antofagasta, Valparaíso, Santiago, **Rancagua**, Concepción y Puerto Montt. Tres alternativas de transporte (AT1, AT2, AT3) con costos unitarios por ciudad-región.

## Formulación 

---

## Conjuntos

* $I$: ciudades que pueden **producir y despachar**.
  $I=\{\text{Antofagasta}\,\text{Valparaíso}\,\text{Santiago}\,\text{Rancagua}\,\text{Concepción}\,\text{Puerto Montt}\}$
* $I^{\mathrm{new}}\subset I$: **ciudades nuevas** candidatas a apertura.
  $I^{\mathrm{new}}=\{\text{Antofagasta}\,\text{Valparaíso}\,\text{Santiago}\,\text{Concepción}\,\text{Puerto Montt}\}$
* $J$: tipos de planta.
  $J=\{\text{Pequeña}\,\text{Grande}\}$
* $K$: regiones de demanda.
  $K=\{\mathrm{R1}\,\ldots\,\mathrm{R6}\}$
* $F$: modos de transporte.
  $F=\{\mathrm{AT1}\,\mathrm{AT2}\,\mathrm{AT3}\}$
* $T$: años del horizonte.
  $T=\{1,2,3\}$

---

## Parámetros

* $C_{ij}$: costo de **apertura** de planta tipo $j$ en ciudad $i$ (solo $i\in I^{\mathrm{new}}$).
* $CF_{ij}$: costo **fijo anual** de planta tipo $j$ en $i$.
* $CV_{ij}$: costo **variable por unidad** de planta tipo $j$ en $i$.
* $CT_{ikf}$: costo **unitario de transporte** desde $i$ a región $k$ por modo $f$.
* $P_{j}$: **capacidad anual** de una planta tipo $j$.
* $D_{kt}$: demanda de la región $k$ en el año $t$.
* $M$: constante “Big-M” suficientemente grande.

> Planta existente: en **Rancagua** hay una planta **Pequeña** instalada (apertura $=0$), con $CF_{\text{Rancagua},\text{Pequeña}}$, $CV_{\text{Rancagua},\text{Pequeña}}$ y capacidad anual $P_{\text{Pequeña}}$.

---

## Variables de decisión

* $x_{ij}\in\{0,1\}$ $(i\in I^{\text{new}}\, j\in J)$: 1 si se abre una planta tipo $j$ en $i$.
* $z_f\in\{0,1\}$ $(f\in F)$: 1 si se **elige** el modo de transporte $f$ (único para todo el sistema).
* $y_{ikf}\in\mathbb{Z}_{\ge0}$ $(i\in I\,k\in K\,f\in F)$: flujo $i\to k$ por $f$ **acumulado en 3 años**.
* $\mathrm{prod}_i \ge 0$\ $(i\in I)$: producción total de la ciudad $i$ **acumulada en 3 años**.

---

### Función objetivo (término por término)

**Costos de apertura (solo nuevas plantas)**

$$
\sum_{i\in I^{\mathrm{new}}}\sum_{j\in J} C_{ij}\,x_{ij}
$$

**Costos fijos anuales (para 3 años)**

$$
3\left(\sum_{i\in I^{\mathrm{new}}}\sum_{j\in J} CF_{ij} x_{ij} + CF_{\text{Rancagua},\text{Pequeña}}\right)
$$


**Costos variables — planta existente en Rancagua**

$$
CV_{\text{Rancagua},\,\text{Pequeña}}\,\mathrm{prod}_{\text{Rancagua}}
$$

**Costos variables — ciudades nuevas (activadas por $x$)**

$$
\sum_{i\in I^{\mathrm{new}}}\sum_{j\in J} CV_{ij}\,\mathrm{prod}_{i}\,x_{ij}
$$

**Costos de transporte (flujo acumulado 3 años)**

$$
\sum_{i\in I}\sum_{k\in K}\sum_{f\in F} CT_{ikf}\, y_{ikf}
$$

---

### Función objetivo completa

$$
\begin{aligned}
\min z ={}&
\sum_{i\in I^{\mathrm{new}}}\sum_{j\in J} C_{ij} x_{ij}
\\
&+ 3\left(\sum_{i\in I^{\mathrm{new}}}\sum_{j\in J} CF_{ij} x_{ij} + CF_{\text{Rancagua},\text{Pequeña}}\right)
\\
&+ CV_{\text{Rancagua},\text{Pequeña}}\,\mathrm{prod}_{\text{Rancagua}}
\\
&+ \sum_{i\in I^{\mathrm{new}}}\sum_{j\in J} CV_{ij}\,\mathrm{prod}_{i}\,x_{ij}
\\
&+ \sum_{i\in I}\sum_{k\in K}\sum_{f\in F} CT_{ikf}\, y_{ikf}.
\end{aligned}
$$

---

## Restricciones

**1) Demanda acumulada (3 años)**

$$
\sum_{i\in I}\sum_{f\in F} y_{ikf} \ge \bar D_k
$$

para todo $k\in K$.

**2) Capacidad acumulada por ciudad (3 años)**
*Rancagua (planta existente Pequeña):*

$$
\mathrm{prod}_{\text{Rancagua}} \le 3\,P_{\text{Pequeña}}
$$

*Ciudades nuevas:*

$$
\mathrm{prod}_{i} \le 3\sum_{j\in J} P_j\,x_{ij}
$$

para todo $i\in I^{\mathrm{new}}$.

**3) Balance producción–despachos por ciudad**

$$
\mathrm{prod}_{i} = \sum_{k\in K}\sum_{f\in F} y_{ikf}
$$

para todo $i\in I$.

**4) A lo más una planta por ciudad nueva**

$$
\sum_{j\in J} x_{ij} \le 1
$$

para todo $i\in I^{\mathrm{new}}$.

**5) Elección única del modo de transporte**

$$
\sum_{f\in F} z_f = 1
$$

**6) Activación de flujos por modo (Big-M)**

$$
y_{ikf} \le M\,z_f
$$

para todo $i\in I$, $k\in K$, $f\in F$.

**7) Naturaleza de variables**

$$
x_{ij}\in\{0,1\},\ z_f\in\{0,1\},\ y_{ikf}\in\mathbb{Z}_{\ge 0},\ \mathrm{prod}_i\in\mathbb{R}_{\ge 0}.
$$





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




















