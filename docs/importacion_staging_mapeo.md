# Informe de mapeo desde staging hacia dominio real

## Objetivo

Este documento audita el contenido importado desde el Excel real a las tablas `staging` y propone el mapeo conceptual hacia el modelo transaccional del sistema.

No define carga definitiva ni modifica datos. Su objetivo es identificar que puede poblarse automaticamente, que requiere decision manual y cuales son los riesgos antes de construir scripts de importacion hacia tablas reales.

## Alcance revisado

Tablas staging cargadas:

| Tabla staging | Filas |
| --- | ---: |
| `staging.piletas_lotes` | 2225 |
| `staging.movimiento` | 1981 |
| `staging.borrador` | 23 |

Columnas de `staging.piletas_lotes`:

- `id_lote_pileta`
- `lotes_origen`
- `datetime`
- `pileta_nro`
- `capacidad`
- `variedad`
- `cantidad_inicial`
- `cantidad_actual`
- `observaciones_lote`
- `ciu`
- `estado`
- `califiacion_vino`
- `color`

Columnas de `staging.movimiento`:

- `id_movimiento`
- `date_time`
- `lote_origen`
- `pileta_origen`
- `variedad_origen`
- `volumen_trasegado`
- `pileta_destino`
- `lote_destino_original`
- `variedad_destino_original`
- `volumen_destino_original`
- `volumen_destino_final`
- `lote_destino_final`
- `variedad_destino_final`
- `observaciones_movimiento`
- `pileta_origen_estado`
- `pileta_destino_estado`
- `copiar_estado_destino`
- `pileta_destino_final_estado`
- `calificacion_origen`
- `calificacion_destino`
- `calificacion_destino_final`

`staging.borrador` contiene 23 filas y 10 columnas genericas `unnamed_0` a `unnamed_9`. No se recomienda mapearla automaticamente sin una revision funcional previa.

## Hallazgos de datos

### Variedades

Hay muchas variantes textuales en `variedad` y `variedad_origen`. Las mas frecuentes en `staging.piletas_lotes` son:

| Variedad | Filas |
| --- | ---: |
| Syrah | 152 |
| Bonarda | 134 |
| Malbec | 134 |
| Chardonnay | 83 |
| Tinto | 67 |
| AJUSTE COSECHA 2026 | 60 |
| Ajuste semana 13/02/2025 | 51 |
| Criolla Recarga | 50 |
| Cabernet Sauvignon | 49 |
| Borra | 44 |

Riesgo principal: el Excel mezcla variedades reales, cortes, procesos, ajustes, destinos comerciales y descripciones operativas dentro del mismo campo. No conviene crear todas automaticamente como variedades reales sin una tabla de equivalencias.

### Estados

Estados en `staging.piletas_lotes.estado`:

| Estado | Filas |
| --- | ---: |
| Fermentando | 371 |
| Descubada | 365 |
| Terminado | 303 |
| 1er Trasiego | 285 |
| 2do Trasiego | 236 |
| Rectificado | 207 |
| Sin estado | 166 |
| Filtrado Tang | 157 |
| Recarga Fermentando | 59 |
| Traslado Venta | 57 |
| Mosto | 19 |

Estados en movimientos:

- `pileta_origen_estado`: principalmente `Fermentando`, `Descubada`, `1er Trasiego`, `2do Trasiego`, `Rectificado`, `Filtrado Tang`, `Terminado`.
- `pileta_destino_estado`: tiene 734 filas sin valor.
- `pileta_destino_final_estado`: representa mejor el estado resultante de la pileta/lote despues del movimiento.

Riesgo principal: en el Excel el estado parece representar estado productivo del contenido, no necesariamente estado fisico de la pileta. Debe decidirse si cada valor se carga como `estados_lote`, `estados_pileta` o ambos.

### Calificaciones

Calificaciones en `staging.piletas_lotes.califiacion_vino`:

| Calificacion | Filas |
| --- | ---: |
| Sin valor | 1308 |
| 1 | 497 |
| 1+ | 216 |
| 1- | 138 |
| 2+ | 64 |
| 2 | 2 |

En `staging.movimiento` la calificacion aparece principalmente en `calificacion_destino_final`, con muchos nulos. Conviene cargar catalogo de calificaciones desde ambos origenes, normalizando a texto.

### Fechas

| Campo | Desde | Hasta |
| --- | --- | --- |
| `piletas_lotes.datetime` | 2025-02-03 19:50:12 | 2026-07-07 18:48:37 |
| `movimiento.date_time` | 2025-02-15 21:00:53 | 2026-07-07 18:48:19 |

Las fechas cubren principalmente cosechas y operaciones 2025-2026.

### Piletas

| Origen | Piletas unicas |
| --- | ---: |
| `piletas_lotes.pileta_nro` | 101 |
| `movimiento.pileta_origen` | 99 |
| `movimiento.pileta_destino` | 95 |

Cruce con movimientos:

- `movimiento.pileta_origen` no existente en `piletas_lotes.pileta_nro`: 0
- `movimiento.pileta_destino` no existente en `piletas_lotes.pileta_nro`: 0

Conclusion: las piletas son el dato mas consistente para automatizar.

### Lotes

| Origen | Lotes unicos |
| --- | ---: |
| `piletas_lotes.lotes_origen` | 23 |
| `movimiento.lote_origen` | 841 |
| `movimiento.lote_destino_original` | 1393 |
| `movimiento.lote_destino_final` | 1967 |

Cruce con `piletas_lotes.lotes_origen`:

- `movimiento.lote_origen` no existente en `piletas_lotes.lotes_origen`: 1957 movimientos.
- `movimiento.lote_destino_final` no existente en `piletas_lotes.lotes_origen`: 1966 movimientos.

Conclusion: `piletas_lotes.lotes_origen` no parece ser el catalogo completo de lotes. Para lotes historicos y genealogia, el origen mas importante sera `staging.movimiento`.

### Nulos, ceros y negativos

| Campo | Nulos | Negativos | Ceros |
| --- | ---: | ---: | ---: |
| `piletas_lotes.cantidad_inicial` | 254 | 62 | 566 |
| `piletas_lotes.cantidad_actual` | 4 | 66 | 25 |
| `piletas_lotes.capacidad` | 23 | 0 | 0 |
| `movimiento.volumen_trasegado` | 14 | 219 | 2 |
| `movimiento.volumen_destino_original` | 28 | 62 | 560 |
| `movimiento.volumen_destino_final` | 13 | 68 | 22 |

Riesgo principal: hay volumenes negativos. No pueden cargarse directamente como `movimientos_fisicos.litros`, porque el dominio valida litros mayores a cero. Deben interpretarse como ajustes, correcciones, salidas o anulaciones segun contexto.

### Movimientos incompletos

| Condicion | Filas |
| --- | ---: |
| Sin `lote_origen` | 13 |
| Sin `lote_destino_final` | 13 |
| Sin `lote_destino_original` | 586 |
| Sin `pileta_origen` | 13 |
| Sin `pileta_destino` | 27 |

Los movimientos sin origen o destino pueden representar entradas iniciales, salidas, ventas, mermas, ajustes o registros incompletos. Requieren clasificacion antes de cargar al dominio.

## Mapeo por tabla real

### `bodegas`

1. Datos desde staging:
   - No hay columna explicita de bodega.
   - Todo el Excel parece corresponder a una misma bodega: Bodega y Vinedos Lanzarini.

2. Columnas mapeables:
   - `nombre`: valor fijo sugerido `Bodega y Vinedos Lanzarini`.
   - `activa`: `true`.

3. Datos faltantes:
   - `razon_social`.
   - `identificacion_fiscal`.
   - `ubicacion`.

4. Valores por defecto:
   - `nombre`: `Bodega y Vinedos Lanzarini`.
   - `activa`: `true`.

5. Riesgos:
   - Si en el futuro hay multiples bodegas, este Excel no permite distinguirlas.

6. Recomendacion:
   - Carga manual o semiautomatica una sola vez. No debe inferirse en cada fila.

### `depositos`

1. Datos desde staging:
   - No hay columna explicita de deposito.
   - Las piletas podrian pertenecer a un deposito default.

2. Columnas mapeables:
   - `bodega_id`: bodega default.
   - `nombre`: valor fijo sugerido `Deposito principal`.
   - `tipo`: valor opcional `Bodega`.
   - `activo`: `true`.

3. Datos faltantes:
   - Deposito real.
   - Sector.
   - Ubicacion interna.

4. Valores por defecto:
   - `nombre`: `Deposito principal`.
   - `activo`: `true`.

5. Riesgos:
   - Puede ocultar diferencias reales entre sectores, naves o depositos.

6. Recomendacion:
   - Manual para MVP, con un deposito default validado por el usuario.

### `piletas`

1. Datos desde staging:
   - `pileta_nro`.
   - `capacidad`.
   - Estados asociados desde `estado`, `pileta_origen_estado`, `pileta_destino_estado`, `pileta_destino_final_estado`.

2. Columnas mapeables:
   - `codigo`: `pileta_nro` convertido a texto estable, por ejemplo `P-001`.
   - `nombre`: `Pileta {pileta_nro}`.
   - `capacidad_litros`: `capacidad`.
   - `bodega_id`: bodega default.
   - `deposito_id`: deposito default.
   - `estado_pileta_id`: estado default o estado derivado.
   - `activa`: `true`.

3. Datos faltantes:
   - Material.
   - Observaciones propias de la pileta.
   - Deposito real.
   - Estado fisico real de la pileta independiente del vino.
   - `litros_por_cm`.

4. Valores por defecto:
   - `estado_pileta_id`: estado `Activa` o `Disponible` si se decide separar estado fisico de estado productivo.
   - `activa`: `true`.

5. Riesgos:
   - `pileta_nro` llega como numero decimal (`1.0`, `2.0`); debe normalizarse sin decimales.
   - `capacidad` tiene 23 nulos.
   - Puede haber multiples capacidades para la misma pileta a lo largo de filas historicas. Debe validarse si se toma la capacidad maxima, la ultima o la mas frecuente.

6. Recomendacion:
   - Cargable automaticamente con reglas previas:
     - normalizar codigo de pileta;
     - resolver capacidad por pileta;
     - usar deposito default;
     - no usar estado del lote como estado fisico de pileta sin aprobacion.

### `variedades`

1. Datos desde staging:
   - `piletas_lotes.variedad`.
   - `movimiento.variedad_origen`.
   - `movimiento.variedad_destino_original`.
   - `movimiento.variedad_destino_final`.

2. Columnas mapeables:
   - `nombre`: texto normalizado.
   - `activa`: `true`.

3. Datos faltantes:
   - Descripcion.
   - Clasificacion entre variedad pura, corte, ajuste, mosto, borra, venta o proceso.

4. Valores por defecto:
   - `activa`: `true`.

5. Riesgos:
   - Hay valores que no son variedades reales: `Ajuste`, `Borra`, `Claro de Filtro`, `Traslado`, nombres con fechas, destinos de venta y descripciones operativas.
   - Hay errores ortograficos y variantes: `Tanat`, `Tannat`, `Aspirant`, `Aspirat`, `Anccelotta`, `Ancellotta`.

6. Recomendacion:
   - No cargar automaticamente todo como `variedades`.
   - Crear tabla de equivalencias previa: valor_excel -> variedad_real / corte / ajuste / descartar.
   - Automatizar solo valores aprobados.

### `estados_pileta`

1. Datos desde staging:
   - `pileta_origen_estado`.
   - `pileta_destino_estado`.
   - `pileta_destino_final_estado`.
   - posiblemente `piletas_lotes.estado`.

2. Columnas mapeables:
   - `nombre`.
   - `activo`: `true`.

3. Datos faltantes:
   - Distincion entre estado fisico de pileta y estado productivo del vino.

4. Valores por defecto:
   - `activo`: `true`.

5. Riesgos:
   - Valores como `Fermentando`, `Descubada`, `1er Trasiego` y `Rectificado` describen mas al lote/proceso que a la pileta.

6. Recomendacion:
   - Cargar manualmente un catalogo minimo fisico (`Disponible`, `Ocupada`, `Inactiva`, `Mantenimiento`) y no inferirlo automaticamente desde Excel.

### `estados_lote`

1. Datos desde staging:
   - `piletas_lotes.estado`.
   - `movimiento.pileta_origen_estado`.
   - `movimiento.pileta_destino_final_estado`.

2. Columnas mapeables:
   - `nombre`.
   - `activo`: `true`.

3. Datos faltantes:
   - Definicion formal de flujo entre estados.

4. Valores por defecto:
   - `activo`: `true`.

5. Riesgos:
   - Algunos estados tienen sentido de proceso, no de estado final.
   - Hay nulos relevantes.

6. Recomendacion:
   - Cargable automaticamente como catalogo inicial, con revision manual de nombres.

### `calificaciones_vino`

1. Datos desde staging:
   - `califiacion_vino`.
   - `calificacion_origen`.
   - `calificacion_destino`.
   - `calificacion_destino_final`.

2. Columnas mapeables:
   - `nombre`: `1`, `1+`, `1-`, `2+`, `2`.
   - `activa`: `true`.

3. Datos faltantes:
   - Significado funcional de cada calificacion.

4. Valores por defecto:
   - `activa`: `true`.

5. Riesgos:
   - Algunas columnas vienen numericas y otras texto. Deben convertirse todas a texto canonico.

6. Recomendacion:
   - Cargable automaticamente con normalizacion simple y revision posterior de descripcion.

### `recepciones_uva`

1. Datos desde staging:
   - `ciu`.
   - `datetime`.
   - `variedad`.
   - `cantidad_inicial` podria aproximar kilos o litros iniciales, pero no esta claro.
   - `observaciones_lote`.

2. Columnas mapeables:
   - `numero_ciu`: `ciu`.
   - `fecha`: fecha de `datetime`.
   - `cosecha`: año de `datetime`, si no hay dato mejor.
   - `variedad_id`: desde `variedad` aprobada.
   - `observaciones`: `observaciones_lote`.
   - `bodega_id`: bodega default.

3. Datos faltantes:
   - `origen_uva_id`.
   - `responsable_id`.
   - `kilos_recibidos`.
   - Estado confiable de recepcion.
   - Campos CIU ampliados: finca, INV, bruto, tara, neto, brix, chofer, patente, etc.

4. Valores por defecto:
   - `origen_uva_id`: origen default `No informado` si se aprueba.
   - `responsable_id`: usuario tecnico de importacion si se aprueba.
   - `estado`: `importado`.
   - `kilos_recibidos`: no deberia derivarse sin confirmacion.

5. Riesgos:
   - `cantidad_inicial` no necesariamente son kilos de uva recibida.
   - Hay CIU nulos o repetidos potenciales.
   - El Excel de piletas/lotes parece estar mas cerca de stock/lotificacion que de recepcion CIU completa.

6. Recomendacion:
   - No cargar automaticamente como recepciones definitivas sin reglas adicionales.
   - Cargar solo CIU identificables si el usuario valida que `cantidad_inicial` representa kilos o volumen inicial.

### `lotes`

1. Datos desde staging:
   - `piletas_lotes.lotes_origen`.
   - `movimiento.lote_origen`.
   - `movimiento.lote_destino_original`.
   - `movimiento.lote_destino_final`.
   - `datetime` / `date_time`.
   - variedades origen/destino.
   - estados origen/destino/final.
   - calificacion final.
   - color.
   - observaciones.

2. Columnas mapeables:
   - `codigo`: codigo de lote desde movimiento, principalmente `lote_destino_final` y `lote_origen`.
   - `fecha_nacimiento`: primera fecha donde aparece el lote.
   - `cosecha`: año de primera fecha o derivado del codigo si aplica.
   - `variedad_principal_id`: variedad normalizada.
   - `estado_lote_id`: ultimo estado conocido.
   - `calificacion_vino_id`: ultima calificacion conocida.
   - `color`: desde `piletas_lotes.color`, si corresponde.
   - `observaciones`: observaciones consolidadas o de origen.
   - `bodega_id`: default.
   - `tipo_producto_id`: default `Vino` o `Mosto`, si se define regla.
   - `activo`: `true`.

3. Datos faltantes:
   - Relacion segura con `recepcion_uva_id`.
   - Tipo producto confiable para cada lote.
   - Definicion de lote padre/hijo.

4. Valores por defecto:
   - `tipo_producto_id`: `Vino` salvo deteccion aprobada de `Mosto`.
   - `estado_lote_id`: `Importado` o ultimo estado conocido.
   - `activo`: `true`.

5. Riesgos:
   - `piletas_lotes.lotes_origen` no contiene el universo real de lotes.
   - El mismo lote puede cambiar de pileta, estado, variedad textual o calificacion.
   - Las mezclas y divisiones no pueden inferirse solo por codigo sin reglas.

6. Recomendacion:
   - Cargable automaticamente despues de definir una estrategia de consolidacion:
     - universo de lotes desde todos los campos de lote de `staging.movimiento`;
     - fecha nacimiento por primera aparicion;
     - atributos por ultima aparicion o por regla de prioridad.

### `operaciones_productivas`

1. Datos desde staging:
   - `id_movimiento`.
   - `date_time`.
   - `observaciones_movimiento`.
   - estados antes/despues.
   - existencia o no de piletas origen/destino.

2. Columnas mapeables:
   - `codigo_externo`: `id_movimiento`.
   - `fecha`: `date_time`.
   - `observaciones`: `observaciones_movimiento`.
   - `bodega_id`: default.
   - `responsable_id`: usuario tecnico de importacion.
   - `tipo_operacion_id`: inferido por reglas.
   - `estado`: `importada`.
   - `anulada`: `false`.

3. Datos faltantes:
   - Tipo de operacion explicito.
   - Responsable real.
   - Motivo de anulacion.

4. Valores por defecto:
   - `responsable_id`: usuario `Importacion`.
   - `estado`: `importada`.
   - `anulada`: `false`.

5. Riesgos:
   - No todo movimiento Excel equivale a una operacion productiva independiente.
   - Los negativos y ajustes requieren tipos especiales.

6. Recomendacion:
   - Cargable automaticamente una operacion por fila de `staging.movimiento`, siempre que se defina catalogo de tipos: entrada inicial, trasiego, salida, ajuste, mezcla/division candidata, correccion.

### `movimientos_fisicos`

1. Datos desde staging:
   - `id_movimiento`.
   - `date_time`.
   - `lote_origen`.
   - `pileta_origen`.
   - `pileta_destino`.
   - `lote_destino_final`.
   - `volumen_trasegado`.
   - `observaciones_movimiento`.

2. Columnas mapeables:
   - `codigo_externo`: `id_movimiento`.
   - `fecha`: `date_time`.
   - `lote_id`: lote afectado segun regla de origen/destino.
   - `pileta_origen_id`: `pileta_origen`.
   - `pileta_destino_id`: `pileta_destino`.
   - `litros`: valor absoluto de volumen, si el tipo lo permite.
   - `estado`: `importado`.
   - `observaciones`: `observaciones_movimiento`.
   - `responsable_id`: usuario tecnico de importacion.
   - `operacion_productiva_id`: operacion importada asociada.

3. Datos faltantes:
   - Responsable real.
   - Tipo exacto del movimiento.
   - Criterio para movimientos con volumen negativo.

4. Valores por defecto:
   - `estado`: `importado`.
   - `responsable_id`: usuario `Importacion`.

5. Riesgos:
   - El dominio exige `litros > 0`; hay 219 `volumen_trasegado` negativos.
   - 14 movimientos no tienen volumen trasegado.
   - 13 no tienen lote origen, 13 no tienen lote destino final, 13 no tienen pileta origen y 27 no tienen pileta destino.
   - Usar mal `lote_origen` vs `lote_destino_final` puede duplicar o invertir stock.

6. Recomendacion:
   - No cargar automaticamente hasta clasificar movimientos:
     - entrada inicial: sin origen y con destino;
     - salida: con origen y sin destino;
     - trasiego: con origen y destino;
     - ajuste positivo/negativo: volumen con signo o observacion de ajuste;
     - movimiento incompleto: cuarentena.

### `relaciones_genealogicas_lote`

1. Datos desde staging:
   - `lote_origen`.
   - `lote_destino_original`.
   - `lote_destino_final`.
   - `volumen_trasegado`.
   - `volumen_destino_original`.
   - `volumen_destino_final`.
   - `variedad_origen`.
   - `variedad_destino_original`.
   - `variedad_destino_final`.

2. Columnas mapeables:
   - `operacion_productiva_id`: operacion importada.
   - `lote_padre_id`: lote origen.
   - `lote_hijo_id`: lote destino final.
   - `litros_aportados`: `volumen_trasegado`, si positivo.
   - `tipo_relacion`: `mezcla`, `division`, `trasiego`, `ajuste`, segun regla.
   - `observaciones`: `observaciones_movimiento`.

3. Datos faltantes:
   - Marca explicita de mezcla o division.
   - Porcentajes calculados por componente.
   - Identificacion de multiples padres para una misma operacion si el Excel los separa en filas.

4. Valores por defecto:
   - Ninguno recomendable hasta clasificar reglas.

5. Riesgos:
   - Un trasiego simple no siempre crea genealogia nueva.
   - Una mezcla debe generar lote nuevo y relacionar padres con litros aportados.
   - Una division debe crear lotes hijos y relacionarlos con el padre.
   - La inferencia desde `lote_destino_original` y `lote_destino_final` puede ser ambigua.

6. Recomendacion:
   - No cargar automaticamente en primera pasada.
   - Primero cargar catalogos, piletas, lotes, operaciones y movimientos en cuarentena/control.
   - Luego generar genealogia solo con reglas verificadas y reporte de excepciones.

## Tablas que pueden poblarse desde staging

Automatizables con bajo riesgo:

1. `bodegas`: una bodega default, con aprobacion manual.
2. `depositos`: un deposito default, con aprobacion manual.
3. `piletas`: desde `pileta_nro` y `capacidad`, resolviendo capacidades nulas.
4. `calificaciones_vino`: desde valores `1`, `1+`, `1-`, `2+`, `2`.
5. `estados_lote`: desde estados productivos del Excel, previa aprobacion de nombres.

Automatizables con riesgo medio:

1. `estados_pileta`: solo si se decide aceptar los estados productivos tambien como estados de pileta, o si se carga un catalogo fisico separado.
2. `variedades`: requiere tabla de equivalencias para no convertir ajustes/procesos en variedades reales.
3. `lotes`: requiere consolidacion desde todos los campos de lote en `staging.movimiento`.
4. `operaciones_productivas`: posible una operacion por movimiento, pero requiere clasificar tipo de operacion.

No automatizar todavia:

1. `recepciones_uva`: faltan kilos confiables, origen, responsable y datos CIU completos.
2. `movimientos_fisicos`: hay volumenes negativos, nulos e incompletos que requieren clasificacion.
3. `relaciones_genealogicas_lote`: requiere reglas de mezcla/division confirmadas.

## Tablas que requieren decision manual

| Tabla | Decision pendiente |
| --- | --- |
| `bodegas` | Confirmar nombre legal, ubicacion y datos fiscales. |
| `depositos` | Confirmar si todo va a un deposito default o si hay sectores reales. |
| `estados_pileta` | Separar estado fisico de pileta vs estado productivo del lote. |
| `variedades` | Definir equivalencias y descartar valores operativos. |
| `recepciones_uva` | Confirmar si `ciu` y `cantidad_inicial` alcanzan para crear recepciones reales. |
| `lotes` | Definir codigo canonico y regla para atributos finales. |
| `operaciones_productivas` | Definir tipos de operacion por patron. |
| `movimientos_fisicos` | Definir tratamiento de negativos, nulos y movimientos incompletos. |
| `relaciones_genealogicas_lote` | Definir reglas para inferir mezcla/division. |

## Riesgos detectados

### Criticos

1. Los codigos de lote de `staging.movimiento` no cruzan con `staging.piletas_lotes.lotes_origen`. Si se toma `piletas_lotes` como maestro de lotes, se perderia casi toda la historia de movimientos.
2. Hay volumenes negativos en campos que el dominio no permite cargar como litros directos. Requieren interpretacion como ajustes, correcciones o salidas.
3. No hay responsable real ni tipo de operacion explicito en los movimientos.
4. La genealogia no puede inferirse de forma segura sin reglas adicionales.

### Importantes

1. `variedad` contiene datos operativos y comerciales, no solo variedades.
2. `estado` parece representar estado productivo del vino, no estado fisico de pileta.
3. Hay capacidades nulas en piletas.
4. Hay movimientos sin lote o sin pileta en origen/destino.
5. `borrador` no tiene encabezados utiles y debe quedar fuera de carga automatica por ahora.

### Menores

1. `califiacion_vino` viene con nombre de columna mal escrito, pero ya esta normalizado como columna staging.
2. Piletas llegan como numericas con decimal; deben transformarse a codigo texto.
3. Algunas fechas incluyen hora, aunque ciertas tablas del dominio usan fecha sin hora.

## Recomendacion de orden de importacion

1. Crear datos controlados base:
   - bodega default;
   - deposito default;
   - usuario tecnico `Importacion`;
   - tipos de producto minimos: `Vino`, `Mosto`;
   - tipos de operacion minimos para importacion.

2. Cargar catalogos confiables:
   - `calificaciones_vino`;
   - `estados_lote`;
   - `estados_pileta` solo si se define separacion correcta;
   - `variedades` desde tabla de equivalencias aprobada.

3. Cargar piletas:
   - normalizar `pileta_nro`;
   - resolver capacidad por pileta;
   - asignar bodega/deposito default.

4. Consolidar lotes:
   - construir universo desde `lote_origen`, `lote_destino_original`, `lote_destino_final` y eventualmente `lotes_origen`;
   - asignar fecha de nacimiento por primera aparicion;
   - asignar variedad/estado/calificacion por regla de prioridad.

5. Crear operaciones productivas importadas:
   - una por fila valida de `staging.movimiento`, usando `id_movimiento` como `codigo_externo`;
   - clasificar tipo de operacion por patron.

6. Crear movimientos fisicos:
   - cargar solo movimientos clasificados y validos;
   - enviar a cuarentena los negativos, nulos e incompletos hasta resolverlos.

7. Reconstruir genealogia:
   - aplicar reglas aprobadas para mezcla/division;
   - generar relaciones padre-hijo con litros aportados;
   - validar porcentajes acumulados con muestras reales.

8. Evaluar recepciones CIU:
   - cargar solo si se confirma que los datos disponibles representan recepcion real.

## Recomendacion final

El staging es util y suficiente para iniciar una importacion historica controlada, pero no debe cargarse directamente al dominio real sin una capa intermedia de reglas y equivalencias.

La primera automatizacion deberia limitarse a catalogos, bodega/deposito default, piletas y calificaciones. Lotes y movimientos deben abordarse en una segunda etapa con reporte de excepciones. Genealogia debe quedar para una tercera etapa, una vez validadas las reglas de mezcla y division con ejemplos reales de la bodega.
