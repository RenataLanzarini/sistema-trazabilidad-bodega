# Mockup - Dashboard Ejecutivo

## Objetivo de la pantalla

La pagina principal debe funcionar como tablero de control ejecutivo para Bodega y Vinedos Lanzarini. Debe permitir entender en pocos segundos el estado general de la bodega: recepcion de uva, vino en produccion, stock, productos terminados, ventas, mermas, calidad y alertas operativas.

La pantalla debe sentirse como un sistema profesional de gestion vitivinicola: elegante, limpio, moderno, con estetica de bodega y foco operativo.

## Resolucion base

- Formato: 16:9.
- Resolucion recomendada de diseno: 1920 x 1080 px.
- Fondo general: crema `#F8F5EF`.
- Layout: menu lateral fijo, header superior, filtros, KPIs, graficos y tablas inferiores.

```text
+----------------------+----------------------------------------------------------+
| Menu lateral         | Header / banner fotografico                            |
|                      +----------------------------------------------------------+
|                      | Filtros                                                  |
|                      +----------------------------------------------------------+
|                      | KPIs principales                                         |
|                      +----------------------------------------------------------+
|                      | Produccion mensual | Stock variedad | Capacidad piletas |
|                      +----------------------------------------------------------+
|                      | Ventas | Merma | Calidad                                  |
|                      +----------------------------------------------------------+
|                      | Ultimos movimientos | Ultimas operaciones | Alertas       |
+----------------------+----------------------------------------------------------+
```

## Header

### Banner superior

- Ubicacion: parte superior del area principal, a la derecha del menu lateral.
- Alto sugerido: 120 px.
- Imagen: mesa de degustacion de Bodega y Vinedos Lanzarini.
- Tratamiento: fotografia real con overlay marron madera `#2B1E1A` al 45-55% para asegurar legibilidad.
- Borde inferior: linea fina dorada `#B88646` de 2 px.

### Logo

- Ubicacion: superior izquierdo del banner, dentro del area principal, alineado a 24 px del margen izquierdo del contenido.
- Tamano sugerido: 56 x 56 px.
- Contenedor: sin tarjeta, integrado al banner.
- Regla: debe tener margen suficiente para no competir con el titulo.

### Titulo

- Texto: `Bodega y Vinedos Lanzarini`
- Ubicacion: dentro del banner, a la derecha del logo.
- Color: crema claro `#F8F5EF`.
- Tamano: 30-34 px.
- Peso: semibold.

### Subtitulo

- Texto: `Sistema Integral de Gestion Vitivinicola`
- Ubicacion: debajo del titulo.
- Color: crema claro con opacidad visual menor o `#E8E0D6`.
- Tamano: 13-15 px.
- Peso: regular.

### Metadatos opcionales

- Extremo derecho del banner.
- Texto sugerido: `Actualizado: dd/mm/aaaa hh:mm`.
- Color: crema claro.
- Tamano: 11-12 px.

## Menu lateral

### Estructura

- Ubicacion: lateral izquierdo, fijo.
- Ancho: 240 px.
- Alto: 100% de la pagina.
- Fondo: marron madera `#2B1E1A`.
- Separador derecho: linea dorada `#B88646` al 40% de opacidad.

### Items

1. Inicio
2. Produccion
3. Stock
4. Trazabilidad
5. Calidad
6. Comercial
7. Ordenes de Trabajo
8. Reportes
9. Configuracion

### Iconos sugeridos

- Inicio: casa.
- Produccion: racimo o fabrica simple.
- Stock: tanque/pileta.
- Trazabilidad: nodos conectados.
- Calidad: matraz o gota.
- Comercial: documento o carrito.
- Ordenes de Trabajo: checklist.
- Reportes: grafico de barras.
- Configuracion: engranaje.

### Tamano y espaciado

- Alto por item: 48 px.
- Padding horizontal: 20 px.
- Separacion icono-texto: 12 px.
- Icono: 18-20 px.
- Texto: 13-14 px.
- Separacion entre grupos: 16 px si se divide en secciones.

### Colores

- Item normal: texto `#F8F5EF` con opacidad media.
- Icono normal: `#A89F91`.
- Item hover: fondo `#3A2A25`; texto `#FFFFFF`; icono dorado `#B88646`.
- Item activo: fondo borravino `#3E244A`; texto `#FFFFFF`; icono dorado `#B88646`.
- Indicador activo: barra vertical izquierda dorada de 4 px.

### Reglas visuales

- El item activo debe ser evidente.
- No usar submenus en la primera version.
- El menu no debe cambiar de posicion entre paginas.

## Filtros

### Ubicacion

- Debajo del header.
- Altura de la franja: 72 px.
- Fondo: crema `#F8F5EF`.
- Contenedor de filtros: blanco `#FFFFFF`, borde suave `#E8E0D6`, radio 8 px.

### Tipo

- Filtros de seleccion desplegable para listas largas.
- Segmentadores tipo boton para filtros cortos si aplica.
- Fecha/anio como dropdown o slicer horizontal compacto.

### Cantidad

- Maximo visible recomendado: 8 filtros.
- Si la pantalla se siente cargada, dejar Cliente y Operacion en panel desplegable de filtros avanzados.

### Orden

1. Ano
2. Cosecha
3. Bodega
4. Variedad
5. Pileta
6. Estado
7. Cliente
8. Operacion

### Filtros documentados

#### Ano

- Uso: limitar toda la pagina por periodo calendario.
- Afecta: todos los KPIs, graficos y tablas.
- Control: dropdown o slicer horizontal.

#### Cosecha

- Uso: analizar produccion y lotes por cosecha.
- Afecta: uva recibida, litros en produccion, stock, calidad, trazabilidad indirecta.
- Control: dropdown.

#### Bodega

- Uso: preparado para multiples bodegas.
- Afecta: toda la pagina.
- Control: dropdown.

#### Variedad

- Uso: filtrar por variedad principal.
- Afecta: produccion, stock por variedad, calidad, merma y movimientos.
- Control: dropdown con busqueda.

#### Pileta

- Uso: analizar stock y capacidad por tanque.
- Afecta: stock, capacidad, movimientos, calidad.
- Control: dropdown con busqueda.

#### Estado

- Uso: filtrar estados de lote, pileta, operacion u OT segun contexto.
- Afecta: KPIs y tablas operativas.
- Control: dropdown.

#### Cliente

- Uso: filtrar ventas a granel.
- Afecta: ventas granel y tablas comerciales.
- Control: dropdown con busqueda.

#### Operacion

- Uso: filtrar por tipo de operacion productiva.
- Afecta: movimientos, merma, ultimas operaciones.
- Control: dropdown.

## KPIs

### Disposicion general

- Ubicacion: debajo de filtros.
- Layout: 6 tarjetas en una fila en resolucion grande.
- Alto: 118 px.
- Separacion: 14 px.
- Fondo: blanco `#FFFFFF`.
- Radio: 8 px.
- Borde: `#E8E0D6`.
- Acento superior: linea de 3 px segun KPI.

### KPI 1 - Uva recibida

- Posicion: primera tarjeta.
- Color acento: dorado envejecido `#B88646`.
- Icono: racimo o balanza.
- Valor: total kg uva recibida.
- Formato: `###.### kg`.
- Comparacion: variacion contra periodo anterior.
- Tooltip: kilos recibidos, cantidad de CIU, promedio Brix, variedad principal.
- Interaccion: click filtra graficos de produccion y tabla de ultimas operaciones de recepcion.

### KPI 2 - Litros en produccion

- Posicion: segunda tarjeta.
- Color acento: borravino `#3E244A`.
- Icono: tanque/pileta.
- Valor: litros en lotes activos o en piletas productivas.
- Formato: `###.### L`.
- Comparacion: variacion contra periodo anterior.
- Tooltip: litros por estado de lote, cantidad de lotes activos.
- Interaccion: click navega o filtra a Stock.

### KPI 3 - Stock actual

- Posicion: tercera tarjeta.
- Color acento: marron madera `#2B1E1A`.
- Icono: deposito/tanque.
- Valor: litros stock actual.
- Formato: `###.### L`.
- Comparacion: ocupacion promedio de capacidad.
- Tooltip: stock por bodega, piletas ocupadas, capacidad disponible.
- Interaccion: click filtra graficos de stock y capacidad.

### KPI 4 - Productos terminados

- Posicion: cuarta tarjeta.
- Color acento: verde suave `#8FAF77`.
- Icono: botella o caja.
- Valor: unidades o cantidad de productos terminados.
- Formato: `###.### un`.
- Comparacion: variacion contra periodo anterior.
- Tooltip: unidades producidas, litros fraccionados, tipo de producto.
- Interaccion: click filtra reportes de producto terminado.

### KPI 5 - Ventas granel

- Posicion: quinta tarjeta.
- Color acento: dorado envejecido `#B88646`.
- Icono: documento comercial o camion.
- Valor: litros vendidos a granel.
- Formato: `###.### L`.
- Comparacion: variacion contra periodo anterior.
- Tooltip: litros por cliente, cantidad de ventas, lote principal.
- Interaccion: click filtra grafico de ventas y tabla comercial.

### KPI 6 - % Merma

- Posicion: sexta tarjeta.
- Color acento segun estado:
  - correcto: verde oliva `#6F7F3F`;
  - advertencia: ambar `#D69A2D`;
  - error: rojo vino `#8A1F2D`.
- Icono: alerta/gota.
- Valor: porcentaje de merma.
- Formato: `0,00%`.
- Comparacion: contra umbral objetivo o periodo anterior.
- Tooltip: litros merma, causa principal, lote/pileta con mayor incidencia.
- Interaccion: click filtra merma y movimientos relacionados.

## Graficos

### Produccion mensual

- Tipo: columnas agrupadas o linea + columnas.
- Posicion: primera fila de graficos, izquierda.
- Tamano sugerido: 34% del ancho disponible, 260 px de alto.
- Objetivo: mostrar kilos recibidos y/o litros movidos por mes.
- Colores: columnas doradas `#B88646`; linea borravino `#3E244A`.
- Interaccion: click en mes filtra KPIs, tablas y graficos secundarios.

### Stock por variedad

- Tipo: barras horizontales.
- Posicion: primera fila de graficos, centro.
- Objetivo: comparar litros actuales por variedad.
- Colores: paleta de datos por tipo de vino; tintos para tintas, blancos para blancas, rosados para rosadas.
- Interaccion: click en variedad filtra stock, produccion, calidad y movimientos.

### Capacidad de piletas

- Tipo: barras apiladas o bullet chart.
- Posicion: primera fila de graficos, derecha.
- Objetivo: mostrar litros ocupados vs capacidad disponible.
- Colores: ocupado borravino suave, disponible crema oscuro, alerta en ambar o rojo vino.
- Interaccion: click en pileta filtra tablas, stock y calidad.

### Ventas

- Tipo: linea mensual con barras por cliente o columnas por periodo.
- Posicion: segunda fila, izquierda.
- Objetivo: visualizar litros vendidos a granel.
- Colores: dorado para ventas totales, neutros para clientes.
- Interaccion: click en cliente o mes filtra tabla comercial y KPIs.

### Merma

- Tipo: dona por causa + barra temporal secundaria si hay espacio.
- Posicion: segunda fila, centro.
- Objetivo: identificar causas principales de merma y evolucion.
- Colores: rojo vino para causas criticas, ambar para advertencias, neutros para menores.
- Interaccion: click en causa filtra movimientos y alertas.

### Calidad

- Tipo: tarjetas pequenas o lineas de indicadores: Brix, alcohol, pH, Baume.
- Posicion: segunda fila, derecha.
- Objetivo: monitorear variables enologicas principales.
- Colores: pH marron, alcohol borravino, Brix dorado, Baume neutro.
- Interaccion: click en indicador abre o filtra pagina Calidad.

## Tablas

### Ultimos movimientos

- Ubicacion: fila inferior, izquierda.
- Columnas: fecha, lote, pileta origen, pileta destino, litros, tipo operacion, responsable.
- Orden: fecha descendente.
- Estilo: tabla compacta, encabezado marron madera, filas alternas suaves.
- Interaccion: click en fila filtra lote/pileta y puede navegar a Trazabilidad.

### Ultimas operaciones

- Ubicacion: fila inferior, centro.
- Columnas: fecha, tipo operacion, estado, responsable, anulada, observaciones breves.
- Orden: fecha descendente.
- Interaccion: click en operacion filtra movimientos asociados.

### Alertas

- Ubicacion: fila inferior, derecha.
- Columnas: severidad, tipo, descripcion, fecha, entidad relacionada.
- Estados visuales: icono + color.
- Interaccion: click en alerta filtra entidad relacionada o navega a pagina correspondiente.

## Estados

### Correcto

- Color: verde oliva `#6F7F3F`.
- Uso: procesos en orden, capacidad saludable, OT completadas.

### Advertencia

- Color: ambar `#D69A2D`.
- Uso: capacidad alta, dato faltante, merma elevada pero no critica.

### Error

- Color: rojo vino `#8A1F2D`.
- Uso: stock insuficiente, operacion anulada critica, OT vencida.

### Pendiente

- Color: gris calido `#A89F91`.
- Uso: OT pendiente, lote sin clasificar, analisis incompleto.

## Responsive

### Resoluciones grandes

- En 1920 x 1080, usar 6 KPIs en una fila.
- Graficos en dos filas de tres columnas.
- Tablas inferiores con tres paneles.
- Panel de detalle puede abrirse como columna derecha adicional si se usa bookmark.

### Resoluciones medianas

- KPIs en dos filas de tres.
- Graficos principales en dos columnas.
- Alertas debajo de tablas.

### Resoluciones chicas o proyector

- Priorizar KPIs, produccion mensual, stock y alertas.
- Reducir cantidad de filtros visibles.
- Usar botones para abrir filtros avanzados.

## Interacciones

### Click en KPI

- Uva recibida: filtra produccion y recepciones.
- Litros en produccion: filtra stock/lotes activos.
- Stock actual: filtra vista de stock y capacidad.
- Productos terminados: filtra fraccionamiento/producto terminado.
- Ventas granel: filtra comercial.
- % Merma: filtra merma y movimientos relacionados.

### Click en grafico

- Mes: filtra todas las visualizaciones por periodo.
- Variedad: filtra stock, produccion, calidad y trazabilidad.
- Pileta: filtra stock, movimientos y calidad.
- Cliente: filtra ventas y detalle comercial.
- Causa merma: filtra movimientos, alertas y tabla de operaciones.

### Filtros globales

- Ano, cosecha y bodega afectan toda la pagina.
- Variedad afecta produccion, stock, calidad, trazabilidad y merma.
- Pileta afecta stock, capacidad, movimientos, calidad y alertas.
- Cliente afecta solo ventas y comercial.
- Operacion afecta movimientos, merma y ultimas operaciones.

### Navegacion

- Menu lateral navega entre paginas.
- Click derecho o boton contextual puede ir a detalle de lote, pileta o trazabilidad.
- Tabla de ultimos movimientos debe permitir drill-through hacia trazabilidad del lote.

## Reglas de calidad visual

- Ningun visual debe quedar sin titulo.
- Cada KPI debe mostrar unidad.
- Los colores de estado deben ser consistentes en toda la pantalla.
- No usar mas de tres visuales con colores intensos al mismo tiempo.
- Las fotografias solo deben aparecer en header o separadores, no detras de tablas.
