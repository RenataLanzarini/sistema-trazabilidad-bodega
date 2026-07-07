# Construccion de la Pagina Stock en Power BI Desktop

Esta guia documenta como construir la pagina **Stock** del Centro de Control Vitivinicola Lanzarini. La pagina debe mostrar litros actuales, stock por pileta, stock por lote, capacidad, ocupacion y alertas operativas.

## 1. Objetivo de la pagina

### Preguntas que responde

- Cuantos litros hay actualmente en la bodega?
- En que pileta esta cada lote?
- Que piletas estan ocupadas, vacias o cerca del limite?
- Cual es el stock por lote, variedad, deposito o estado?
- Que capacidad libre queda disponible?
- Como evoluciono el stock historicamente?

### Usuario principal

- Enologo.
- Gerente / dueno.
- Operario para consulta operativa.

### Relacion con otras paginas

- Dashboard Ejecutivo: recibe contexto desde KPIs de stock y capacidad.
- Produccion: permite consultar stock de lotes generados desde recepcion.
- Trazabilidad: permite abrir el recorrido completo del lote seleccionado.

## 2. Configuracion visual

### Layout 16:9

- Formato: 16:9.
- Resolucion de diseno recomendada: 1920 x 1080 px.
- Sin scroll.
- Fondo general: crema `#F8F5EF`.

### Menu lateral

- Mismo menu global.
- Item activo: `Stock`.
- Fondo: marron madera `#2B1E1A`.
- Activo: borravino `#3E244A` con barra dorada.

### Header

- Titulo: `Stock`.
- Subtitulo sugerido: `Litros actuales, ocupacion y capacidad de piletas`.
- Alto: 88 px.
- Estilo sobrio, sin imagen dominante.
- Linea inferior dorada `#B88646`.

### Filtros superiores

- Ubicacion: debajo del header.
- Contenedor blanco con borde suave.
- Alto: 72 px.

### Colores

- Stock: borravino `#3E244A`.
- Capacidad: marron madera `#2B1E1A`.
- Disponible: crema oscuro `#E8E0D6`.
- Correcto: verde oliva `#6F7F3F`.
- Advertencia: ambar `#D69A2D`.
- Error: rojo vino `#8A1F2D`.

### Espaciado

- Separacion entre KPIs: 14 px.
- Separacion entre visuales: 16 px.
- Padding interno de tarjetas: 14-16 px.

### Estilo de tarjetas

- Fondo blanco.
- Radio 8 px.
- Borde `#E8E0D6`.
- Valor grande con unidad `L` o `%`.
- Tooltip obligatorio en capacidad y ocupacion.

### Uso de alertas visuales

- Usar color en bordes o pequenos indicadores, no fondos intensos.
- Las alertas criticas deben aparecer tambien en tabla y panel lateral.

## 3. Filtros

### Ano

- Visual sugerido: slicer dropdown o horizontal.
- Vista origen: calendario / `vw_movimientos[fecha_movimiento]`.
- Interaccion: afecta evolucion historica y movimientos; stock actual solo si se crea contexto historico.

### Cosecha

- Visual sugerido: dropdown.
- Vista origen: `vw_stock_actual[cosecha]`.
- Interaccion: filtra lotes y stock por cosecha.

### Bodega

- Visual sugerido: dropdown.
- Vista origen: `vw_stock_actual[bodega_nombre]`.
- Interaccion: afecta toda la pagina.

### Deposito

- Visual sugerido: dropdown.
- Vista origen: `vw_stock_actual[deposito_nombre]`.
- Interaccion: filtra piletas, capacidad y tabla.

### Pileta

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_stock_actual[pileta_codigo]`.
- Interaccion: filtra stock, ocupacion, movimientos y panel lateral.

### Lote

- Visual sugerido: dropdown con busqueda.
- Vista origen: `vw_stock_actual[lote_codigo]`.
- Interaccion: filtra stock por lote y habilita trazabilidad.

### Variedad

- Visual sugerido: dropdown.
- Vista origen: `vw_stock_actual[variedad_nombre]`.
- Interaccion: filtra stock por variedad y conecta con Produccion.

### Estado de pileta

- Visual sugerido: dropdown.
- Vista origen: `vw_stock_actual[estado_pileta]`.
- Interaccion: filtra piletas disponibles, ocupadas o bloqueadas segun definicion.

### Estado de lote

- Visual sugerido: dropdown.
- Vista origen: `vw_stock_actual[estado_lote]`.
- Interaccion: filtra lotes activos, bloqueados u otros estados.

## 4. KPIs principales

### Litros Stock Actual

- Medida DAX: `Litros Stock Actual`.
- Formato: `#,0.00 L`.
- Origen: `vw_stock_actual[litros_stock]`.
- Tooltip: litros por bodega, deposito, lote y pileta.
- Interaccion: click resalta matriz de stock.

### Capacidad Total

- Medida DAX: `Capacidad Total`.
- Formato: `#,0.00 L`.
- Origen: `vw_stock_actual[capacidad_litros]`.
- Tooltip: capacidad por piletas unicas; advertir si se usa medida defensiva para no duplicar por lote.
- Interaccion: click resalta visual de ocupacion.

### Capacidad Ocupada %

- Medida DAX: `Capacidad Ocupada %`.
- Formato: `0.00%`.
- Origen: `vw_stock_actual[litros_stock]` y `vw_stock_actual[capacidad_litros]`.
- Tooltip: litros ocupados, capacidad total y capacidad libre.
- Interaccion: filtra piletas con mayor ocupacion.

### Capacidad Libre

- Medida DAX sugerida: `Capacidad Libre = [Capacidad Total] - [Litros Stock Actual]`.
- Formato: `#,0.00 L`.
- Origen: `vw_stock_actual`.
- Tooltip: capacidad disponible por deposito o bodega.
- Interaccion: resalta visual de capacidad por deposito.

### Piletas Ocupadas

- Medida DAX sugerida: conteo de piletas con `litros_stock > 0`.
- Formato: entero.
- Origen: `vw_stock_actual[pileta_id]`, `vw_stock_actual[litros_stock]`.
- Tooltip: cantidad de piletas con stock y total de piletas visibles.
- Interaccion: filtra tabla a piletas con stock.

### Lotes Activos

- Medida DAX sugerida: `DISTINCTCOUNT(vw_stock_actual[lote_id])`.
- Formato: entero.
- Origen: `vw_stock_actual`.
- Tooltip: lotes con stock actual en el contexto.
- Interaccion: click filtra tabla de stock por lote.

## 5. Visuales principales

## Ocupacion por pileta

- Tipo de grafico: barras horizontales o bullet chart.
- Campos:
  - eje: `pileta_codigo`;
  - valores: `Litros Stock Actual`;
  - referencia: `Capacidad Total` o capacidad por pileta.
- Medidas: `Litros Stock Actual`, `Capacidad Total`, `Capacidad Ocupada %`.
- Colores:
  - ocupado: `#3E244A`;
  - libre: `#E8E0D6`;
  - advertencia: `#D69A2D`;
  - critico: `#8A1F2D`.
- Tooltip: pileta, litros, capacidad, ocupacion, estado.
- Drill-through: Stock detalle o Trazabilidad por lote si hay lote seleccionado.
- Interaccion: click en pileta abre panel lateral.

## Stock por lote

- Tipo de grafico: barras horizontales.
- Campos:
  - eje: `lote_codigo`;
  - valores: `Litros Stock Actual`.
- Medidas: `Litros Stock Actual`.
- Colores: borravino con variacion neutra.
- Tooltip: lote, variedad, cosecha, piletas asociadas.
- Drill-through: Trazabilidad.
- Interaccion: click en lote filtra tabla y panel lateral.

## Stock por variedad

- Tipo de grafico: barras horizontales o columnas.
- Campos:
  - eje: `variedad_nombre`;
  - valores: `Litros Stock Actual`.
- Medidas: `Litros Stock Actual`.
- Colores: paleta de datos de variedades.
- Tooltip: litros, lotes, piletas, cosecha.
- Drill-through: Produccion filtrada por variedad.
- Interaccion: click en variedad filtra pagina.

## Capacidad utilizada por deposito

- Tipo de grafico: columnas apiladas o barras.
- Campos:
  - eje: `deposito_nombre`;
  - valores: `Litros Stock Actual`, `Capacidad Libre`.
- Medidas: `Litros Stock Actual`, `Capacidad Libre`.
- Colores: ocupado borravino, libre crema oscuro.
- Tooltip: deposito, capacidad total, ocupacion, piletas.
- Drill-through: Reportes de stock.
- Interaccion: click en deposito filtra piletas.

## Evolucion historica de stock

- Tipo de grafico: linea.
- Campos:
  - eje: `DimFecha[Fecha]` o `AnioMes`;
  - valor: medida de stock historico si se implementa en el modelo.
- Medidas: stock historico derivado de movimientos.
- Colores: marron madera o borravino.
- Tooltip: fecha, stock, entradas, salidas.
- Drill-through: Movimientos.
- Interaccion: seleccion de periodo filtra movimientos.

## Piletas con ocupacion critica

- Tipo de grafico: tabla compacta o barras filtradas.
- Campos:
  - `pileta_codigo`;
  - `litros_stock`;
  - `capacidad_litros`;
  - `porcentaje_ocupacion`.
- Medidas: `Litros Stock Actual`, `Capacidad Ocupada %`.
- Colores:
  - mayor a 90%: rojo vino;
  - 75% a 90%: ambar;
  - menor a 75%: verde oliva.
- Tooltip: pileta, estado, deposito, lote principal.
- Drill-through: detalle de Stock.
- Interaccion: click abre panel lateral.

## 6. Tabla inferior

### Tabla de stock

- Visual: Table o Matrix.
- Ubicacion: parte inferior.
- Orden recomendado: `porcentaje_ocupacion` descendente y luego `pileta_codigo`.

### Campos

- `bodega_nombre`
- `deposito_nombre`
- `pileta_codigo`
- `lote_codigo`
- `variedad_nombre`
- `estado_pileta`
- `estado_lote`
- `litros_stock`
- `capacidad_litros`
- `porcentaje_ocupacion`
- ultima operacion desde `vw_movimientos[tipo_operacion]`
- fecha ultimo movimiento desde `vw_movimientos[fecha_movimiento]`

### Formato

- Encabezado marron madera.
- Texto encabezado crema.
- Filas alternas suaves.
- Litros y capacidad alineados a la derecha.
- Porcentaje con formato `0.00%`.
- Ocupacion critica con formato condicional.

## 7. Panel lateral de detalle

### Activacion

Se muestra al seleccionar una pileta o lote.

### Si se selecciona pileta

- codigo de pileta.
- deposito.
- estado.
- capacidad.
- litros actuales.
- ocupacion.
- lotes contenidos.
- ultimos movimientos.
- alertas de capacidad.

### Si se selecciona lote

- codigo de lote.
- variedad.
- cosecha.
- estado.
- litros actuales.
- piletas donde esta distribuido.
- ultimas operaciones.
- boton o accion `Ver trazabilidad`.

### Vinculo a trazabilidad

- Accion: navegar a pagina Trazabilidad con `lote_id` o `lote_codigo`.

## 8. Alertas

### Pileta sobre 90%

- Color: rojo vino `#8A1F2D`.
- Regla: `Capacidad Ocupada % >= 90%`.
- Accion: abrir detalle de pileta.

### Pileta vacia

- Color: gris calido `#A89F91`.
- Regla: stock en pileta igual a cero o sin registro en `vw_stock_actual`.
- Accion: revisar disponibilidad.

### Lote sin movimientos recientes

- Color: ambar `#D69A2D`.
- Regla: ultimo movimiento anterior al umbral definido por la bodega.
- Accion: revisar trazabilidad o movimientos.

### Stock negativo logico

- Color: rojo vino.
- Regla: `litros_stock < 0`.
- Accion: revisar movimientos; no deberia ocurrir.

### Capacidad superada

- Color: rojo vino.
- Regla: `litros_stock > capacidad_litros`.
- Accion: revisar movimientos y capacidad configurada.

## 9. Navegacion

### Click en pileta

- Abre o actualiza panel lateral.
- Filtra tabla inferior y visuales de ocupacion.

### Click en lote

- Destino: Trazabilidad.
- Contexto: lote seleccionado.

### Click en variedad

- Destino: Produccion filtrada.
- Contexto: variedad seleccionada.

### Click en alerta

- Destino:
  - sobreocupacion -> panel detalle;
  - stock negativo -> Reportes;
  - lote sin movimientos -> Trazabilidad;
  - pileta vacia -> Stock filtrado.

## 10. Performance

- No usar demasiadas tablas grandes en la misma pagina.
- Limitar tabla inferior a columnas necesarias.
- Usar medidas agregadas para capacidad y ocupacion.
- Evitar relaciones ambiguas activas entre `pileta_origen_id` y `pileta_destino_id`.
- Evitar visuales con alta cardinalidad sin filtro.
- Usar top N para piletas criticas si hay muchas piletas.
- Validar que la capacidad no se sume duplicada por lote-pileta.
- Usar Import mode.

## 11. Checklist final

- [ ] Filtros funcionan.
- [ ] KPIs correctos.
- [ ] Ocupacion calculada correctamente.
- [ ] Tabla ordenada.
- [ ] Drill-through a trazabilidad.
- [ ] Alertas correctas.
- [ ] Colores consistentes.
- [ ] Sin scroll.
- [ ] Valores coinciden con `vw_stock_actual`.
- [ ] Capacidad no se duplica por lote.
- [ ] Panel lateral muestra pileta/lote seleccionado.
- [ ] Ultimo movimiento se muestra correctamente.
