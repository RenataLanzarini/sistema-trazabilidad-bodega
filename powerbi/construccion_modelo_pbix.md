# Construccion del Modelo PBIX

Esta guia documenta como construir el modelo semantico dentro de Power BI Desktop para el **Centro de Control Vitivinicola Lanzarini**. El objetivo es preparar un `.pbix` limpio, estable y listo para construir las paginas del dashboard.

## 1. Crear el archivo PBIX

### Nombre sugerido

`Centro_Control_Vitivinicola_Lanzarini.pbix`

### Configuracion regional

- Idioma del archivo: espanol.
- Configuracion regional: Argentina.
- Separador decimal: coma.
- Separador de miles: punto.
- Formatos recomendados:
  - fechas: `dd/mm/yyyy`;
  - fecha y hora: `dd/mm/yyyy hh:mm`;
  - litros: `#,0.00 L`;
  - kilos: `#,0.00 kg`;
  - porcentajes: `0.00%`.

### Configuracion de actualizacion

- Modo inicial: Import.
- Actualizacion manual durante desarrollo.
- Al publicar, configurar actualizacion programada segun uso real.
- Recomendacion MVP: una actualizacion diaria o bajo demanda.

### Ubicacion del archivo

Guardar el `.pbix` fuera del backend operativo, por ejemplo:

`powerbi/pbix/Centro_Control_Vitivinicola_Lanzarini.pbix`

Si se versiona el `.pbix`, hacerlo con cuidado porque es binario y puede crecer rapidamente.

## 2. Conexion a PostgreSQL

### Servidor

Usar el host donde corre PostgreSQL. En desarrollo puede ser:

- `localhost`
- `127.0.0.1`
- nombre del servicio Docker si Power BI accede desde otro contenedor o red.

### Base

Usar la base de datos del sistema de trazabilidad. Debe estar migrada y con las vistas del schema `powerbi` creadas.

### Autenticacion

- Usuario de solo lectura recomendado para Power BI.
- Evitar usar credenciales administradoras.
- Guardar credenciales en Power BI Desktop solo si el equipo de trabajo lo permite.

### Recomendaciones

- Conectar a las vistas del schema `powerbi`.
- No conectar directamente a tablas transaccionales si existe una vista analitica equivalente.
- Probar la conexion antes de cargar todo el modelo.
- Confirmar que el usuario tenga permisos `SELECT` sobre las vistas.

### Modo Import

Usar **Import** para este proyecto porque:

- mejora performance visual;
- simplifica relaciones;
- reduce dependencia de la base en tiempo real;
- el volumen esperado del MVP es manejable;
- permite medidas DAX mas fluidas.

### DirectQuery

No se recomienda para el MVP. Solo evaluarlo si:

- el volumen historico crece mucho;
- se necesita informacion casi en tiempo real;
- las vistas estan optimizadas;
- PostgreSQL cuenta con indices, recursos y monitoreo adecuados.

DirectQuery agrega complejidad de performance, relaciones y experiencia de usuario. Para una bodega pequena, Import es la opcion mas robusta.

## 3. Importacion

### Orden de importacion

1. Calendario.
2. `vw_stock_actual`.
3. `vw_produccion`.
4. `vw_movimientos`.
5. `vw_trazabilidad`.
6. `vw_calidad`.
7. `vw_comercial`.
8. `vw_ordenes_trabajo`.
9. `vw_cortes_teoricos`.

### Por que este orden

- Calendario debe estar primero para ordenar la estructura temporal.
- Stock y produccion forman la base ejecutiva.
- Movimientos y trazabilidad explican el origen de stock.
- Calidad y comercial agregan dimensiones funcionales.
- Ordenes y cortes completan la capa operativa y de simulacion.

## 4. Tipos de datos

## `vw_stock_actual`

- Fechas: no expone fecha.
- Texto: `bodega_nombre`, `lote_codigo`, `color`, `variedad_nombre`, `estado_lote`, `pileta_codigo`, `pileta_nombre`, `estado_pileta`, `deposito_nombre`.
- Numericas: `bodega_id`, `lote_id`, `cosecha`, `pileta_id`, `deposito_id`.
- Litros: `capacidad_litros`, `litros_stock`.
- Porcentajes: `porcentaje_ocupacion`.
- Conversiones: asegurar `porcentaje_ocupacion` como decimal o porcentaje segun visual. Si viene como 65.5, dividir por 100 para formato porcentaje.

## `vw_produccion`

- Fechas: `fecha_recepcion`, `fecha_lote`.
- Texto: CIU, finca, inv, cambio, cuartel, chofer, cuit/cuil, camion, modelo, patente, destino, vasija, estados, origen, variedad, responsable, lote, tipo producto, calificacion.
- Numericas: IDs, `cosecha`, `semana`, `tachos`.
- Kilos: `kilos_recibidos`, `bruto_kg`, `tara_kg`, `neto_kg`, `uva_real_kg`.
- Indicadores: `rto`, `brix_real`, `tenor_azucar`.
- Conversiones: revisar que campos decimales no entren como texto por configuracion regional.

## `vw_movimientos`

- Fechas: `fecha_operacion`, `fecha_movimiento`.
- Texto: codigos externos, estados, motivo anulacion, tipo operacion, lote, variedad, piletas, responsable, observaciones.
- Numericas: IDs.
- Litros: `litros`.
- Booleanos: `operacion_anulada`.
- Conversiones: confirmar booleano y fecha/hora.

## `vw_trazabilidad`

- Fechas: `fecha_operacion`.
- Texto: bodega, tipo operacion, tipo relacion, codigos, variedades, estados, observaciones.
- Numericas: IDs, cosechas.
- Litros: `litros_aportados`.
- Conversiones: ninguna especial salvo litros decimal.

## `vw_calidad`

- Fechas: `fecha`.
- Texto: `tipo_registro`, bodega, lote, pileta, codigo externo, tipo, observaciones.
- Numericas: IDs.
- Indicadores: `alcohol`, `azucar`, `volatil`, `acidez_total`, `ph`, `anhidrido_libre`, `anhidrido_total`, `extracto_seco`, `brix`, `grado_baume`, `temperatura`.
- Conversiones: todos los indicadores deben ser decimales.

## `vw_comercial`

- Fechas: `fecha_venta`.
- Texto: bodega, documento, estado, cliente, responsable, lote, pileta, observaciones.
- Numericas: IDs.
- Litros: `litros`.
- Conversiones: confirmar fecha/hora y litros decimal.

## `vw_ordenes_trabajo`

- Fechas: `fecha`, `fecha_completada`.
- Texto: codigo externo, numero, estado operativo, tarea, operario, lote, piletas, variedad, insumo, observaciones.
- Numericas: IDs, `anio`.
- Litros/volumen: `volumen_lleno`, `litros_a_trasegar`, `lleno_disponible`, `litros_por_cm`.
- Otros: `cantidad`, `so2l_real`.
- Booleanos: `completada`, `pasada_a_trazabilidad`.
- Conversiones: revisar booleanos y fecha de completado.

## `vw_cortes_teoricos`

- Fechas: `fecha`, `fecha_operacion_vinculada`.
- Texto: codigos, nombre de corte, responsable, lote, pileta, varietal snapshot, observaciones.
- Numericas: IDs.
- Volumen: `volumen_al_corte`, `volumen_actual_snapshot`.
- Indicadores: `alcohol`, `acidez_volatil`, `acidez_total`, `ph`, `so2_libre`, `so2_total`.
- Conversiones: revisar decimales.

## 5. Relaciones

### Reglas generales

- Preferir relaciones uno-a-muchos desde dimensiones hacia vistas.
- Direccion de filtro recomendada: simple, desde dimension hacia hechos.
- Evitar muchos-a-muchos salvo necesidad justificada.
- Mantener relaciones inactivas cuando existan roles multiples: fechas alternativas, pileta origen/destino, lote padre/hijo.

### Tabla resumen de relaciones sugeridas

| Tabla origen | Campo origen | Tabla destino | Campo destino | Tipo |
|---|---|---|---|---|
| DimFecha | Fecha | vw_produccion | fecha_recepcion | 1:* activa |
| DimFecha | Fecha | vw_produccion | fecha_lote | 1:* inactiva |
| DimFecha | Fecha | vw_movimientos | fecha_movimiento | 1:* activa |
| DimFecha | Fecha | vw_movimientos | fecha_operacion | 1:* inactiva |
| DimFecha | Fecha | vw_calidad | fecha | 1:* activa |
| DimFecha | Fecha | vw_comercial | fecha_venta | 1:* activa |
| DimFecha | Fecha | vw_ordenes_trabajo | fecha | 1:* activa |
| DimFecha | Fecha | vw_ordenes_trabajo | fecha_completada | 1:* inactiva |
| DimFecha | Fecha | vw_cortes_teoricos | fecha | 1:* activa |
| DimBodega | bodega_id | vw_stock_actual | bodega_id | 1:* |
| DimBodega | bodega_id | vw_produccion | bodega_id | 1:* |
| DimBodega | bodega_id | vw_movimientos | bodega_id | 1:* |
| DimBodega | bodega_id | vw_trazabilidad | bodega_id | 1:* |
| DimBodega | bodega_id | vw_calidad | bodega_id | 1:* |
| DimBodega | bodega_id | vw_comercial | bodega_id | 1:* |
| DimLote | lote_id | vw_stock_actual | lote_id | 1:* |
| DimLote | lote_id | vw_produccion | lote_id | 1:* |
| DimLote | lote_id | vw_movimientos | lote_id | 1:* |
| DimLote | lote_id | vw_calidad | lote_id | 1:* |
| DimLote | lote_id | vw_comercial | lote_id | 1:* |
| DimLote | lote_id | vw_cortes_teoricos | lote_id | 1:* |
| DimLote | lote_id | vw_trazabilidad | lote_hijo_id | 1:* activa |
| DimLote | lote_id | vw_trazabilidad | lote_padre_id | 1:* inactiva |
| DimPileta | pileta_id | vw_stock_actual | pileta_id | 1:* |
| DimPileta | pileta_id | vw_calidad | pileta_id | 1:* |
| DimPileta | pileta_id | vw_comercial | pileta_id | 1:* |
| DimPileta | pileta_id | vw_ordenes_trabajo | pileta_id | 1:* activa |
| DimPileta | pileta_id | vw_movimientos | pileta_destino_id | 1:* activa |
| DimPileta | pileta_id | vw_movimientos | pileta_origen_id | 1:* inactiva |
| DimCliente | cliente_id | vw_comercial | cliente_id | 1:* |
| DimUsuario | usuario_id | vw_movimientos | responsable_id | 1:* |
| DimUsuario | usuario_id | vw_comercial | responsable_id | 1:* |
| DimUsuario | usuario_id | vw_ordenes_trabajo | operario_id | 1:* |
| DimUsuario | usuario_id | vw_cortes_teoricos | responsable_id | 1:* |
| DimTipoOperacion | tipo_operacion_id | vw_movimientos | tipo_operacion_id | 1:* |

### Dimensiones

Si no se crean vistas `dim_*` en PostgreSQL, pueden derivarse en Power Query desde las vistas cargadas, quitando duplicados. Para MVP es aceptable, aunque a futuro conviene publicar dimensiones SQL.

## 6. Calendario

### Tabla calendario

Crear `DimFecha` en Power BI con DAX o Power Query. Debe incluir:

- Fecha.
- Anio.
- MesNumero.
- MesNombre.
- AnioMes.
- Trimestre.
- Semana.
- Dia.
- DiaSemana.
- InicioMes.
- FinMes.

### Relaciones con fechas

Usar una relacion activa por vista y relaciones inactivas para fechas alternativas.

### Inteligencia temporal

Crear medidas para:

- acumulado anual;
- comparacion periodo anterior;
- variacion mensual;
- promedio movil si se necesita para calidad.

Marcar `DimFecha` como tabla de fechas en Power BI.

## 7. Medidas

### Crear primero

1. Litros Stock Actual.
2. Capacidad Total.
3. Capacidad Ocupada %.
4. Kg Uva Recibida.
5. Litros Movidos.
6. Litros Vendidos.
7. Litros Merma.
8. % Merma.
9. Ordenes Pendientes.
10. Ordenes Completadas.
11. Promedio Brix.
12. Promedio Alcohol.
13. Promedio pH.
14. Promedio Baume.
15. Temperatura Promedio.

### Medidas por pagina

| Pagina | Medidas |
|---|---|
| Dashboard Ejecutivo | stock, kg uva, litros vendidos, % merma, ordenes, calidad |
| Produccion | kg uva, Brix, lotes, movimientos |
| Stock | stock, capacidad, ocupacion |
| Trazabilidad | litros aportados, movimientos, relaciones |
| Calidad | Brix, alcohol, pH, Baume, temperatura |
| Comercial | litros vendidos, ventas, clientes |
| Ordenes | pendientes, completadas, cumplimiento |
| Corte Teorico | volumen al corte, componentes, snapshots |
| Reportes | medidas generales y conteos |

## 8. Carpetas de medidas

Crear una tabla dedicada llamada `Medidas` y organizar las medidas en carpetas:

- Stock
- Produccion
- Calidad
- Comercial
- KPIs
- Trazabilidad
- Ordenes
- Generales

### Reglas

- Una medida puede estar en la carpeta de su dominio o en `KPIs` si se usa en tarjetas ejecutivas.
- Medidas tecnicas auxiliares pueden ir en `Generales`.
- Mantener nombres claros y sin abreviaturas oscuras.

## 9. Ocultar columnas

### IDs y FKs

Ocultar al usuario final:

- `bodega_id`
- `lote_id`
- `pileta_id`
- `deposito_id`
- `responsable_id`
- `operario_id`
- `cliente_id`
- `tipo_operacion_id`
- `operacion_productiva_id`
- `recepcion_uva_id`
- `venta_granel_id`
- `venta_granel_detalle_id`
- `relacion_genealogica_id`
- `corte_teorico_id`
- `corte_teorico_detalle_id`

Mantener visibles solo si se usan en tablas tecnicas de auditoria.

### Campos auxiliares

Ocultar si no se usan:

- codigos externos tecnicos;
- flags auxiliares;
- columnas de observaciones largas;
- motivos de anulacion fuera de auditoria;
- campos de transporte de CIU si la pagina no los usa.

### Observaciones tecnicas

Mantener disponibles para tooltips o reportes, pero ocultas en vistas ejecutivas.

## 10. Validacion

Checklist del modelo:

- [ ] Todas las vistas cargan.
- [ ] Relaciones sin errores.
- [ ] No hay muchos-a-muchos inesperadas.
- [ ] Fechas correctas.
- [ ] Tipos correctos.
- [ ] Modelo limpio.
- [ ] Sin columnas innecesarias visibles.
- [ ] Theme aplicado.
- [ ] Medidas principales calculan.
- [ ] Totales validados contra PostgreSQL.
- [ ] Filtros no generan resultados inconsistentes.
- [ ] Relaciones inactivas documentadas.

## 11. Buenas practicas

### Nombres de medidas

- Usar nombres de negocio: `Litros Stock Actual`, no `sum_litros`.
- Mantener unidades en el nombre cuando ayude.
- No usar prefijos tecnicos innecesarios.

### Carpetas

- Todas las medidas deben estar en una carpeta.
- Evitar medidas sueltas en tablas de hechos.

### Formato

- Litros: decimal con unidad `L`.
- Kilos: decimal con unidad `kg`.
- Porcentajes: `0.00%`.
- Conteos: entero.
- Fechas: `dd/mm/yyyy`.

### Performance

- Evitar columnas calculadas si puede resolverse con medidas.
- Ocultar columnas no usadas.
- Reducir cardinalidad de columnas de texto largas.
- Usar dimensiones para filtros frecuentes.
- No abusar de relaciones bidireccionales.

### Actualizacion

- Probar refresco manual.
- Revisar credenciales.
- Validar tiempo de actualizacion.
- Documentar fecha/hora de ultima actualizacion en el reporte.

## 12. Entregables

Al finalizar la construccion del modelo PBIX deberian quedar:

- Archivo `.pbix` creado y guardado.
- Conexion a PostgreSQL configurada.
- Vistas cargadas.
- Calendario creado.
- Relaciones creadas y revisadas.
- Medidas base cargadas.
- Carpetas de medidas organizadas.
- Columnas tecnicas ocultas.
- Theme Lanzarini aplicado.
- Checklist de validacion completado.
