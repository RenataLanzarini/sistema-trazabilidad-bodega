# Validacion Tecnica del Modelo SQL para Power BI

Este informe audita las vistas analiticas creadas para Power BI. No reemplaza la validacion con datos reales en Power BI Desktop, pero deja identificados objetivos, granularidad, claves, riesgos y recomendaciones antes de construir el archivo `.pbix`.

## 1. `vw_stock_actual`

### Objetivo

Exponer stock actual por combinacion lote-pileta-bodega, calculado desde `movimientos_fisicos`, incluyendo capacidad y porcentaje de ocupacion.

### Tablas de origen

- `movimientos_fisicos`
- `operaciones_productivas`
- `lotes`
- `piletas`
- `bodegas`
- `depositos`
- `estados_pileta`
- `estados_lote`
- `variedades`

### Columnas expuestas

- `bodega_id`, `bodega_nombre`
- `lote_id`, `lote_codigo`, `cosecha`, `color`, `variedad_nombre`, `estado_lote`
- `pileta_id`, `pileta_codigo`, `pileta_nombre`, `estado_pileta`
- `deposito_id`, `deposito_nombre`
- `capacidad_litros`, `litros_stock`, `porcentaje_ocupacion`

### Claves principales

- Grano esperado: `lote_id` + `pileta_id`.
- No hay clave tecnica unica expuesta; puede crearse una columna calculada en Power BI: `lote_id & "-" & pileta_id`.

### Posibles claves foraneas para Power BI

- `bodega_id`
- `lote_id`
- `pileta_id`
- `deposito_id`

### Tipos de datos esperados

- IDs: entero.
- Nombres/codigos/estados: texto.
- `cosecha`: entero.
- `capacidad_litros`, `litros_stock`, `porcentaje_ocupacion`: decimal.

### Riesgos de duplicacion

- Si una pileta contiene varios lotes, la `capacidad_litros` se repite por lote. La medida `Capacidad Total = SUM(capacidad_litros)` puede sobrecontar.
- Para capacidad total conviene sumar capacidad por pileta unica o crear una dimension/vista de piletas.

### Riesgos de nulos

- `variedad_nombre`, `cosecha`, `color` pueden ser nulos.
- `porcentaje_ocupacion` puede ser nulo si la capacidad es cero o inexistente.

### Posibles problemas de rendimiento

- Agrega todos los movimientos con `UNION ALL`.
- En volumen alto puede requerir indices en `movimientos_fisicos(lote_id)`, `pileta_origen_id`, `pileta_destino_id`, `operacion_productiva_id`.

### Recomendaciones de optimizacion

- Crear vista materializada si el volumen de movimientos crece.
- Crear una vista separada `dim_piletas` para capacidad y evitar sobreconteo.
- En Power BI, medir capacidad con `SUMX(VALUES(pileta_id), MAX(capacidad_litros))`.

## 2. `vw_produccion`

### Objetivo

Exponer recepcion de uva, datos ampliados de CIU y lotes generados desde cada recepcion.

### Tablas de origen

- `recepciones_uva`
- `bodegas`
- `origenes_uva`
- `variedades`
- `usuarios`
- `lotes`
- `estados_lote`
- `tipos_producto`
- `calificaciones_vino`

### Columnas expuestas

- Datos de bodega: `bodega_id`, `bodega_nombre`
- Recepcion: `recepcion_uva_id`, `numero_ciu`, `fecha_recepcion`, `cosecha`, `kilos_recibidos`, `estado_recepcion`
- Campos CIU ampliados: `semana`, `rto`, `finca`, `inv`, `cambio`, `cuartel`, `tachos`, `chofer`, `cuit_cuil`, `camion`, `modelo`, `patente`, `bruto_kg`, `tara_kg`, `neto_kg`, `uva_real_kg`, `destino_vino`, `brix_real`, `tenor_azucar`, `vasija`
- Origen/variedad/responsable: `origen_uva_id`, `origen_uva_nombre`, `origen_uva_tipo`, `variedad_id`, `variedad_nombre`, `responsable_id`, `responsable_nombre`
- Lote: `lote_id`, `lote_codigo`, `fecha_lote`, `lote_color`, `estado_lote`, `tipo_producto`, `calificacion_vino`

### Claves principales

- Grano mixto: una fila por recepcion y lote asociado.
- Si una recepcion genera varios lotes, `recepcion_uva_id` se repite.

### Posibles claves foraneas para Power BI

- `bodega_id`
- `recepcion_uva_id`
- `origen_uva_id`
- `variedad_id`
- `responsable_id`
- `lote_id`

### Tipos de datos esperados

- Fechas: `fecha_recepcion`, `fecha_lote`.
- Numericos: kilos, kg de pesada, Brix, tenor, semana, tachos, cosecha.
- Texto: finca, patente, chofer, estado, codigo.

### Riesgos de duplicacion

- `kilos_recibidos` se duplica si una recepcion tiene mas de un lote.
- Medidas de kilos deben calcularse por `recepcion_uva_id` unica o usar una vista de recepciones separada.

### Riesgos de nulos

- Todos los datos ampliados de CIU pueden venir incompletos.
- `lote_id` puede ser nulo si la recepcion aun no genero lote.

### Posibles problemas de rendimiento

- Riesgo bajo para MVP.
- Puede crecer con recepciones historicas y campos de Excel.

### Recomendaciones de optimizacion

- Si se reportan kilos por recepcion, usar `SUMX(VALUES(recepcion_uva_id), MAX(kilos_recibidos))`.
- Considerar separar `fact_recepciones` y `fact_lotes_generados` en una futura version analitica.

## 3. `vw_movimientos`

### Objetivo

Exponer operaciones productivas y movimientos fisicos con lote, piletas origen/destino, litros, tipo de operacion y responsable.

### Tablas de origen

- `movimientos_fisicos`
- `operaciones_productivas`
- `bodegas`
- `tipos_operacion`
- `lotes`
- `variedades`
- `piletas`
- `usuarios`

### Columnas expuestas

- Bodega y operacion: `bodega_id`, `bodega_nombre`, `operacion_productiva_id`, `operacion_codigo_externo`, `fecha_operacion`, `estado_operacion`, `operacion_anulada`, `motivo_anulacion`, `tipo_operacion_id`, `tipo_operacion`
- Movimiento: `movimiento_fisico_id`, `movimiento_codigo_externo`, `fecha_movimiento`, `litros`, `estado_movimiento`, `observaciones`
- Lote/variedad: `lote_id`, `lote_codigo`, `cosecha`, `variedad_nombre`
- Piletas: `pileta_origen_id`, `pileta_origen_codigo`, `pileta_origen_nombre`, `pileta_destino_id`, `pileta_destino_codigo`, `pileta_destino_nombre`
- Responsable: `responsable_id`, `responsable_nombre`

### Claves principales

- `movimiento_fisico_id`.

### Posibles claves foraneas para Power BI

- `bodega_id`
- `operacion_productiva_id`
- `tipo_operacion_id`
- `lote_id`
- `pileta_origen_id`
- `pileta_destino_id`
- `responsable_id`

### Tipos de datos esperados

- Fechas: `fecha_operacion`, `fecha_movimiento`.
- Numericos: `litros`.
- Booleano: `operacion_anulada`.
- Texto: estados, codigos, nombres.

### Riesgos de duplicacion

- Bajo: grano por movimiento fisico.
- Una operacion con multiples movimientos repite datos de operacion, pero es correcto para analisis por movimiento.

### Riesgos de nulos

- `pileta_origen_id` nulo para entradas.
- `pileta_destino_id` nulo para salidas.
- `motivo_anulacion` nulo si no esta anulada.
- `variedad_nombre` puede ser nulo.

### Posibles problemas de rendimiento

- Es una vista central y puede crecer rapido.
- Filtros por fecha, lote y pileta son criticos.

### Recomendaciones de optimizacion

- Mantener indices en fecha, lote, origen, destino y operacion.
- Evitar relaciones activas simultaneas con origen y destino en la misma dimension pileta.
- Crear medidas separadas para entradas, salidas y trasiegos en DAX.

## 4. `vw_trazabilidad`

### Objetivo

Exponer aristas base de genealogia lote padre -> lote hijo, con litros aportados y operacion asociada.

### Tablas de origen

- `relaciones_genealogicas_lote`
- `operaciones_productivas`
- `bodegas`
- `tipos_operacion`
- `lotes`
- `variedades`
- `estados_lote`

### Columnas expuestas

- `relacion_genealogica_id`
- `bodega_id`, `bodega_nombre`
- `operacion_productiva_id`, `fecha_operacion`, `tipo_operacion`
- `tipo_relacion`, `litros_aportados`, `observaciones`
- Datos lote padre: `lote_padre_id`, `lote_padre_codigo`, `lote_padre_cosecha`, `lote_padre_variedad`, `lote_padre_estado`
- Datos lote hijo: `lote_hijo_id`, `lote_hijo_codigo`, `lote_hijo_cosecha`, `lote_hijo_variedad`, `lote_hijo_estado`

### Claves principales

- `relacion_genealogica_id`.

### Posibles claves foraneas para Power BI

- `bodega_id`
- `operacion_productiva_id`
- `lote_padre_id`
- `lote_hijo_id`

### Tipos de datos esperados

- Fecha: `fecha_operacion`.
- Numerico: `litros_aportados`.
- Texto: codigos, estados, tipo relacion.

### Riesgos de duplicacion

- Bajo a nivel arista.
- Para analizar un lote, hay que decidir si se filtra por padre, hijo o ambos; relaciones ambiguas pueden duplicar conteos.

### Riesgos de nulos

- Variedad y cosecha pueden ser nulas.
- Observaciones normalmente nulas.

### Posibles problemas de rendimiento

- Bajo en MVP.
- Grafo recursivo no esta resuelto por esta vista; Power BI debera construir exploracion con aristas base.

### Recomendaciones de optimizacion

- Mantener esta vista como aristas base.
- No agregar recursividad hasta conocer necesidad real del reporte.
- Para grafo avanzado, preparar una tabla de nodos separada en futuras fases.

## 5. `vw_calidad`

### Objetivo

Unificar analisis enologicos y mediciones de fermentacion en una vista comun para seguimiento por lote, pileta y fecha.

### Tablas de origen

- `analisis_enologicos`
- `mediciones_fermentacion`
- `bodegas`
- `lotes`
- `piletas`

### Columnas expuestas

- Identificacion: `tipo_registro`, `registro_id`, `bodega_id`, `bodega_nombre`, `lote_id`, `lote_codigo`, `pileta_id`, `pileta_codigo`, `codigo_externo`
- Contexto: `fecha`, `tipo`
- Analisis: `alcohol`, `azucar`, `volatil`, `acidez_total`, `ph`, `anhidrido_libre`, `anhidrido_total`, `extracto_seco`, `brix`, `observaciones`
- Fermentacion: `grado_baume`, `temperatura`

### Claves principales

- Clave compuesta recomendada: `tipo_registro` + `registro_id`.

### Posibles claves foraneas para Power BI

- `bodega_id`
- `lote_id`
- `pileta_id`

### Tipos de datos esperados

- Fecha: `fecha`.
- Numericos: alcohol, azucar, volatil, acidez, pH, anhidridos, extracto, Brix, Baume, temperatura.
- Texto: tipo, observaciones.

### Riesgos de duplicacion

- Bajo si se usa `tipo_registro` + `registro_id`.
- Si se usa solo `registro_id`, puede colisionar entre analisis y medicion.

### Riesgos de nulos

- Muy altos por diseno: los campos de analisis son nulos en registros de fermentacion, y Baume/temperatura son nulos en analisis.
- `lote_id` y `pileta_id` son opcionales.

### Posibles problemas de rendimiento

- Bajo en MVP.
- El `UNION ALL` es correcto, pero puede complicar medidas si se mezclan indicadores incompatibles.

### Recomendaciones de optimizacion

- Crear medidas que filtren por `tipo_registro` cuando corresponda.
- En visuales de fermentacion usar solo registros con `tipo_registro = "medicion_fermentacion"`.
- En visuales enologicos usar solo `tipo_registro = "analisis_enologico"`.

## 6. `vw_comercial`

### Objetivo

Exponer ventas a granel y detalle de litros vendidos por cliente, lote y pileta.

### Tablas de origen

- `ventas_granel`
- `operaciones_productivas`
- `bodegas`
- `clientes`
- `usuarios`
- `venta_granel_detalles`
- `lotes`
- `piletas`

### Columnas expuestas

- `bodega_id`, `bodega_nombre`
- `venta_granel_id`, `operacion_productiva_id`, `fecha_venta`, `documento`, `estado_venta`
- `cliente_id`, `cliente_nombre`
- `responsable_id`, `responsable_nombre`
- `venta_granel_detalle_id`, `litros`
- `lote_id`, `lote_codigo`
- `pileta_id`, `pileta_codigo`, `pileta_nombre`
- `venta_observaciones`, `detalle_observaciones`

### Claves principales

- `venta_granel_detalle_id`.

### Posibles claves foraneas para Power BI

- `bodega_id`
- `venta_granel_id`
- `operacion_productiva_id`
- `cliente_id`
- `responsable_id`
- `lote_id`
- `pileta_id`

### Tipos de datos esperados

- Fecha: `fecha_venta`.
- Numerico: `litros`.
- Texto: documento, estado, cliente, lote, pileta.

### Riesgos de duplicacion

- Una venta con varios detalles repite datos de cabecera. Es correcto si el grano es detalle.
- Conteo de ventas debe usar `DISTINCTCOUNT(venta_granel_id)`.

### Riesgos de nulos

- `documento` puede ser nulo.
- Observaciones pueden ser nulas.

### Posibles problemas de rendimiento

- Bajo a medio segun volumen comercial.

### Recomendaciones de optimizacion

- Definir claramente medidas por detalle y por cabecera.
- Usar `DISTINCTCOUNT` para cantidad de ventas.
- Evaluar vista separada de cabecera comercial si se necesitan metricas no repetidas.

## 7. `vw_ordenes_trabajo`

### Objetivo

Exponer ordenes operativas, estado pendiente/completada, tarea, operario, lote, pileta y datos de cumplimiento.

### Tablas de origen

- `ordenes_trabajo`
- `tareas_orden_trabajo`
- `usuarios`
- `lotes`
- `piletas`

### Columnas expuestas

- Identificacion: `orden_trabajo_id`, `codigo_externo`, `numero`
- Fechas/estado: `fecha`, `completada`, `estado_operativo`, `fecha_completada`
- Tarea/operario: `tarea_orden_trabajo_id`, `tarea_nombre`, `operario_id`, `operario_nombre`
- Lote/piletas: `lote_id`, `lote_codigo`, `pileta_id`, `pileta_codigo`, `pileta_origen_id`, `pileta_origen_codigo`, `pileta_destino_id`, `pileta_destino_codigo`
- Operacion: `operacion_productiva_id`
- Datos operativos: `volumen_lleno`, `variedad`, `anio`, `insumo`, `cantidad`, `litros_a_trasegar`, `lleno_disponible`, `litros_por_cm`, `pasada_a_trazabilidad`, `so2l_real`, `observaciones`, `observaciones_completada`

### Claves principales

- `orden_trabajo_id`.

### Posibles claves foraneas para Power BI

- `tarea_orden_trabajo_id`
- `operario_id`
- `lote_id`
- `pileta_id`
- `pileta_origen_id`
- `pileta_destino_id`
- `operacion_productiva_id`

### Tipos de datos esperados

- Fechas: `fecha`, `fecha_completada`.
- Booleanos: `completada`, `pasada_a_trazabilidad`.
- Numericos: volumen, cantidad, litros, SO2.
- Texto: tarea, operario, codigos, observaciones.

### Riesgos de duplicacion

- Bajo: una fila por orden.

### Riesgos de nulos

- Muy altos por naturaleza operativa: tarea, operario, lote, pileta, operacion y fechas pueden ser opcionales.

### Posibles problemas de rendimiento

- Bajo para MVP.

### Recomendaciones de optimizacion

- Medidas de pendientes/completadas deben usar `estado_operativo`.
- Crear indicador de OT vencida en DAX si se define fecha objetivo.
- No relacionar simultaneamente `pileta_id`, `pileta_origen_id` y `pileta_destino_id` como activas contra la misma dimension.

## 8. `vw_cortes_teoricos`

### Objetivo

Exponer simulaciones de corte, detalles, componentes, volumen planificado y snapshots analiticos.

### Tablas de origen

- `cortes_teoricos`
- `usuarios`
- `operaciones_productivas`
- `corte_teorico_detalles`
- `lotes`
- `piletas`

### Columnas expuestas

- Corte: `corte_teorico_id`, `corte_codigo_externo`, `fecha`, `corte_nombre`, `responsable_id`, `responsable_nombre`, `operacion_productiva_id`, `fecha_operacion_vinculada`, `observaciones`
- Detalle: `corte_teorico_detalle_id`, `detalle_codigo_externo`, `lote_id`, `lote_codigo`, `pileta_id`, `pileta_codigo`, `pileta_nombre`
- Volumen/snapshots: `volumen_al_corte`, `varietal_snapshot`, `volumen_actual_snapshot`, `alcohol`, `acidez_volatil`, `acidez_total`, `ph`, `so2_libre`, `so2_total`

### Claves principales

- Grano esperado: detalle de corte.
- Clave principal de detalle: `corte_teorico_detalle_id`.
- Si un corte no tiene detalle, `corte_teorico_detalle_id` sera nulo por `LEFT JOIN`.

### Posibles claves foraneas para Power BI

- `corte_teorico_id`
- `responsable_id`
- `operacion_productiva_id`
- `lote_id`
- `pileta_id`

### Tipos de datos esperados

- Fechas: `fecha`, `fecha_operacion_vinculada`.
- Numericos: volumen, alcohol, acidez, pH, SO2.
- Texto: codigos, nombres, varietal snapshot.

### Riesgos de duplicacion

- Una cabecera de corte se repite por cada detalle. Es correcto para analizar componentes.
- Conteo de cortes debe usar `DISTINCTCOUNT(corte_teorico_id)`.

### Riesgos de nulos

- Detalles pueden ser nulos si el corte no tiene componentes.
- Operacion vinculada puede ser nula.
- Snapshots analiticos pueden ser nulos.

### Posibles problemas de rendimiento

- Bajo para MVP.

### Recomendaciones de optimizacion

- Usar medidas por detalle para volumen.
- Usar `DISTINCTCOUNT` para cantidad de cortes.
- Diferenciar visualmente simulacion de operacion real.

## Auditoria general

### Consistencia de nombres

Las vistas usan nombres claros y consistentes en snake_case. Se observa una convencion razonable:

- IDs terminan en `_id`.
- Codigos terminan en `_codigo`.
- Fechas se nombran segun contexto.
- Nombres descriptivos se exponen como `_nombre`.

Riesgo menor: algunas columnas de fecha se llaman simplemente `fecha` en vistas especificas (`vw_calidad`, `vw_cortes_teoricos`) mientras otras usan nombres contextuales (`fecha_movimiento`, `fecha_venta`). Power BI puede manejarlo, pero conviene nombrarlas en el modelo con alias amigables.

### Convenciones

Conviene mantener:

- vistas de hechos con prefijo `vw_`;
- columnas tecnicas visibles para relaciones;
- textos de negocio para segmentadores;
- medidas en DAX, no en SQL, salvo calculos de lectura directa como `porcentaje_ocupacion`.

### Compatibilidad con modelo estrella

El modelo es compatible con estrella liviana, pero todavia no expone dimensiones separadas. Para MVP alcanza con vistas denormalizadas. Para crecimiento conviene agregar vistas `dim_bodega`, `dim_lote`, `dim_pileta`, `dim_usuario`, `dim_cliente`, `dim_variedad`, `dim_fecha`.

### Facilidad para relaciones en Power BI

Buena en general, con cuidados:

- `vw_stock_actual`: grano lote-pileta.
- `vw_produccion`: grano recepcion-lote; riesgo de duplicar kilos.
- `vw_calidad`: clave compuesta `tipo_registro + registro_id`.
- `vw_trazabilidad`: dos roles de lote, padre e hijo.
- `vw_movimientos`: dos roles de pileta, origen y destino.
- `vw_ordenes_trabajo`: varias piletas posibles.

### Medidas que conviene dejar en DAX

- Kg uva recibida sin duplicar por recepcion.
- Capacidad total sin duplicar por lote.
- Cantidad de ventas.
- Cantidad de cortes.
- Entradas, salidas y trasiegos.
- % merma.
- % ocupacion ponderada.
- OT vencidas.
- Ultimo analisis por lote/pileta.

### Columnas posiblemente innecesarias

No eliminarlas todavia; pueden servir para auditoria. Pero en Power BI se pueden ocultar:

- Observaciones largas si no se usan en paginas.
- Datos de camiones/chofer en paginas ejecutivas.
- Codigos externos si no se usan como filtro.
- `motivo_anulacion` fuera de reportes de auditoria.

### Riesgos generales detectados

1. Sobreconteo de capacidad en `vw_stock_actual` por repeticion de pileta por lote.
2. Sobreconteo de kilos en `vw_produccion` si una recepcion genera varios lotes.
3. Relaciones ambiguas en vistas con doble rol: lote padre/hijo, pileta origen/destino.
4. Nulos esperados en calidad, ordenes y cortes por datos parciales.
5. Grafo de trazabilidad necesita interpretacion de aristas, no una relacion simple.

### Recomendaciones generales

- Crear medidas DAX defensivas con `DISTINCTCOUNT`, `VALUES` y `SUMX`.
- Ocultar columnas tecnicas no usadas por el usuario final.
- Validar totales contra consultas SQL simples antes de publicar.
- Considerar dimensiones dedicadas en PBI-7 si el modelo crece.
- Mantener vistas como capa de lectura y no replicar reglas de negocio en Power BI.
