# Construccion de la Pagina Reportes en Power BI Desktop

Esta guia documenta como construir la pagina **Reportes** del Centro de Control Vitivinicola Lanzarini. La pagina debe servir para auditoria, consulta detallada, exportacion y analisis externo.

## 1. Objetivo de la pagina

### Preguntas que responde

- Que registros respaldan un indicador del dashboard?
- Cual es el detalle completo de recepciones, lotes, movimientos, ventas o analisis?
- Que datos se pueden exportar para auditoria o administracion?
- Que registros estan incompletos o requieren revision?
- Como consultar informacion historica con filtros avanzados?

### Usuario principal

- Gerente / dueno.
- Comercial / administracion.
- Enologo.
- Usuarios que necesiten auditoria o exportacion.

### Diferencia entre Reportes y paginas analiticas

- Paginas analiticas: resumen, visualizacion, decision rapida.
- Reportes: detalle, trazabilidad documental, auditoria, exportacion y revision fila por fila.

La pagina Reportes debe ser mas densa y utilitaria, pero mantener consistencia visual con el Design System.

### Relacion con paginas anteriores

- Recibe contexto desde Dashboard Ejecutivo, Produccion, Stock, Trazabilidad, Calidad, Comercial, Ordenes de Trabajo y Corte Teorico.
- Permite volver desde un registro detallado hacia la pagina analitica correspondiente.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion recomendada: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Sin scroll en la pagina general; la tabla puede tener scroll interno.

### Menu lateral

- Mismo menu global.
- Item activo: `Reportes`.
- Fondo marron madera `#2B1E1A`.
- Activo borravino `#3E244A` con acento dorado.

### Header

- Titulo: `Reportes`.
- Subtitulo: `Consulta detallada, auditoria y exportacion`.
- Alto: 88 px.
- Linea inferior dorada.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px o dos filas compactas si se necesitan filtros avanzados.
- Contenedor blanco con borde suave.

### Selector de tipo de reporte

- Ubicacion: primera posicion de filtros o panel superior izquierdo.
- Visual recomendado: botones segmentados, dropdown o bookmark navigator.
- Debe controlar que tabla o vista se muestra.

### Zona de tabla principal

- Ocupa la mayor parte de la pagina.
- Debe ser clara, exportable y ordenable.
- Usar tabla o matriz segun reporte.

### Panel lateral de detalle

- Derecha.
- Ancho: 320-380 px.
- Opcional por bookmark si la tabla necesita mas ancho.

### Zona de exportacion

- Boton o instrucciones visibles:
  - exportar datos;
  - copiar tabla;
  - abrir reporte paginado si existiera.

## 3. Tipos de reporte

## Recepciones de uva

- Vista SQL origen: `vw_produccion`.
- Columnas principales: fecha recepcion, numero CIU, cosecha, finca, origen, variedad, kilos, Brix, estado recepcion, responsable.
- Filtros: fecha, cosecha, finca, variedad, bodega.
- Orden sugerido: fecha recepcion descendente.
- Uso: auditoria de ingresos de uva y control de CIU.

## Lotes

- Vista SQL origen: `vw_produccion`, `vw_stock_actual`, `vw_trazabilidad`.
- Columnas principales: lote, fecha nacimiento, cosecha, variedad, estado, recepcion asociada, stock actual.
- Filtros: lote, cosecha, variedad, estado, bodega.
- Orden sugerido: fecha lote descendente.
- Uso: consulta maestra de lotes y acceso a trazabilidad.

## Movimientos fisicos

- Vista SQL origen: `vw_movimientos`.
- Columnas principales: fecha movimiento, lote, pileta origen, pileta destino, litros, tipo operacion, responsable, estado.
- Filtros: fecha, lote, pileta, tipo operacion, responsable.
- Orden sugerido: fecha movimiento descendente.
- Uso: auditoria de stock y recorrido fisico.

## Stock

- Vista SQL origen: `vw_stock_actual`.
- Columnas principales: bodega, deposito, pileta, lote, variedad, estado, litros, capacidad, ocupacion.
- Filtros: bodega, deposito, pileta, lote, variedad, estado.
- Orden sugerido: ocupacion descendente.
- Uso: control detallado de stock actual.

## Trazabilidad

- Vista SQL origen: `vw_trazabilidad`.
- Columnas principales: lote padre, lote hijo, tipo relacion, litros aportados, operacion, fecha, estados.
- Filtros: lote, tipo relacion, fecha, cosecha, variedad.
- Orden sugerido: fecha operacion ascendente.
- Uso: auditoria genealogica.

## Mermas

- Vista SQL origen: `vw_movimientos` filtrada por tipo operacion/merma o futura vista especifica.
- Columnas principales: fecha, lote, pileta, litros, tipo operacion, responsable, observaciones.
- Filtros: fecha, lote, pileta, responsable, tipo operacion.
- Orden sugerido: fecha descendente.
- Uso: control de perdidas y causas.

## Fraccionamientos

- Vista SQL origen: vistas futuras de fraccionamiento o movimientos/productos relacionados.
- Columnas principales: fecha, lote, pileta, litros consumidos, responsable, producto generado.
- Filtros: fecha, lote, pileta, responsable.
- Orden sugerido: fecha descendente.
- Uso: auditoria de consumo para producto terminado.

## Productos terminados

- Vista SQL origen: producto terminado o vista futura dedicada.
- Columnas principales: codigo, lote origen, tipo producto, unidades, volumen unidad, litros totales, fecha produccion, estado.
- Filtros: fecha, lote, tipo producto, estado.
- Orden sugerido: fecha produccion descendente.
- Uso: control de producto final y trazabilidad al origen.

## Ventas granel

- Vista SQL origen: `vw_comercial`.
- Columnas principales: fecha, cliente, documento, lote, pileta, litros, responsable, operacion.
- Filtros: fecha, cliente, lote, pileta, responsable.
- Orden sugerido: fecha venta descendente.
- Uso: auditoria comercial y salida fisica.

## Analisis enologico

- Vista SQL origen: `vw_calidad` filtrada por `tipo_registro = analisis_enologico`.
- Columnas principales: fecha, lote, pileta, alcohol, azucar, acidez, pH, Brix, observaciones.
- Filtros: fecha, lote, pileta, tipo registro.
- Orden sugerido: fecha descendente.
- Uso: historial de calidad enologica.

## Fermentacion

- Vista SQL origen: `vw_calidad` filtrada por `tipo_registro = medicion_fermentacion`.
- Columnas principales: fecha, lote, pileta, Baume, temperatura, turno.
- Filtros: fecha, lote, pileta.
- Orden sugerido: fecha descendente.
- Uso: seguimiento de fermentacion.

## Ordenes de trabajo

- Vista SQL origen: `vw_ordenes_trabajo`.
- Columnas principales: fecha, numero, tarea, operario, pileta, lote, estado, fecha completada, operacion vinculada.
- Filtros: fecha, estado, operario, tarea, pileta, lote.
- Orden sugerido: pendientes primero, luego fecha descendente.
- Uso: auditoria operativa.

## Cortes teoricos

- Vista SQL origen: `vw_cortes_teoricos`.
- Columnas principales: fecha, codigo, nombre, responsable, lote, pileta, volumen, snapshots analiticos, operacion vinculada.
- Filtros: fecha, responsable, corte, lote, pileta, operacion vinculada.
- Orden sugerido: fecha descendente.
- Uso: auditoria de simulaciones y comparacion con ejecucion.

## 4. Filtros

### Ano

- Visual sugerido: dropdown o horizontal.
- Vista origen: calendario.
- Interaccion: filtra todos los reportes con fechas relacionadas.

### Fecha desde/hasta

- Visual sugerido: slicer de rango.
- Vista origen: calendario y fechas de cada vista.
- Interaccion: filtro principal obligatorio para reportes grandes.

### Bodega

- Visual sugerido: dropdown.
- Vista origen: vistas con `bodega_id` o `bodega_nombre`.
- Interaccion: filtra todo el contenido.

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: vistas con `lote_codigo`.
- Interaccion: filtra reportes de lote, stock, movimientos, trazabilidad, calidad, comercial.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: vistas con `pileta_codigo`.
- Interaccion: filtra stock, movimientos, calidad, ventas y ordenes.

### Variedad

- Visual sugerido: dropdown.
- Vista origen: produccion, stock, trazabilidad o dimension de variedad.
- Interaccion: filtra lotes y analisis relacionados.

### Cliente

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_comercial[cliente_nombre]`.
- Interaccion: filtra reportes comerciales.

### Responsable

- Visual sugerido: dropdown.
- Vista origen: responsables/operarios de vistas.
- Interaccion: filtra movimientos, ventas, ordenes, cortes.

### Tipo de operacion

- Visual sugerido: dropdown.
- Vista origen: `vw_movimientos[tipo_operacion]`, `vw_trazabilidad[tipo_operacion]`.
- Interaccion: filtra operaciones y movimientos.

### Estado

- Visual sugerido: dropdown o botones.
- Vista origen: estados de lote, pileta, operacion, OT o producto segun reporte.
- Interaccion: filtra estados operativos.

### Tipo de reporte

- Visual sugerido: botones segmentados o dropdown.
- Vista origen: tabla desconectada creada en Power BI.
- Interaccion: cambia tabla visible mediante bookmarks o medidas de visibilidad.

## 5. KPIs superiores

### Total registros

- Medida DAX: `COUNTROWS` de la tabla activa o medidas separadas por reporte.
- Formato: entero.
- Origen: vista seleccionada.
- Comportamiento: cambia segun tipo de reporte.

### Litros totales

- Medida DAX: segun reporte:
  - stock: `Litros Stock Actual`;
  - movimientos: `Litros Movidos`;
  - comercial: `Litros Vendidos`;
  - trazabilidad: litros aportados.
- Formato: `#,0.00 L`.
- Origen: vista activa.
- Comportamiento: visible solo si el reporte tiene litros.

### Kg totales

- Medida DAX: `Kg Uva Recibida`.
- Formato: `#,0.00 kg`.
- Origen: `vw_produccion`.
- Comportamiento: visible en reportes de recepcion/produccion.

### Cantidad de lotes

- Medida DAX: `DISTINCTCOUNT(lote_id)`.
- Formato: entero.
- Origen: vistas con lote.
- Comportamiento: cambia con filtros.

### Cantidad de operaciones

- Medida DAX: `DISTINCTCOUNT(operacion_productiva_id)`.
- Formato: entero.
- Origen: movimientos, trazabilidad, comercial, ordenes o cortes.
- Comportamiento: visible en reportes operativos.

### Ultima fecha registrada

- Medida DAX: `MAX(fecha)` segun reporte activo.
- Formato: `dd/mm/yyyy`.
- Origen: vista seleccionada.
- Comportamiento: muestra ultimo dato disponible del reporte.

## 6. Tabla principal

### Estructura

Dos alternativas:

1. Una pagina con bookmarks que muestran una tabla distinta por tipo de reporte.
2. Varias paginas ocultas de detalle, una por reporte, navegadas desde selector.

Para MVP, se recomienda bookmarks o paginas separadas ocultas si la complejidad crece.

### Columnas dinamicas o paginas separadas

- Power BI no maneja tablas con columnas totalmente dinamicas de forma simple.
- Para mejor control, usar una tabla visual por tipo de reporte y alternar visibilidad.

### Formato

- Encabezado marron madera.
- Texto encabezado crema.
- Filas alternas suaves.
- Numeros alineados a la derecha.
- Fechas con formato uniforme.
- Observaciones truncadas.

### Orden

- Por defecto, fecha descendente.
- En trazabilidad, fecha ascendente para lectura historica.
- En stock, ocupacion descendente.
- En ordenes, pendientes primero.

### Busqueda

- Usar slicers con busqueda para lote, pileta, cliente y responsable.
- Agregar filtro de texto si el reporte lo requiere.

### Tooltips

- Mostrar detalle extendido de observaciones, codigos externos, responsable y estado.

### Exportacion

- Habilitar exportacion de datos desde la tabla.
- Incluir solo columnas necesarias y comprensibles.

## 7. Panel lateral de detalle

### Lote

- Codigo.
- Cosecha.
- Variedad.
- Estado.
- Stock actual.
- Trazabilidad disponible.

### Movimiento

- Fecha.
- Tipo operacion.
- Lote.
- Pileta origen.
- Pileta destino.
- Litros.
- Responsable.

### Recepcion

- CIU.
- Fecha.
- Finca/origen.
- Variedad.
- Kilos.
- Brix.
- Lote generado.

### Venta

- Fecha.
- Cliente.
- Documento.
- Lote.
- Pileta.
- Litros.
- Responsable.

### Analisis

- Fecha.
- Lote.
- Pileta.
- Alcohol.
- Brix.
- pH.
- Acidez.
- Observaciones.

### Orden

- Numero.
- Tarea.
- Operario.
- Estado.
- Fecha completada.
- Operacion vinculada.

### Corte

- Nombre.
- Responsable.
- Fecha.
- Componentes.
- Volumen.
- Snapshots.
- Operacion vinculada.

## 8. Exportacion

### Exportar a Excel/CSV

- Power BI permite exportar datos desde visuales.
- Validar permisos del workspace si se publica.
- Mantener nombres de columnas claros.

### Limitaciones

- Exportacion puede tener limite de filas.
- Algunos visuales exportan datos resumidos y no detalle completo.
- Observaciones largas pueden truncarse segun configuracion.

### Recomendaciones

- Para reportes operativos grandes, usar filtros obligatorios.
- Para auditoria formal, evaluar Power BI Paginated Reports.
- Documentar fecha de exportacion y filtros aplicados.

### Reporte paginado

Conviene si:

- se necesita PDF formal;
- se exportan miles de filas;
- se requiere formato exacto;
- hay auditorias recurrentes.

## 9. Navegacion

### Desde Reportes a Trazabilidad

- Click en lote o relacion genealogica.
- Llevar contexto de lote.

### Desde Reportes a Stock

- Click en pileta o lote con stock.
- Llevar contexto de pileta/lote.

### Desde Reportes a Calidad

- Click en analisis o lote.
- Llevar contexto de lote/pileta/fecha.

### Desde Reportes a Comercial

- Click en cliente o venta.
- Llevar contexto comercial.

### Desde cualquier pagina hacia Reportes

- Boton `Ver detalle` o drill-through.
- Debe conservar filtros principales: lote, pileta, fecha, cliente, operacion.

## 10. Alertas

### Registros incompletos

- Color: ambar.
- Uso: campos obligatorios faltantes o valores nulos relevantes.

### Lote sin trazabilidad

- Color: ambar.
- Uso: lote sin relaciones esperadas.

### Venta sin lote

- Color: rojo vino.
- Uso: no deberia ocurrir en venta detalle.

### Movimiento sin pileta destino/origen cuando corresponda

- Color: ambar o rojo vino segun tipo de operacion.
- Uso: revisar movimiento fisico.

### Analisis sin lote

- Color: ambar.
- Uso: puede ser valido si es por pileta, pero debe revisarse.

### OT sin completar

- Color: gris calido o ambar si es antigua.
- Uso: seguimiento operativo.

## 11. Performance

- Evitar cargar demasiadas columnas visibles.
- Usar filtros obligatorios para reportes grandes.
- Limitar rango de fechas por defecto.
- Paginar o segmentar reportes mediante bookmarks/paginas separadas.
- Evitar tablas gigantes sin filtro.
- Ocultar observaciones largas salvo panel lateral.
- Usar Import mode.
- Evitar relaciones bidireccionales innecesarias.
- Usar medidas agregadas para KPIs superiores.

## 12. Checklist final

- [ ] Selector de reporte funciona.
- [ ] Filtros funcionan.
- [ ] Tabla correcta segun reporte.
- [ ] KPIs cambian segun contexto.
- [ ] Exportacion posible.
- [ ] Navegacion correcta.
- [ ] Panel lateral util.
- [ ] No hay exceso visual.
- [ ] Colores consistentes.
- [ ] Valores coinciden con vistas SQL.
- [ ] Reportes grandes tienen filtros aplicados.
- [ ] Observaciones largas no saturan la tabla.
- [ ] Drill-through conserva contexto.
