# Guía 06 · Redes, Nginx, Contenedores Docker/Podman y Despliegue Seguro

> **Objetivo:** entender qué ocurre entre tu servidor de aplicación (`localhost:8000`) y un usuario real en internet: DNS, TLS, proxy inverso con Nginx, imágenes multicapa y tareas programadas.

## 1. Arquitectura mínima de un servicio desplegado

```text
Navegador ──HTTPS (443)──▶ Nginx (TLS + límites + estáticos) ──HTTP local──▶ App Python/Go (127.0.0.1:8000) ──▶ PostgreSQL
```

- **Por qué no exponer directamente el servidor de desarrollo:** un proxy inverso como **Nginx** termina el cifrado TLS, impone límites de tamaño de cuerpo (`client_max_body_size`), protege contra conexiones lentas y sirve archivos estáticos sin bloquear los hilos de tu aplicación.
- **Imágenes reproducibles y ligeras:** usa builds multicapa (*multi-stage*), usuario no privilegiado (`USER app`), versiones fijadas y `.dockerignore` para no copiar `.git` ni secretos dentro de la imagen.
- **Tareas programadas (`cron` vs `systemd` timers):** siempre valida expresiones `cron` antes de desplegar y redirige logs a `journald` o salida estándar estructurada.

## 2. Comprobaciones locales antes de publicar

```bash
# Validar sintaxis de configuración Nginx antes de recargar (en entorno con nginx)
nginx -t

# Verificar resolución DNS y cabeceras HTTP de respuesta reales
curl -I https://example.com
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** papel del proxy inverso (terminación TLS, cabeceras `X-Forwarded-*`, límites), aislamiento mínimo en contenedores y operación segura usando [Nginx Docs](https://nginx.org/en/docs/), [Play with Docker](https://labs.play-with-docker.com/) y [Podman](https://podman.io/).
2. **Enseñarlo con palabras simples:** tu aplicación en Python o Go es como el cocinero dentro de la cocina: sabe preparar pedidos (`POST /products`), pero no debería estar además atendiendo la puerta de la calle bajo la lluvia ni revisando pasaportes. **Nginx** es el recepcionista en la entrada: habla el idioma cifrado de la calle (HTTPS), frena paquetes demasiado grandes antes de que entren y pasa los pedidos limpios por la ventanilla interna a la cocina.
3. **Identificar lagunas y volver a la fuente original:** cuando el servidor detrás de Nginx vea siempre `127.0.0.1` como IP de todos los clientes o pierda si la petición original fue HTTPS, regresa a [Nginx Docs](https://nginx.org/en/docs/) para revisar `proxy_set_header Host`, `X-Forwarded-For` y `X-Forwarded-Proto`, y al capítulo de seguridad en [The Copenhagen Book](https://thecopenhagenbook.com/).
4. **Simplificar y revisar con analogías:** *analogía de la aduana y la caja fuerte:* el proxy inverso es la aduana en la puerta del edificio que sella los sobres (TLS) y pesa las maletas antes de dejarlas pasar; el contenedor con usuario sin privilegios es darle al cocinero solo la llave de su cocina y no la llave maestra de todo el edificio. (*Límite:* ejecutar dentro de Docker/Podman no hace seguro un código con inyección SQL o secretos metidos en el `Dockerfile`).

## Recursos activos FMHY.net

- [Play with Docker](https://labs.play-with-docker.com/) — laboratorio activo en navegador para practicar contenedores y redes Docker.
- [Podman](https://podman.io/) — motor de contenedores compatible con Docker sin demonio raíz obligatorio.
- [Nginx Docs](https://nginx.org/en/docs/) — documentación oficial de directivas, proxy inverso y TLS.
- [Roadmap Docker](https://roadmap.sh/docker) y [Roadmap Linux](https://roadmap.sh/linux) — mapas estructurados paso a paso.
- [Crontab Guru](https://crontab.guru/) — verificador instantáneo de expresiones `cron`.
