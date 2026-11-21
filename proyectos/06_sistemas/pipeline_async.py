"""Etapa 6 · Transactional Outbox, consumidor idempotente, caché TTL y percentiles."""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EntradaCache:
    valor: object
    expira_en: float


class CacheTTL:
    """Caché en memoria con tiempo de vida e invalidación explícita."""

    def __init__(self, ttl_segundos: float = 5.0, reloj=time.monotonic) -> None:
        self.ttl = ttl_segundos
        self.reloj = reloj
        self._datos: dict[str, EntradaCache] = {}

    def obtener(self, clave: str) -> object | None:
        ent = self._datos.get(clave)
        if ent is None:
            return None
        if self.reloj() >= ent.expira_en:
            del self._datos[clave]
            return None
        return ent.valor

    def guardar(self, clave: str, valor: object) -> None:
        self._datos[clave] = EntradaCache(valor=valor, expira_en=self.reloj() + self.ttl)

    def invalidar(self, clave: str) -> None:
        self._datos.pop(clave, None)


class PipelineOutbox:
    """Implementa publicación segura con outbox transaccional y worker idempotente."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)
        self._init()

    def _conectar(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._conectar() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS ordenes (
                    id TEXT PRIMARY KEY,
                    monto INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outbox (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave_evento TEXT NOT NULL UNIQUE,
                    payload TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'pendiente',
                    intentos INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS proyeccion_consumidor (
                    clave_evento TEXT PRIMARY KEY,
                    total_aplicado INTEGER NOT NULL
                );
                """
            )

    def registrar_orden_con_outbox(self, orden_id: str, monto: int, clave_evento: str) -> None:
        """Guarda orden y evento pendiente dentro de la misma transacción."""
        payload = json.dumps({"orden_id": orden_id, "monto": monto})
        with self._conectar() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute("INSERT INTO ordenes (id, monto) VALUES (?, ?)", (orden_id, monto))
                conn.execute(
                    "INSERT INTO outbox (clave_evento, payload) VALUES (?, ?)",
                    (clave_evento, payload),
                )
                conn.execute("COMMIT")
            except Exception:
                conn.execute("ROLLBACK")
                raise

    def procesar_pendientes(self, simular_caida_antes_de_ack: bool = False) -> int:
        """Consume eventos con idempotencia en el destino (soporta redelivery)."""
        procesados = 0
        with self._conectar() as conn:
            filas = conn.execute(
                "SELECT id, clave_evento, payload, intentos FROM outbox WHERE estado = 'pendiente' ORDER BY id"
            ).fetchall()
            for fila in filas:
                datos = json.loads(fila["payload"])
                conn.execute("BEGIN IMMEDIATE")
                try:
                    # Consumidor idempotente: INSERT OR IGNORE garantiza efecto único ante reentregas.
                    conn.execute(
                        "INSERT OR IGNORE INTO proyeccion_consumidor (clave_evento, total_aplicado) VALUES (?, ?)",
                        (fila["clave_evento"], int(datos["monto"])),
                    )
                    if simular_caida_antes_de_ack:
                        conn.execute(
                            "UPDATE outbox SET intentos = intentos + 1 WHERE id = ?",
                            (fila["id"],),
                        )
                        conn.execute("COMMIT")
                        raise RuntimeError("Caída inyectada antes de marcar ack en outbox")
                    conn.execute(
                        "UPDATE outbox SET estado = 'procesado', intentos = intentos + 1 WHERE id = ?",
                        (fila["id"],),
                    )
                    conn.execute("COMMIT")
                    procesados += 1
                except Exception:
                    if conn.in_transaction:
                        conn.execute("ROLLBACK")
                    raise
        return procesados

    def total_consumido(self) -> int:
        with self._conectar() as conn:
            row = conn.execute("SELECT COALESCE(SUM(total_aplicado), 0) AS t FROM proyeccion_consumidor").fetchone()
            return int(row["t"])


def calcular_percentiles(muestras: list[float]) -> tuple[float, float]:
    """Calcula p50 y p95 sobre una lista no vacía de latencias."""
    if not muestras:
        raise ValueError("Sin muestras")
    ordenadas = sorted(muestras)
    n = len(ordenadas)
    p50 = ordenadas[int(0.50 * (n - 1))]
    p95 = ordenadas[int(0.95 * (n - 1))]
    return p50, p95
