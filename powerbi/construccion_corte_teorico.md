# Construccion de la Pagina Corte Teorico en Power BI Desktop

Esta guia documenta como construir la pagina **Corte Teorico** del Centro de Control Vitivinicola Lanzarini. La pagina debe mostrar simulaciones de cortes, componentes, volumen al corte, snapshots analiticos y comparacion con operacion real.

Un corte teorico representa planificacion o simulacion. No modifica stock real y no crea genealogia real hasta que exista una operacion productiva ejecutada y registrada.

## 1. Objetivo de la pagina

### Preguntas que responde

- Que cortes teoricos fueron planificados?
- Que lotes y piletas componen cada corte?
- Cual es el volumen simulado?
- Que snapshots analiticos tenia cada componente?
- El corte fue vinculado a una operacion real?
- Hay diferencias entre lo planificado y lo ejecutado?

### Usuario principal

- Enologo.
- Gerente / dueno para seguimiento de planificacion.

### Diferencia entre corte teorico y operacion real

- Corte teorico: simulacion, no afecta stock, no genera movimientos, no modifica genealogia.
- Operacion real: evento productivo ejecutado, puede generar movimientos fisicos y relaciones genealogicas.
- La pagina debe mostrar esta diferencia de forma visible para evitar confusiones.

### Relacion con otras paginas

- Trazabilidad: permite revisar lotes componentes.
- Calidad: permite comparar snapshots con analisis reales.
- Stock: permite ver disponibilidad actual de lotes/piletas.
- Ordenes de Trabajo: puede relacionarse con tareas previas o posteriores.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion recomendada: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Sin scroll.

### Menu lateral

- Mismo menu global.
- Item activo: `Corte Teorico`.
- Fondo marron madera `#2B1E1A`.
- Activo borravino `#3E244A` con acento dorado.

### Header

- Titulo: `Corte Teorico`.
- Subtitulo: `Simulacion de cortes y comparacion con ejecucion real`.
- Alto: 88 px.
- Linea inferior dorada.
- Incluir etiqueta visible: `Simulacion - no modifica stock`.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px.
- Contenedor blanco con borde suave.

### Zona KPI

- Seis tarjetas superiores.
- Deben distinguir planificado, vinculado y pendiente de ejecucion.

### Zona de simulacion

- Area principal izquierda/central.
- Visuales de componentes, volumen y composicion.

### Zona de comparacion

- Area derecha o fila secundaria.
- Visuales planificado vs ejecutado y snapshots.

### Tabla inferior

- Tabla detallada de cortes y componentes.

### Panel lateral de detalle

- Derecha.
- Ancho: 320-380 px.
- Muestra detalle completo del corte seleccionado.

## 3. Filtros

### Ano

- Visual sugerido: slicer dropdown o horizontal.
- Vista origen: calendario / `vw_cortes_teoricos[fecha]`.
- Interaccion: filtra cortes por periodo.

### Fecha

- Visual sugerido: slicer de rango.
- Vista origen: `vw_cortes_teoricos[fecha]`.
- Interaccion: filtra cortes, snapshots y tabla.

### Responsable

- Visual sugerido: dropdown.
- Vista origen: `vw_cortes_teoricos[responsable_nombre]`.
- Interaccion: filtra cortes por enologo/responsable.

### Corte teorico

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_cortes_teoricos[corte_nombre]`, `corte_codigo_externo`.
- Interaccion: selecciona corte y actualiza componentes/panel.

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_cortes_teoricos[lote_codigo]`.
- Interaccion: filtra componentes del corte y habilita trazabilidad.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_cortes_teoricos[pileta_codigo]`.
- Interaccion: filtra componentes por pileta y permite ir a Stock.

### Variedad

- Visual sugerido: dropdown.
- Vista origen: `vw_cortes_teoricos[varietal_snapshot]`.
- Interaccion: filtra composicion varietal simulada.

### Operacion productiva vinculada

- Visual sugerido: dropdown o selector con/sin operacion.
- Vista origen: `vw_cortes_teoricos[operacion_productiva_id]`.
- Interaccion: diferencia cortes ejecutados/vinculados de simulaciones pendientes.

### Estado: vinculado/no vinculado

- Visual sugerido: botones segmentados.
- Vista origen: columna calculada en Power BI:
  - `Vinculado` si `operacion_productiva_id` no es nulo;
  - `No vinculado` si es nulo.
- Interaccion: filtra estado de ejecucion.

## 4. KPIs principales

### Cortes Teoricos

- Medida DAX sugerida: `DISTINCTCOUNT(vw_cortes_teoricos[corte_teorico_id])`.
- Formato: entero.
- Origen: `vw_cortes_teoricos`.
- Tooltip: cantidad de cortes en el periodo.
- Interaccion: filtra tabla de cortes.

### Volumen Total Simulado

- Medida DAX sugerida: `SUM(vw_cortes_teoricos[volumen_al_corte])`.
- Formato: `#,0.00 L`.
- Origen: `vw_cortes_teoricos[volumen_al_corte]`.
- Tooltip: volumen total por corte y componentes.
- Interaccion: resalta grafico de volumen simulado.

### Componentes por Corte

- Medida DAX sugerida: conteo de `corte_teorico_detalle_id`.
- Formato: entero.
- Origen: `vw_cortes_teoricos`.
- Tooltip: cantidad de lotes/piletas componentes.
- Interaccion: filtra composicion del corte.

### Cortes Vinculados a Operacion

- Medida DAX sugerida: conteo de cortes con `operacion_productiva_id` no nulo.
- Formato: entero.
- Origen: `vw_cortes_teoricos`.
- Tooltip: cortes con operacion real asociada.
- Interaccion: filtra comparacion planificado vs ejecutado.

### Cortes sin Ejecutar

- Medida DAX sugerida: cortes sin `operacion_productiva_id`.
- Formato: entero.
- Origen: `vw_cortes_teoricos`.
- Tooltip: simulaciones pendientes de ejecutar o vincular.
- Interaccion: filtra alertas y tabla.

### Diferencia Planificado vs Ejecutado

- Medida DAX sugerida: diferencia entre `volumen_al_corte` y litros reales de `vw_movimientos` para operacion vinculada.
- Formato: `#,0.00 L` o porcentaje.
- Origen: `vw_cortes_teoricos`, `vw_movimientos`.
- Tooltip: planificado, ejecutado, diferencia absoluta y relativa.
- Interaccion: resalta visual de comparacion.

## 5. Visuales principales

## Volumen simulado por corte

- Tipo de grafico: barras horizontales.
- Campos:
  - eje: `corte_nombre` o `corte_codigo_externo`;
  - valores: `Volumen Total Simulado`.
- Medidas: volumen total simulado.
- Colores: dorado `#B88646`.
- Tooltip: corte, fecha, responsable, volumen, componentes.
- Drill-through: Reportes de corte.
- Interaccion: click en corte actualiza panel lateral.

## Composicion del corte por lote/pileta

- Tipo de grafico: barras apiladas, dona o treemap controlado.
- Campos:
  - categoria: `lote_codigo` o `pileta_codigo`;
  - valores: `volumen_al_corte`;
  - leyenda: `varietal_snapshot`.
- Medidas: volumen al corte.
- Colores: paleta de variedades/tipos de vino.
- Tooltip: lote, pileta, volumen, varietal snapshot.
- Drill-through: Trazabilidad o Stock.
- Interaccion: click en lote filtra detalle y habilita trazabilidad.

## Comparacion planificado vs ejecutado

- Tipo de grafico: columnas agrupadas o barras comparativas.
- Campos:
  - eje: corte;
  - valores: volumen planificado y litros ejecutados.
- Medidas: volumen total simulado, litros ejecutados, diferencia.
- Colores:
  - planificado: dorado;
  - ejecutado: borravino;
  - diferencia: ambar/rojo segun magnitud.
- Tooltip: planificado, ejecutado, diferencia, operacion vinculada.
- Drill-through: Movimientos/Reportes.
- Interaccion: click en diferencia muestra detalle lateral.

## Cortes por responsable

- Tipo de grafico: barras.
- Campos:
  - eje: `responsable_nombre`;
  - valores: cantidad de cortes.
- Medidas: Cortes Teoricos.
- Colores: marron y dorado.
- Tooltip: responsable, cortes, vinculados, sin ejecutar.
- Drill-through: Reportes.
- Interaccion: click en responsable filtra pagina.

## Evolucion de cortes teoricos

- Tipo de grafico: linea o columnas por mes.
- Campos:
  - eje: `DimFecha[AnioMes]`;
  - valores: Cortes Teoricos o Volumen Total Simulado.
- Medidas: Cortes Teoricos, Volumen Total Simulado.
- Colores: dorado.
- Tooltip: periodo, cortes, volumen.
- Drill-through: Reportes.
- Interaccion: seleccion de periodo filtra visuales.

## Snapshots analiticos del corte

- Tipo de grafico: matriz o barras comparativas.
- Campos:
  - filas/eje: `lote_codigo`;
  - valores: `alcohol`, `ph`, `acidez_total`, `so2_libre`, `so2_total`.
- Medidas: promedios o valores snapshot.
- Colores: indicadores segun Design System.
- Tooltip: lote, pileta, snapshot, fecha.
- Drill-through: Calidad.
- Interaccion: click en lote navega a Calidad o Trazabilidad.

## 6. Tabla inferior

### Tabla de cortes

- Visual: Table.
- Ubicacion: parte inferior.
- Orden: `fecha` descendente.

### Campos

- `fecha`
- `corte_codigo_externo`
- `corte_nombre`
- `responsable_nombre`
- `lote_codigo`
- `pileta_codigo`
- `volumen_al_corte`
- `varietal_snapshot`
- `alcohol`
- `ph`
- `acidez_total`
- `so2_libre`
- `so2_total`
- `operacion_productiva_id`
- `observaciones`

### Formato

- Encabezado marron madera.
- Texto encabezado crema.
- Volumen alineado a la derecha.
- Indicadores analiticos con dos decimales.
- Operacion vinculada visible con indicador de estado.
- Observaciones truncadas con tooltip.

## 7. Panel lateral de detalle

### Datos de cabecera

- Codigo externo.
- Nombre.
- Fecha.
- Responsable.
- Observaciones.

### Componentes

- Lotes incluidos.
- Piletas.
- Volumen por componente.
- Varietal snapshot.

### Volumen total

- Volumen total simulado.
- Porcentaje por componente si se crea medida.

### Composicion varietal

- Resumen por `varietal_snapshot`.
- Participacion porcentual.

### Snapshots analiticos

- Alcohol.
- pH.
- Acidez volatil.
- Acidez total.
- SO2 libre.
- SO2 total.

### Operacion vinculada

- `operacion_productiva_id`.
- Fecha operacion vinculada.
- Estado de ejecucion:
  - vinculado;
  - no vinculado;
  - diferencia detectada.

### Vinculos

- `Ver trazabilidad` para lote.
- `Ver stock` para pileta.
- `Ver movimientos` para operacion vinculada.

## 8. Alertas

### Corte sin operacion vinculada

- Color: ambar.
- Condicion: `operacion_productiva_id` nulo.
- Accion: revisar si sigue siendo simulacion o debe vincularse.

### Diferencia grande entre planificado y ejecutado

- Color: rojo vino.
- Condicion: diferencia supera umbral definido.
- Accion: revisar movimientos reales.

### Corte sin snapshots analiticos

- Color: ambar.
- Condicion: valores analiticos nulos en componentes.
- Accion: revisar calidad.

### Componente sin lote

- Color: rojo vino.
- Condicion: detalle sin `lote_id`.
- Accion: revisar datos de corte.

### Volumen simulado atipico

- Color: ambar.
- Condicion: volumen fuera de rango habitual o mayor al stock disponible.
- Accion: revisar stock y componentes.

## 9. Navegacion

### Click en lote

- Destino: Trazabilidad.
- Contexto: lote seleccionado.

### Click en pileta

- Destino: Stock.
- Contexto: pileta seleccionada.

### Click en operacion vinculada

- Destino: Movimientos/Reportes.
- Contexto: operacion productiva.

### Click en alerta

- Accion: abre panel lateral con detalle del corte o componente.

### Click en corte

- Accion: actualiza panel lateral de detalle.

## 10. Performance

- No mostrar demasiados componentes simultaneos.
- Agrupar por corte.
- Usar filtros por fecha y responsable.
- Mantener snapshots analiticos en tabla o panel, no en todos los graficos.
- Usar Top N si hay muchos cortes.
- Evitar graficos con demasiadas medidas analiticas simultaneas.
- Usar Import mode.
- Validar que comparacion planificado vs ejecutado no genere relaciones ambiguas.

## 11. Checklist final

- [ ] Filtros funcionan.
- [ ] KPIs correctos.
- [ ] Cortes vinculados correctamente.
- [ ] Comparacion planificado vs ejecutado clara.
- [ ] Tabla ordenada.
- [ ] Panel lateral completo.
- [ ] Alertas visibles.
- [ ] Drill-through correcto.
- [ ] Colores consistentes.
- [ ] Sin scroll.
- [ ] Valores coinciden con `vw_cortes_teoricos`.
- [ ] La pagina indica claramente que es simulacion.
- [ ] No se confunde corte teorico con stock real.
