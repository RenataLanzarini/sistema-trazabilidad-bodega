# Paginas del Centro de Control Vitivinicola Lanzarini

Este documento define el diseno funcional completo de las paginas restantes del dashboard, manteniendo continuidad con el Dashboard Ejecutivo, el Design System Lanzarini y la experiencia de usuario definida para el Centro de Control Vitivinicola.

## 1. Produccion

### Objetivo

Analizar la recepcion de uva, la creacion de lotes y la evolucion productiva inicial por cosecha, variedad, finca y origen.

### Usuario principal

Enologo, gerente / dueno.

### Preguntas que debe responder

- Cuantos kilos de uva se recibieron?
- De que finca, origen o variedad provino la uva?
- Que lotes nacieron desde cada CIU?
- Como evoluciona la recepcion por mes o cosecha?
- Que rendimiento o indicadores iniciales se observan?

### KPIs

- Kg uva recibida.
- Cantidad de CIU.
- Lotes generados.
- Promedio Brix.
- Kilos por variedad principal.
- Rendimiento estimado si existe dato disponible.

### Graficos

- Produccion mensual: columnas por kg recibidos.
- Kg por variedad: barras horizontales.
- Recepcion por finca/origen: barras o treemap controlado.
- Brix promedio por periodo: linea.
- Lotes generados por estado: dona simple o barras.

### Tablas

- Recepciones de uva: CIU, fecha, finca, variedad, kilos, Brix, estado.
- Lotes generados: codigo, fecha nacimiento, cosecha, variedad, estado, recepcion asociada.

### Filtros

- Ano.
- Cosecha.
- Bodega.
- Variedad.
- Finca.
- Origen de uva.
- Estado recepcion.
- Tipo de producto.

### Drill-through

- Produccion -> Stock por lote.
- Produccion -> Trazabilidad por lote.
- Produccion -> Calidad por lote o pileta si ya existe dato asociado.

### Panel lateral de detalle

Opcional. Se muestra al seleccionar una CIU o lote:

- CIU.
- fecha.
- kilos.
- finca.
- variedad.
- Brix.
- lotes generados.
- responsable.

### Alertas visuales

- Recepcion sin lote asociado.
- Brix faltante.
- Lote sin variedad.
- Datos incompletos de CIU.

### Interacciones

- Click en variedad filtra lotes, recepciones y graficos.
- Click en CIU muestra lotes generados.
- Click en lote permite drill-through a trazabilidad.

### Vistas SQL necesarias

- `vw_produccion`
- `vw_movimientos`
- `vw_stock_actual`

### Medidas DAX necesarias

- Kg Uva Recibida.
- Promedio Brix.
- Litros Movidos.
- Lotes Generados.
- Cantidad CIU.

### Relacion con otras paginas

- Envia contexto a Stock por lote.
- Envia contexto a Trazabilidad por lote.
- Envia contexto a Calidad por lote/pileta.

### Consideraciones visuales

- Usar dorado para kilos recibidos.
- Usar paleta de datos para variedades.
- Evitar saturar con demasiadas fincas visibles; usar ranking top N.

## 2. Stock

### Objetivo

Controlar litros actuales, ocupacion, capacidad y distribucion por lote, pileta, bodega y variedad.

### Usuario principal

Enologo, gerente / dueno, operario.

### Preguntas que debe responder

- Cuantos litros hay actualmente?
- En que piletas esta cada lote?
- Que piletas estan cerca de capacidad maxima?
- Cual es el stock por variedad o cosecha?
- Como era el stock a una fecha determinada?

### KPIs

- Litros stock actual.
- Capacidad total.
- Capacidad ocupada %.
- Piletas ocupadas.
- Lotes con stock.
- Piletas en advertencia por ocupacion.

### Graficos

- Matriz lote por pileta.
- Barras de ocupacion por pileta.
- Stock por variedad.
- Stock por estado de lote.
- Tendencia de stock historico si se habilita fecha de corte.

### Tablas

- Stock actual: bodega, deposito, pileta, lote, variedad, litros, capacidad, ocupacion.
- Ultimos movimientos de la pileta o lote seleccionado.

### Filtros

- Bodega.
- Deposito.
- Pileta.
- Lote.
- Cosecha.
- Variedad.
- Estado pileta.
- Estado lote.
- Fecha de corte para stock historico.

### Drill-through

- Stock -> Trazabilidad por lote.
- Stock -> Calidad por lote/pileta.
- Stock -> Produccion por lote.
- Stock -> Reportes por pileta.

### Panel lateral de detalle

Debe existir. Al seleccionar una pileta o lote muestra:

- codigo.
- capacidad.
- litros actuales.
- ocupacion.
- estado.
- lote/s contenidos.
- ultimos movimientos.
- alertas.

### Alertas visuales

- Pileta sobre 90% de capacidad.
- Pileta sin estado.
- Stock negativo no deberia existir; si aparece, alerta critica.
- Lote con stock distribuido en muchas piletas.

### Interacciones

- Click en pileta filtra movimientos y calidad.
- Click en lote habilita drill-through a trazabilidad.
- Selector de fecha recalcula stock historico.

### Vistas SQL necesarias

- `vw_stock_actual`
- `vw_movimientos`
- `vw_calidad`

### Medidas DAX necesarias

- Litros Stock Actual.
- Capacidad Total.
- Capacidad Ocupada %.
- Litros Movidos.
- Piletas Ocupadas.

### Relacion con otras paginas

- Recibe contexto desde Inicio y Produccion.
- Envia contexto a Trazabilidad y Calidad.

### Consideraciones visuales

- Usar matriz clara y compacta.
- Ocupacion con escala de estados: correcto, advertencia, error.
- No usar muchos colores de variedad en la matriz; priorizar legibilidad.

## 3. Trazabilidad

### Objetivo

Reconstruir la genealogia y recorrido de un lote o producto, hacia atras y hacia adelante, con una lectura visual clara.

### Usuario principal

Enologo, gerente / dueno, comercial / administracion.

### Preguntas que debe responder

- De donde viene este lote?
- Que lotes participaron en una mezcla?
- A que lotes, productos o ventas fue este lote?
- Que litros aporto cada lote padre?
- Que operaciones, piletas y fechas intervinieron?

### KPIs

- Lotes padres.
- Lotes hijos.
- Litros aportados.
- Operaciones vinculadas.
- Mermas asociadas.
- Salidas comerciales o fraccionamientos.

### Graficos

- Grafo central de trazabilidad.
- Timeline cronologica.
- Mini tabla de aristas padre-hijo.
- Resumen de litros por tipo de nodo.

### Tablas

- Relaciones genealogicas: padre, hijo, litros, tipo relacion, operacion.
- Movimientos del lote: fecha, origen, destino, litros, responsable.

### Filtros

- Lote.
- Cosecha.
- Variedad.
- Tipo relacion.
- Direccion: hacia atras / hacia adelante.
- Mostrar operaciones.
- Mostrar piletas.
- Mostrar ventas/fraccionamientos.

### Drill-through

- Trazabilidad -> Calidad por lote.
- Trazabilidad -> Comercial por venta.
- Trazabilidad -> Stock por pileta/lote.
- Trazabilidad -> Produccion por CIU/lote.

### Panel lateral de detalle

Debe existir. Al seleccionar un nodo o arista muestra:

- tipo de nodo.
- codigo.
- fecha.
- litros.
- variedad.
- pileta.
- responsable.
- observaciones.
- conexiones entrantes y salientes.

### Alertas visuales

- Lote sin padres cuando deberia tenerlos.
- Relacion sin litros aportados.
- Operacion anulada en la cadena.
- Dato de calidad faltante.

### Interacciones

- Click en nodo resalta conexiones directas.
- Click en arista muestra litros aportados.
- Doble click navega a pagina relacionada.
- Timeline filtra el grafo por periodo.

### Vistas SQL necesarias

- `vw_trazabilidad`
- `vw_movimientos`
- `vw_produccion`
- `vw_calidad`
- `vw_comercial`

### Medidas DAX necesarias

- Litros Movidos.
- Litros Stock Actual.
- Litros Vendidos.
- Litros Merma.
- Conteo Relaciones.

### Relacion con otras paginas

- Recibe contexto desde Inicio, Produccion, Stock, Calidad y Comercial.
- Envia contexto a Calidad, Stock, Comercial y Reportes.

### Consideraciones visuales

- El grafo ocupa el area principal.
- Etiquetas cortas en nodos.
- Detalle completo solo en panel lateral.
- Colores de nodo por tipo, no por decoracion.

## 4. Calidad

### Objetivo

Monitorear analisis enologicos y mediciones de fermentacion por lote, pileta y fecha.

### Usuario principal

Enologo.

### Preguntas que debe responder

- Como evolucionan alcohol, pH, acidez y Brix?
- Como evoluciona Baume y temperatura durante fermentacion?
- Que lotes o piletas estan fuera de rango?
- Cual es el ultimo analisis disponible?

### KPIs

- Promedio Alcohol.
- Promedio pH.
- Promedio Brix.
- Promedio Baume.
- Temperatura Promedio.
- Analisis registrados.

### Graficos

- Linea de pH por fecha.
- Linea de alcohol por fecha.
- Baume y temperatura por fecha.
- Barras por lote/pileta con ultimos valores.
- Dispersion pH vs alcohol si aporta analisis.

### Tablas

- Analisis enologicos: fecha, lote, pileta, alcohol, azucar, acidez, pH.
- Mediciones fermentacion: fecha, lote, pileta, Baume, temperatura, turno.

### Filtros

- Fecha.
- Lote.
- Pileta.
- Bodega.
- Tipo registro.
- Variedad.
- Rango pH.
- Rango Baume.

### Drill-through

- Calidad -> Trazabilidad por lote.
- Calidad -> Stock por pileta.
- Calidad -> Produccion por lote.

### Panel lateral de detalle

Debe existir. Muestra ultimo analisis o medicion seleccionada:

- lote.
- pileta.
- fecha.
- valores analiticos.
- observaciones.
- comparacion contra ultimo registro.

### Alertas visuales

- pH fuera de rango.
- Baume sin medicion reciente.
- Temperatura alta.
- Analisis parcial o incompleto.

### Interacciones

- Click en punto de linea filtra detalle.
- Click en lote navega a trazabilidad.
- Seleccion de pileta filtra stock.

### Vistas SQL necesarias

- `vw_calidad`
- `vw_stock_actual`
- `vw_trazabilidad`

### Medidas DAX necesarias

- Promedio Brix.
- Promedio Alcohol.
- Promedio pH.
- Promedio Baume.
- Temperatura Promedio.
- Ultimo Analisis.

### Relacion con otras paginas

- Recibe contexto desde Stock y Trazabilidad.
- Envia contexto a Trazabilidad y Reportes.

### Consideraciones visuales

- Usar graficos de linea limpios.
- Colores estables por indicador.
- Alertas visuales discretas, no alarmistas salvo casos criticos.

## 5. Comercial

### Objetivo

Analizar ventas a granel, clientes, litros vendidos y relacion de cada venta con lote/pileta de origen.

### Usuario principal

Comercial / administracion, gerente / dueno.

### Preguntas que debe responder

- Cuantos litros se vendieron?
- A que clientes?
- Desde que lote y pileta salio la venta?
- Como evolucionan las ventas por fecha?
- Que stock queda disponible?

### KPIs

- Litros Vendidos.
- Clientes con venta.
- Cantidad de ventas.
- Lote mas vendido.
- Litros promedio por venta.

### Graficos

- Ventas por fecha.
- Ventas por cliente.
- Ventas por lote.
- Ventas por pileta.

### Tablas

- Ventas granel: fecha, cliente, documento, lote, pileta, litros, responsable.
- Detalle por cliente: total litros, cantidad operaciones, ultima venta.

### Filtros

- Fecha.
- Cliente.
- Lote.
- Pileta.
- Bodega.
- Responsable.
- Documento.

### Drill-through

- Comercial -> Trazabilidad por lote vendido.
- Comercial -> Stock por lote/pileta.
- Comercial -> Reportes por cliente.

### Panel lateral de detalle

Debe existir. Muestra venta seleccionada:

- cliente.
- documento.
- fecha.
- lote.
- pileta.
- litros.
- responsable.
- operacion productiva.

### Alertas visuales

- Venta sin documento.
- Venta de lote con trazabilidad incompleta.
- Venta con stock actual bajo posterior.

### Interacciones

- Click en cliente filtra ventas y tabla.
- Click en lote habilita trazabilidad.
- Click en fecha filtra tendencia y detalle.

### Vistas SQL necesarias

- `vw_comercial`
- `vw_stock_actual`
- `vw_trazabilidad`

### Medidas DAX necesarias

- Litros Vendidos.
- Cantidad Ventas.
- Clientes Activos.
- Litros Promedio por Venta.

### Relacion con otras paginas

- Recibe contexto desde Inicio.
- Envia contexto a Trazabilidad, Stock y Reportes.

### Consideraciones visuales

- Estetica sobria y administrativa.
- Tablas claras y exportables.
- Usar dorado para ventas destacadas, no para todos los clientes.

## 6. Ordenes de Trabajo

### Objetivo

Controlar tareas operativas pendientes y completadas, por operario, tarea, lote y pileta.

### Usuario principal

Operario, enologo, gerente / dueno.

### Preguntas que debe responder

- Que tareas estan pendientes?
- Que tareas se completaron?
- Quien es el operario asignado?
- Sobre que lote o pileta trabaja cada OT?
- Que OT estan vinculadas a operaciones productivas?

### KPIs

- Ordenes Pendientes.
- Ordenes Completadas.
- % Cumplimiento.
- Ordenes por operario.
- Ordenes vencidas o sin completar.

### Graficos

- Pendientes vs completadas.
- Ordenes por tarea.
- Ordenes por operario.
- Ordenes por fecha.
- Ordenes por pileta.

### Tablas

- Listado operativo: numero, fecha, tarea, operario, lote, pileta, estado.
- Observaciones y fecha de completado.

### Filtros

- Fecha.
- Tarea.
- Operario.
- Pileta.
- Lote.
- Estado completada/pendiente.
- Operacion vinculada.

### Drill-through

- Ordenes -> Stock por pileta/lote.
- Ordenes -> Trazabilidad por lote.
- Ordenes -> Operacion Productiva asociada.

### Panel lateral de detalle

Debe existir. Muestra:

- numero.
- tarea.
- operario.
- fecha.
- lote/pileta.
- estado.
- observaciones.
- operacion vinculada.

### Alertas visuales

- OT pendiente vencida.
- OT sin operario.
- OT completada sin observaciones.
- OT sin lote/pileta cuando deberia tenerlo.

### Interacciones

- Click en operario filtra tablero.
- Click en tarea filtra pendientes.
- Click en lote navega a trazabilidad.

### Vistas SQL necesarias

- `vw_ordenes_trabajo`
- `vw_stock_actual`
- `vw_movimientos`

### Medidas DAX necesarias

- Ordenes Pendientes.
- Ordenes Completadas.
- % Cumplimiento OT.
- Ordenes Vencidas.

### Relacion con otras paginas

- Recibe contexto desde Inicio y Trazabilidad.
- Envia contexto a Stock y Reportes.

### Consideraciones visuales

- Debe sentirse operativo.
- Priorizar tablas y estados.
- Usar colores de estado con claridad.

## 7. Corte Teorico

### Objetivo

Analizar simulaciones de mezcla/corte, componentes, volumen proyectado y snapshots analiticos sin afectar stock real.

### Usuario principal

Enologo.

### Preguntas que debe responder

- Que cortes teoricos existen?
- Que lotes y piletas componen cada corte?
- Cual es el volumen al corte?
- Que valores analiticos tenia cada componente?
- Existe operacion real vinculada?

### KPIs

- Cortes teoricos creados.
- Volumen total al corte.
- Componentes por corte.
- Cortes vinculados a operacion real.
- Promedio alcohol snapshot.
- Promedio pH snapshot.

### Graficos

- Componentes del corte por volumen.
- Comparacion volumen actual vs volumen al corte.
- Snapshots analiticos por componente.
- Cortes por fecha/responsable.

### Tablas

- Cortes: fecha, nombre, responsable, operacion vinculada.
- Detalles: lote, pileta, volumen, varietal snapshot, alcohol, acidez, pH.

### Filtros

- Fecha.
- Responsable.
- Lote.
- Pileta.
- Operacion vinculada.
- Corte.

### Drill-through

- Corte Teorico -> Stock por lote/pileta.
- Corte Teorico -> Calidad por lote/pileta.
- Corte Teorico -> Trazabilidad por lote.

### Panel lateral de detalle

Debe existir. Muestra corte seleccionado:

- nombre.
- fecha.
- responsable.
- componentes.
- volumen total.
- snapshots.
- operacion vinculada.

### Alertas visuales

- Corte sin detalle.
- Corte sin responsable.
- Corte vinculado a operacion anulada.
- Diferencia significativa entre volumen snapshot y stock actual.

### Interacciones

- Click en componente filtra stock/calidad.
- Click en operacion vinculada muestra movimientos reales.
- Click en lote navega a trazabilidad.

### Vistas SQL necesarias

- `vw_cortes_teoricos`
- `vw_stock_actual`
- `vw_calidad`
- `vw_movimientos`

### Medidas DAX necesarias

- Volumen al Corte.
- Componentes por Corte.
- Promedio Alcohol Snapshot.
- Promedio pH Snapshot.
- Diferencia Volumen Actual vs Corte.

### Relacion con otras paginas

- Recibe contexto desde Calidad y Stock.
- Envia contexto a Trazabilidad y Produccion.

### Consideraciones visuales

- Debe diferenciar simulacion de operacion real.
- Usar dorado y neutros, evitando colores de alerta salvo diferencias importantes.
- Incluir aviso visual: "No modifica stock real".

## 8. Reportes

### Objetivo

Ofrecer tablas exportables y vistas detalladas para auditoria, administracion y analisis externo.

### Usuario principal

Gerente / dueno, comercial / administracion, enologo.

### Preguntas que debe responder

- Que datos necesito exportar?
- Cual es el detalle completo por lote, pileta, cliente u operacion?
- Que registros respaldan un indicador?
- Que informacion sirve para auditoria?

### KPIs

- Registros visibles.
- Periodo seleccionado.
- Lotes incluidos.
- Operaciones incluidas.
- Total litros segun reporte.

### Graficos

- Minimos. La pagina debe priorizar tablas.
- Puede incluir tarjetas de resumen arriba.

### Tablas

- Reporte de stock.
- Reporte de movimientos.
- Reporte de trazabilidad.
- Reporte de calidad.
- Reporte comercial.
- Reporte de ordenes de trabajo.
- Reporte de cortes teoricos.

### Filtros

- Fecha.
- Bodega.
- Lote.
- Pileta.
- Variedad.
- Cliente.
- Responsable.
- Tipo operacion.
- Estado.
- Tipo de reporte.

### Drill-through

- Reportes -> paginas de detalle segun entidad.
- Desde cualquier pagina -> Reportes con contexto prefiltrado.

### Panel lateral de detalle

Opcional. Puede mostrar resumen de filtros aplicados y explicacion del reporte.

### Alertas visuales

- Datos incompletos.
- Reporte sin registros.
- Filtros demasiado amplios.
- Exportacion con demasiados registros si aplica.

### Interacciones

- Seleccion de tipo de reporte cambia tabla visible.
- Click en registro habilita drill-through a pagina correspondiente.
- Filtros avanzados refinan el dataset exportable.

### Vistas SQL necesarias

- `vw_stock_actual`
- `vw_produccion`
- `vw_movimientos`
- `vw_trazabilidad`
- `vw_calidad`
- `vw_comercial`
- `vw_ordenes_trabajo`
- `vw_cortes_teoricos`

### Medidas DAX necesarias

- Litros Stock Actual.
- Kg Uva Recibida.
- Litros Movidos.
- Litros Vendidos.
- Ordenes Pendientes.
- Ordenes Completadas.
- Conteos por entidad.

### Relacion con otras paginas

- Recibe contexto desde todas las paginas.
- Debe funcionar como salida de auditoria y exportacion.

### Consideraciones visuales

- Mas densa y utilitaria que ejecutiva.
- Tablas limpias, filtros claros, encabezados fijos.
- Evitar decoracion; priorizar legibilidad y exportabilidad.
