# Checklist de Importacion en Power BI Desktop

Usar este checklist al cargar cada vista analitica en Power BI Desktop.

## Checklist por vista

### `vw_stock_actual`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas, si aplica.
- [ ] IDs sin duplicados segun grano `lote_id + pileta_id`.
- [ ] Relaciones posibles con bodega, lote, pileta y deposito.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_produccion`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha_recepcion`, `fecha_lote`.
- [ ] IDs sin duplicados segun uso: `recepcion_uva_id` puede repetirse por lote.
- [ ] Relaciones posibles con bodega, recepcion, origen, variedad, responsable y lote.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_movimientos`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha_operacion`, `fecha_movimiento`.
- [ ] IDs sin duplicados: `movimiento_fisico_id`.
- [ ] Relaciones posibles con bodega, operacion, tipo operacion, lote, pileta origen, pileta destino y responsable.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_trazabilidad`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha_operacion`.
- [ ] IDs sin duplicados: `relacion_genealogica_id`.
- [ ] Relaciones posibles con bodega, operacion, lote padre y lote hijo.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_calidad`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha`.
- [ ] IDs sin duplicados usando clave compuesta `tipo_registro + registro_id`.
- [ ] Relaciones posibles con bodega, lote y pileta.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_comercial`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha_venta`.
- [ ] IDs sin duplicados: `venta_granel_detalle_id`.
- [ ] Relaciones posibles con bodega, venta, operacion, cliente, responsable, lote y pileta.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_ordenes_trabajo`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha`, `fecha_completada`.
- [ ] IDs sin duplicados: `orden_trabajo_id`.
- [ ] Relaciones posibles con tarea, operario, lote, pileta y operacion.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

### `vw_cortes_teoricos`

- [ ] Vista carga correctamente.
- [ ] Tipos de datos correctos.
- [ ] Fechas reconocidas: `fecha`, `fecha_operacion_vinculada`.
- [ ] IDs sin duplicados segun grano: `corte_teorico_detalle_id`; `corte_teorico_id` puede repetirse por detalle.
- [ ] Relaciones posibles con corte, responsable, operacion, lote y pileta.
- [ ] Sin errores de importacion.
- [ ] Sin columnas innecesarias visibles al usuario final.
- [ ] Rendimiento aceptable.

## Checklist general del modelo

- [ ] Tabla calendario creada.
- [ ] Relaciones de fecha revisadas.
- [ ] Relaciones ambiguas desactivadas o controladas.
- [ ] Tipos decimal aplicados a litros, kilos y porcentajes.
- [ ] IDs configurados como numeros enteros.
- [ ] Columnas de observaciones ocultas si no se usan.
- [ ] Medidas DAX comparadas contra SQL.
- [ ] Totales de stock validados contra `vw_stock_actual`.
- [ ] Totales de uva validados sin duplicar recepciones.
- [ ] Totales de ventas validados por detalle.
- [ ] Capacidad validada sin duplicar piletas.
- [ ] Refresco de datos probado.
- [ ] Rendimiento aceptable en filtros principales.
- [ ] Ningun grafico queda en blanco por relacion incorrecta.
