# Design System Lanzarini para Power BI

## Objetivo visual

El dashboard debe sentirse como un sistema profesional de gestion para bodega: sobrio, elegante, claro y operativo. La estetica debe recordar madera, cava, vino y mesa de degustacion, sin perder legibilidad ni velocidad de lectura.

## Personalidad de marca

- Profesional: informacion precisa, jerarquia clara y sin ruido visual.
- Vitivinicola: colores asociados a madera, vino, dorado envejecido y crema.
- Moderna: tarjetas limpias, espacios consistentes, navegacion estable.
- Confiable: foco en trazabilidad, stock y procesos, evitando decoracion excesiva.

## Principios visuales

1. La informacion operativa manda sobre la decoracion.
2. Los colores de interfaz no deben competir con los colores de datos.
3. Cada pagina debe poder leerse de izquierda a derecha y de arriba hacia abajo.
4. Las tarjetas KPI deben ser escaneables en menos de cinco segundos.
5. Las fotografias reales se usan como ambientacion controlada, no como fondo dominante de tablas o graficos.

## Paleta oficial

### Interfaz

- Marron madera: `#2B1E1A`
- Borravino principal: `#3E244A`
- Dorado envejecido: `#B88646`
- Crema fondo: `#F8F5EF`
- Blanco tarjeta: `#FFFFFF`
- Texto principal: `#2D2D2D`
- Texto secundario: `#6B625C`

### Datos

- Tintos: `#6B1F2A`, `#7A263A`, `#4E1A24`
- Blancos: `#D8B75A`, `#E8DCA2`, `#B9A44C`
- Rosados: `#C97B84`, `#D9A0A7`
- Neutros: `#8C7B6B`, `#A89F91`

## Uso correcto de colores

- Usar crema como fondo general.
- Usar blanco para tarjetas, tablas y contenedores principales.
- Usar marron madera para menu lateral, titulos fuertes y headers.
- Usar borravino para seleccion activa, botones primarios y acentos puntuales.
- Usar dorado para resaltar KPIs, lineas divisorias finas y estados destacados.
- Evitar paginas dominadas por borravino: debe ser acento, no fondo principal.

## Interfaz vs datos

Los colores de interfaz ordenan la experiencia. Los colores de datos explican categorias del negocio. Para evitar confusion:

- No usar `#3E244A` para variedades si tambien identifica navegacion activa.
- Reservar tintos, blancos y rosados para grupos de vino o variedades.
- Reservar dorado para acentos de interfaz o valores clave, no para grandes series comparativas.
- Usar neutros para categorias secundarias, pendientes o sin clasificar.

## Tipografias sugeridas

Power BI no permite todas las familias en todos los entornos. Prioridad sugerida:

1. Segoe UI
2. Aptos
3. Arial

Usar una sola familia tipografica en todo el reporte. La sofisticacion debe venir de jerarquia, color y espaciado, no de mezclar fuentes.

## Jerarquia visual

- Titulo de pagina: 24-30 px, marron madera, peso semibold.
- Subtitulo o periodo activo: 11-13 px, texto secundario.
- KPI principal: 28-36 px, marron madera o borravino.
- Etiqueta KPI: 10-12 px, texto secundario.
- Titulos de visuales: 12-14 px, marron madera.
- Tablas: 10-11 px, texto principal.

## Espaciado

- Margen exterior de pagina: 20-24 px.
- Separacion entre tarjetas: 12-16 px.
- Padding interno de tarjetas: 12-16 px.
- Separacion entre titulo y visual: 8 px.
- Mantener alineaciones por grilla; evitar visuales flotando sin eje comun.

## Bordes

- Radio recomendado en tarjetas: 8 px.
- Radio maximo: 12 px solo en tarjetas KPI o panel lateral.
- Bordes de tarjetas: `#E8E0D6` con 1 px o sin borde si hay sombra sutil.
- Evitar bordes gruesos y contornos negros.

## Sombras

Usar sombras muy suaves:

- Tarjetas: sombra gris calida con baja opacidad.
- Panel lateral: sombra un poco mayor para indicar superposicion.
- No usar sombras fuertes tipo boton web antiguo.

## Iconografia

- Estilo lineal, simple y consistente.
- Usar iconos solo para reforzar significado: stock, lote, venta, calidad, alerta, tareas.
- Color principal: texto secundario o dorado.
- Iconos activos: borravino.
- Evitar iconos multicolor salvo excepciones de estado.

## Filtros

- Ubicacion preferida: barra superior bajo header o panel lateral fijo.
- Fondo blanco, borde sutil, texto secundario.
- Filtros clave: fecha, bodega, lote, pileta, variedad, cosecha.
- No saturar cada pagina con todos los filtros posibles.

## Navegacion

- Menu lateral fijo en marron madera.
- Item activo con fondo borravino y acento dorado.
- Items inactivos en crema claro o gris calido.
- Mantener el mismo orden de paginas en todo el reporte.

## Tablas

- Fondo blanco.
- Encabezado marron madera con texto claro o crema.
- Filas alternas muy suaves.
- Numeros alineados a la derecha.
- Codigos y nombres alineados a la izquierda.
- Evitar grillas pesadas.

## Tooltips

- Fondo blanco o crema.
- Titulo corto en marron madera.
- Datos clave en formato lista.
- Incluir contexto: lote, pileta, fecha, litros, responsable.
- Evitar tooltips con demasiadas columnas.

## Estilo de paginas

- Cada pagina debe tener: header, filtros, KPIs principales, visual central y detalle.
- Las paginas operativas deben priorizar tablas y matrices.
- Las paginas ejecutivas deben priorizar KPIs y tendencias.
- La pagina de trazabilidad puede usar un area visual mas amplia para el grafo.
