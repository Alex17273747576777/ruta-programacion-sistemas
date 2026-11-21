# CheatSheet · Redes, HTTP y Seguridad de Aplicaciones

| Concepto | Regla operativa | Código o prueba esperada |
|---|---|---|
| **Autenticación vs Autorización** | `401` = no sé quién eres; `403` = sé quién eres, pero este recurso no es tuyo | Verificar `recurso.owner == usuario_actual` en servidor |
| **Idempotencia HTTP** | `POST` con `clave_operacion` única devuelve mismo resultado ante reintento | Misma clave + payload distinto → `409 Conflict` |
| **Límites de entrada** | Validar `Content-Length`, esquema y rangos antes de procesar | Payload excesivo o malformado → `400` / `422` sin stacktrace |
| **Secretos y TLS** | Tokens nunca en Git, URLs o logs; HTTPS obligatorio fuera de localhost | Censurar campos sensibles en logs estructurados |

## Comprobación rápida

```bash
python3 -m unittest proyectos/04_redes/test_etapa04_api.py -v
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** códigos de estado HTTP, control de acceso por objeto y protección de credenciales mediante [MDN: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview), [Protocol Explorer](https://protocol-explorer-alpha.vercel.app/) y [The Copenhagen Book](https://thecopenhagenbook.com/).
2. **Enseñarlo con palabras simples:** autenticar es comprobar el carné en la entrada; autorizar por objeto es comprobar que tu llave abre la taquilla 12 y no la 13, aunque hayas pedido el número 13 por la ventanilla.
3. **Identificar lagunas y volver a la fuente original:** si dudas cuándo usar `401`, `403` o `404` (para no filtrar si un ID privado existe) o por qué un token en una URL acaba en los logs del proxy, consulta [OWASP Top 10](https://owasp.org/www-project-top-ten/) y [The Copenhagen Book](https://thecopenhagenbook.com/).
4. **Simplificar y revisar con analogías:** *analogía de la taquilla y la postal:* tu token es la llave del casillero y HTTPS es el sobre cerrado; mandarlo por HTTP sin cifrar es escribir la combinación de tu casillero detrás de una postal abierta. (*Límite:* TLS protege el viaje por la red, no corrige errores de autorización dentro de tu propio código de servidor).
