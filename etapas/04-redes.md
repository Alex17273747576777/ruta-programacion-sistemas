# 4 · Redes, HTTP y seguridad de aplicaciones

## Objetivo
Entender petición, respuesta, estado y confianza. Una API es un mostrador: el cliente entrega una solicitud y recibe un resultado; verificar identidad no implica que tenga permiso para cualquier objeto.

## Proyecto: API de inventario
Extiende etapa 3 con servidor HTTP. Endpoints sugeridos: `POST /products`, `GET /products/{id}`, `POST /products/{id}/movements`. Documenta JSON, errores, tamaño máximo, idempotencia y códigos. Identidades de prueba con permisos de lectura y escritura; comprueba autorización **por recurso**, no solo inicio de sesión. Las credenciales reales nunca entran en Git, logs ni ejemplos.

**Contrato:** crear producto válido → 201 y ubicación; consulta inexistente → 404; entrada inválida → 400 o 422 documentado; usuario sin permiso → 403 (o 404 si se documenta ocultamiento); operación repetida con clave idéntica no duplica movimiento; caída de BD no devuelve éxito ficticio.

## Ejercicios y criterios

1. Captura con cliente local una petición y respuesta; identifica método, ruta, estado, tipo y cuerpo. Nunca captures tokens reales.
2. Envia entrada ausente, tipo incorrecto y cuerpo sobredimensionado: respuesta controlada, sin traza ni cambio de datos.
3. Prueba dos usuarios: A no puede consultar/modificar recurso privado de B aunque conozca su ID; ejecuta control en servidor.
4. Repite una operación tras simular pérdida de respuesta; comprueba cantidad, número de movimientos y respuesta de reintento.
5. Construye una consulta con caracteres especiales y verifica que no cambia la lógica; usa parámetros, no filtros artesanales de caracteres.
6. Documenta HTTPS para despliegue, almacenamiento seguro de secretos y límites de tasa como decisiones de despliegue. No afirmes protección TLS en localhost sin configurarla.

## Entrega y avance
Contrato OpenAPI o equivalente, servidor ejecutable, suite de integración con base desechable y ejemplos reproducibles. Prueba normal, denegación, error y reintento. Registra qué mecanismo de identidad se utiliza y sus limitaciones. Aplica rúbrica.

## Recursos
- [MDN: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — estructura de intercambio.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — identificación de riesgos; no reemplaza revisión de amenazas.
