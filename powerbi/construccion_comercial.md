# Construccion de la Pagina Comercial en Power BI Desktop

Esta guia documenta como construir la pagina **Comercial** del Centro de Control Vitivinicola Lanzarini. La pagina debe mostrar ventas a granel, clientes, productos terminados, litros vendidos y relacion con trazabilidad.

## 1. Objetivo de la pagina

### Preguntas que responde

- Cuantos litros se vendieron a granel?
- A que clientes se vendio mas volumen?
- Desde que lote y pileta salio cada venta?
- Que responsables registraron ventas?
- Que productos terminados existen y como se relacionan con lotes?
- Que ventas requieren revision de trazabilidad?

### Usuario principal

- Comercial / administracion.
- Gerente / dueno.

### Relacion con otras paginas

- Dashboard Ejecutivo: recibe contexto desde KPI `Ventas granel`.
- Trazabilidad: permite rastrear lote vendido hasta origen.
- Reportes: permite exportar detalle comercial y auditoria.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion recomendada: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Sin scroll.

### Menu lateral

- Mismo menu global.
- Item activo: `Comercial`.
- Fondo marron madera `#2B1E1A`.
- Activo borravino `#3E244A` con acento dorado.

### Header

- Titulo: `Comercial`.
- Subtitulo: `Ventas a granel, clientes y productos terminados`.
- Alto: 88 px.
- Linea inferior dorada.

### Filtros superiores

- Ubicacion: debajo del header.
- Alto: 72 px.
- Contenedor blanco con borde suave.

### Zona KPI

- Seis tarjetas superiores.
- Fondo blanco.
- Acento dorado y neutros comerciales.

### Zona de graficos

- Fila principal: ventas por mes, ventas por cliente, litros por lote/variedad.
- Fila secundaria: productos terminados, responsables, clientes top.

### Panel lateral de detalle

- Derecha.
- Ancho: 320-380 px.
- Muestra detalle de cliente, venta, lote o producto.

### Tabla inferior

- Tabla comercial detallada.
- Debe ser exportable y ordenada por fecha.

## 3. Filtros

### Ano

- Visual sugerido: slicer dropdown o horizontal.
- Vista origen: calendario / `vw_comercial[fecha_venta]`.
- Interaccion: afecta ventas, clientes y tabla.

### Fecha

- Visual sugerido: slicer de rango.
- Vista origen: `vw_comercial[fecha_venta]`.
- Interaccion: filtra toda la pagina por periodo.

### Cliente

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_comercial[cliente_nombre]`.
- Interaccion: filtra ventas, KPIs y panel lateral.

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_comercial[lote_codigo]`.
- Interaccion: filtra ventas por lote y habilita trazabilidad.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_comercial[pileta_codigo]`.
- Interaccion: filtra ventas por pileta de origen.

### Variedad

- Visual sugerido: dropdown.
- Vista origen: dimension/vista de lote o `vw_stock_actual[variedad_nombre]` relacionada.
- Interaccion: filtra lotes vendidos y graficos por variedad.

### Tipo de producto

- Visual sugerido: dropdown.
- Vista origen: vista de productos terminados o dimensiones de producto.
- Interaccion: filtra productos terminados y ventas relacionadas.

### Estado producto

- Visual sugerido: dropdown.
- Vista origen: productos terminados.
- Interaccion: filtra productos terminados disponibles, vendidos o bloqueados si se modelan.

### Responsable

- Visual sugerido: dropdown.
- Vista origen: `vw_comercial[responsable_nombre]`.
- Interaccion: filtra ventas registradas por responsable.

## 4. KPIs principales

### Litros Vendidos

- Medida DAX: `Litros Vendidos`.
- Formato: `#,0.00 L`.
- Origen: `vw_comercial[litros]`.
- Tooltip: litros vendidos por periodo, cliente principal y lote principal.
- Interaccion: click resalta ventas por mes y tabla comercial.

### Ventas Granel

- Medida DAX sugerida: `Ventas Granel = DISTINCTCOUNT(vw_comercial[venta_granel_id])`.
- Formato: entero.
- Origen: `vw_comercial`.
- Tooltip: cantidad de ventas y documentos.
- Interaccion: filtra tabla a ventas del periodo.

### Clientes Activos

- Medida DAX sugerida: `Clientes Activos = DISTINCTCOUNT(vw_comercial[cliente_id])`.
- Formato: entero.
- Origen: `vw_comercial`.
- Tooltip: clientes con ventas en el periodo.
- Interaccion: resalta ranking de clientes.

### Productos Terminados

- Medida DAX: `Productos Terminados`.
- Formato: entero o unidades.
- Origen: vista o tabla de productos terminados.
- Tooltip: productos producidos, unidades y litros totales.
- Interaccion: filtra visual de productos por tipo.

### Litros por Cliente

- Medida DAX sugerida: `Litros por Cliente = DIVIDE([Litros Vendidos], [Clientes Activos])`.
- Formato: `#,0.00 L`.
- Origen: `vw_comercial`.
- Tooltip: promedio de litros vendidos por cliente activo.
- Interaccion: resalta clientes con mayor volumen.

### Ultima Venta

- Medida DAX sugerida: `MAX(vw_comercial[fecha_venta])`.
- Formato: `dd/mm/yyyy`.
- Origen: `vw_comercial`.
- Tooltip: cliente, documento y litros de la ultima venta si se define medida auxiliar.
- Interaccion: actualiza panel lateral con ultima venta.

## 5. Visuales principales

## Ventas por mes

- Tipo de grafico: columnas o linea.
- Campos:
  - eje: `DimFecha[AnioMes]`;
  - valores: `Litros Vendidos`.
- Medidas: `Litros Vendidos`.
- Colores: dorado `#B88646`.
- Tooltip: mes, litros, cantidad ventas, clientes activos.
- Drill-through: Reportes comerciales.
- Interaccion: click en mes filtra toda la pagina.

## Ventas por cliente

- Tipo de grafico: barras horizontales.
- Campos:
  - eje: `cliente_nombre`;
  - valores: `Litros Vendidos`.
- Medidas: `Litros Vendidos`.
- Colores: neutros con acento dorado para top cliente.
- Tooltip: cliente, litros, cantidad ventas, ultima venta.
- Drill-through: Reportes por cliente.
- Interaccion: click en cliente actualiza panel lateral.

## Litros vendidos por variedad/lote

- Tipo de grafico: barras horizontales o matriz.
- Campos:
  - eje: `lote_codigo` o variedad relacionada;
  - valores: `Litros Vendidos`.
- Medidas: `Litros Vendidos`.
- Colores: paleta de datos por tipo de vino.
- Tooltip: lote, variedad, litros, cliente principal.
- Drill-through: Trazabilidad.
- Interaccion: click en lote navega o filtra trazabilidad.

## Productos terminados por tipo

- Tipo de grafico: barras o dona.
- Campos:
  - categoria: tipo producto;
  - valores: productos terminados o unidades.
- Medidas: `Productos Terminados`.
- Colores: dorado, verde suave y neutros.
- Tooltip: tipo producto, unidades, litros totales.
- Drill-through: Reportes.
- Interaccion: filtra tabla de productos si existe.

## Ventas por responsable

- Tipo de grafico: barras.
- Campos:
  - eje: `responsable_nombre`;
  - valores: `Litros Vendidos` o `Ventas Granel`.
- Medidas: `Litros Vendidos`, `Ventas Granel`.
- Colores: marron y dorado.
- Tooltip: responsable, ventas, litros, clientes.
- Drill-through: Reportes.
- Interaccion: click filtra ventas del responsable.

## Clientes con mayor volumen

- Tipo de grafico: ranking Top N.
- Campos:
  - eje: `cliente_nombre`;
  - valores: `Litros Vendidos`.
- Medidas: `Litros Vendidos`.
- Colores: top 1 dorado, resto neutros.
- Tooltip: litros, participacion, ultima venta.
- Drill-through: Reportes por cliente.
- Interaccion: click abre detalle lateral.

## 6. Tabla inferior

### Tabla comercial

- Visual: Table.
- Ubicacion: parte inferior.
- Orden: `fecha_venta` descendente.

### Campos

- `fecha_venta`
- `cliente_nombre`
- `lote_codigo`
- `pileta_codigo`
- variedad relacionada si esta disponible
- `litros`
- `responsable_nombre`
- `operacion_productiva_id`
- `venta_observaciones`
- `detalle_observaciones`

### Formato

- Encabezado marron madera.
- Texto encabezado crema.
- Filas alternas suaves.
- Litros alineados a la derecha.
- Observaciones truncadas con tooltip.
- Documento visible si se incorpora como columna adicional.

## 7. Panel lateral de detalle

### Al seleccionar cliente

- Nombre del cliente.
- Identificacion fiscal si esta disponible.
- Litros comprados.
- Cantidad de ventas.
- Ultima venta.
- Lotes comprados.
- Responsable principal.

### Al seleccionar venta

- Fecha.
- Documento.
- Cliente.
- Litros.
- Lote.
- Pileta.
- Responsable.
- Operacion productiva.
- Observaciones.

### Al seleccionar lote

- Codigo lote.
- Variedad.
- Litros vendidos.
- Pileta asociada.
- Stock actual si existe relacion.
- Trazabilidad disponible.
- Boton: `Ver trazabilidad`.

### Al seleccionar producto terminado

- Codigo.
- Tipo producto.
- Lote origen.
- Cantidad unidades.
- Litros totales.
- Estado.
- Botones: `Ver trazabilidad`, `Ver stock`.

## 8. Alertas

### Venta sin lote asociado

- Color: rojo vino.
- Condicion: venta/detalle sin lote.
- Accion: revisar Reportes.

### Venta sin trazabilidad completa

- Color: ambar.
- Condicion: lote vendido sin relaciones o movimientos suficientes para reconstruir origen.
- Accion: navegar a Trazabilidad.

### Cliente con volumen alto

- Color: dorado o ambar segun umbral.
- Condicion: cliente concentra volumen superior al umbral definido.
- Accion: revisar detalle de cliente.

### Producto terminado sin stock asociado

- Color: ambar.
- Condicion: producto terminado sin lote o sin relacion clara con stock.
- Accion: revisar Trazabilidad o Reportes.

### Ventas concentradas en pocos clientes

- Color: ambar.
- Condicion: top clientes concentran porcentaje alto de litros.
- Accion: revisar ranking de clientes.

## 9. Navegacion

### Click en lote

- Destino: Trazabilidad.
- Contexto: lote seleccionado.

### Click en cliente

- Accion: abre panel lateral de detalle.
- Contexto: cliente seleccionado.

### Click en venta

- Destino: Reportes.
- Contexto: venta, documento o cliente.

### Click en producto terminado

- Destino: Trazabilidad o Stock.
- Contexto: producto/lote origen.

## 10. Performance

- Evitar tablas comerciales demasiado grandes en la pagina principal.
- Usar agregaciones por cliente y mes.
- Filtrar por ano por defecto.
- Ocultar observaciones extensas salvo en panel lateral o tooltip.
- Limitar ranking de clientes a Top N.
- Usar `DISTINCTCOUNT` para conteo de ventas.
- Validar que litros vendidos coincidan con `vw_comercial`.
- Usar Import mode.

## 11. Checklist final

- [ ] Filtros funcionan.
- [ ] KPIs correctos.
- [ ] Ventas por cliente correctas.
- [ ] Litros vendidos coinciden con `vw_comercial`.
- [ ] Tabla ordenada.
- [ ] Drill-through a trazabilidad.
- [ ] Alertas visibles.
- [ ] Colores consistentes.
- [ ] Sin scroll.
- [ ] Panel lateral muestra cliente/venta/lote correctamente.
- [ ] Observaciones no saturan la pagina.
- [ ] Productos terminados se distinguen de venta granel.
