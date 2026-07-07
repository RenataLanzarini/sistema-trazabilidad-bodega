CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_trazabilidad AS
SELECT
    rgl.id AS relacion_genealogica_id,
    op.bodega_id,
    b.nombre AS bodega_nombre,
    rgl.operacion_productiva_id,
    op.fecha AS fecha_operacion,
    top.nombre AS tipo_operacion,
    rgl.tipo_relacion,
    rgl.litros_aportados,
    lp.id AS lote_padre_id,
    lp.codigo AS lote_padre_codigo,
    lp.cosecha AS lote_padre_cosecha,
    vp.nombre AS lote_padre_variedad,
    elp.nombre AS lote_padre_estado,
    lh.id AS lote_hijo_id,
    lh.codigo AS lote_hijo_codigo,
    lh.cosecha AS lote_hijo_cosecha,
    vh.nombre AS lote_hijo_variedad,
    elh.nombre AS lote_hijo_estado,
    rgl.observaciones
FROM relaciones_genealogicas_lote rgl
JOIN operaciones_productivas op ON op.id = rgl.operacion_productiva_id
JOIN bodegas b ON b.id = op.bodega_id
JOIN tipos_operacion top ON top.id = op.tipo_operacion_id
JOIN lotes lp ON lp.id = rgl.lote_padre_id
JOIN lotes lh ON lh.id = rgl.lote_hijo_id
LEFT JOIN variedades vp ON vp.id = lp.variedad_principal_id
LEFT JOIN variedades vh ON vh.id = lh.variedad_principal_id
LEFT JOIN estados_lote elp ON elp.id = lp.estado_lote_id
LEFT JOIN estados_lote elh ON elh.id = lh.estado_lote_id;
