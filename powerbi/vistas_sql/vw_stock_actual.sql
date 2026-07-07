CREATE SCHEMA IF NOT EXISTS powerbi;

CREATE OR REPLACE VIEW powerbi.vw_stock_actual AS
WITH movimientos_stock AS (
    SELECT
        mf.lote_id,
        mf.pileta_destino_id AS pileta_id,
        mf.litros AS litros
    FROM movimientos_fisicos mf
    JOIN operaciones_productivas op ON op.id = mf.operacion_productiva_id
    WHERE mf.pileta_destino_id IS NOT NULL
      AND op.anulada = FALSE

    UNION ALL

    SELECT
        mf.lote_id,
        mf.pileta_origen_id AS pileta_id,
        -mf.litros AS litros
    FROM movimientos_fisicos mf
    JOIN operaciones_productivas op ON op.id = mf.operacion_productiva_id
    WHERE mf.pileta_origen_id IS NOT NULL
      AND op.anulada = FALSE
),
stock AS (
    SELECT
        lote_id,
        pileta_id,
        SUM(litros) AS litros_stock
    FROM movimientos_stock
    GROUP BY lote_id, pileta_id
)
SELECT
    p.bodega_id,
    b.nombre AS bodega_nombre,
    l.id AS lote_id,
    l.codigo AS lote_codigo,
    l.cosecha,
    l.color,
    v.nombre AS variedad_nombre,
    el.nombre AS estado_lote,
    p.id AS pileta_id,
    p.codigo AS pileta_codigo,
    p.nombre AS pileta_nombre,
    ep.nombre AS estado_pileta,
    d.id AS deposito_id,
    d.nombre AS deposito_nombre,
    p.capacidad_litros,
    COALESCE(s.litros_stock, 0) AS litros_stock,
    CASE
        WHEN p.capacidad_litros > 0
            THEN ROUND((COALESCE(s.litros_stock, 0) / p.capacidad_litros) * 100, 2)
        ELSE NULL
    END AS porcentaje_ocupacion
FROM stock s
JOIN lotes l ON l.id = s.lote_id
JOIN piletas p ON p.id = s.pileta_id
JOIN bodegas b ON b.id = p.bodega_id
JOIN depositos d ON d.id = p.deposito_id
JOIN estados_pileta ep ON ep.id = p.estado_pileta_id
JOIN estados_lote el ON el.id = l.estado_lote_id
LEFT JOIN variedades v ON v.id = l.variedad_principal_id
WHERE COALESCE(s.litros_stock, 0) <> 0;
