# Modelo Analitico Propuesto

## Objetivo

Construir un modelo de lectura para Power BI que permita analizar stock, produccion, trazabilidad, calidad, ventas, ordenes de trabajo y cortes teoricos sin afectar el backend operacional.

## Dimensiones principales

- `DimFecha`: calendario comun para fechas de recepcion, movimientos, ventas, analisis, fermentacion, OT y cortes.
- `DimBodega`: bodega propietaria de la informacion.
- `DimPileta`: pileta/tanque, capacidad, deposito y estado.
- `DimLote`: lote, codigo, cosecha, color, estado, variedad y tipo de producto.
- `DimVariedad`: variedad principal u origen varietal.
- `DimUsuario`: responsables, operarios y usuarios de procesos.
- `DimCliente`: clientes para venta a granel.
- `DimTipoOperacion`: tipos de operaciones productivas.
- `DimTareaOrdenTrabajo`: tareas operativas.

## Hechos principales

- `FactStockActual`: stock calculado desde `movimientos_fisicos`.
- `FactProduccion`: recepciones de uva y nacimiento de lotes.
- `FactMovimientos`: movimientos fisicos y operaciones productivas.
- `FactTrazabilidad`: aristas padre-hijo entre lotes.
- `FactCalidad`: analisis enologicos y mediciones de fermentacion.
- `FactComercial`: ventas a granel.
- `FactOrdenesTrabajo`: planificacion y avance operativo.
- `FactCortesTeoricos`: simulaciones de corte.

## Relaciones recomendadas

- `DimFecha[Fecha]` con fechas de cada vista de hechos.
- `DimBodega[bodega_id]` con todas las vistas que expongan `bodega_id`.
- `DimLote[lote_id]` con stock, produccion, movimientos, trazabilidad, calidad, comercial y cortes.
- `DimPileta[pileta_id]` con stock, calidad, comercial, ordenes y cortes.
- `DimUsuario[usuario_id]` con responsables u operarios.
- `DimCliente[cliente_id]` con comercial.

## Modelo estrella

Para el MVP conviene un modelo estrella liviano: vistas de hechos en el centro y dimensiones reutilizables alrededor. Si una dimension todavia no se publica como vista dedicada, Power BI puede derivarla temporalmente desde las vistas analiticas, aunque a futuro conviene crear vistas `dim_*`.

## Vistas por pagina

- Ejecutivo: `vw_stock_actual`, `vw_produccion`, `vw_comercial`, `vw_ordenes_trabajo`, `vw_calidad`.
- Produccion: `vw_produccion`, `vw_movimientos`, `vw_stock_actual`.
- Stock: `vw_stock_actual`, `vw_movimientos`.
- Trazabilidad: `vw_trazabilidad`, `vw_movimientos`, `vw_produccion`.
- Calidad: `vw_calidad`.
- Comercial: `vw_comercial`, `vw_stock_actual`.
- Ordenes de Trabajo: `vw_ordenes_trabajo`.
- Corte Teorico: `vw_cortes_teoricos`, `vw_stock_actual`, `vw_calidad`.
- Reportes: todas las vistas segun necesidad.
