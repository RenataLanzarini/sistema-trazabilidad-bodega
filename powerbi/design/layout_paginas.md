# Layout Base de Paginas

## Resolucion

- Formato recomendado: 16:9.
- Tamano sugerido Power BI: 1280 x 720 px o 1920 x 1080 px si se busca mayor densidad.
- Mantener una grilla consistente para todas las paginas.

## Estructura base

```text
+----------------+------------------------------------------------+
| Menu lateral   | Header / titulo / periodo activo               |
|                +------------------------------------------------+
|                | Filtros principales                            |
|                +------------------------------------------------+
|                | KPIs                                          |
|                +------------------------------------------------+
|                | Graficos principales              | Detalle    |
|                |                                   | opcional   |
|                +-----------------------------------+------------+
|                | Tabla / matriz / detalle operativo             |
+----------------+------------------------------------------------+
```

## Menu lateral

- Ancho: 220-260 px.
- Fijo en todas las paginas.
- Contiene: Ejecutivo, Produccion, Stock, Trazabilidad, Calidad, Comercial, Ordenes, Corte Teorico, Reportes.
- Item activo con fondo borravino y acento dorado.

## Header

- Alto: 64-88 px.
- Contenido: titulo, subtitulo, fecha de actualizacion, periodo activo.
- Puede incluir una fotografia real con overlay suave en paginas ejecutivas.
- En paginas operativas, preferir header limpio sin imagen.

## Zona de filtros

- Alto sugerido: 48-64 px.
- Filtros maximos visibles: 4 a 6.
- Filtros globales: fecha, bodega, cosecha.
- Filtros especificos: lote, pileta, cliente, tarea, tipo de operacion.

## Zona KPI

- Ubicacion: debajo de filtros.
- Altura sugerida: 100-130 px.
- Cantidad: 3 a 6 tarjetas segun pagina.
- Cada KPI debe tener unidad y etiqueta clara.

## Zona de graficos

- Area principal: 55-65% del ancho disponible.
- Graficos secundarios: columna derecha o fila inferior.
- Evitar mezclar mas de tres tipos de visual por pagina.

## Zona de tablas

- Ubicacion: parte inferior o pagina de reportes.
- Altura sugerida: 180-280 px.
- Usar para detalle exportable, no como visual principal de todas las paginas.

## Panel de detalle

- Ancho: 300-380 px.
- Uso: trazabilidad, lote seleccionado, pileta seleccionada, OT seleccionada.
- Puede aparecer fijo en paginas tecnicas o por bookmark.

## Navegacion entre paginas

- Mantener orden estable.
- Usar iconos consistentes.
- No depender solo de bookmarks ocultos para navegacion principal.
- El usuario debe saber siempre en que pagina esta.

## Adaptacion por pagina

- Ejecutivo: mas KPIs y graficos resumidos.
- Produccion: graficos + tabla de recepciones/lotes.
- Stock: matriz lote-pileta + ocupacion.
- Trazabilidad: grafo central + panel de detalle.
- Calidad: lineas temporales + tabla de analisis.
- Comercial: ventas por cliente/lote + detalle.
- Ordenes: tablero de pendientes/completadas.
- Corte Teorico: componentes + snapshots.
