-- Equivalente PostgreSQL para Etapa 3 (migracion idempotente y actualizacion atomica)
CREATE TABLE IF NOT EXISTS productos (
    id BIGSERIAL PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0)
);

CREATE TABLE IF NOT EXISTS movimientos (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES productos(id),
    delta INTEGER NOT NULL,
    clave_operacion TEXT NOT NULL UNIQUE,
    payload_hash TEXT NOT NULL,
    cantidad_resultante INTEGER NOT NULL CHECK (cantidad_resultante >= 0),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_movimientos_producto ON movimientos(producto_id);

-- Contrato de salida atomica sin condiciones de carrera:
-- UPDATE productos SET cantidad = cantidad - $1 WHERE id = $2 AND cantidad >= $1 RETURNING cantidad;
