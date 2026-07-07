# Diccionario Inicial de Datos

| Vista | Campo | Descripcion | Origen | Uso Power BI | Tipo |
|---|---|---|---|---|---|
| vw_stock_actual | bodega_id | Identificador de bodega | bodegas/piletas/lotes | Relacion y filtro | Dimension |
| vw_stock_actual | bodega_nombre | Nombre de bodega | bodegas | Segmentador | Atributo |
| vw_stock_actual | lote_id | Identificador de lote | lotes | Relacion | Dimension |
| vw_stock_actual | lote_codigo | Codigo unico del lote | lotes | Filtro y detalle | Atributo |
| vw_stock_actual | pileta_id | Identificador de pileta | piletas | Relacion | Dimension |
| vw_stock_actual | pileta_codigo | Codigo de pileta | piletas | Filtro y matriz | Atributo |
| vw_stock_actual | capacidad_litros | Capacidad maxima de pileta | piletas | Capacidad total | Medida base |
| vw_stock_actual | litros_stock | Litros calculados desde movimientos | movimientos_fisicos | Stock actual | Medida |
| vw_stock_actual | porcentaje_ocupacion | Ocupacion de pileta | calculado | KPI | Medida |
| vw_produccion | numero_ciu | Codigo CIU de recepcion | recepciones_uva | Trazabilidad de origen | Atributo |
| vw_produccion | fecha_recepcion | Fecha de ingreso de uva | recepciones_uva | Calendario | Dimension |
| vw_produccion | kilos_recibidos | Kilos declarados recibidos | recepciones_uva | Kg uva recibida | Medida |
| vw_produccion | brix_real | Brix medido | recepciones_uva | Calidad inicial | Medida |
| vw_produccion | finca | Finca registrada | recepciones_uva | Segmentador | Atributo |
| vw_produccion | origen_uva_nombre | Origen de uva | origenes_uva | Segmentador | Atributo |
| vw_produccion | variedad_nombre | Variedad | variedades | Segmentador | Atributo |
| vw_movimientos | operacion_productiva_id | Operacion que agrupa movimientos | operaciones_productivas | Drill-through | Dimension |
| vw_movimientos | tipo_operacion | Tipo de operacion | tipos_operacion | Segmentador | Atributo |
| vw_movimientos | fecha_movimiento | Fecha del movimiento fisico | movimientos_fisicos | Calendario | Dimension |
| vw_movimientos | litros | Litros movidos | movimientos_fisicos | Litros movidos | Medida |
| vw_movimientos | pileta_origen_codigo | Pileta origen | piletas | Trazabilidad fisica | Atributo |
| vw_movimientos | pileta_destino_codigo | Pileta destino | piletas | Trazabilidad fisica | Atributo |
| vw_trazabilidad | lote_padre_id | Lote origen | relaciones_genealogicas_lote | Grafo | Dimension |
| vw_trazabilidad | lote_hijo_id | Lote resultante | relaciones_genealogicas_lote | Grafo | Dimension |
| vw_trazabilidad | litros_aportados | Litros aportados por lote padre | relaciones_genealogicas_lote | Peso de arista | Medida |
| vw_trazabilidad | tipo_relacion | Mezcla, division u otra relacion | relaciones_genealogicas_lote | Segmentador | Atributo |
| vw_calidad | tipo_registro | Analisis o fermentacion | calculado | Segmentador | Atributo |
| vw_calidad | fecha | Fecha del dato de calidad | analisis/fermentacion | Calendario | Dimension |
| vw_calidad | alcohol | Alcohol | analisis_enologicos | Promedio alcohol | Medida |
| vw_calidad | brix | Brix | analisis_enologicos | Promedio Brix | Medida |
| vw_calidad | ph | pH | analisis_enologicos | Promedio pH | Medida |
| vw_calidad | grado_baume | Grado Baume | mediciones_fermentacion | Promedio Baume | Medida |
| vw_calidad | temperatura | Temperatura | mediciones_fermentacion | Temperatura promedio | Medida |
| vw_comercial | cliente_id | Cliente | clientes | Relacion | Dimension |
| vw_comercial | fecha_venta | Fecha de venta | ventas_granel | Calendario | Dimension |
| vw_comercial | litros | Litros vendidos | venta_granel_detalles | Litros vendidos | Medida |
| vw_ordenes_trabajo | completada | Estado operativo | ordenes_trabajo | KPI pendientes/completadas | Atributo |
| vw_ordenes_trabajo | fecha | Fecha planificada | ordenes_trabajo | Calendario | Dimension |
| vw_ordenes_trabajo | fecha_completada | Fecha de cierre | ordenes_trabajo | Analisis de cumplimiento | Dimension |
| vw_cortes_teoricos | volumen_al_corte | Volumen planificado | corte_teorico_detalles | Simulacion | Medida |
| vw_cortes_teoricos | volumen_actual_snapshot | Foto de volumen al momento | corte_teorico_detalles | Comparacion | Medida |
| vw_cortes_teoricos | alcohol | Snapshot alcohol | corte_teorico_detalles | Calidad simulada | Medida |
| vw_cortes_teoricos | ph | Snapshot pH | corte_teorico_detalles | Calidad simulada | Medida |
