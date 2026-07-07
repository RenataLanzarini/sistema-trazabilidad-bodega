# Medidas DAX Base

## Litros Stock Actual

- Objetivo: total de litros disponibles calculados desde movimientos.
- Formula:

```DAX
Litros Stock Actual = SUM ( vw_stock_actual[litros_stock] )
```

- Origen: `vw_stock_actual`
- Paginas: Ejecutivo, Stock, Comercial, Corte Teorico

## Kg Uva Recibida

- Objetivo: total de kilos de uva ingresados por CIU.
- Formula:

```DAX
Kg Uva Recibida = SUM ( vw_produccion[kilos_recibidos] )
```

- Origen: `vw_produccion`
- Paginas: Ejecutivo, Produccion

## Litros Movidos

- Objetivo: total de litros registrados en movimientos fisicos.
- Formula:

```DAX
Litros Movidos = SUM ( vw_movimientos[litros] )
```

- Origen: `vw_movimientos`
- Paginas: Produccion, Stock, Trazabilidad

## Litros Merma

- Objetivo: total de litros perdidos por merma.
- Formula sugerida:

```DAX
Litros Merma =
CALCULATE (
    [Litros Movidos],
    CONTAINSSTRING ( LOWER ( vw_movimientos[tipo_operacion] ), "merma" )
)
```

- Origen: `vw_movimientos`
- Paginas: Ejecutivo, Produccion, Stock

## % Merma

- Objetivo: proporcion de merma sobre litros movidos.
- Formula:

```DAX
% Merma = DIVIDE ( [Litros Merma], [Litros Movidos] )
```

- Origen: `vw_movimientos`
- Paginas: Ejecutivo, Produccion

## Litros Vendidos

- Objetivo: total de litros vendidos a granel.
- Formula:

```DAX
Litros Vendidos = SUM ( vw_comercial[litros] )
```

- Origen: `vw_comercial`
- Paginas: Ejecutivo, Comercial

## Productos Terminados

- Objetivo: cantidad de registros de producto terminado.
- Formula sugerida si se carga tabla/vista de productos terminados:

```DAX
Productos Terminados = COUNTROWS ( vw_productos_terminados )
```

- Origen: tabla o vista futura de productos terminados
- Paginas: Ejecutivo, Produccion

## Capacidad Total

- Objetivo: capacidad total de piletas presentes en stock.
- Formula:

```DAX
Capacidad Total = SUM ( vw_stock_actual[capacidad_litros] )
```

- Origen: `vw_stock_actual`
- Paginas: Ejecutivo, Stock

## Capacidad Ocupada %

- Objetivo: ocupacion ponderada de capacidad.
- Formula:

```DAX
Capacidad Ocupada % = DIVIDE ( [Litros Stock Actual], [Capacidad Total] )
```

- Origen: `vw_stock_actual`
- Paginas: Ejecutivo, Stock

## Ordenes Pendientes

- Objetivo: contar ordenes de trabajo no completadas.
- Formula:

```DAX
Ordenes Pendientes =
CALCULATE (
    COUNTROWS ( vw_ordenes_trabajo ),
    vw_ordenes_trabajo[estado_operativo] = "Pendiente"
)
```

- Origen: `vw_ordenes_trabajo`
- Paginas: Ejecutivo, Ordenes de Trabajo

## Ordenes Completadas

- Objetivo: contar ordenes de trabajo completadas.
- Formula:

```DAX
Ordenes Completadas =
CALCULATE (
    COUNTROWS ( vw_ordenes_trabajo ),
    vw_ordenes_trabajo[estado_operativo] = "Completada"
)
```

- Origen: `vw_ordenes_trabajo`
- Paginas: Ejecutivo, Ordenes de Trabajo

## Promedio Brix

- Objetivo: promedio de Brix en recepcion o calidad.
- Formula:

```DAX
Promedio Brix = AVERAGE ( vw_calidad[brix] )
```

- Origen: `vw_calidad`
- Paginas: Produccion, Calidad

## Promedio Alcohol

- Objetivo: promedio de alcohol en analisis.
- Formula:

```DAX
Promedio Alcohol = AVERAGE ( vw_calidad[alcohol] )
```

- Origen: `vw_calidad`
- Paginas: Ejecutivo, Calidad, Corte Teorico

## Promedio pH

- Objetivo: promedio de pH en analisis.
- Formula:

```DAX
Promedio pH = AVERAGE ( vw_calidad[ph] )
```

- Origen: `vw_calidad`
- Paginas: Ejecutivo, Calidad, Corte Teorico

## Promedio Baume

- Objetivo: promedio de Baume durante fermentacion.
- Formula:

```DAX
Promedio Baume = AVERAGE ( vw_calidad[grado_baume] )
```

- Origen: `vw_calidad`
- Paginas: Calidad

## Temperatura Promedio

- Objetivo: promedio de temperatura durante fermentacion.
- Formula:

```DAX
Temperatura Promedio = AVERAGE ( vw_calidad[temperatura] )
```

- Origen: `vw_calidad`
- Paginas: Calidad
