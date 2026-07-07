# Construccion de la Pagina Produccion en Power BI Desktop

Esta guia documenta como construir la pagina **Produccion** del Centro de Control Vitivinicola Lanzarini. La pagina profundiza en recepcion de uva, cosecha, variedad, finca, kilos, Brix, rendimiento y lotes generados.

## 1. Objetivo de la pagina

### Preguntas que responde

- Cuantos kilos de uva se recibieron por periodo?
- Que variedades ingresaron y en que volumen?
- De que finca, origen o productor provino la uva?
- Cual fue el Brix promedio por variedad, finca o cosecha?
- Que recepciones generaron lotes?
- Que lotes nacieron desde cada CIU?
- Hay recepciones sin lote generado o datos incompletos?

### Usuario principal

- Enologo.
- Gerente / dueno.

### Relacion con otras paginas

- Dashboard Ejecutivo: recibe contexto desde el KPI `Uva recibida` y graficos de produccion mensual.
- Stock: permite analizar los lotes generados y su stock actual.
- Trazabilidad: permite abrir la genealogia de un lote creado desde recepcion.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion de diseno recomendada: 1920 x 1080 px.
- Sin scroll.
- Fondo general: crema `#F8F5EF`.

### Menu lateral

- Mismo menu que Dashboard Ejecutivo.
- Item activo: `Produccion`.
- Fondo menu: marron madera `#2B1E1A`.
- Item activo: borravino `#3E244A` con acento dorado.

### Header

- Header sobrio, sin fotografia dominante.
- Titulo: `Produccion`.
- Subtitulo sugerido: `Recepcion de uva, lotes y cosecha`.
- Alto sugerido: 88 px.
- Fondo: crema o marron madera suave.
- Linea inferior: dorado `#B88646`.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px.
- Fondo del contenedor: blanco.
- Borde: `#E8E0D6`.
- Radio: 8 px.

### Colores

- Kilos: dorado `#B88646`.
- Brix: borravino `#3E244A`.
- Variedades: paleta de datos segun tipo de vino.
- Alertas: ambar `#D69A2D` y rojo vino `#8A1F2D`.

### Espaciado

- Separacion entre filtros: 10-12 px.
- Separacion entre tarjetas: 14 px.
- Separacion entre visuales: 16 px.
- Padding interno de tarjetas: 14-16 px.

### Estilo de tarjetas

- Fondo: blanco.
- Radio: 8 px.
- Borde suave.
- Valor grande, etiqueta pequena.
- Unidad visible: kg, Brix, cantidad.

## 3. Filtros

### Ano

- Visual sugerido: slicer dropdown o horizontal.
- Vista origen: calendario / `vw_produccion[fecha_recepcion]`.
- Interaccion: afecta todos los visuales de la pagina.

### Cosecha

- Visual sugerido: dropdown.
- Vista origen: `vw_produccion[cosecha]`.
- Interaccion: filtra recepciones, lotes y graficos por cosecha.

### Bodega

- Visual sugerido: dropdown.
- Vista origen: `vw_produccion[bodega_nombre]`.
- Interaccion: afecta toda la pagina.

### Variedad

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_produccion[variedad_nombre]`.
- Interaccion: filtra kilos, Brix, lotes y tabla inferior.

### Finca

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_produccion[finca]`.
- Interaccion: filtra recepciones, kilos y Brix por finca.

### Origen / Productor

- Visual sugerido: dropdown.
- Vista origen: `vw_produccion[origen_uva_nombre]` y `vw_produccion[origen_uva_tipo]`.
- Interaccion: diferencia uva propia y comprada a terceros.

### Fecha de recepcion

- Visual sugerido: slicer de rango de fechas.
- Vista origen: `vw_produccion[fecha_recepcion]`.
- Interaccion: filtra todo el contenido temporal.

### Estado de lote

- Visual sugerido: dropdown.
- Vista origen: `vw_produccion[estado_lote]`.
- Interaccion: filtra lotes generados y tablas.

## 4. KPIs principales

### Kg Uva Recibida

- Medida DAX: `Kg Uva Recibida`.
- Formato: `#,0.00 kg`.
- Origen: `vw_produccion[kilos_recibidos]`.
- Tooltip: kilos recibidos, cantidad de CIU, periodo, variedad principal.
- Interaccion: click filtra tabla de recepciones.

### Promedio Brix

- Medida DAX: `Promedio Brix`.
- Formato: `0.00`.
- Origen: `vw_produccion[brix_real]` o `vw_calidad[brix]` segun definicion final.
- Tooltip: promedio, minimo, maximo, cantidad de recepciones con Brix.
- Interaccion: click resalta visual de Brix por variedad.

### Recepciones

- Medida DAX sugerida: `Recepciones = DISTINCTCOUNT(vw_produccion[recepcion_uva_id])`.
- Formato: entero.
- Origen: `vw_produccion`.
- Tooltip: cantidad de CIU en el periodo.
- Interaccion: filtra tabla inferior a recepciones.

### Lotes Generados

- Medida DAX sugerida: `Lotes Generados = DISTINCTCOUNT(vw_produccion[lote_id])`.
- Formato: entero.
- Origen: `vw_produccion`.
- Tooltip: lotes con codigo asociado, estado y cosecha.
- Interaccion: click prepara drill-through a Trazabilidad.

### Variedades Activas

- Medida DAX sugerida: `Variedades Activas = DISTINCTCOUNT(vw_produccion[variedad_id])`.
- Formato: entero.
- Origen: `vw_produccion`.
- Tooltip: variedades presentes en el periodo filtrado.
- Interaccion: resalta grafico de kg por variedad.

### Rendimiento Estimado

- Medida DAX sugerida: relacion entre kilos recibidos y litros generados/movidos si el modelo lo permite.
- Formato: porcentaje o litros por kg.
- Origen: `vw_produccion` + `vw_movimientos` o `vw_stock_actual`.
- Tooltip: explicar formula usada y advertir si es estimado.
- Interaccion: filtra visuales de lotes generados y movimientos iniciales.

## 5. Visuales principales

## Produccion mensual

- Tipo de grafico: columnas agrupadas.
- Campos:
  - eje: `DimFecha[AnioMes]`;
  - valores: `Kg Uva Recibida`.
- Medidas: `Kg Uva Recibida`.
- Colores: dorado `#B88646`.
- Tooltip: kg, cantidad de recepciones, Brix promedio.
- Drill-through: Dashboard Ejecutivo o Reportes de produccion.
- Interaccion: click en mes filtra todos los visuales.

## Kg recibidos por variedad

- Tipo de grafico: barras horizontales.
- Campos:
  - eje: `variedad_nombre`;
  - valores: `Kg Uva Recibida`.
- Medidas: `Kg Uva Recibida`.
- Colores: paleta de datos por tipo de vino.
- Tooltip: kg, cantidad CIU, Brix promedio, lotes generados.
- Drill-through: Stock filtrado por variedad.
- Interaccion: click en variedad filtra pagina completa.

## Kg recibidos por finca/origen

- Tipo de grafico: barras horizontales o columnas.
- Campos:
  - eje: `finca` o `origen_uva_nombre`;
  - valores: `Kg Uva Recibida`.
- Medidas: `Kg Uva Recibida`.
- Colores: neutros con acento dorado para top finca.
- Tooltip: kg, variedad principal, cantidad CIU.
- Drill-through: Reportes.
- Interaccion: click en finca filtra recepciones y lotes.

## Brix promedio por variedad

- Tipo de grafico: barras o dot plot.
- Campos:
  - eje: `variedad_nombre`;
  - valores: `Promedio Brix`.
- Medidas: `Promedio Brix`.
- Colores: borravino `#3E244A`.
- Tooltip: promedio, minimo, maximo, cantidad de mediciones.
- Drill-through: Calidad.
- Interaccion: click filtra tabla inferior y visuales relacionados.

## Recepciones por cosecha

- Tipo de grafico: columnas o dona simple.
- Campos:
  - eje/leyenda: `cosecha`;
  - valores: `Recepciones`.
- Medidas: `Recepciones`.
- Colores: dorado, marron y neutros.
- Tooltip: cantidad CIU, kg, variedades.
- Drill-through: Produccion filtrada.
- Interaccion: click filtra toda la pagina por cosecha.

## Lotes generados por estado

- Tipo de grafico: dona o barras.
- Campos:
  - categoria: `estado_lote`;
  - valores: `Lotes Generados`.
- Medidas: `Lotes Generados`.
- Colores:
  - activo/completado: verde suave;
  - pendiente: gris calido;
  - alerta: ambar.
- Tooltip: cantidad de lotes, kg asociados, cosecha.
- Drill-through: Trazabilidad o Reportes.
- Interaccion: click filtra tabla de lotes.

## 6. Tabla inferior

### Tabla de recepciones/lotes

- Visual: Table.
- Ubicacion: parte inferior de la pagina.
- Orden: `fecha_recepcion` descendente.

### Campos

- `fecha_recepcion`
- `numero_ciu`
- `cosecha`
- `finca`
- `variedad_nombre`
- `kilos_recibidos`
- `brix_real`
- `lote_codigo`
- `estado_lote`

### Formato

- Encabezado marron madera.
- Texto encabezado crema.
- Filas alternas suaves.
- Kilos alineados a la derecha.
- Brix con dos decimales.
- Lote vacio debe mostrarse como alerta visual o texto `Sin lote`.

### Interacciones

- Click en CIU abre panel lateral de detalle.
- Click en lote permite drill-through a Trazabilidad.
- Click en variedad filtra visuales.

## 7. Panel lateral de detalle

### Activacion

Se muestra al seleccionar una recepcion o lote en la tabla inferior o en un visual.

### Datos de CIU

- numero CIU.
- fecha recepcion.
- cosecha.
- finca.
- origen/productor.
- variedad.
- kilos recibidos.
- bruto, tara, neto si estan disponibles.
- chofer, patente y camion si se requiere auditoria.

### Datos analiticos

- Brix.
- tenor azucar.
- observaciones si existen.

### Datos de lote

- codigo lote.
- fecha nacimiento.
- estado.
- tipo producto.
- calificacion.

### Vinculo a trazabilidad

- Boton o accion: `Ver trazabilidad`.
- Debe navegar a Trazabilidad con el lote seleccionado.

## 8. Alertas

### Brix fuera de rango

- Color: ambar o rojo vino segun umbral.
- Ubicacion: tabla inferior y panel lateral.
- Accion: navegar a Calidad.

### Recepcion sin lote generado

- Color: ambar.
- Regla: `recepcion_uva_id` sin `lote_id`.
- Accion: revisar Produccion o Reportes.

### Kilos atipicos

- Color: ambar.
- Regla: valor fuera del rango esperado definido por la bodega.
- Accion: revisar detalle CIU.

### Lote sin movimiento inicial

- Color: rojo vino si el lote ya deberia tener ingreso fisico.
- Requiere comparar lotes generados contra `vw_movimientos`.
- Accion: navegar a Stock o Trazabilidad.

## 9. Navegacion

### Click en lote

- Destino: Trazabilidad.
- Contexto: `lote_id` o `lote_codigo`.

### Click en variedad

- Destino: Stock filtrado.
- Contexto: `variedad_nombre`.

### Click en finca

- Destino: misma pagina Produccion filtrada.
- Contexto: `finca`.

### Click en alerta

- Destino:
  - Brix fuera de rango -> Calidad.
  - Recepcion sin lote -> Reportes o detalle.
  - Kilos atipicos -> panel lateral.
  - Lote sin movimiento -> Stock o Trazabilidad.

## 10. Performance

- Evitar cargar demasiadas columnas de texto largo en visuales principales.
- Limitar tabla inferior a columnas relevantes.
- Usar top N para finca/origen si hay muchas categorias.
- Evitar visuales con demasiadas variedades simultaneas.
- Mantener relaciones simples desde dimensiones.
- Usar medidas con `DISTINCTCOUNT` para no duplicar recepciones o lotes.
- Validar que `Kg Uva Recibida` no duplique kilos cuando una recepcion tenga varios lotes.

## 11. Checklist final

- [ ] Filtros funcionan.
- [ ] KPIs correctos.
- [ ] Tabla ordenada por fecha descendente.
- [ ] Drill-through a trazabilidad funciona.
- [ ] Colores consistentes con Design System.
- [ ] Sin scroll.
- [ ] Valores coinciden con backend/vistas.
- [ ] Brix formateado correctamente.
- [ ] Kilos no se duplican por recepcion-lote.
- [ ] Alertas visibles y comprensibles.
- [ ] Panel lateral muestra datos correctos.
- [ ] Navegacion a Stock y Trazabilidad conserva contexto.
