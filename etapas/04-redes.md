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
Contrato OpenAPI o equivalente, servidor ejecutable, suite de integración con base desechable, ejemplos reproducibles y la **ficha Feynman completa (4 pasos)** sobre HTTP, autorización por objeto e inyección de consultas. Prueba normal, denegación, error y reintento. Registra qué mecanismo de identidad se utiliza y sus limitaciones. Aplica rúbrica.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** estructura de peticiones y códigos HTTP, diferencia entre autenticación (quién eres) y autorización por recurso (qué puedes tocar), y consultas parametrizadas frente a inyección, desde MDN HTTP y OWASP Top 10.
2. **Enseñarlo con palabras simples (sin jerga):**
   - Pedir datos por red es como enviar una carta a una oficina: dices qué acción quieres (ver o crear), en qué ventanilla (`/products/5`) y el sobre trae un número de respuesta (`200` todo bien, `404` no existe, `403` prohibido entrar).
   - Mostrar tu carné en la puerta demuestra quién eres, pero no te da permiso para abrir los casilleros de los demás vecinos: el guardia dentro del servidor debe mirar tu nombre **y** comprobar si ese casillero concreto te pertenece.
3. **Identificar lagunas y volver a la fuente original:**
   - *Laguna típica:* «¿Por qué un filtro casero que borra comillas `'` no detiene la inyección SQL si la consulta concatena texto?» y «¿Por qué devolver `403` vs `404` revela o esconde la existencia de un objeto?»
   - *Regreso a la fuente:* consulta en [OWASP Top 10](https://owasp.org/www-project-top-ten/) (*Broken Access Control* e *Injection*) y [MDN: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) cómo los parámetros preparados separan el comando de los datos igual que un formulario con casillas fijas, sin importar qué caracteres escriba el usuario.
4. **Simplificar y revisar con analogías:**
   - *Analogía de la llave del hotel y la plantilla impresa:* iniciar sesión te da la tarjeta del hotel (**autenticación**); probar en el servidor que la habitación `304` es la tuya antes de abrir la puerta es la **autorización por recurso**. Y una consulta SQL parametrizada es un cheque preimpreso donde el cliente solo rellena la casilla del nombre: nunca puede escribir instrucciones nuevas en la línea donde el banco dice «páguese». (*Límite:* el protocolo HTTP plano sin HTTPS viaja como postal abierta; el cifrado TLS en despliegue es aparte).
   - *Comprobación del estudiante:* explica en lenguaje cotidiano qué diferencia hay entre `401`, `403` y `404` en tu API y por qué nunca pegaste texto del usuario dentro del SQL.

## Recursos
- [MDN: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — estructura de intercambio.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — identificación de riesgos; no reemplaza revisión de amenazas.
