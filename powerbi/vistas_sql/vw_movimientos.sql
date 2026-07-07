CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_movimientos AS
SELECT
    op.bodega_id,
    b.nombre AS bodega_nombre,
    op.id AS operacion_productiva_id,
    op.codigo_externo AS operacion_codigo_externo,
    op.fecha AS fecha_operacion,
    op.estado AS estado_operacion,
    op.anulada AS operacion_anulada,
    op.motivo_anulacion,
    top.id AS tipo_operacion_id,
    top.nombre AS tipo_operacion,
    mf.id AS movimiento_fisico_id,
    mf.codigo_externo AS movimiento_codigo_externo,
    mf.fecha AS fecha_movimiento,
    mf.litros,
    mf.estado AS estado_movimiento,
    l.id AS lote_id,
    l.codigo AS lote_codigo,
    l.cosecha,
    vo.nombre AS variedad_nombre,
    po.id AS pileta_origen_id,
    po.codigo AS pileta_origen_codigo,
    po.nombre AS pileta_origen_nombre,
    pd.id AS pileta_destino_id,
    pd.codigo AS pileta_destino_codigo,
    pd.nombre AS pileta_destino_nombre,
    u.id AS responsable_id,
    u.nombre AS responsable_nombre,
    mf.observaciones
FROM movimientos_fisicos mf
JOIN operaciones_productivas op ON op.id = mf.operacion_productiva_id
JOIN bodegas b ON b.id = op.bodega_id
JOIN tipos_operacion top ON top.id = op.tipo_operacion_id
JOIN lotes l ON l.id = mf.lote_id
LEFT JOIN variedades vo ON vo.id = l.variedad_principal_id
LEFT JOIN piletas po ON po.id = mf.pileta_origen_id
LEFT JOIN piletas pd ON pd.id = mf.pileta_destino_id
JOIN usuarios u ON u.id = mf.responsable_id;
