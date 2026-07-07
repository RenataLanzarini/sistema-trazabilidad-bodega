# Trazabilidad: Diseno del Grafo

## Objetivo

La pagina de trazabilidad debe permitir entender el origen, transformacion y destino de un lote o producto terminado. El grafo debe mostrar relaciones tecnicas sin convertirse en una maraña visual.

## Apariencia general

- Area central amplia con fondo crema.
- Nodos con forma simple, bordes suaves y sombra leve.
- Flechas claras de izquierda a derecha para genealogia historica.
- El nodo seleccionado usa borde borravino y acento dorado.
- El detalle completo vive en panel lateral, no dentro del nodo.

## Informacion minima por nodo

Cada nodo debe conservar:

- Tipo de nodo.
- Identificador o codigo.
- Fecha principal.
- Litros asociados si aplica.
- Estado principal si aplica.
- Variedad o producto si aplica.

## Tipos de nodos

### Recepcion

- Representa CIU/origen de uva.
- Datos clave: numero CIU, fecha, finca/origen, variedad, kilos, Brix.
- Color: crema con borde dorado.

### Lote

- Representa unidad genealogica central.
- Datos clave: codigo, cosecha, variedad, color, estado.
- Color: segun grupo varietal si existe; si no, blanco con borde borravino.

### Operacion

- Representa evento productivo.
- Datos clave: tipo, fecha, responsable, estado, anulada.
- Color: marron madera suave o gris calido.

### Pileta

- Representa ubicacion fisica.
- Datos clave: codigo, estado, capacidad, litros.
- Color: blanco con borde marron.

### Merma

- Representa perdida registrada.
- Datos clave: causa, litros, fecha, responsable.
- Color: rojo vino controlado.

### Fraccionamiento

- Representa consumo de vino para producto terminado.
- Datos clave: fecha, litros consumidos, responsable.
- Color: dorado suave.

### Producto terminado

- Representa salida a producto final.
- Datos clave: codigo, unidades, volumen por unidad, litros totales.
- Color: verde suave o dorado segun contexto.

### Venta granel

- Representa salida comercial a granel.
- Datos clave: cliente, documento, litros, fecha.
- Color: neutro oscuro con acento dorado.

## Flechas

- Direccion genealogica: origen -> resultado.
- Direccion fisica: pileta origen -> pileta destino.
- Direccion comercial: lote/pileta -> venta o producto terminado.
- Color por defecto: gris calido.
- Color resaltado: dorado.
- Grosor proporcional a litros cuando el visual lo permita.

## Etiquetas de litros

- Mostrar litros en flechas cuando sean clave para entender mezcla, division o salida.
- Formato recomendado: `1.250 L`.
- Si hay porcentaje, mostrar `1.250 L - 35%`.
- Evitar etiquetas superpuestas; priorizar tooltip si el grafo esta cargado.

## Panel lateral de detalle

Debe mostrar para el nodo seleccionado:

- Codigo y tipo.
- Fechas.
- Litros, kilos o unidades.
- Variedad, color, cosecha.
- Pileta asociada y estado.
- Responsable.
- Observaciones.
- Relaciones entrantes y salientes.

## Filtros

- Lote o producto terminado.
- Fecha o cosecha.
- Tipo de relacion.
- Variedad.
- Pileta.
- Mostrar/ocultar operaciones intermedias.
- Mostrar/ocultar nodos comerciales.

## Leyenda

La leyenda debe explicar:

- Color por tipo de nodo.
- Significado de flechas.
- Diferencia entre genealogia y movimiento fisico.
- Estado seleccionado/resaltado.

## Mantener estetica sin perder informacion

- Mostrar etiquetas cortas en nodos.
- Usar tooltips para informacion secundaria.
- Usar panel lateral para detalle completo.
- Limitar el grafo inicial a la consulta seleccionada.
- Permitir expandir hacia atras o adelante en lugar de mostrar todo el universo.
- Usar colores tecnicos consistentes, no decorativos.
