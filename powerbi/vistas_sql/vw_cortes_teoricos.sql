CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_cortes_teoricos AS
SELECT
    ct.id AS corte_teorico_id,
    ct.codigo_externo AS corte_codigo_externo,
    ct.fecha,
    ct.nombre AS corte_nombre,
    ct.responsable_id,
    u.nombre AS responsable_nombre,
    ct.operacion_productiva_id,
    op.fecha AS fecha_operacion_vinculada,
    ctd.id AS corte_teorico_detalle_id,
    ctd.codigo_externo AS detalle_codigo_externo,
    ctd.lote_id,
    l.codigo AS lote_codigo,
    ctd.pileta_id,
    p.codigo AS pileta_codigo,
    p.nombre AS pileta_nombre,
    ctd.volumen_al_corte,
    ctd.varietal_snapshot,
    ctd.volumen_actual_snapshot,
    ctd.alcohol,
    ctd.acidez_volatil,
    ctd.acidez_total,
    ctd.ph,
    ctd.so2_libre,
    ctd.so2_total,
    ct.observaciones
FROM cortes_teoricos ct
LEFT JOIN usuarios u ON u.id = ct.responsable_id
LEFT JOIN operaciones_productivas op ON op.id = ct.operacion_productiva_id
LEFT JOIN corte_teorico_detalles ctd ON ctd.corte_teorico_id = ct.id
LEFT JOIN lotes l ON l.id = ctd.lote_id
LEFT JOIN piletas p ON p.id = ctd.pileta_id;
