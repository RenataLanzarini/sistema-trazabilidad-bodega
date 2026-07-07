# Power BI - Sistema de Trazabilidad de Bodega

Esta carpeta contiene la preparacion inicial del modelo analitico para Power BI. La fuente oficial es PostgreSQL, usando el modelo normalizado del sistema. El Excel original queda como referencia funcional, no como fuente de datos para reportes productivos.

## Conexion recomendada

1. Abrir Power BI Desktop.
2. Seleccionar **Obtener datos > PostgreSQL database**.
3. Informar servidor, base de datos y credenciales de solo lectura.
4. Preferir **Import** para el MVP. Evaluar **DirectQuery** solo si el volumen crece y las vistas estan optimizadas.
5. Cargar vistas del schema `powerbi`.

## Vistas iniciales

- `powerbi.vw_stock_actual`
- `powerbi.vw_produccion`
- `powerbi.vw_movimientos`
- `powerbi.vw_trazabilidad`
- `powerbi.vw_calidad`
- `powerbi.vw_comercial`
- `powerbi.vw_ordenes_trabajo`
- `powerbi.vw_cortes_teoricos`

## Orden sugerido de carga

1. Crear o cargar tabla calendario.
2. Cargar dimensiones maestras si se decide exponerlas directamente: bodegas, piletas, lotes, variedades, usuarios, clientes.
3. Cargar vistas de hechos: stock, produccion, movimientos, calidad, comercial, ordenes y cortes.
4. Definir relaciones con la tabla calendario y dimensiones.
5. Crear medidas DAX base.

## Advertencia

No consumir directamente tablas transaccionales cuando exista una vista analitica equivalente. Las vistas encapsulan reglas de lectura, nombres amigables y criterios de consistencia para reporting.
