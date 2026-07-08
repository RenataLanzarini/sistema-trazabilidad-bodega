# Construccion de la Pagina Trazabilidad en Power BI Desktop

La pagina **Trazabilidad** es la pantalla diferencial del Centro de Control Vitivinicola Lanzarini. Debe permitir seguir la historia completa de un lote hacia atras y hacia adelante, mostrando genealogia, movimientos, litros aportados, operaciones, origen y destino sin perder claridad visual.

## 1. Objetivo de la pagina

### Preguntas que responde

- De donde viene este lote?
- Que recepcion, variedad y origen explican su nacimiento?
- Que lotes padre aportaron litros?
- Que lotes hijo o productos derivaron del lote seleccionado?
- En que piletas estuvo?
- Que operaciones productivas explican los cambios?
- Hubo mermas, fraccionamiento, producto terminado o venta granel?
- Que informacion de calidad existe en el recorrido?

### Usuario principal

- Enologo.
- Gerente / dueno.
- Comercial / administracion para rastrear ventas.

### Relacion con otras paginas

- Stock: recibe lote/pileta seleccionados y devuelve ubicacion fisica actual.
- Produccion: conecta con recepcion de uva, CIU, cosecha y lote generado.
- Calidad: permite consultar analisis y fermentacion por lote/pileta.
- Comercial: muestra ventas granel y clientes asociados.
- Reportes: permite exportar historia completa del lote.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion recomendada: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Sin scroll.

### Menu lateral

- Igual al resto del informe.
- Item activo: `Trazabilidad`.
- Fondo: marron madera `#2B1E1A`.
- Activo: borravino `#3E244A` con acento dorado.

### Header

- Titulo: `Trazabilidad`.
- Subtitulo: `Genealogia, movimientos y destino del lote`.
- Alto: 88 px.
- Estilo sobrio, tecnico y elegante.
- Linea inferior dorada `#B88646`.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px.
- Contenedor blanco, borde suave, radio 8 px.
- El filtro de lote debe ser protagonista.

### Zona central para grafo

- Debe ocupar 55-65% del area util.
- Fondo crema o blanco muy suave.
- Debe tener espacio suficiente para nodos y flechas.
- No colocar tablas grandes dentro de esta zona.

### Panel lateral derecho

- Ancho sugerido: 340-380 px.
- Fondo: blanco.
- Borde izquierdo: `#E8E0D6`.
- Muestra detalle del nodo/arista seleccionado.

### Timeline inferior

- Ubicacion: debajo del grafo.
- Alto: 140-180 px.
- Muestra eventos cronologicos.

### Leyenda

- Ubicacion: esquina superior derecha del grafo o parte inferior del panel lateral.
- Debe explicar colores de nodos, flechas y estados.

## 3. Filtros

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_trazabilidad[lote_padre_codigo]`, `vw_trazabilidad[lote_hijo_codigo]`, `vw_movimientos[lote_codigo]`, `vw_stock_actual[lote_codigo]`.
- Interaccion: obligatorio para construir el grafo inicial. Define el lote central.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_movimientos[pileta_origen_codigo]`, `vw_movimientos[pileta_destino_codigo]`, `vw_stock_actual[pileta_codigo]`.
- Interaccion: filtra movimientos fisicos y nodos de pileta.

### Variedad

- Visual sugerido: dropdown.
- Vista origen: `vw_trazabilidad[lote_padre_variedad]`, `vw_trazabilidad[lote_hijo_variedad]`, `vw_stock_actual[variedad_nombre]`.
- Interaccion: filtra lotes y nodos vinculados.

### Cosecha

- Visual sugerido: dropdown.
- Vista origen: `vw_trazabilidad[lote_padre_cosecha]`, `vw_trazabilidad[lote_hijo_cosecha]`, `vw_stock_actual[cosecha]`.
- Interaccion: limita la genealogia a la cosecha seleccionada.

### Bodega

- Visual sugerido: dropdown.
- Vista origen: todas las vistas con `bodega_id` o `bodega_nombre`.
- Interaccion: afecta toda la pagina.

### Tipo de operacion

- Visual sugerido: dropdown o botones segmentados.
- Vista origen: `vw_movimientos[tipo_operacion]`, `vw_trazabilidad[tipo_operacion]`.
- Interaccion: filtra operaciones y aristas.

### Fecha

- Visual sugerido: slicer de rango.
- Vista origen: `vw_movimientos[fecha_movimiento]`, `vw_trazabilidad[fecha_operacion]`, `vw_produccion[fecha_recepcion]`, `vw_comercial[fecha_venta]`.
- Interaccion: filtra timeline, movimientos y operaciones.

### Cliente

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_comercial[cliente_nombre]`.
- Interaccion: filtra ventas granel relacionadas con el lote.

### Producto terminado

- Visual sugerido: dropdown o busqueda cuando exista vista/dimension de productos terminados.
- Vista origen: producto terminado o reporte derivado de fraccionamiento.
- Interaccion: permite rastrear producto final hacia lote origen.

## 4. KPIs superiores

### Litros del lote seleccionado

- Medida DAX: `Litros Stock Actual` filtrada por lote.
- Formato: `#,0.00 L`.
- Origen: `vw_stock_actual`.
- Tooltip: litros actuales, piletas actuales, estado del lote.
- Interaccion: click filtra panel a stock actual.

### Cantidad de lotes padre

- Medida DAX sugerida: `DISTINCTCOUNT(vw_trazabilidad[lote_padre_id])`.
- Formato: entero.
- Origen: `vw_trazabilidad`.
- Tooltip: cantidad de lotes que aportan al lote seleccionado.
- Interaccion: resalta nodos padre.

### Cantidad de lotes hijo

- Medida DAX sugerida: `DISTINCTCOUNT(vw_trazabilidad[lote_hijo_id])`.
- Formato: entero.
- Origen: `vw_trazabilidad`.
- Tooltip: cantidad de lotes derivados.
- Interaccion: resalta nodos hijo.

### Operaciones asociadas

- Medida DAX sugerida: `DISTINCTCOUNT(vw_movimientos[operacion_productiva_id])`.
- Formato: entero.
- Origen: `vw_movimientos`, `vw_trazabilidad`.
- Tooltip: operaciones productivas vinculadas al lote.
- Interaccion: filtra timeline y tabla de movimientos.

### Mermas asociadas

- Medida DAX: `Litros Merma` o conteo de operaciones/relaciones de merma si se expone.
- Formato: litros o entero segun medida.
- Origen: `vw_movimientos` y futuras vistas especificas de merma si se crean.
- Tooltip: litros perdidos, fecha y operacion.
- Interaccion: resalta nodos de merma.

### Productos/Ventas asociadas

- Medida DAX: `Litros Vendidos` y conteo de productos terminados si se carga esa vista.
- Formato: litros o unidades.
- Origen: `vw_comercial`, productos terminados/fraccionamiento.
- Tooltip: ventas, clientes, productos y litros asociados.
- Interaccion: resalta nodos destino.

## 5. Grafo central

### Visual nativo recomendado si no se usa grafo avanzado

- Decomposition Tree para explorar jerarquias.
- Matrix padre/hijo para relaciones.
- Table de aristas con formato condicional.
- Timeline para secuencia.

### Visual personalizado recomendado

Si la politica de Power BI permite visuales custom:

- Force-Directed Graph.
- Network Navigator.
- Drill Down Network PRO.
- Sankey si se priorizan flujos de litros.

### Estructura de nodos

Cada nodo representa una entidad de trazabilidad:

- Recepcion.
- Lote.
- Operacion.
- Pileta.
- Merma.
- Fraccionamiento.
- Producto terminado.
- Venta granel.
- Cliente.

### Informacion minima por nodo

- Codigo.
- Tipo.
- Fecha.
- Litros.
- Variedad o categoria.
- Estado.
- Pileta asociada si corresponde.

### Estructura de aristas

Cada arista representa relacion o flujo:

- nodo origen;
- nodo destino;
- litros;
- fecha;
- tipo de operacion;
- tipo de relacion;
- operacion asociada.

### Direccion de lectura

- Izquierda a derecha.
- Origen y recepcion a la izquierda.
- Lote seleccionado al centro.
- Destinos, productos y ventas a la derecha.
- Movimientos fisicos pueden leerse de arriba hacia abajo dentro de cada etapa.

### Colores de nodos

- Recepcion: crema con borde dorado.
- Lote: blanco con borde borravino o color de variedad.
- Operacion: gris calido.
- Pileta: blanco con borde marron.
- Merma: rojo vino.
- Fraccionamiento: dorado suave.
- Producto terminado: verde suave.
- Venta granel: neutro oscuro con acento dorado.
- Cliente: marron claro o neutro.

### Flechas

- Genealogia: flecha dorada.
- Movimiento fisico: flecha gris calido.
- Salida comercial: flecha marron.
- Merma: flecha rojo vino.
- Fraccionamiento/producto terminado: flecha verde suave o dorada.

### Etiquetas de litros

- Mostrar en aristas principales.
- Formato: `#,0.00 L`.
- Si hay porcentaje disponible: `#,0.00 L - 00.00%`.
- Evitar superposicion; usar tooltip cuando el grafo sea denso.

### Etiquetas de operacion

- Mostrar tipo de operacion abreviado.
- Detalle completo en tooltip o panel lateral.

### Agrupacion por etapas

Separar visualmente:

1. Origen / recepcion.
2. Lote y genealogia.
3. Movimientos / piletas.
4. Procesos: merma, fraccionamiento.
5. Destino: producto terminado, venta, cliente.

### Seleccion de nodo

- Nodo seleccionado: borde borravino grueso y sombra suave.
- Nodos conectados: color normal.
- Nodos no relacionados: atenuar al 30-40%.

### Resaltado de ruta

- La ruta activa debe quedar en dorado.
- El resto del grafo debe bajar contraste.
- Panel lateral muestra resumen de la ruta.

### Atenuacion de nodos no relacionados

- Aplicar transparencia visual.
- No ocultar completamente salvo que el usuario filtre.

## 6. Aristas

### Lote padre -> lote hijo

- Origen: `vw_trazabilidad`.
- Campos: `lote_padre_id`, `lote_hijo_id`, `litros_aportados`, `tipo_relacion`, `fecha_operacion`.
- Uso: genealogia.

### Operacion -> movimiento

- Origen: `vw_movimientos`.
- Campos: `operacion_productiva_id`, `movimiento_fisico_id`, `tipo_operacion`, `litros`, `fecha_movimiento`.
- Uso: explicar cambio fisico.

### Lote -> producto terminado

- Origen: producto terminado/fraccionamiento.
- Campos: lote origen, codigo producto, litros totales, fecha produccion.
- Uso: trazabilidad hacia producto final.

### Lote -> venta granel

- Origen: `vw_comercial`.
- Campos: `lote_id`, `venta_granel_id`, `cliente_id`, `litros`, `fecha_venta`.
- Uso: salida comercial.

### Lote -> merma

- Origen: `vw_movimientos` filtrado por tipo de operacion/merma o vista especifica futura.
- Campos: lote, litros, fecha, operacion.
- Uso: perdida registrada.

### Datos obligatorios de arista

- Litros aportados o movidos.
- Fecha.
- Tipo de operacion.
- Codigo o identificador de operacion si existe.

## 7. Timeline inferior

### Eventos a mostrar

- Recepcion.
- Nacimiento de lote.
- Movimientos.
- Analisis relevantes.
- Mermas.
- Fraccionamiento.
- Venta.
- Producto terminado.

### Campos por evento

- Fecha.
- Tipo.
- Icono.
- Color.
- Tooltip.
- Vinculo con nodo del grafo.

### Iconos sugeridos

- Recepcion: ingreso/documento.
- Lote: etiqueta.
- Movimiento: flecha.
- Analisis: matraz.
- Merma: alerta/gota.
- Fraccionamiento: botella.
- Venta: documento comercial.
- Producto terminado: caja/botella.

### Colores

- Recepcion: dorado.
- Lote: borravino.
- Movimiento: gris calido.
- Calidad: marron.
- Merma: rojo vino.
- Fraccionamiento: verde suave.
- Venta: dorado oscuro.

### Interaccion

- Click en evento resalta nodo/arista correspondiente.
- Hover muestra tooltip.
- Seleccion de periodo filtra grafo.

## 8. Panel lateral de detalle

### Lote

- Identificacion: codigo y lote_id oculto si no es auditoria.
- Fecha nacimiento.
- Litros actuales.
- Estado.
- Variedad.
- Cosecha.
- Piletas actuales.
- Padres e hijos.
- Botones: `Ver Stock`, `Ver Calidad`, `Exportar historia`.

### Operacion

- Tipo.
- Fecha.
- Responsable.
- Estado.
- Anulada.
- Motivo anulacion.
- Movimientos relacionados.
- Boton: `Ver movimientos`.

### Pileta

- Codigo.
- Deposito.
- Capacidad.
- Litros actuales.
- Ocupacion.
- Estado.
- Lotes asociados.
- Boton: `Ver Stock`.

### Producto terminado

- Codigo.
- Fecha produccion.
- Lote origen.
- Cantidad unidades.
- Volumen por unidad.
- Litros totales.
- Estado.
- Boton: `Ver Reportes`.

### Venta

- Documento.
- Fecha.
- Cliente.
- Litros.
- Lote.
- Pileta.
- Responsable.
- Boton: `Ver Comercial`.

### Merma

- Fecha.
- Litros.
- Causa si esta disponible.
- Lote.
- Pileta.
- Operacion.
- Responsable.
- Boton: `Ver Reportes`.

## 9. Leyenda

### Color por tipo de nodo

- Recepcion: crema/dorado.
- Lote: blanco/borravino.
- Operacion: gris calido.
- Pileta: blanco/marron.
- Merma: rojo vino.
- Fraccionamiento: dorado suave.
- Producto terminado: verde suave.
- Venta granel: neutro oscuro.
- Cliente: marron claro.

### Color por variedad/tipo de vino

- Tintos: paleta de tintos.
- Blancos: paleta de blancos.
- Rosados: paleta de rosados.
- Sin clasificar: neutros.

### Tipos de flecha

- Dorada: genealogia.
- Gris: movimiento fisico.
- Roja: merma.
- Verde/dorada: fraccionamiento/producto terminado.
- Marron: venta granel.

### Estados

- Correcto: verde oliva.
- Advertencia: ambar.
- Error: rojo vino.
- Pendiente: gris calido.
- Completado: verde suave.

## 10. Visuales alternativos

### Matriz padre/hijo

- Util si no se permite grafo.
- Filas: lote padre, lote hijo.
- Valores: litros aportados.

### Tabla de aristas

- Visual mas confiable para auditoria.
- Debe incluir padre, hijo, litros, fecha y operacion.

### Sankey

- Muy util para litros aportados y flujos.
- Menos preciso para mostrar operaciones y piletas.

### Decomposition Tree

- Bueno para explorar jerarquias.
- Limitado para genealogia bidireccional.

### Hierarchy Slicer

- Util como filtro auxiliar.
- No reemplaza el grafo.

### Visual custom de red

- Mejor alternativa para experiencia visual.
- Validar performance y politicas de seguridad antes de usar.

## 11. Interacciones

### Click en nodo

- Selecciona nodo.
- Resalta conexiones directas.
- Actualiza panel lateral.
- Atenua nodos no relacionados.

### Click en arista

- Muestra detalle de litros, fecha, tipo de operacion y observaciones.
- Resalta ruta entre origen y destino.

### Click en timeline

- Selecciona evento.
- Filtra o resalta nodo/arista asociada.
- Actualiza panel lateral.

### Drill-through a Calidad

- Desde lote o pileta.
- Lleva contexto de lote/pileta y fecha si aplica.

### Drill-through a Stock

- Desde lote o pileta.
- Lleva contexto de stock actual.

### Drill-through a Comercial

- Desde venta granel o cliente.
- Lleva contexto de venta/lote.

### Exportar historia del lote

- Desde panel lateral.
- Destino sugerido: Reportes con lote filtrado.
- Debe mostrar relaciones, movimientos, calidad y salidas.

## 12. Alertas

### Lote sin origen

- Color: ambar.
- Condicion: lote sin recepcion o sin relacion padre cuando deberia tenerla.

### Lote sin movimientos

- Color: ambar.
- Condicion: lote sin movimientos fisicos asociados.

### Stock inconsistente

- Color: rojo vino.
- Condicion: stock negativo o capacidad superada.

### Merma alta

- Color: ambar o rojo vino.
- Condicion: merma supera umbral definido.

### Venta sin trazabilidad completa

- Color: ambar.
- Condicion: venta visible sin camino claro a origen.

### Producto terminado sin lote origen

- Color: rojo vino.
- Condicion: producto terminado sin lote asociado.

## 13. Performance

- El filtro de lote debe ser obligatorio para cargar el grafo completo.
- Limitar profundidad inicial del grafo: un nivel hacia atras y un nivel hacia adelante.
- No cargar todos los nodos del sistema a la vez.
- Usar aristas base de `vw_trazabilidad`.
- Usar `vw_movimientos` para detalle fisico, no para dibujar todo el universo.
- Usar panel lateral para informacion extensa.
- Evitar etiquetas largas dentro de nodos.
- Usar tooltips para datos secundarios.
- Si se usa visual custom, probar con volumen real antes de publicarlo.
- Mantener tablas filtradas por lote seleccionado.

## 14. Checklist final

- [ ] Filtro de lote obligatorio.
- [ ] Grafo legible.
- [ ] Nodos con informacion minima.
- [ ] Flechas con litros.
- [ ] Timeline sincronizado.
- [ ] Panel lateral funcional.
- [ ] Drill-through correcto.
- [ ] Alertas visibles.
- [ ] Colores consistentes.
- [ ] No se pierde informacion tecnica.
- [ ] Valores coinciden con `vw_trazabilidad` y `vw_movimientos`.
- [ ] Nodos no relacionados se atenuan correctamente.
- [ ] Ruta seleccionada se resalta.
- [ ] Leyenda visible y comprensible.
