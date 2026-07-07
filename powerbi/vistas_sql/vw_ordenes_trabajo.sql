CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_ordenes_trabajo AS
SELECT
    ot.id AS orden_trabajo_id,
    ot.codigo_externo,
    ot.numero,
    ot.fecha,
    ot.completada,
    CASE WHEN COALESCE(ot.completada, FALSE) THEN 'Completada' ELSE 'Pendiente' END AS estado_operativo,
    ot.fecha_completada,
    tot.id AS tarea_orden_trabajo_id,
    tot.nombre AS tarea_nombre,
    u.id AS operario_id,
    u.nombre AS operario_nombre,
    l.id AS lote_id,
    l.codigo AS lote_codigo,
    p.id AS pileta_id,
    p.codigo AS pileta_codigo,
    po.id AS pileta_origen_id,
    po.codigo AS pileta_origen_codigo,
    pd.id AS pileta_destino_id,
    pd.codigo AS pileta_destino_codigo,
    ot.operacion_productiva_id,
    ot.volumen_lleno,
    ot.variedad,
    ot.anio,
    ot.insumo,
    ot.cantidad,
    ot.litros_a_trasegar,
    ot.lleno_disponible,
    ot.litros_por_cm,
    ot.pasada_a_trazabilidad,
    ot.so2l_real,
    ot.observaciones,
    ot.observaciones_completada
FROM ordenes_trabajo ot
LEFT JOIN tareas_orden_trabajo tot ON tot.id = ot.tarea_orden_trabajo_id
LEFT JOIN usuarios u ON u.id = ot.operario_id
LEFT JOIN lotes l ON l.id = ot.lote_id
LEFT JOIN piletas p ON p.id = ot.pileta_id
LEFT JOIN piletas po ON po.id = ot.pileta_origen_id
LEFT JOIN piletas pd ON pd.id = ot.pileta_destino_id;
