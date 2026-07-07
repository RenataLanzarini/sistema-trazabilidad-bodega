# Checklist de Construccion en Power BI Desktop

Esta guia transforma la documentacion del Centro de Control Vitivinicola Lanzarini en pasos practicos para construir el informe completo en Power BI Desktop.

## 1. Preparacion previa

### Verificaciones tecnicas

- Confirmar que PostgreSQL esta activo.
- Confirmar que la base del sistema esta actualizada.
- Confirmar que las vistas SQL del schema `powerbi` fueron creadas en PostgreSQL.
- Confirmar credenciales de lectura para Power BI.
- Confirmar nombre del servidor, puerto, base de datos y usuario.
- Abrir Power BI Desktop.
- Importar el tema desde `powerbi/theme/LanzariniTheme.json`.

### Verificacion de artefactos

- Vistas SQL: `powerbi/vistas_sql/`.
- Medidas DAX sugeridas: `powerbi/dax/medidas_base.md`.
- Design system: `powerbi/design/`.
- Mockups: `powerbi/mockups/`.
- Modelo analitico: `powerbi/modelo_analitico.md`.

## 2. Orden de carga de datos

### Orden recomendado

1. Tabla calendario.
2. `vw_stock_actual`.
3. `vw_produccion`.
4. `vw_movimientos`.
5. `vw_trazabilidad`.
6. `vw_calidad`.
7. `vw_comercial`.
8. `vw_ordenes_trabajo`.
9. `vw_cortes_teoricos`.

### Recomendaciones

- Para el MVP, usar modo **Import**.
- Cargar solo columnas necesarias para el dashboard.
- Revisar tipos de datos despues de importar.
- Fechas deben quedar como `Date` o `Date/Time`.
- IDs deben quedar como enteros.
- Litros, kilos y porcentajes deben quedar numericos.
- No cargar tablas transaccionales directas si ya existe una vista analitica equivalente.

## 3. Relaciones

### Calendario

Relacionar `DimFecha[Fecha]` con:

- `vw_produccion[fecha_recepcion]`.
- `vw_produccion[fecha_lote]`.
- `vw_movimientos[fecha_movimiento]`.
- `vw_calidad[fecha]`.
- `vw_comercial[fecha_venta]`.
- `vw_ordenes_trabajo[fecha]`.
- `vw_ordenes_trabajo[fecha_completada]`.
- `vw_cortes_teoricos[fecha]`.

Si Power BI no permite multiples relaciones activas entre las mismas tablas, dejar activa la relacion principal y usar `USERELATIONSHIP` en medidas especificas.

### Bodega

- Relacionar por `bodega_id` entre vistas.
- Si se crea `DimBodega`, usarla como dimension central.

### Lote

- Relacionar `lote_id` entre stock, produccion, movimientos, calidad, comercial, trazabilidad y cortes.
- Para trazabilidad, considerar dos relaciones: `lote_padre_id` y `lote_hijo_id`. Mantener una activa y otra inactiva si hace falta.

### Pileta

- Relacionar `pileta_id` entre stock, calidad, comercial, ordenes y cortes.
- Para movimientos, `pileta_origen_id` y `pileta_destino_id` requieren relaciones separadas.

### Cliente

- Relacionar `cliente_id` en `vw_comercial`.

### Usuario

- Usar `responsable_id` u `operario_id` segun vista.
- Si se crea `DimUsuario`, relacionarla contra responsables y operarios con relaciones activas/inactivas segun pagina.

### Tipo operacion

- Usar `tipo_operacion_id` en movimientos y operaciones.
- Si no se crea dimension, usar `tipo_operacion` desde `vw_movimientos`.

### Variedad

- Usar `variedad_nombre` o `variedad_id` cuando este disponible.
- Para MVP, puede usarse como atributo desde las vistas.

## 4. Medidas DAX

### Donde copiarlas

Las medidas base estan documentadas en:

`powerbi/dax/medidas_base.md`

### Crear primero

1. Litros Stock Actual.
2. Kg Uva Recibida.
3. Litros Movidos.
4. Litros Vendidos.
5. Capacidad Total.
6. Capacidad Ocupada %.
7. Ordenes Pendientes.
8. Ordenes Completadas.
9. Promedio Brix.
10. Promedio Alcohol.
11. Promedio pH.
12. Promedio Baume.
13. Temperatura Promedio.
14. Litros Merma.
15. % Merma.

### Imprescindibles por pagina

- Dashboard Ejecutivo: stock, kg uva, ventas, merma, ordenes, calidad.
- Produccion: kg uva, promedio Brix, lotes, movimientos.
- Stock: stock, capacidad, ocupacion.
- Trazabilidad: litros aportados, litros movidos, relaciones.
- Calidad: Brix, alcohol, pH, Baume, temperatura.
- Comercial: litros vendidos, clientes, ventas.
- Ordenes: pendientes, completadas, cumplimiento.
- Corte Teorico: volumen al corte, componentes, snapshots.
- Reportes: medidas generales y conteos por entidad.

## 5. Construccion de paginas

## Dashboard Ejecutivo

### Orden de armado

1. Crear fondo crema.
2. Crear menu lateral.
3. Crear header con banner fotografico y titulo.
4. Agregar filtros globales.
5. Crear seis tarjetas KPI.
6. Crear graficos principales.
7. Crear tablas inferiores.
8. Configurar interacciones y navegacion.

### Visuales

- KPIs: uva recibida, litros en produccion, stock actual, productos terminados, ventas granel, % merma.
- Graficos: produccion mensual, stock por variedad, capacidad de piletas, ventas, merma, calidad.
- Tablas: ultimos movimientos, ultimas operaciones, alertas.

### Filtros

Ano, cosecha, bodega, variedad, pileta, estado, cliente, operacion.

### Navegacion

Cada KPI debe permitir ir o filtrar la pagina relacionada.

## Produccion

### Orden de armado

1. Reutilizar menu y header.
2. Agregar filtros de produccion.
3. Crear KPIs productivos.
4. Agregar graficos por fecha, variedad y finca.
5. Agregar tablas de recepciones y lotes.
6. Configurar drill-through a Stock y Trazabilidad.

### Visuales

- Columnas de kg por mes.
- Barras de kg por variedad.
- Barras por finca/origen.
- Linea de Brix promedio.
- Tabla de CIU y lotes.

## Stock

### Orden de armado

1. Crear KPIs de stock y capacidad.
2. Crear matriz lote-pileta.
3. Crear barras de ocupacion por pileta.
4. Crear stock por variedad.
5. Agregar tabla de ultimos movimientos.
6. Agregar panel lateral de detalle.

### Visuales

- Matriz stock.
- Barras de ocupacion.
- Barras por variedad.
- Tabla de movimientos.

### Interacciones

Click en pileta filtra movimientos y panel. Click en lote permite drill-through a Trazabilidad.

## Trazabilidad

### Orden de armado

1. Crear filtros especificos de lote y direccion.
2. Reservar area central para grafo.
3. Crear timeline cronologica.
4. Crear tabla de aristas.
5. Crear panel lateral de detalle.
6. Configurar navegacion a Stock, Calidad, Comercial y Produccion.

### Visuales

- Grafo o alternativa jerarquica.
- Timeline.
- Tabla de relaciones genealogicas.
- Tabla de movimientos del lote.

## Calidad

### Orden de armado

1. Crear KPIs enologicos.
2. Crear lineas de pH, alcohol, Brix, Baume y temperatura.
3. Agregar tabla de analisis.
4. Agregar tabla de fermentacion.
5. Crear panel lateral de ultimo analisis.

### Visuales

- Lineas temporales.
- Tarjetas de ultimo valor.
- Tabla analitica.

## Comercial

### Orden de armado

1. Crear KPIs comerciales.
2. Crear ventas por fecha.
3. Crear ventas por cliente.
4. Crear ventas por lote/pileta.
5. Agregar tabla comercial.
6. Configurar drill-through a Trazabilidad.

### Visuales

- Linea o columnas de ventas.
- Barras por cliente.
- Tabla de ventas granel.

## Ordenes de Trabajo

### Orden de armado

1. Crear KPIs de pendientes y completadas.
2. Crear tablero por estado.
3. Crear graficos por tarea y operario.
4. Crear tabla operativa.
5. Crear panel lateral de detalle.

### Visuales

- Barras pendientes/completadas.
- Barras por operario.
- Tabla de OT.
- Alertas de vencimiento o pendiente.

## Corte Teorico

### Orden de armado

1. Crear filtros por corte, fecha, lote y responsable.
2. Crear KPIs de volumen y componentes.
3. Crear grafico de componentes.
4. Crear comparacion de volumen snapshot vs actual.
5. Crear tabla de detalles.
6. Crear panel lateral.

### Visuales

- Barras o dona de componentes.
- Tabla de snapshots.
- Tarjetas de alcohol, pH y volumen.

## Reportes

### Orden de armado

1. Crear filtros avanzados.
2. Crear selector de tipo de reporte.
3. Agregar tablas exportables.
4. Agregar tarjetas resumen.
5. Configurar drill-through inverso hacia paginas de detalle.

### Visuales

- Tablas.
- Matrices.
- Tarjetas de resumen.

## 6. Diseno

### Menu lateral

- Fondo marron madera `#2B1E1A`.
- Item activo borravino `#3E244A`.
- Acento dorado `#B88646`.
- Mantener mismo orden en todas las paginas.

### Header

- Dashboard Ejecutivo puede usar imagen.
- Paginas operativas deben tener header mas limpio.
- Titulo siempre visible.

### Colores

- Fondo general crema.
- Tarjetas blancas.
- Texto principal oscuro.
- Estados segun paleta definida.

### Tarjetas

- Fondo blanco.
- Radio 8 px.
- Numero grande.
- Unidad visible.
- Tooltip con contexto.

### Tipografias

- Segoe UI o Aptos.
- No mezclar familias.
- Mantener jerarquia definida en design system.

### Iconografia

- Iconos lineales.
- Una familia visual.
- Icono solo cuando aporte reconocimiento rapido.

### Fondos

- Fotografias solo en header o separadores.
- No colocar tablas sobre imagenes.

### Graficos

- Titulos claros.
- Colores de datos separados de colores de interfaz.
- Evitar exceso de categorias.

## 7. Trazabilidad

### Representar el grafo en Power BI

Power BI no trae un grafo genealogico avanzado nativo. Opciones:

1. Visual personalizado de grafo/red.
2. Visual de decomposition tree como alternativa parcial.
3. Matriz jerarquica padre-hijo.
4. Tabla de aristas + timeline + panel de detalle.

### Visuales nativos posibles

- Decomposition Tree: util para explorar jerarquias.
- Matrix: permite padre-hijo en formato tabular.
- Scatter chart: alternativa manual si se precalculan posiciones.
- Table: aristas base con filtros.

### Visuales personalizados opcionales

- Network Navigator.
- Force-Directed Graph.
- Drill Down Network PRO u otro visual certificado si la politica de la empresa lo permite.

### Alternativa sin visual de grafo

Construir la pagina con:

- tabla de relaciones padre-hijo;
- timeline cronologica;
- tabla de movimientos;
- panel lateral de detalle;
- bookmarks para alternar "hacia atras" y "hacia adelante".

### Nodos y aristas

Nodos minimos:

- recepcion;
- lote;
- operacion;
- pileta;
- merma;
- fraccionamiento;
- producto terminado;
- venta granel.

Aristas minimas:

- lote padre -> lote hijo;
- pileta origen -> pileta destino;
- lote/pileta -> venta;
- lote/pileta -> fraccionamiento.

Cada arista debe conservar litros y operacion asociada cuando exista.

## 8. Validacion del informe

### Checklist funcional

- Los filtros globales afectan las paginas esperadas.
- Los filtros especificos no rompen otras visualizaciones.
- Las medidas coinciden con las vistas SQL.
- Las relaciones no duplican valores.
- Las paginas navegan correctamente.
- Los drill-through mantienen contexto.
- Los paneles laterales muestran el elemento seleccionado.
- Los datos coinciden con consultas del backend o PostgreSQL.
- Ningun grafico queda sin datos por error de relacion.

### Checklist visual

- El menu lateral es consistente.
- Header y titulos son consistentes.
- Colores respetan el design system.
- Estados usan colores correctos.
- KPIs muestran unidad.
- Tablas son legibles.
- Tooltips tienen contexto util.
- No hay elementos superpuestos.

### Checklist tecnico

- Tema importado correctamente.
- Tipos de datos revisados.
- Relaciones revisadas.
- Medidas sin errores.
- Refresco de datos probado.
- Credenciales guardadas correctamente.
- Archivo `.pbix` abre sin errores.

## 9. Entregables finales

- Archivo `.pbix` del Centro de Control Vitivinicola Lanzarini.
- Documentacion de Power BI en `powerbi/`.
- Capturas principales de cada pagina.
- Tema `LanzariniTheme.json`.
- Scripts de vistas SQL.
- Medidas DAX documentadas.
- Checklist de validacion completado.
- Version final lista para revision funcional.

## Orden recomendado de construccion

1. Preparar PostgreSQL y vistas.
2. Crear archivo Power BI nuevo.
3. Importar tema Lanzarini.
4. Crear calendario.
5. Cargar vistas.
6. Revisar tipos de datos.
7. Crear relaciones.
8. Crear medidas base.
9. Construir Dashboard Ejecutivo.
10. Construir Produccion.
11. Construir Stock.
12. Construir Trazabilidad.
13. Construir Calidad.
14. Construir Comercial.
15. Construir Ordenes de Trabajo.
16. Construir Corte Teorico.
17. Construir Reportes.
18. Validar datos, relaciones, filtros e interacciones.
19. Preparar entregables finales.
