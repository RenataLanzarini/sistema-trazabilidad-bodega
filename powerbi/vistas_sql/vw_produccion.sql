CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_produccion AS
SELECT
    ru.bodega_id,
    b.nombre AS bodega_nombre,
    ru.id AS recepcion_uva_id,
    ru.numero_ciu,
    ru.fecha AS fecha_recepcion,
    ru.cosecha,
    ru.kilos_recibidos,
    ru.semana,
    ru.rto,
    ru.finca,
    ru.inv,
    ru.cambio,
    ru.cuartel,
    ru.tachos,
    ru.chofer,
    ru.cuit_cuil,
    ru.camion,
    ru.modelo,
    ru.patente,
    ru.bruto_kg,
    ru.tara_kg,
    ru.neto_kg,
    ru.uva_real_kg,
    ru.destino_vino,
    ru.brix_real,
    ru.tenor_azucar,
    ru.vasija,
    ru.estado AS estado_recepcion,
    ou.id AS origen_uva_id,
    ou.nombre AS origen_uva_nombre,
    ou.tipo AS origen_uva_tipo,
    v.id AS variedad_id,
    v.nombre AS variedad_nombre,
    u.id AS responsable_id,
    u.nombre AS responsable_nombre,
    l.id AS lote_id,
    l.codigo AS lote_codigo,
    l.fecha_nacimiento AS fecha_lote,
    l.color AS lote_color,
    el.nombre AS estado_lote,
    tp.nombre AS tipo_producto,
    cv.nombre AS calificacion_vino
FROM recepciones_uva ru
JOIN bodegas b ON b.id = ru.bodega_id
JOIN origenes_uva ou ON ou.id = ru.origen_uva_id
JOIN variedades v ON v.id = ru.variedad_id
JOIN usuarios u ON u.id = ru.responsable_id
LEFT JOIN lotes l ON l.recepcion_uva_id = ru.id
LEFT JOIN estados_lote el ON el.id = l.estado_lote_id
LEFT JOIN tipos_producto tp ON tp.id = l.tipo_producto_id
LEFT JOIN calificaciones_vino cv ON cv.id = l.calificacion_vino_id;
