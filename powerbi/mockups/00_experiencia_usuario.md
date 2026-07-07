# Experiencia de Usuario - Centro de Control Vitivinicola Lanzarini

## 1. Concepto general del producto

El producto debe presentarse como el **Centro de Control Vitivinicola Lanzarini**: un tablero integral para gestionar, analizar y auditar la operacion de una bodega real.

No debe sentirse como un conjunto de reportes aislados. Debe funcionar como un sistema de control ejecutivo y operativo donde cada pagina responde una pregunta concreta y se conecta naturalmente con las demas.

El usuario debe poder pasar de una senal ejecutiva a una investigacion tecnica sin perder contexto:

- detectar un problema;
- identificar lote, pileta o proceso;
- revisar trazabilidad;
- consultar calidad;
- ver movimientos;
- llegar a la orden de trabajo u operacion relacionada.

## 2. Tipos de usuarios

### Gerente / dueno

Perfil ejecutivo. Necesita una vision rapida de estado general, riesgos, stock, ventas y desviaciones.

Necesita ver:

- stock total;
- litros en produccion;
- ventas granel;
- productos terminados;
- mermas;
- alertas;
- estado de ordenes de trabajo;
- evolucion general por periodo.

### Enologo

Perfil tecnico-productivo. Necesita controlar lotes, calidad, fermentacion, movimientos, cortes y trazabilidad.

Necesita ver:

- lotes activos;
- stock por pileta y variedad;
- analisis enologicos;
- mediciones de fermentacion;
- mermas por causa;
- genealogia de lotes;
- operaciones productivas;
- cortes teoricos;
- ordenes asociadas a procesos.

### Operario

Perfil operativo. Necesita saber que tareas hacer, sobre que pileta/lote, con que prioridad y si estan completas.

Necesita ver:

- ordenes pendientes;
- ordenes completadas;
- lote o pileta asignada;
- observaciones;
- tareas por fecha;
- alertas simples;
- estado operativo de cada trabajo.

### Comercial / administracion

Perfil administrativo-comercial. Necesita informacion de ventas, clientes, producto disponible y reportes.

Necesita ver:

- ventas granel por cliente;
- litros vendidos;
- lotes/piletas asociados a venta;
- productos terminados;
- stock disponible;
- reportes exportables;
- documentos o codigos de operacion.

## 3. Necesidades por usuario

| Usuario | Pregunta principal | Paginas clave |
|---|---|---|
| Gerente / dueno | Como esta la bodega hoy? | Inicio, Stock, Comercial, Reportes |
| Enologo | Que paso con este lote y en que estado esta? | Produccion, Stock, Trazabilidad, Calidad, Corte Teorico |
| Operario | Que tengo que hacer y que ya esta completado? | Ordenes de Trabajo, Stock |
| Comercial / administracion | Que se vendio y desde que lote/pileta salio? | Comercial, Stock, Trazabilidad, Reportes |

## 4. Flujo principal de navegacion

### Inicio

Puerta de entrada ejecutiva. Resume KPIs, graficos principales y alertas.

### Produccion

Detalle de recepcion de uva, lotes, cosecha, variedad y operaciones productivas.

### Stock

Control de litros actuales por lote, pileta, bodega y capacidad.

### Trazabilidad

Vista genealogica y tecnica de origen, transformaciones, movimientos y destino.

### Calidad

Analisis enologicos y mediciones de fermentacion.

### Comercial

Ventas a granel, clientes, litros vendidos y origen comercial.

### Ordenes de Trabajo

Seguimiento operativo de tareas pendientes, completadas y vinculadas a operaciones.

### Reportes

Tablas exportables, vistas administrativas y consultas detalladas.

## 5. Narrativa de uso

Un gerente abre **Inicio** y detecta que el KPI **% Merma** esta en advertencia. Hace click sobre el KPI y la pagina filtra los graficos por causa de merma.

Desde ahi entra a **Stock** para ver que pileta y lote estan asociados al desvio. Selecciona la pileta con mayor incidencia y observa capacidad, stock y ultimos movimientos.

Luego navega a **Trazabilidad** con el lote seleccionado. En el grafo ve el origen del lote, mezclas anteriores, movimientos y si hubo fraccionamiento o venta granel.

Desde el panel lateral abre **Calidad** para revisar analisis enologicos, pH, alcohol, Brix o Baume asociados al lote/pileta.

Finalmente entra a **Ordenes de Trabajo** para revisar si existia una tarea vinculada, quien la ejecuto, si fue completada y que observaciones se cargaron.

El flujo completo debe sentirse continuo: el lote, pileta, fecha o filtro seleccionado acompana al usuario entre paginas.

## 6. Conexion entre paginas

- Inicio conecta con todas las paginas por KPIs, graficos y alertas.
- Produccion conecta con Stock por lote, cosecha y variedad.
- Produccion conecta con Trazabilidad por lote.
- Stock conecta con Trazabilidad por lote y pileta.
- Stock conecta con Calidad por pileta/lote.
- Trazabilidad conecta con Calidad, Comercial, Produccion y Ordenes.
- Calidad conecta con Trazabilidad por lote y pileta.
- Comercial conecta con Trazabilidad por lote vendido.
- Ordenes conecta con Operaciones Productivas y Stock por lote/pileta.
- Reportes recibe contexto desde cualquier pagina para exportacion o analisis detallado.

## 7. Filtros globales y filtros por pagina

### Filtros globales

Deben estar disponibles como contexto transversal:

- Ano;
- Cosecha;
- Bodega;
- Variedad;
- Lote;
- Pileta.

### Filtros por pagina

#### Inicio

- Estado;
- Cliente;
- Operacion.

#### Produccion

- Origen de uva;
- Finca;
- CIU;
- Tipo de producto.

#### Stock

- Deposito;
- Estado de pileta;
- Estado de lote;
- Capacidad / ocupacion.

#### Trazabilidad

- Tipo de relacion;
- Direccion: hacia atras / hacia adelante;
- Mostrar operaciones;
- Mostrar piletas;
- Mostrar destinos comerciales.

#### Calidad

- Tipo de registro: analisis / fermentacion;
- Rango de pH;
- Rango de alcohol;
- Rango de Baume;
- Fecha de medicion.

#### Comercial

- Cliente;
- Documento;
- Tipo de salida;
- Fecha de venta.

#### Ordenes de Trabajo

- Tarea;
- Operario;
- Completada / pendiente;
- Fecha completada;
- Operacion vinculada.

#### Reportes

- Filtros avanzados segun reporte.

## 8. Paginas con drill-through

Deben permitir drill-through:

- Inicio -> Stock por pileta/lote.
- Inicio -> Comercial por cliente.
- Inicio -> Ordenes por estado.
- Produccion -> Trazabilidad por lote.
- Stock -> Trazabilidad por lote/pileta.
- Stock -> Calidad por lote/pileta.
- Trazabilidad -> Calidad por lote.
- Trazabilidad -> Comercial por venta granel.
- Comercial -> Trazabilidad por lote vendido.
- Ordenes de Trabajo -> Operacion Productiva asociada.
- Reportes -> detalle por lote, pileta, cliente u operacion.

## 9. Paginas con panel lateral de detalle

### Deben tener panel lateral

- Trazabilidad;
- Stock;
- Calidad;
- Ordenes de Trabajo;
- Corte Teorico;
- Comercial.

### Pueden tener panel lateral opcional

- Inicio;
- Produccion;
- Reportes.

### Contenido del panel

Debe mostrar informacion contextual del elemento seleccionado:

- codigo;
- nombre;
- estado;
- fecha;
- litros/kilos/unidades;
- responsable;
- observaciones;
- links o acciones de navegacion.

## 10. Paginas con alertas

Deben tener alertas:

- Inicio;
- Stock;
- Calidad;
- Ordenes de Trabajo;
- Produccion.

Alertas sugeridas:

- stock bajo;
- pileta cerca de capacidad maxima;
- merma alta;
- analisis fuera de rango;
- OT pendiente o vencida;
- operacion anulada;
- lote sin trazabilidad esperada;
- datos incompletos.

## 11. Paginas ejecutivas y operativas

### Ejecutivas

- Inicio;
- Comercial;
- Reportes.

Orientacion: KPIs, tendencias, resumen, comparacion.

### Operativas

- Produccion;
- Stock;
- Trazabilidad;
- Calidad;
- Ordenes de Trabajo;
- Corte Teorico.

Orientacion: detalle, filtros especificos, tablas, panel lateral y acciones de analisis.

## 12. Reglas de consistencia visual

### Menu lateral

- Siempre fijo a la izquierda.
- Mismo orden de paginas.
- Item activo en borravino.
- Iconos consistentes.

### Header

- Titulo de pagina siempre visible.
- Subtitulo con contexto o periodo.
- En Inicio puede usar imagen; en paginas operativas debe ser mas sobrio.

### KPIs

- Mismo formato de tarjeta.
- Valor grande, unidad visible, comparacion secundaria.
- Colores de acento consistentes.

### Filtros

- Misma ubicacion bajo header.
- Globales primero, especificos despues.
- No mas de 8 visibles por pagina.

### Graficos

- Titulos claros.
- Colores de datos consistentes.
- Evitar visuales decorativos sin decision asociada.

### Tablas

- Encabezado marron madera.
- Filas alternas suaves.
- Numeros a la derecha.
- Codigos y nombres a la izquierda.

### Colores

- Crema para fondo.
- Blanco para tarjetas.
- Marron para estructura.
- Borravino para foco/interaccion.
- Dorado para acento.
- Colores de datos separados de colores de interfaz.

### Iconos

- Lineales, simples, de una familia visual.
- No mezclar estilos rellenos y lineales.
- No usar iconos multicolor salvo estados.

### Estados

- Correcto: verde oliva.
- Advertencia: ambar.
- Error: rojo vino.
- Pendiente: gris calido.
- Completado: verde suave.

## 13. Experiencia especifica de trazabilidad

### Grafo

Debe ser el centro de la pagina. Muestra nodos y conexiones:

- recepcion;
- lote;
- operacion;
- pileta;
- merma;
- fraccionamiento;
- producto terminado;
- venta granel.

El usuario debe poder entender de donde viene un lote, que operaciones lo afectaron, donde estuvo fisicamente y hacia donde fue.

### Timeline

Debe complementar al grafo con una secuencia cronologica:

- recepcion;
- nacimiento de lote;
- movimientos;
- mezclas/divisiones;
- mermas;
- fraccionamiento;
- venta.

La timeline ayuda cuando el grafo se vuelve complejo.

### Panel de detalle

Al seleccionar un nodo, el panel muestra:

- tipo de nodo;
- codigo;
- fecha;
- litros/kilos/unidades;
- variedad;
- pileta;
- responsable;
- estado;
- observaciones;
- relaciones entrantes y salientes.

### Filtros

- lote;
- cosecha;
- variedad;
- tipo de relacion;
- rango de fecha;
- mostrar/ocultar piletas;
- mostrar/ocultar operaciones;
- direccion: hacia atras o hacia adelante.

### Interaccion al seleccionar nodos

- Click en nodo: resalta nodo, conexiones directas y muestra panel.
- Doble click o drill-through: navega a pagina relacionada.
- Hover: tooltip tecnico corto.
- Seleccion de arista: muestra litros aportados, porcentaje si existe y operacion asociada.

## 14. Sensacion esperada del producto

El Centro de Control Vitivinicola Lanzarini debe sentirse:

- profesional, porque organiza informacion critica;
- elegante, porque representa una bodega real;
- claro, porque prioriza decisiones;
- tecnico, porque conserva trazabilidad y datos de proceso;
- confiable, porque distingue stock, calidad, operaciones y auditoria;
- propio, porque usa una identidad visual coherente con Lanzarini.

El resultado final debe parecer una herramienta de gestion diaria para una bodega, no un informe aislado creado solo para presentacion.
