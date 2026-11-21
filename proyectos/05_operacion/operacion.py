"""Etapa 5 · Operación: liveness/readiness, respaldo verificado y logs sin secretos."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

CAMPOS_SENSIBLES = {"token", "password", "secret", "authorization", "api_key"}


def log_estructurado(evento: str, **campos: object) -> str:
    """Serializa un log JSON censurando campos sensibles."""
    limpio: dict[str, object] = {"evento": evento}
    for k, v in campos.items():
        if k.lower() in CAMPOS_SENSIBLES:
            limpio[k] = "[REDACTADO]"
        else:
            limpio[k] = v
    return json.dumps(limpio, ensure_ascii=False, sort_keys=True)


def comprobar_liveness() -> tuple[bool, str]:
    """El proceso Python está vivo y responde."""
    return True, "alive"


def comprobar_readiness(db_path: str | Path) -> tuple[bool, str]:
    """Solo está listo si la base de datos responde a una consulta real."""
    ruta = Path(db_path)
    if not ruta.exists():
        return False, "db_missing"
    try:
        conn = sqlite3.connect(str(ruta), timeout=2.0)
        try:
            conn.execute("SELECT 1").fetchone()
            return True, "ready"
        finally:
            conn.close()
    except sqlite3.Error as exc:
        return False, f"db_error:{type(exc).__name__}"


def respaldar_sqlite(origen: str | Path, destino: str | Path) -> str:
    """Crea una copia consistente en caliente usando SQLite backup API y devuelve su SHA-256."""
    dest_path = Path(destino)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(str(origen))
    dst = sqlite3.connect(str(dest_path))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    return hashlib.sha256(dest_path.read_bytes()).hexdigest()


def restaurar_y_verificar(backup_path: str | Path, sha256_esperado: str, destino_restaurado: str | Path) -> bool:
    """Verifica el SHA-256 del respaldo y lo restaura a una base nueva comprobando integridad."""
    bkp = Path(backup_path)
    actual = hashlib.sha256(bkp.read_bytes()).hexdigest()
    if actual != sha256_esperado:
        raise ValueError("SHA-256 del respaldo no coincide")
    respaldar_sqlite(bkp, destino_restaurado)
    conn = sqlite3.connect(str(destino_restaurado))
    try:
        res = conn.execute("PRAGMA integrity_check").fetchone()
        return bool(res and res[0] == "ok")
    finally:
        conn.close()
