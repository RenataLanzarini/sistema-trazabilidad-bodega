# Construccion de la Pagina Calidad en Power BI Desktop

Esta guia documenta como construir la pagina **Calidad** del Centro de Control Vitivinicola Lanzarini. La pagina debe mostrar analisis enologicos y mediciones de fermentacion, permitiendo seguir la evolucion por lote, pileta, fecha y variedad.

## 1. Objetivo de la pagina

### Preguntas que responde

- Como evolucionan Brix, alcohol, pH, acidez, Baume y temperatura?
- Que lotes o piletas tienen valores fuera de rango?
- Cual fue el ultimo analisis registrado?
- Que mediciones de fermentacion estan disponibles?
- Hay lotes sin analisis reciente?
- Como se relaciona la calidad con stock y trazabilidad?

### Usuario principal

- Enologo.
- Gerente / dueno para vista resumida.

### Relacion con otras paginas

- Trazabilidad: permite consultar calidad dentro de la historia de un lote.
- Produccion: conecta Brix inicial y recepcion con evolucion posterior.
- Stock: permite revisar calidad por pileta actual.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion recomendada: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Sin scroll.

### Menu lateral

- Mismo menu global.
- Item activo: `Calidad`.
- Fondo marron madera `#2B1E1A`.
- Activo en borravino `#3E244A` con acento dorado.

### Header

- Titulo: `Calidad`.
- Subtitulo: `Analisis enologicos y fermentacion`.
- Alto: 88 px.
- Estilo sobrio y tecnico.
- Linea inferior dorada.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px.
- Contenedor blanco, borde suave y radio 8 px.

### Zona KPI

- Seis tarjetas superiores.
- Alto aproximado: 118 px.
- Fondo blanco.
- Acentos por indicador.

### Zona de graficos

- Dos filas principales:
  - evolucion de fermentacion;
  - evolucion enologica y comparaciones.

### Panel lateral de detalle

- Derecha.
- Ancho: 320-380 px.
- Muestra detalle del lote, pileta o analisis seleccionado.

### Tabla inferior

- Ubicacion: parte inferior.
- Tabla compacta de analisis y mediciones.

## 3. Filtros

### Ano

- Visual sugerido: slicer dropdown o horizontal.
- Vista origen: calendario / `vw_calidad[fecha]`.
- Interaccion: afecta todos los visuales temporales.

### Cosecha

- Visual sugerido: dropdown.
- Vista origen: `vw_produccion[cosecha]`, `vw_stock_actual[cosecha]`.
- Interaccion: filtra lotes relacionados con calidad.

### Bodega

- Visual sugerido: dropdown.
- Vista origen: `vw_calidad[bodega_nombre]`.
- Interaccion: afecta toda la pagina.

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_calidad[lote_codigo]`.
- Interaccion: filtra analisis, mediciones, graficos y panel lateral.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_calidad[pileta_codigo]`.
- Interaccion: filtra calidad por pileta y permite navegar a Stock.

### Variedad

- Visual sugerido: dropdown.
- Vista origen: `vw_produccion[variedad_nombre]`, `vw_stock_actual[variedad_nombre]`.
- Interaccion: filtra lotes y piletas asociadas.

### Fecha

- Visual sugerido: slicer de rango.
- Vista origen: `vw_calidad[fecha]`.
- Interaccion: limita evoluciones temporales y tabla.

### Tipo de registro

- Visual sugerido: botones segmentados o dropdown.
- Valores: `analisis_enologico`, `medicion_fermentacion`.
- Vista origen: `vw_calidad[tipo_registro]`.
- Interaccion: cambia foco entre analisis y fermentacion.

## 4. KPIs principales

### Promedio Brix

- Medida DAX: `Promedio Brix`.
- Formato: `0.00`.
- Origen: `vw_calidad[brix]` y/o `vw_produccion[brix_real]`.
- Tooltip: promedio, minimo, maximo, cantidad de registros.
- Interaccion: resalta visuales de Brix y Produccion.

### Promedio Alcohol

- Medida DAX: `Promedio Alcohol`.
- Formato: `0.00`.
- Origen: `vw_calidad[alcohol]`.
- Tooltip: promedio por lote, pileta y fecha.
- Interaccion: filtra grafico de evolucion de alcohol.

### Promedio pH

- Medida DAX: `Promedio pH`.
- Formato: `0.00`.
- Origen: `vw_calidad[ph]`.
- Tooltip: promedio, minimo, maximo y registros fuera de rango.
- Interaccion: resalta alertas de pH.

### Promedio Baume

- Medida DAX: `Promedio Baume`.
- Formato: `0.00`.
- Origen: `vw_calidad[grado_baume]`.
- Tooltip: promedio por fecha y estado de fermentacion.
- Interaccion: filtra evolucion de fermentacion.

### Temperatura Promedio

- Medida DAX: `Temperatura Promedio`.
- Formato: `0.00 °C`.
- Origen: `vw_calidad[temperatura]`.
- Tooltip: promedio, maximo y alertas de temperatura.
- Interaccion: resalta grafico de temperatura.

### Ultimo Analisis Registrado

- Medida DAX sugerida: fecha maxima de analisis o conteo de dias desde ultimo analisis.
- Formato: fecha `dd/mm/yyyy` o dias.
- Origen: `vw_calidad[fecha]` filtrado por `tipo_registro = analisis_enologico`.
- Tooltip: lote, pileta, fecha, valores principales.
- Interaccion: actualiza panel lateral de detalle.

## 5. Visuales principales

## Evolucion de Baume por fecha

- Tipo de grafico: linea.
- Campos:
  - eje: `vw_calidad[fecha]`;
  - valor: `Promedio Baume`;
  - leyenda opcional: lote o pileta.
- Medidas: `Promedio Baume`.
- Colores: neutro `#8C7B6B` o dorado suave.
- Tooltip: fecha, lote, pileta, Baume, temperatura.
- Drill-through: Trazabilidad por lote.
- Interaccion: click en punto actualiza panel lateral.

## Evolucion de temperatura por fecha

- Tipo de grafico: linea.
- Campos:
  - eje: `fecha`;
  - valor: `Temperatura Promedio`.
- Medidas: `Temperatura Promedio`.
- Colores: ambar `#D69A2D`; rojo vino para puntos fuera de rango.
- Tooltip: fecha, temperatura, lote, pileta.
- Drill-through: Stock por pileta.
- Interaccion: seleccion de fecha filtra tabla inferior.

## Evolucion de alcohol

- Tipo de grafico: linea o area suave.
- Campos:
  - eje: `fecha`;
  - valor: `Promedio Alcohol`.
- Medidas: `Promedio Alcohol`.
- Colores: borravino `#3E244A`.
- Tooltip: alcohol, lote, pileta, fecha.
- Drill-through: Trazabilidad.
- Interaccion: click en lote/punto actualiza panel.

## Evolucion de pH

- Tipo de grafico: linea con banda de referencia si se define rango.
- Campos:
  - eje: `fecha`;
  - valor: `Promedio pH`.
- Medidas: `Promedio pH`.
- Colores: marron madera `#2B1E1A`; alertas en rojo vino.
- Tooltip: pH, lote, pileta, fecha, rango esperado.
- Drill-through: Reportes o Trazabilidad.
- Interaccion: seleccion resalta registros fuera de rango.

## Comparacion de acidez por lote

- Tipo de grafico: barras horizontales o scatter.
- Campos:
  - eje: `lote_codigo`;
  - valores: promedio de `acidez_total` y/o `volatil`.
- Medidas: medidas DAX de promedio de acidez.
- Colores: dorado para acidez total, rojo vino suave para volatil.
- Tooltip: lote, pileta, acidez total, volatil, fecha ultimo analisis.
- Drill-through: Trazabilidad.
- Interaccion: click en lote filtra toda la pagina.

## Ultimos analisis por pileta/lote

- Tipo de visual: tabla o matriz compacta.
- Campos:
  - lote;
  - pileta;
  - fecha ultimo analisis;
  - alcohol;
  - pH;
  - Brix;
  - acidez.
- Medidas: ultimos valores si se definen.
- Colores: formato condicional por rangos.
- Tooltip: observaciones y codigo externo.
- Drill-through: Trazabilidad o Stock.
- Interaccion: click en fila abre panel lateral.

## 6. Tabla inferior

### Tabla de analisis/mediciones

- Visual: Table.
- Ubicacion: parte inferior.
- Orden: `fecha` descendente.

### Campos

- `fecha`
- `tipo_registro`
- `lote_codigo`
- `pileta_codigo`
- `variedad_nombre` si se incorpora desde dimensiones o vista relacionada
- `alcohol`
- `brix`
- `grado_baume`
- `temperatura`
- `ph`
- `acidez_total`
- `volatil`
- `observaciones`

### Formato

- Encabezado marron madera.
- Filas alternas suaves.
- Decimales con dos posiciones.
- Valores fuera de rango con formato condicional.
- Observaciones truncadas con tooltip.

## 7. Panel lateral de detalle

### Al seleccionar lote

- Codigo lote.
- Variedad.
- Cosecha.
- Piletas asociadas.
- Ultimo analisis.
- Ultima medicion de fermentacion.
- Evolucion resumida.
- Alertas activas.
- Boton: `Ver trazabilidad`.

### Al seleccionar pileta

- Codigo pileta.
- Estado.
- Litros actuales.
- Capacidad.
- Lotes contenidos.
- Ultimas mediciones.
- Boton: `Ver stock`.

### Al seleccionar analisis

- Fecha.
- Tipo registro.
- Lote.
- Pileta.
- Alcohol.
- Brix.
- Baume.
- Temperatura.
- pH.
- Acidez.
- Observaciones.

### Estado de fermentacion

- Mostrar resumen textual:
  - sin datos;
  - en seguimiento;
  - estable;
  - requiere revision.

## 8. Alertas

### Temperatura fuera de rango

- Color: ambar o rojo vino.
- Regla: temperatura por encima o debajo del rango definido por enologia.
- Accion: revisar detalle de pileta/lote.

### Baume estancado

- Color: ambar.
- Regla: Baume sin variacion relevante durante el periodo definido.
- Accion: revisar fermentacion y ordenes asociadas.

### pH fuera de rango

- Color: rojo vino si supera umbral critico.
- Accion: abrir panel lateral y navegar a Trazabilidad.

### Alcohol fuera de rango

- Color: ambar o rojo vino.
- Accion: revisar analisis historico del lote.

### Lote sin analisis reciente

- Color: gris calido o ambar.
- Regla: no existe analisis en los ultimos N dias.
- Accion: enviar a Reportes o generar revision operativa.

## 9. Navegacion

### Click en lote

- Destino: Trazabilidad.
- Contexto: lote seleccionado.

### Click en pileta

- Destino: Stock.
- Contexto: pileta seleccionada.

### Click en alerta

- Destino: Reportes o panel lateral, segun tipo.
- Contexto: lote/pileta/fecha.

### Click en analisis

- Accion: abre o actualiza panel lateral de detalle.

## 10. Performance

- Limitar series temporales por filtro de lote, pileta o fecha.
- Evitar demasiadas lineas simultaneas.
- Usar small multiples solo si hay pocas categorias.
- Resumir promedios por fecha.
- Ocultar observaciones largas en visuales principales.
- Evitar mezclar analisis y fermentacion en un mismo grafico sin filtrar `tipo_registro`.
- Usar Import mode.
- Validar que las medidas ignoren nulos correctamente.

## 11. Checklist final

- [ ] Filtros funcionan.
- [ ] KPIs correctos.
- [ ] Evolucion temporal legible.
- [ ] Alertas visibles.
- [ ] Tabla ordenada.
- [ ] Drill-through a trazabilidad.
- [ ] Colores consistentes.
- [ ] Sin scroll.
- [ ] Valores coinciden con `vw_calidad`.
- [ ] Tipo de registro separa analisis y fermentacion.
- [ ] Panel lateral muestra ultimo analisis correctamente.
- [ ] Pileta navega a Stock.
- [ ] Lote navega a Trazabilidad.
