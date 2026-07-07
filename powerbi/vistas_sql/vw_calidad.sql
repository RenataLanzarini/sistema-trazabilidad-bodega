CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_calidad AS
SELECT
    'analisis_enologico' AS tipo_registro,
    ae.id AS registro_id,
    ae.bodega_id,
    b.nombre AS bodega_nombre,
    ae.lote_id,
    l.codigo AS lote_codigo,
    ae.pileta_id,
    p.codigo AS pileta_codigo,
    ae.codigo_externo,
    ae.fecha,
    ae.tipo,
    ae.alcohol,
    ae.azucar,
    ae.volatil,
    ae.acidez_total,
    ae.ph,
    ae.anhidrido_libre,
    ae.anhidrido_total,
    ae.extracto_seco,
    ae.brix,
    NULL::numeric AS grado_baume,
    NULL::numeric AS temperatura,
    ae.observaciones
FROM analisis_enologicos ae
JOIN bodegas b ON b.id = ae.bodega_id
LEFT JOIN lotes l ON l.id = ae.lote_id
LEFT JOIN piletas p ON p.id = ae.pileta_id

UNION ALL

SELECT
    'medicion_fermentacion' AS tipo_registro,
    mf.id AS registro_id,
    mf.bodega_id,
    b.nombre AS bodega_nombre,
    mf.lote_id,
    l.codigo AS lote_codigo,
    mf.pileta_id,
    p.codigo AS pileta_codigo,
    mf.codigo_externo,
    mf.fecha,
    mf.turno AS tipo,
    NULL::numeric AS alcohol,
    NULL::numeric AS azucar,
    NULL::numeric AS volatil,
    NULL::numeric AS acidez_total,
    NULL::numeric AS ph,
    NULL::numeric AS anhidrido_libre,
    NULL::numeric AS anhidrido_total,
    NULL::numeric AS extracto_seco,
    NULL::numeric AS brix,
    mf.grado_baume,
    mf.temperatura,
    NULL::text AS observaciones
FROM mediciones_fermentacion mf
JOIN bodegas b ON b.id = mf.bodega_id
LEFT JOIN lotes l ON l.id = mf.lote_id
LEFT JOIN piletas p ON p.id = mf.pileta_id;
