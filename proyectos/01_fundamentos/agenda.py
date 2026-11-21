"""Etapa 1 · Agenda CLI con persistencia JSON atómica y protección ante corrupción."""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path

MAX_LONGITUD_NOMBRE = 120
MAX_LONGITUD_TELEFONO = 32


class ErrorAgenda(ValueError):
    """Error de validación o persistencia controlada."""


@dataclass(frozen=True)
class Contacto:
    id: str
    nombre: str
    telefono: str


class Agenda:
    """Agenda de contactos sintéticos con escritura atómica por archivo temporal."""

    def __init__(self, ruta_archivo: str | Path) -> None:
        self.ruta = Path(ruta_archivo)
        self._contactos: dict[str, Contacto] = {}
        self._cargar()

    def _cargar(self) -> None:
        if not self.ruta.exists():
            return
        try:
            crudo = self.ruta.read_text(encoding="utf-8")
            datos = json.loads(crudo)
        except (OSError, json.JSONDecodeError) as exc:
            raise ErrorAgenda(
                f"Archivo JSON corrupto o ilegible en {self.ruta}; no se sobrescribió"
            ) from exc
        if not isinstance(datos, list):
            raise ErrorAgenda("Estructura de agenda inválida: se esperaba una lista")
        for item in datos:
            c = Contacto(
                id=str(item["id"]),
                nombre=str(item["nombre"]),
                telefono=str(item["telefono"]),
            )
            self._contactos[c.id] = c

    def guardar(self) -> None:
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            [asdict(c) for c in self._contactos.values()],
            ensure_ascii=False,
            indent=2,
        )
        fd, tmp_name = tempfile.mkstemp(
            prefix=".tmp-agenda-",
            suffix=".json",
            dir=str(self.ruta.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(payload)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_name, self.ruta)
        except Exception:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise

    def agregar(self, nombre: str, telefono: str) -> Contacto:
        nombre_limpio = nombre.strip()
        tel_limpio = telefono.strip()
        if not nombre_limpio or len(nombre_limpio) > MAX_LONGITUD_NOMBRE:
            raise ErrorAgenda("Nombre vacío o demasiado largo")
        if not tel_limpio or len(tel_limpio) > MAX_LONGITUD_TELEFONO:
            raise ErrorAgenda("Teléfono vacío o demasiado largo")
        contacto = Contacto(id=str(uuid.uuid4()), nombre=nombre_limpio, telefono=tel_limpio)
        self._contactos[contacto.id] = contacto
        self.guardar()
        return contacto

    def listar(self) -> list[Contacto]:
        return list(self._contactos.values())

    def buscar(self, consulta: str) -> list[Contacto]:
        q = consulta.strip().lower()
        return [
            c
            for c in self._contactos.values()
            if q in c.nombre.lower() or q in c.telefono.lower()
        ]

    def eliminar(self, contacto_id: str) -> bool:
        if contacto_id not in self._contactos:
            return False
        del self._contactos[contacto_id]
        self.guardar()
        return True
