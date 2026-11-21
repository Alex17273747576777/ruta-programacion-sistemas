"""Etapa 3 · Inventario transaccional con concurrencia e idempotencia (SQLite + contrato SQL)."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path


class ErrorInventario(RuntimeError):
    """Error de negocio o conflicto de idempotencia."""


class StockInsuficiente(ErrorInventario):
    """La salida supera la cantidad disponible."""


class ConflictoIdempotencia(ErrorInventario):
    """La misma clave de operación fue reutilizada con parámetros distintos."""


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    owner TEXT NOT NULL DEFAULT 'public',
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0)
);

CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL REFERENCES productos(id),
    delta INTEGER NOT NULL,
    clave_operacion TEXT NOT NULL UNIQUE,
    payload_hash TEXT NOT NULL,
    cantidad_resultante INTEGER NOT NULL CHECK (cantidad_resultante >= 0)
);

CREATE INDEX IF NOT EXISTS idx_movimientos_producto ON movimientos(producto_id);
"""


@dataclass(frozen=True)
class ResultadoMovimiento:
    producto_id: int
    cantidad: int
    clave_operacion: str
    reutilizado: bool


class InventarioDB:
    """Almacén transaccional con protección ante carreras e idempotencia."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)
        self._migrar()

    def _conectar(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def _migrar(self) -> None:
        with self._conectar() as conn:
            conn.executescript(SCHEMA_SQL)

    def crear_producto(self, sku: str, nombre: str, cantidad_inicial: int = 0, owner: str = "public") -> int:
        if cantidad_inicial < 0:
            raise ErrorInventario("Cantidad inicial negativa")
        with self._conectar() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                cur = conn.execute(
                    "INSERT INTO productos (sku, nombre, owner, cantidad) VALUES (?, ?, ?, ?)",
                    (sku.strip(), nombre.strip(), owner.strip(), int(cantidad_inicial)),
                )
                conn.execute("COMMIT")
                return int(cur.lastrowid)
            except sqlite3.IntegrityError as exc:
                conn.execute("ROLLBACK")
                raise ErrorInventario(f"SKU duplicado o inválido: {sku}") from exc
            except Exception:
                conn.execute("ROLLBACK")
                raise

    def obtener_producto(self, producto_id: int) -> dict | None:
        with self._conectar() as conn:
            row = conn.execute(
                "SELECT id, sku, nombre, owner, cantidad FROM productos WHERE id = ?",
                (producto_id,),
            ).fetchone()
            return dict(row) if row else None

    def aplicar_movimiento(self, producto_id: int, delta: int, clave_operacion: str) -> ResultadoMovimiento:
        if delta == 0:
            raise ErrorInventario("El delta no puede ser cero")
        if not clave_operacion.strip():
            raise ErrorInventario("La clave de operación es obligatoria")

        payload_hash = hashlib.sha256(
            json.dumps({"producto_id": producto_id, "delta": delta}, sort_keys=True).encode()
        ).hexdigest()

        with self._conectar() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                existente = conn.execute(
                    "SELECT producto_id, payload_hash, cantidad_resultante FROM movimientos WHERE clave_operacion = ?",
                    (clave_operacion,),
                ).fetchone()
                if existente is not None:
                    if existente["payload_hash"] != payload_hash:
                        conn.execute("ROLLBACK")
                        raise ConflictoIdempotencia("Clave reutilizada con distinto contenido")
                    conn.execute("COMMIT")
                    return ResultadoMovimiento(
                        producto_id=int(existente["producto_id"]),
                        cantidad=int(existente["cantidad_resultante"]),
                        clave_operacion=clave_operacion,
                        reutilizado=True,
                    )

                if delta < 0:
                    cur = conn.execute(
                        "UPDATE productos SET cantidad = cantidad + ? WHERE id = ? AND cantidad + ? >= 0",
                        (delta, producto_id, delta),
                    )
                else:
                    cur = conn.execute(
                        "UPDATE productos SET cantidad = cantidad + ? WHERE id = ?",
                        (delta, producto_id),
                    )

                if cur.rowcount == 0:
                    existe = conn.execute("SELECT id FROM productos WHERE id = ?", (producto_id,)).fetchone()
                    conn.execute("ROLLBACK")
                    if existe is None:
                        raise ErrorInventario("Producto inexistente")
                    raise StockInsuficiente("Stock insuficiente para la salida solicitada")

                nuevo_stock = int(
                    conn.execute("SELECT cantidad FROM productos WHERE id = ?", (producto_id,)).fetchone()["cantidad"]
                )
                conn.execute(
                    "INSERT INTO movimientos (producto_id, delta, clave_operacion, payload_hash, cantidad_resultante) VALUES (?, ?, ?, ?, ?)",
                    (producto_id, delta, clave_operacion, payload_hash, nuevo_stock),
                )
                conn.execute("COMMIT")
                return ResultadoMovimiento(
                    producto_id=producto_id,
                    cantidad=nuevo_stock,
                    clave_operacion=clave_operacion,
                    reutilizado=False,
                )
            except Exception:
                try:
                    if conn.in_transaction:
                        conn.execute("ROLLBACK")
                except sqlite3.Error:
                    pass
                raise

    def listar_movimientos(self, producto_id: int) -> list[dict]:
        with self._conectar() as conn:
            rows = conn.execute(
                "SELECT id, producto_id, delta, clave_operacion, cantidad_resultante FROM movimientos WHERE producto_id = ? ORDER BY id",
                (producto_id,),
            ).fetchall()
            return [dict(r) for r in rows]
