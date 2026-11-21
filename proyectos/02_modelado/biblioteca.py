"""Etapa 2 · Dominio de biblioteca separado de persistencia e interfaz."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


class ErrorDominio(ValueError):
    """Violación de una invariante de biblioteca."""


@dataclass(frozen=True)
class Libro:
    id: str
    titulo: str


@dataclass(frozen=True)
class Usuario:
    id: str
    nombre: str


@dataclass(frozen=True)
class Prestamo:
    id: str
    libro_id: str
    usuario_id: str
    fecha_inicio: date
    fecha_limite: date
    fecha_devolucion: date | None = None

    @property
    def activo(self) -> bool:
        return self.fecha_devolucion is None


class RepositorioBiblioteca(Protocol):
    def guardar_libro(self, libro: Libro) -> None: ...
    def obtener_libro(self, libro_id: str) -> Libro | None: ...
    def guardar_usuario(self, usuario: Usuario) -> None: ...
    def obtener_usuario(self, usuario_id: str) -> Usuario | None: ...
    def guardar_prestamo(self, prestamo: Prestamo) -> None: ...
    def listar_prestamos(self) -> list[Prestamo]: ...


class RepositorioMemoria:
    def __init__(self) -> None:
        self.libros: dict[str, Libro] = {}
        self.usuarios: dict[str, Usuario] = {}
        self.prestamos: dict[str, Prestamo] = {}

    def guardar_libro(self, libro: Libro) -> None:
        self.libros[libro.id] = libro

    def obtener_libro(self, libro_id: str) -> Libro | None:
        return self.libros.get(libro_id)

    def guardar_usuario(self, usuario: Usuario) -> None:
        self.usuarios[usuario.id] = usuario

    def obtener_usuario(self, usuario_id: str) -> Usuario | None:
        return self.usuarios.get(usuario_id)

    def guardar_prestamo(self, prestamo: Prestamo) -> None:
        self.prestamos[prestamo.id] = prestamo

    def listar_prestamos(self) -> list[Prestamo]:
        return list(self.prestamos.values())


class ServicioBiblioteca:
    """Reglas puras con reloj inyectable e invariantes estrictas."""

    def __init__(self, repo: RepositorioBiblioteca, reloj=date.today) -> None:
        self.repo = repo
        self.reloj = reloj
        self._seq = 0

    def registrar_libro(self, libro_id: str, titulo: str) -> Libro:
        if not libro_id.strip() or not titulo.strip():
            raise ErrorDominio("ID y título son obligatorios")
        if self.repo.obtener_libro(libro_id) is not None:
            raise ErrorDominio("Ya existe un ejemplar con ese ID")
        libro = Libro(id=libro_id, titulo=titulo.strip())
        self.repo.guardar_libro(libro)
        return libro

    def registrar_usuario(self, usuario_id: str, nombre: str) -> Usuario:
        if not usuario_id.strip() or not nombre.strip():
            raise ErrorDominio("ID y nombre son obligatorios")
        if self.repo.obtener_usuario(usuario_id) is not None:
            raise ErrorDominio("Ya existe un usuario con ese ID")
        usuario = Usuario(id=usuario_id, nombre=nombre.strip())
        self.repo.guardar_usuario(usuario)
        return usuario

    def prestar(self, libro_id: str, usuario_id: str, dias: int = 7) -> Prestamo:
        if dias <= 0:
            raise ErrorDominio("Los días de préstamo deben ser positivos")
        if self.repo.obtener_libro(libro_id) is None:
            raise ErrorDominio("Libro inexistente")
        if self.repo.obtener_usuario(usuario_id) is None:
            raise ErrorDominio("Usuario inexistente")
        for p in self.repo.listar_prestamos():
            if p.libro_id == libro_id and p.activo:
                raise ErrorDominio("El libro ya está prestado")
        self._seq += 1
        hoy = self.reloj()
        limite = date.fromordinal(hoy.toordinal() + dias)
        prestamo = Prestamo(
            id=f"P-{self._seq}",
            libro_id=libro_id,
            usuario_id=usuario_id,
            fecha_inicio=hoy,
            fecha_limite=limite,
        )
        self.repo.guardar_prestamo(prestamo)
        return prestamo

    def devolver(self, prestamo_id: str) -> tuple[Prestamo, int]:
        actual = next((p for p in self.repo.listar_prestamos() if p.id == prestamo_id), None)
        if actual is None:
            raise ErrorDominio("Préstamo inexistente")
        if not actual.activo:
            raise ErrorDominio("El préstamo ya fue devuelto")
        hoy = self.reloj()
        atraso = max(0, (hoy - actual.fecha_limite).days)
        cerrado = Prestamo(
            id=actual.id,
            libro_id=actual.libro_id,
            usuario_id=actual.usuario_id,
            fecha_inicio=actual.fecha_inicio,
            fecha_limite=actual.fecha_limite,
            fecha_devolucion=hoy,
        )
        self.repo.guardar_prestamo(cerrado)
        return cerrado, atraso
