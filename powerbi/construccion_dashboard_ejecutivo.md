# Construccion del Dashboard Ejecutivo en Power BI Desktop

Esta guia describe paso a paso como construir la pagina **Dashboard Ejecutivo** del Centro de Control Vitivinicola Lanzarini dentro de Power BI Desktop.

La pagina debe respetar el Design System Lanzarini y el mockup funcional definido en `powerbi/mockups/dashboard_ejecutivo.md`.

## 1. Configuracion de pagina

### Tamano

- Tipo: 16:9.
- Resolucion sugerida de diseno: 1920 x 1080 px.
- En Power BI: usar formato de pagina `16:9`.
- Evitar scroll vertical y horizontal.

### Margenes

- Margen exterior general: 24 px.
- Menu lateral: 240 px de ancho.
- Margen entre menu y contenido: 0 px si el menu esta pegado al borde; 24 px dentro del area principal.
- Separacion entre bloques: 14 a 16 px.

### Grid sugerida

Area total:

- Menu lateral: 240 px.
- Area principal: ancho restante.
- Header: 120 px de alto.
- Filtros: 72 px.
- KPIs: 118 px.
- Graficos principales: 260 px.
- Graficos secundarios: 220 px.
- Tablas inferiores: 220 px.

### Espaciado

- Padding interno de tarjetas KPI: 14-16 px.
- Separacion entre KPIs: 14 px.
- Separacion entre visuales: 16 px.
- Padding interno de tablas: 8-10 px.

### Fondo

- Fondo general de pagina: crema `#F8F5EF`.
- Tarjetas y contenedores: blanco `#FFFFFF`.
- Bordes suaves: `#E8E0D6`.

### Banner

- Ubicacion: parte superior del area principal.
- Alto: 120 px.
- Fondo: fotografia de mesa de degustacion Lanzarini con overlay marron madera.
- Linea inferior: dorado envejecido `#B88646`, 2 px.

### Menu lateral

- Ubicacion: izquierda.
- Ancho: 240 px.
- Alto: 100% de pagina.
- Fondo: marron madera `#2B1E1A`.

## 2. Header

### Posicion

- X: 240 px.
- Y: 0 px.
- Ancho: ancho total menos menu lateral.
- Alto: 120 px.

### Fotografia utilizada

- Imagen: mesa de degustacion de Bodega y Vinedos Lanzarini.
- Tratamiento: overlay marron madera `#2B1E1A` con transparencia aproximada 45-55%.
- La imagen no debe competir con texto ni logo.

### Logo

- Posicion: X 264 px, Y 32 px.
- Tamano: 56 x 56 px.
- Fondo: transparente.
- Alineacion: izquierda, antes del titulo.

### Titulo

- Texto: `Bodega y Vinedos Lanzarini`.
- Posicion: a la derecha del logo.
- Color: crema `#F8F5EF`.
- Fuente: Segoe UI o Aptos.
- Tamano: 30-34 px.
- Peso: semibold.

### Subtitulo

- Texto: `Sistema Integral de Gestion Vitivinicola`.
- Posicion: debajo del titulo.
- Color: crema suavizado o `#E8E0D6`.
- Tamano: 13-15 px.

### Metadato de actualizacion

- Posicion: extremo derecho del header.
- Texto: `Actualizado: dd/mm/yyyy hh:mm`.
- Color: crema.
- Tamano: 11-12 px.

## 3. Menu lateral

### Botones

Crear un boton por pagina:

1. Inicio
2. Produccion
3. Stock
4. Trazabilidad
5. Calidad
6. Comercial
7. Ordenes de Trabajo
8. Reportes
9. Configuracion

### Iconos

- Inicio: casa.
- Produccion: racimo o fabrica simple.
- Stock: tanque.
- Trazabilidad: nodos conectados.
- Calidad: matraz o gota.
- Comercial: documento comercial.
- Ordenes de Trabajo: checklist.
- Reportes: grafico de barras.
- Configuracion: engranaje.

### Navegacion

- Usar botones con accion de navegacion a pagina.
- Si se usan bookmarks, nombrarlos con prefijo `NAV_`.
- Ejemplos: `NAV_Inicio`, `NAV_Produccion`, `NAV_Stock`.

### Estado activo

- Boton Inicio activo:
  - fondo `#3E244A`;
  - texto `#FFFFFF`;
  - icono `#B88646`;
  - barra izquierda dorada de 4 px.

### Hover

- Fondo hover: `#3A2A25`.
- Texto hover: `#FFFFFF`.
- Icono hover: `#B88646`.

### Colores normales

- Fondo: `#2B1E1A`.
- Texto: `#F8F5EF`.
- Icono: `#A89F91`.

## 4. Filtros

### Contenedor

- Ubicacion: debajo del header.
- Alto: 72 px.
- Fondo: blanco `#FFFFFF`.
- Borde: `#E8E0D6`.
- Radio visual: 8 px.

### Ano

- Tipo de slicer: dropdown o horizontal si hay pocos anos.
- Posicion: primer filtro, izquierda.
- Tamano sugerido: 120 x 40 px.
- Interaccion: afecta toda la pagina.
- Vista SQL origen: fechas desde `vw_produccion`, `vw_movimientos`, `vw_comercial`, `vw_calidad`, calendario.

### Cosecha

- Tipo de slicer: dropdown.
- Posicion: segundo filtro.
- Tamano: 130 x 40 px.
- Interaccion: afecta produccion, stock, calidad y trazabilidad.
- Vista SQL origen: `vw_produccion`, `vw_stock_actual`, `vw_movimientos`.

### Bodega

- Tipo de slicer: dropdown.
- Posicion: tercer filtro.
- Tamano: 150 x 40 px.
- Interaccion: afecta toda la pagina.
- Vista SQL origen: todas las vistas con `bodega_id`.

### Variedad

- Tipo de slicer: dropdown con busqueda.
- Posicion: cuarto filtro.
- Tamano: 160 x 40 px.
- Interaccion: afecta produccion, stock, movimientos y calidad.
- Vista SQL origen: `vw_produccion`, `vw_stock_actual`, `vw_movimientos`.

### Pileta

- Tipo de slicer: dropdown con busqueda.
- Posicion: quinto filtro.
- Tamano: 150 x 40 px.
- Interaccion: afecta stock, capacidad, movimientos y calidad.
- Vista SQL origen: `vw_stock_actual`, `vw_movimientos`, `vw_calidad`.

### Estado

- Tipo de slicer: dropdown.
- Posicion: sexto filtro.
- Tamano: 140 x 40 px.
- Interaccion: afecta stock, operaciones y ordenes.
- Vista SQL origen: `vw_stock_actual`, `vw_movimientos`, `vw_ordenes_trabajo`.

### Cliente

- Tipo de slicer: dropdown con busqueda.
- Posicion: septimo filtro.
- Tamano: 160 x 40 px.
- Interaccion: afecta ventas y visuales comerciales.
- Vista SQL origen: `vw_comercial`.

### Operacion

- Tipo de slicer: dropdown.
- Posicion: octavo filtro.
- Tamano: 160 x 40 px.
- Interaccion: afecta movimientos, merma y operaciones.
- Vista SQL origen: `vw_movimientos`.

## 5. KPIs

### Configuracion general

- Visual sugerido: Card o New Card.
- Cantidad: 6 tarjetas.
- Distribucion: una fila.
- Alto: 118 px.
- Fondo: blanco.
- Radio: 8 px.
- Borde: `#E8E0D6`.
- Acento superior: linea de color por KPI.

### Uva recibida

- Medida DAX: `Kg Uva Recibida`.
- Formato: `#,0.00 kg`.
- Icono: racimo o balanza.
- Color: dorado `#B88646`.
- Tooltip: kg recibidos, cantidad de CIU, Brix promedio, variedad principal.
- Interaccion: filtra produccion mensual y tabla de ultimas operaciones.
- Vista origen: `vw_produccion`.

### Litros en produccion

- Medida DAX: puede usar `Litros Stock Actual` filtrado por estados productivos.
- Formato: `#,0.00 L`.
- Icono: tanque.
- Color: borravino `#3E244A`.
- Tooltip: litros por estado de lote y cantidad de lotes activos.
- Interaccion: navega o filtra Stock.
- Vista origen: `vw_stock_actual`.

### Stock actual

- Medida DAX: `Litros Stock Actual`.
- Formato: `#,0.00 L`.
- Icono: deposito/tanque.
- Color: marron madera `#2B1E1A`.
- Tooltip: stock por bodega, piletas ocupadas, capacidad disponible.
- Interaccion: filtra stock por variedad y capacidad de piletas.
- Vista origen: `vw_stock_actual`.

### Productos terminados

- Medida DAX: `Productos Terminados`.
- Formato: entero o unidades.
- Icono: botella o caja.
- Color: verde suave `#8FAF77`.
- Tooltip: unidades producidas, litros fraccionados, tipo de producto.
- Interaccion: navega o filtra pagina Produccion/Reportes.
- Vista origen: tabla o vista futura de productos terminados.

### Ventas granel

- Medida DAX: `Litros Vendidos`.
- Formato: `#,0.00 L`.
- Icono: documento comercial o camion.
- Color: dorado `#B88646`.
- Tooltip: litros por cliente, cantidad de ventas, lote principal.
- Interaccion: filtra grafico de ventas y tabla comercial.
- Vista origen: `vw_comercial`.

### % Merma

- Medida DAX: `% Merma`.
- Formato: `0.00%`.
- Icono: alerta/gota.
- Color:
  - correcto `#6F7F3F`;
  - advertencia `#D69A2D`;
  - error `#8A1F2D`.
- Tooltip: litros merma, causa principal, lote/pileta con mayor incidencia.
- Interaccion: filtra visual de merma y movimientos.
- Vista origen: `vw_movimientos`.

## 6. Graficos

## Produccion mensual

- Tipo de visual Power BI: columnas agrupadas o combo line and clustered column.
- Campos:
  - eje: `DimFecha[AnioMes]`;
  - valores: `Kg Uva Recibida`;
  - linea opcional: `Litros Movidos`.
- Colores:
  - columnas: `#B88646`;
  - linea: `#3E244A`.
- Filtros: Ano, cosecha, bodega, variedad.
- Interaccion: seleccionar mes filtra KPIs, tablas y visuales secundarios.
- Tooltip: kg recibidos, CIU, Brix promedio.
- Drill-through: Produccion.

## Stock por variedad

- Tipo de visual Power BI: barras horizontales.
- Campos:
  - eje: `variedad_nombre`;
  - valores: `Litros Stock Actual`.
- Colores: paleta de datos por variedad o tipo de vino.
- Filtros: cosecha, bodega, pileta, estado.
- Interaccion: seleccionar variedad filtra stock, calidad y movimientos.
- Tooltip: litros, lotes, piletas, cosecha.
- Drill-through: Stock o Trazabilidad.

## Capacidad de piletas

- Tipo de visual Power BI: barras apiladas, bullet chart o barra horizontal.
- Campos:
  - eje: `pileta_codigo`;
  - valores: `Litros Stock Actual`, `Capacidad Total`;
  - porcentaje: `Capacidad Ocupada %`.
- Colores:
  - ocupado: `#3E244A`;
  - disponible: `#E8E0D6`;
  - advertencia: `#D69A2D`;
  - error: `#8A1F2D`.
- Filtros: bodega, deposito, pileta.
- Interaccion: seleccionar pileta filtra movimientos, stock y calidad.
- Tooltip: capacidad, litros, ocupacion, estado pileta.
- Drill-through: Stock.

## Ventas

- Tipo de visual Power BI: line chart o columnas por mes.
- Campos:
  - eje: `DimFecha[AnioMes]`;
  - valores: `Litros Vendidos`;
  - leyenda opcional: cliente.
- Colores:
  - principal: `#B88646`;
  - clientes: neutros.
- Filtros: ano, cliente, bodega.
- Interaccion: seleccionar mes o cliente filtra tabla comercial.
- Tooltip: litros vendidos, cantidad ventas, cliente principal.
- Drill-through: Comercial.

## Merma

- Tipo de visual Power BI: dona por tipo de operacion/causa si se dispone, o barras por operacion.
- Campos:
  - categoria: `tipo_operacion`;
  - valores: `Litros Merma`.
- Colores:
  - principal: `#8A1F2D`;
  - advertencia: `#D69A2D`;
  - secundarios: neutros.
- Filtros: ano, lote, pileta, operacion.
- Interaccion: seleccionar categoria filtra movimientos y alertas.
- Tooltip: litros merma, % merma, periodo.
- Drill-through: Stock o Reportes.

## Calidad

- Tipo de visual Power BI: small multiples, line chart o tarjetas pequenas.
- Campos:
  - eje: fecha;
  - valores: `Promedio Brix`, `Promedio Alcohol`, `Promedio pH`, `Promedio Baume`, `Temperatura Promedio`.
- Colores:
  - Brix: `#B88646`;
  - Alcohol: `#3E244A`;
  - pH: `#2B1E1A`;
  - Baume: `#8C7B6B`;
  - Temperatura: `#D69A2D`.
- Filtros: lote, pileta, variedad, fecha.
- Interaccion: seleccionar indicador navega o filtra Calidad.
- Tooltip: ultimo valor, promedio, fecha, lote/pileta.
- Drill-through: Calidad.

## 7. Tablas inferiores

## Ultimos movimientos

- Visual: Table.
- Campos:
  - `fecha_movimiento`;
  - `lote_codigo`;
  - `pileta_origen_codigo`;
  - `pileta_destino_codigo`;
  - `litros`;
  - `tipo_operacion`;
  - `responsable_nombre`.
- Orden: `fecha_movimiento` descendente.
- Formato:
  - encabezado marron `#2B1E1A`;
  - texto encabezado crema;
  - filas alternas suaves;
  - litros alineados a la derecha.
- Interacciones:
  - click en lote filtra graficos;
  - drill-through a Trazabilidad.

## Ultimas operaciones

- Visual: Table.
- Campos:
  - `fecha_operacion`;
  - `tipo_operacion`;
  - `estado_operacion`;
  - `operacion_anulada`;
  - `responsable_nombre`;
  - `motivo_anulacion`.
- Orden: `fecha_operacion` descendente.
- Formato:
  - operacion anulada en rojo vino;
  - estado normal en texto principal.
- Interacciones:
  - click en operacion filtra movimientos.

## Alertas

- Visual: Table o matriz compacta.
- Campos sugeridos:
  - severidad;
  - tipo;
  - descripcion;
  - fecha;
  - entidad relacionada.
- Origen:
  - puede construirse inicialmente con reglas DAX/visuales sobre stock, merma, calidad y ordenes.
- Orden:
  - severidad descendente;
  - fecha descendente.
- Formato:
  - correcto verde;
  - advertencia ambar;
  - error rojo vino;
  - pendiente gris calido.
- Interacciones:
  - click filtra entidad relacionada o navega a pagina correspondiente.

## 8. Tooltips

### Tooltip KPI

Debe mostrar:

- valor actual;
- periodo seleccionado;
- comparacion periodo anterior;
- principales dimensiones afectadas;
- fecha de actualizacion.

### Tooltip stock

- lote;
- pileta;
- litros;
- capacidad;
- ocupacion;
- estado.

### Tooltip produccion

- mes;
- kilos;
- CIU;
- variedad principal;
- Brix promedio.

### Tooltip calidad

- lote;
- pileta;
- fecha;
- ultimo valor;
- promedio del periodo.

### Tooltip comercial

- cliente;
- litros vendidos;
- cantidad de ventas;
- lote principal.

## 9. Navegacion

### Click en KPI

- Uva recibida: navega a Produccion.
- Litros en produccion: navega a Stock.
- Stock actual: navega a Stock.
- Productos terminados: navega a Reportes o Produccion.
- Ventas granel: navega a Comercial.
- % Merma: navega a Stock o Reportes con foco en mermas.

### Click en grafico

- Produccion mensual: filtra periodo y permite drill-through a Produccion.
- Stock por variedad: filtra variedad y permite ir a Stock.
- Capacidad de piletas: filtra pileta y permite ir a Stock.
- Ventas: filtra cliente/periodo y permite ir a Comercial.
- Merma: filtra operacion/causa y permite ir a Reportes.
- Calidad: permite ir a Calidad.

### Click en tabla

- Ultimos movimientos: drill-through a Trazabilidad por lote.
- Ultimas operaciones: filtra movimientos de la operacion.
- Alertas: navega a pagina correspondiente segun tipo.

## 10. Performance

- Usar vistas analiticas, no tablas transaccionales directas.
- Mantener el modo Import.
- Reducir columnas visibles en tablas.
- Limitar tablas inferiores a ultimos N registros.
- Evitar demasiadas leyendas con alta cardinalidad.
- Usar medidas DAX simples en la pagina principal.
- No usar relaciones bidireccionales salvo necesidad real.
- Evitar visuales personalizados pesados en la pagina Inicio.
- Usar tooltips dedicados solo donde aporten valor.
- Validar que slicers no usen columnas de alta cardinalidad innecesarias.

## 11. Checklist

- [ ] Todos los filtros funcionan.
- [ ] KPIs correctos.
- [ ] Colores del theme aplicados.
- [ ] Navegacion correcta.
- [ ] Tooltips funcionando.
- [ ] Sin scroll.
- [ ] Responsive 16:9.
- [ ] Consistencia con Design System.
- [ ] Tablas ordenadas por fecha descendente.
- [ ] Alertas usan colores correctos.
- [ ] No hay visuales sin titulo.
- [ ] Las unidades de litros y kilos son visibles.
- [ ] Los drill-through conservan contexto.

## 12. Entregables

Al finalizar la construccion de esta pagina en Power BI Desktop deberian quedar:

- Pagina `Dashboard Ejecutivo` creada.
- Header con banner y logo.
- Menu lateral funcional.
- Filtros globales configurados.
- Seis KPIs creados.
- Seis bloques graficos principales.
- Tres tablas inferiores.
- Tooltips enriquecidos.
- Navegacion y drill-through configurados.
- Checklist visual y funcional validado.
