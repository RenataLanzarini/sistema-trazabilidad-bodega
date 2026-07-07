# Tabla Calendario

## Objetivo

Usar una tabla calendario unica para comparar recepcion, produccion, movimientos, ventas, calidad, fermentacion, ordenes de trabajo y cortes teoricos.

## Columnas recomendadas

- `Fecha`
- `Anio`
- `MesNumero`
- `MesNombre`
- `AnioMes`
- `Trimestre`
- `Semana`
- `Dia`
- `DiaSemanaNumero`
- `DiaSemanaNombre`
- `EsFinDeSemana`
- `InicioMes`
- `FinMes`
- `Cosecha` si se desea alinear periodos vitivinicolas.

## Relaciones sugeridas

- `DimFecha[Fecha]` -> `vw_produccion[fecha_recepcion]`
- `DimFecha[Fecha]` -> `vw_produccion[fecha_lote]`
- `DimFecha[Fecha]` -> `vw_movimientos[fecha_movimiento]`
- `DimFecha[Fecha]` -> `vw_comercial[fecha_venta]`
- `DimFecha[Fecha]` -> `vw_calidad[fecha]`
- `DimFecha[Fecha]` -> `vw_ordenes_trabajo[fecha]`
- `DimFecha[Fecha]` -> `vw_ordenes_trabajo[fecha_completada]`
- `DimFecha[Fecha]` -> `vw_cortes_teoricos[fecha]`

Cuando una vista tenga mas de una fecha, dejar una relacion activa principal y usar `USERELATIONSHIP` en medidas especificas.

## DAX sugerido

```DAX
DimFecha =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2035, 12, 31 ) ),
    "Anio", YEAR ( [Date] ),
    "MesNumero", MONTH ( [Date] ),
    "MesNombre", FORMAT ( [Date], "mmmm" ),
    "AnioMes", FORMAT ( [Date], "YYYY-MM" ),
    "Trimestre", "T" & FORMAT ( [Date], "Q" ),
    "Semana", WEEKNUM ( [Date], 2 ),
    "Dia", DAY ( [Date] ),
    "DiaSemanaNumero", WEEKDAY ( [Date], 2 ),
    "DiaSemanaNombre", FORMAT ( [Date], "dddd" ),
    "EsFinDeSemana", WEEKDAY ( [Date], 2 ) > 5,
    "InicioMes", DATE ( YEAR ( [Date] ), MONTH ( [Date] ), 1 ),
    "FinMes", EOMONTH ( [Date], 0 )
)
```

Renombrar la columna `[Date]` a `[Fecha]` en Power BI.
