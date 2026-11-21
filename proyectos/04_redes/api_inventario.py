"""Etapa 4 · Servidor HTTP de inventario con autorización por recurso e idempotencia."""
from __future__ import annotations

import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ETAPA3_DIR = Path(__file__).resolve().parents[1] / "03_datos"
if str(ETAPA3_DIR) not in sys.path:
    sys.path.insert(0, str(ETAPA3_DIR))

from inventario import ConflictoIdempotencia, ErrorInventario, InventarioDB, StockInsuficiente  # noqa: E402

MAX_BODY_BYTES = 16 * 1024


class InventarioHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], db: InventarioDB, tokens: dict[str, str]):
        self.db = db
        self.tokens = tokens
        super().__init__(server_address, InventarioHandler)


class InventarioHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return

    def _usuario_actual(self) -> str | None:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth[len("Bearer "):].strip()
        return self.server.tokens.get(token)

    def _responder_json(self, status: int, cuerpo: dict, headers: dict[str, str] | None = None) -> None:
        data = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _leer_json(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._responder_json(HTTPStatus.BAD_REQUEST, {"error": "Content-Length inválido"})
            return None
        if length <= 0 or length > MAX_BODY_BYTES:
            self._responder_json(HTTPStatus.BAD_REQUEST, {"error": "Cuerpo vacío o excede límite"})
            return None
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._responder_json(HTTPStatus.BAD_REQUEST, {"error": "JSON mal formado"})
            return None

    def do_GET(self) -> None:
        usuario = self._usuario_actual()
        if not usuario:
            self._responder_json(HTTPStatus.UNAUTHORIZED, {"error": "Autenticación requerida"})
            return

        ruta = urlparse(self.path).path.strip("/")
        partes = ruta.split("/")
        if len(partes) == 2 and partes[0] == "products" and partes[1].isdigit():
            pid = int(partes[1])
            prod = self.server.db.obtener_producto(pid)
            if prod is None:
                self._responder_json(HTTPStatus.NOT_FOUND, {"error": "Producto no encontrado"})
                return
            if prod["owner"] != usuario:
                self._responder_json(HTTPStatus.FORBIDDEN, {"error": "Sin permiso sobre este recurso"})
                return
            self._responder_json(HTTPStatus.OK, prod)
            return

        self._responder_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada"})

    def do_POST(self) -> None:
        usuario = self._usuario_actual()
        if not usuario:
            self._responder_json(HTTPStatus.UNAUTHORIZED, {"error": "Autenticación requerida"})
            return

        ruta = urlparse(self.path).path.strip("/")
        partes = ruta.split("/")

        if partes == ["products"]:
            data = self._leer_json()
            if data is None:
                return
            sku = str(data.get("sku", "")).strip()
            nombre = str(data.get("nombre", "")).strip()
            cantidad = data.get("cantidad", 0)
            if not sku or not nombre or not isinstance(cantidad, int) or cantidad < 0:
                self._responder_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "Datos de producto inválidos"})
                return
            try:
                pid = self.server.db.crear_producto(sku=sku, nombre=nombre, cantidad_inicial=cantidad, owner=usuario)
            except ErrorInventario as exc:
                self._responder_json(HTTPStatus.CONFLICT, {"error": str(exc)})
                return
            prod = self.server.db.obtener_producto(pid)
            self._responder_json(HTTPStatus.CREATED, prod, headers={"Location": f"/products/{pid}"})
            return

        if len(partes) == 3 and partes[0] == "products" and partes[1].isdigit() and partes[2] == "movements":
            pid = int(partes[1])
            prod = self.server.db.obtener_producto(pid)
            if prod is None:
                self._responder_json(HTTPStatus.NOT_FOUND, {"error": "Producto no encontrado"})
                return
            if prod["owner"] != usuario:
                self._responder_json(HTTPStatus.FORBIDDEN, {"error": "Sin permiso sobre este recurso"})
                return
            data = self._leer_json()
            if data is None:
                return
            delta = data.get("delta")
            clave = str(data.get("clave_operacion", "")).strip()
            if not isinstance(delta, int) or delta == 0 or not clave:
                self._responder_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "Movimiento inválido"})
                return
            try:
                res = self.server.db.aplicar_movimiento(pid, delta, clave)
            except ConflictoIdempotencia as exc:
                self._responder_json(HTTPStatus.CONFLICT, {"error": str(exc)})
                return
            except StockInsuficiente as exc:
                self._responder_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": str(exc)})
                return
            self._responder_json(
                HTTPStatus.OK,
                {
                    "producto_id": res.producto_id,
                    "cantidad": res.cantidad,
                    "clave_operacion": res.clave_operacion,
                    "reutilizado": res.reutilizado,
                },
            )
            return

        self._responder_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada"})
