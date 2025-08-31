# 01 — Diseño de la Red de Distribución

Este proyecto resuelve la localización de plantas (tipo pequeña/grande) y la asignación de flujos a 6 regiones durante 3 años, minimizando costos de apertura, fijos, variables y de transporte. Se modela en **PuLP** y se visualiza la solución en un **mapa interactivo (Folium)**.

## Contexto
Funnys Company enfrenta un aumento de demanda y debe rediseñar su red con posibles plantas en Antofagasta, Valparaíso, Santiago, **Rancagua**, Concepción y Puerto Montt. Tres alternativas de transporte (AT1, AT2, AT3) con costos unitarios por ciudad-región.

## Formulación (resumen)
**Variables:**  
- \(x_{c,p}\in\{0,1\}\): abrir planta tipo \(p\in\{\text{Pequeña, Grande}\}\) en ciudad \(c\).  
- \(y_{c,r,m,t}\ge 0\): flujo desde ciudad \(c\) a región \(r\) por modo \(m\) en año \(t\).

**Función objetivo (min):** costos de apertura + fijos (+ multiplicador por 3 años si corresponde) + variables por unidad + transporte.

**Restricciones clave:**
1. **Demanda por región y año:** \(\sum_{c,m} y_{c,r,m,t}\ge D_{r,t}\).
2. **Capacidad por ciudad y año:** \(\sum_{r,m} y_{c,r,m,t}\le \sum_{p} P_p\,x_{c,p}\).
3. **A lo más una planta por ciudad:** \(\sum_p x_{c,p}\le 1\).

## Supuestos
Horizonte de 3 años sin inventarios; decisiones de apertura al inicio y vigentes todo el horizonte; flujos continuos; costos variables por ciudad (independientes del tipo); mix de transporte permitido; conectividad completa ciudad-región-modo.

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
