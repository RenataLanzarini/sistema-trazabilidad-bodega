CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_comercial AS
SELECT
    op.bodega_id,
    b.nombre AS bodega_nombre,
    vg.id AS venta_granel_id,
    vg.operacion_productiva_id,
    vg.fecha AS fecha_venta,
    vg.documento,
    vg.estado AS estado_venta,
    c.id AS cliente_id,
    c.nombre AS cliente_nombre,
    u.id AS responsable_id,
    u.nombre AS responsable_nombre,
    vgd.id AS venta_granel_detalle_id,
    vgd.litros,
    l.id AS lote_id,
    l.codigo AS lote_codigo,
    p.id AS pileta_id,
    p.codigo AS pileta_codigo,
    p.nombre AS pileta_nombre,
    vg.observaciones AS venta_observaciones,
    vgd.observaciones AS detalle_observaciones
FROM ventas_granel vg
JOIN operaciones_productivas op ON op.id = vg.operacion_productiva_id
JOIN bodegas b ON b.id = op.bodega_id
JOIN clientes c ON c.id = vg.cliente_id
JOIN usuarios u ON u.id = vg.responsable_id
JOIN venta_granel_detalles vgd ON vgd.venta_granel_id = vg.id
JOIN lotes l ON l.id = vgd.lote_id
JOIN piletas p ON p.id = vgd.pileta_id;
