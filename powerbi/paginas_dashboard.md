# Paginas del Dashboard

## Dashboard Ejecutivo

- Objetivo: vision global de bodega, stock, produccion, ventas, calidad y tareas.
- KPIs: litros stock actual, kg uva recibida, litros vendidos, ordenes pendientes, promedio pH, promedio alcohol.
- Graficos: tarjetas KPI, tendencia mensual, stock por pileta, ventas por cliente.
- Filtros: bodega, cosecha, variedad, fecha.
- Vistas: `vw_stock_actual`, `vw_produccion`, `vw_comercial`, `vw_calidad`, `vw_ordenes_trabajo`.

## Produccion

- Objetivo: analizar recepciones, lotes y operaciones productivas.
- KPIs: kg uva recibida, lotes creados, litros movidos, promedio Brix.
- Graficos: recepcion por finca/origen, kg por variedad, lotes por estado, movimientos por tipo.
- Filtros: fecha, cosecha, variedad, finca, tipo de producto.
- Vistas: `vw_produccion`, `vw_movimientos`.

## Stock

- Objetivo: controlar stock actual por pileta, lote y ocupacion.
- KPIs: litros stock actual, capacidad total, capacidad ocupada %, piletas ocupadas.
- Graficos: matriz lote-pileta, barras de ocupacion, ranking de piletas.
- Filtros: bodega, deposito, pileta, lote, estado pileta.
- Vistas: `vw_stock_actual`, `vw_movimientos`.

## Trazabilidad

- Objetivo: visualizar genealogia padre-hijo y recorrido fisico.
- KPIs: lotes con genealogia, litros aportados, cantidad de relaciones.
- Graficos: grafo lote padre-hijo, tabla de aristas, movimientos del lote.
- Filtros: lote, variedad, cosecha, tipo relacion.
- Vistas: `vw_trazabilidad`, `vw_movimientos`, `vw_produccion`.

## Calidad

- Objetivo: seguir analisis enologicos y fermentacion.
- KPIs: promedio alcohol, promedio pH, promedio Brix, promedio Baume, temperatura promedio.
- Graficos: lineas por fecha, dispersion pH/alcohol, analisis por pileta.
- Filtros: fecha, lote, pileta, tipo registro.
- Vistas: `vw_calidad`.

## Comercial

- Objetivo: analizar ventas a granel.
- KPIs: litros vendidos, clientes activos, ventas por periodo.
- Graficos: ventas por cliente, litros por lote, tendencia mensual.
- Filtros: fecha, cliente, lote, pileta.
- Vistas: `vw_comercial`, `vw_stock_actual`.

## Ordenes de Trabajo

- Objetivo: controlar ejecucion operativa.
- KPIs: ordenes pendientes, ordenes completadas, cumplimiento por operario.
- Graficos: tablero pendientes/completadas, tareas por operario, OT por pileta.
- Filtros: fecha, tarea, operario, lote, pileta.
- Vistas: `vw_ordenes_trabajo`.

## Corte Teorico

- Objetivo: analizar simulaciones de corte y compararlas con datos actuales.
- KPIs: volumen al corte, componentes por corte, snapshots de alcohol y pH.
- Graficos: detalle de componentes, comparacion volumen actual vs planificado, calidad simulada.
- Filtros: fecha, corte, lote, pileta, responsable.
- Vistas: `vw_cortes_teoricos`, `vw_stock_actual`, `vw_calidad`.

## Reportes

- Objetivo: generar tablas exportables y reportes operativos.
- KPIs: segun reporte.
- Graficos: tablas detalladas, matrices, filtros avanzados.
- Filtros: bodega, fecha, lote, pileta, responsable.
- Vistas: todas las vistas analiticas.
