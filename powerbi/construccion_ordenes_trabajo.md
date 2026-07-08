# Construccion de la Pagina Ordenes de Trabajo en Power BI Desktop

Esta guia documenta como construir la pagina **Ordenes de Trabajo** del Centro de Control Vitivinicola Lanzarini. La pagina debe mostrar tareas pendientes, completadas, operarios, piletas, lotes, cumplimiento y seguimiento operativo.

## 1. Objetivo de la pagina

### Preguntas que responde

- Que ordenes estan pendientes?
- Que ordenes fueron completadas?
- Que operario tiene cada tarea?
- Que tareas se acumulan por operario?
- Sobre que pileta o lote se trabaja?
- Que ordenes estan vinculadas a operaciones productivas?
- Hay ordenes antiguas o incompletas que requieren seguimiento?

### Usuario principal

- Operario.
- Enologo.
- Gerente / dueno para control operativo.

### Relacion con otras paginas

- Produccion: conecta tareas con procesos productivos y lotes.
- Stock: conecta ordenes con piletas y lotes actuales.
- Trazabilidad: permite revisar historia del lote asociado.
- Reportes: permite auditar ordenes, operarios y cumplimiento.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion recomendada: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Sin scroll.

### Menu lateral

- Mismo menu global.
- Item activo: `Ordenes de Trabajo`.
- Fondo marron madera `#2B1E1A`.
- Activo borravino `#3E244A` con acento dorado.

### Header

- Titulo: `Ordenes de Trabajo`.
- Subtitulo: `Seguimiento operativo de tareas, piletas y lotes`.
- Alto: 88 px.
- Linea inferior dorada.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px.
- Contenedor blanco con borde suave.

### Zona KPI

- Seis tarjetas.
- Foco operativo: pendientes, completadas, cumplimiento y carga de trabajo.

### Tablero operativo

- Area central.
- Debe mostrar pendientes y completadas de forma muy clara.
- Puede usar barras, tarjetas agrupadas o matriz tipo Kanban.

### Tabla inferior

- Tabla detallada de ordenes.
- Ordenada por fecha descendente o pendientes primero.

### Panel lateral de detalle

- Derecha.
- Ancho: 320-380 px.
- Muestra informacion completa de la orden seleccionada.

## 3. Filtros

### Ano

- Visual sugerido: slicer dropdown o horizontal.
- Vista origen: calendario / `vw_ordenes_trabajo[fecha]`.
- Interaccion: filtra ordenes por periodo.

### Fecha

- Visual sugerido: slicer de rango.
- Vista origen: `vw_ordenes_trabajo[fecha]`, `vw_ordenes_trabajo[fecha_completada]`.
- Interaccion: filtra tablero, KPIs y tabla.

### Estado: pendiente/completada

- Visual sugerido: botones segmentados.
- Vista origen: `vw_ordenes_trabajo[estado_operativo]`.
- Interaccion: alterna foco operativo.

### Operario

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_ordenes_trabajo[operario_nombre]`.
- Interaccion: filtra carga de trabajo por persona.

### Tarea

- Visual sugerido: dropdown.
- Vista origen: `vw_ordenes_trabajo[tarea_nombre]`.
- Interaccion: filtra tipo de tarea.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_ordenes_trabajo[pileta_codigo]`, `pileta_origen_codigo`, `pileta_destino_codigo`.
- Interaccion: filtra ordenes asociadas a tanque/pileta.

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_ordenes_trabajo[lote_codigo]`.
- Interaccion: filtra tareas del lote y habilita trazabilidad.

### Bodega

- Visual sugerido: dropdown si se dispone de dimension bodega relacionada.
- Vista origen: dimension bodega o vistas relacionadas.
- Interaccion: filtra todas las ordenes.

### Operacion productiva vinculada

- Visual sugerido: dropdown o selector.
- Vista origen: `vw_ordenes_trabajo[operacion_productiva_id]`.
- Interaccion: filtra ordenes con o sin operacion asociada.

## 4. KPIs principales

### Ordenes Pendientes

- Medida DAX: `Ordenes Pendientes`.
- Formato: entero.
- Origen: `vw_ordenes_trabajo[estado_operativo]`.
- Tooltip: pendientes por fecha, operario y tarea.
- Interaccion: click filtra tablero a pendientes.

### Ordenes Completadas

- Medida DAX: `Ordenes Completadas`.
- Formato: entero.
- Origen: `vw_ordenes_trabajo[estado_operativo]`.
- Tooltip: completadas por periodo y operario.
- Interaccion: click filtra tablero a completadas.

### % Cumplimiento

- Medida DAX sugerida: `DIVIDE([Ordenes Completadas], [Ordenes Pendientes] + [Ordenes Completadas])`.
- Formato: `0.00%`.
- Origen: `vw_ordenes_trabajo`.
- Tooltip: completadas sobre total visible.
- Interaccion: resalta evolucion de completadas.

### Tareas por Operario

- Medida DAX sugerida: conteo de ordenes por `operario_id`.
- Formato: entero.
- Origen: `vw_ordenes_trabajo[operario_id]`.
- Tooltip: carga por operario, pendientes y completadas.
- Interaccion: filtra grafico de operarios.

### Ordenes Vencidas o Antiguas

- Medida DAX sugerida: conteo de pendientes con fecha anterior a umbral.
- Formato: entero.
- Origen: `vw_ordenes_trabajo[fecha]`, `estado_operativo`.
- Tooltip: antiguedad, operario, tarea.
- Interaccion: filtra alertas y tabla.

### Ultima Orden Completada

- Medida DAX sugerida: `MAX(vw_ordenes_trabajo[fecha_completada])`.
- Formato: `dd/mm/yyyy hh:mm`.
- Origen: `vw_ordenes_trabajo[fecha_completada]`.
- Tooltip: orden, operario y tarea asociada.
- Interaccion: actualiza panel lateral.

## 5. Visuales principales

## Tablero tipo Kanban: pendientes / completadas

- Tipo de grafico: tarjetas agrupadas, matriz o columnas por estado.
- Campos:
  - categoria: `estado_operativo`;
  - detalle: `tarea_nombre`, `numero`, `operario_nombre`.
- Medidas: `Ordenes Pendientes`, `Ordenes Completadas`.
- Colores:
  - pendiente: gris calido `#A89F91`;
  - completada: verde suave `#8FAF77`;
  - vencida: rojo vino `#8A1F2D`.
- Tooltip: numero, tarea, operario, lote, pileta, fecha.
- Drill-through: Reportes o detalle de OT.
- Interaccion: click en tarjeta actualiza panel lateral.

## Ordenes por operario

- Tipo de grafico: barras horizontales.
- Campos:
  - eje: `operario_nombre`;
  - valores: conteo de ordenes;
  - leyenda: `estado_operativo`.
- Medidas: pendientes, completadas, total ordenes.
- Colores: pendiente gris, completada verde, vencida rojo.
- Tooltip: carga total, pendientes, completadas, % cumplimiento.
- Drill-through: Reportes por operario.
- Interaccion: click en operario filtra pagina.

## Ordenes por tarea

- Tipo de grafico: barras.
- Campos:
  - eje: `tarea_nombre`;
  - valores: conteo de ordenes.
- Medidas: total ordenes, pendientes, completadas.
- Colores: dorado y neutros.
- Tooltip: tarea, cantidad, operarios, estado.
- Drill-through: Reportes.
- Interaccion: click en tarea filtra tablero.

## Ordenes por pileta

- Tipo de grafico: barras horizontales o matriz.
- Campos:
  - eje: `pileta_codigo`;
  - valores: conteo de ordenes.
- Medidas: total ordenes.
- Colores: marron y borravino.
- Tooltip: pileta, tareas, operarios, lote asociado.
- Drill-through: Stock.
- Interaccion: click en pileta navega o filtra Stock.

## Evolucion de ordenes completadas

- Tipo de grafico: linea o columnas por fecha.
- Campos:
  - eje: `fecha_completada`;
  - valores: `Ordenes Completadas`.
- Medidas: `Ordenes Completadas`.
- Colores: verde suave `#8FAF77`.
- Tooltip: fecha, completadas, operarios.
- Drill-through: Reportes.
- Interaccion: seleccionar periodo filtra tabla.

## Ordenes vinculadas a operaciones productivas

- Tipo de grafico: dona o barras.
- Campos:
  - categoria: con operacion / sin operacion;
  - valor: conteo de ordenes.
- Medidas: conteo de OT vinculadas.
- Colores: vinculado verde, sin vincular ambar.
- Tooltip: cantidad, porcentaje, operaciones.
- Drill-through: Reportes / Movimientos.
- Interaccion: click filtra tabla a vinculadas o no vinculadas.

## 6. Tabla inferior

### Tabla de ordenes

- Visual: Table.
- Ubicacion: parte inferior.
- Orden: pendientes primero, luego fecha descendente.

### Campos

- `fecha`
- `numero` / `codigo_externo`
- `tarea_nombre`
- `operario_nombre`
- `pileta_codigo`
- `lote_codigo`
- `estado_operativo`
- `fecha_completada`
- `operacion_productiva_id`
- `observaciones`

### Formato

- Encabezado marron madera.
- Texto encabezado crema.
- Filas alternas suaves.
- Estado con formato condicional.
- Observaciones truncadas con tooltip.

## 7. Panel lateral de detalle

### Datos generales

- Numero.
- Codigo externo.
- Fecha.
- Estado.
- Fecha completada.

### Tarea

- Nombre de tarea.
- Insumo si corresponde.
- Cantidad si corresponde.
- Litros a trasegar si corresponde.

### Operario

- Nombre.
- Carga de tareas actual si se muestra medida auxiliar.

### Pileta/lote

- Pileta.
- Pileta origen.
- Pileta destino.
- Lote.

### Observaciones

- Observaciones iniciales.
- Observaciones de completado.

### Operacion productiva vinculada

- ID de operacion.
- Estado de vinculacion.
- Boton: `Ver movimientos/reportes`.

### Accesos

- `Ver trazabilidad` si hay lote.
- `Ver stock` si hay pileta.

## 8. Alertas

### Ordenes pendientes antiguas

- Color: rojo vino o ambar segun antiguedad.
- Condicion: pendiente con fecha anterior a umbral.
- Accion: abrir detalle lateral.

### Ordenes sin operario

- Color: ambar.
- Condicion: `operario_id` nulo.
- Accion: revisar asignacion.

### Ordenes completadas sin fecha

- Color: rojo vino.
- Condicion: completada true sin `fecha_completada`.
- Accion: revisar consistencia.

### Ordenes sin operacion vinculada cuando corresponda

- Color: ambar.
- Condicion: tarea productiva sin `operacion_productiva_id`.
- Accion: revisar operacion.

### Acumulacion de tareas en un operario

- Color: ambar.
- Condicion: operario supera umbral de tareas pendientes.
- Accion: filtrar por operario.

## 9. Navegacion

### Click en lote

- Destino: Trazabilidad.
- Contexto: lote seleccionado.

### Click en pileta

- Destino: Stock.
- Contexto: pileta seleccionada.

### Click en operacion

- Destino: Movimientos/Reportes.
- Contexto: operacion productiva.

### Click en operario

- Accion: filtro de pagina por operario.

### Click en alerta

- Accion: abre panel lateral con la orden relacionada.

## 10. Performance

- Limitar tabla inferior a columnas necesarias.
- Agrupar visuales por estado.
- Usar filtros de fecha por defecto.
- Evitar mostrar observaciones extensas salvo en panel lateral.
- Usar conteos agregados en visuales principales.
- Evitar relaciones bidireccionales innecesarias.
- Mantener Import mode.

## 11. Checklist final

- [ ] Filtros funcionan.
- [ ] KPIs correctos.
- [ ] Tablero operativo legible.
- [ ] Tabla ordenada.
- [ ] Alertas visibles.
- [ ] Drill-through correcto.
- [ ] Colores consistentes.
- [ ] Sin scroll.
- [ ] Datos coinciden con `vw_ordenes_trabajo`.
- [ ] Panel lateral muestra orden seleccionada.
- [ ] Operario filtra correctamente.
- [ ] Lote navega a Trazabilidad.
- [ ] Pileta navega a Stock.
