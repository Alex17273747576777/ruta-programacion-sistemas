# 6 · Ingeniería de sistemas distribuidos

## Objetivo
Diseñar, medir y defender compromisos entre disponibilidad, consistencia, latencia, costes y recuperación. Una cola es una sala de espera, no un hada que garantiza que una tarea se ejecute exactamente una vez: la estrategia de entrega y los reintentos importan.

## Proyecto: procesamiento asíncrono de movimientos
Extiende la API anterior con base de datos, caché, cola y worker. Implementa una operación de importación de movimientos sintéticos. Define esquema del mensaje, clave de idempotencia, política de reintento con límite y tratamiento de fallos permanentes. Explica si usas outbox transaccional para acoplar cambio de BD y publicación, y cómo evitas duplicar efectos en consumidores. Caché: documenta TTL, invalidación, consistencia deseada y fallback.

**Contrato:** una solicitud aceptada informa identificador y estado real; mensajes duplicados no duplican el efecto; una caída del worker no declara procesado lo pendiente; un error permanente queda visible; restablecer el worker permite avanzar. No prometas «exactly once» extremo a extremo sin demostrar sus condiciones.

## Ejercicios y criterios

1. Dibuja secuencia petición → transacción/outbox → publicador → cola → consumidor → estado. Marca límites de fallo y cuál es la fuente de verdad.
2. Inyecta caída después de confirmar la operación pero antes de confirmar el mensaje. Redelivery: comprueba un solo efecto persistido y estado final coherente.
3. Interrumpe la cola y recupera: demuestra cómo se preserva/reintenta la tarea; mide pendiente, antigüedad y errores sin registrar contenido privado.
4. Actualiza un producto con caché activa; muestra comportamiento durante invalidación fallida y tras TTL. Declara ventana de inconsistencia y riesgo.
5. Mide latencia p50/p95 y tasa de error antes/después de una carga definida: fija versión, datos, concurrencia, duración, entorno y calentamiento. Un benchmark local no predice producción.
6. Define un SLI y objetivo SLO medible; realiza un simulacro de incidente y compara evidencia con el objetivo. No fijes disponibilidad por intuición como garantía.
7. Compara al menos dos diseños (sin cola/con cola, invalidación síncrona/TTL): tabla de beneficios, costes, supuestos, riesgos y decisión reversible.
8. Presenta una revisión de arquitectura: seguridad, capacidad, topología, pérdida aceptable, RPO/RTO ensayados, límites de observabilidad y riesgos pendientes. RPO/RTO objetivos no equivalen a mediciones.

## Entrega y avance
Repositorio con diagramas legibles, código y configuración reproducibles, tests de integración y fallos, resultados medidos, runbook de recuperación, decisión de arquitectura y la **ficha Feynman completa (4 pasos)** defendiendo compromisos de entrega, caché y recuperación. Demuestra los ocho ejercicios; defiende por qué una solución más simple podría ser preferible. El despliegue se declara como local si no existe un entorno público real. Esta etapa no convierte automáticamente al estudiante en ingeniero senior: es evidencia de competencias prácticas que requieren revisión y experiencia.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** entrega al menos una vez con consumidores idempotentes, patrón *transactional outbox*, frescura e invalidación de caché, y medición real frente a objetivos (SLI/SLO, RPO/RTO), apoyándote en PostgreSQL, OpenTelemetry y Pro Git.
2. **Enseñarlo con palabras simples (sin jerga):**
   - Cuando envías un encargo por mensajero y no recibes respuesta, vuelves a llamarlo por si se perdió el aviso. El mensajero puede llegar dos veces con el mismo paquete; por eso quien recibe en casa anota en la puerta qué paquetes ya entraron hoy para no cobrar ni guardar el mismo paquete dos veces (**idempotencia**).
   - La caché es una nota adhesiva pegada en tu mesa para no caminar hasta el archivo en cada pregunta: te ahorra tiempo, pero si alguien cambia el expediente original en el archivo y no rompe tu nota adhesiva, durante unos minutos responderás con un dato viejo.
3. **Identificar lagunas y volver a la fuente original:**
   - *Laguna típica:* «Si guardo en la base de datos y justo después publico el mensaje en la cola, ¿qué ocurre si se corta la luz entre las dos líneas?» y «¿Por qué *at-least-once* + idempotencia reemplaza en la práctica la promesa imposible de *exactly-once* mágico?»
   - *Regreso a la fuente:* vuelve a [PostgreSQL: transacciones](https://www.postgresql.org/docs/17/tutorial-transactions.html) y [OpenTelemetry: señales](https://opentelemetry.io/docs/concepts/signals/) para comprobar que dos sistemas independientes no comparten una misma transacción sin coordinación o tabla *outbox* local, y cómo métricas reales (`p50`/`p95`, cola pendiente y edad) permiten verificar un SLO en lugar de adivinarlo.
4. **Simplificar y revisar con analogías:**
   - *Analogía del mostrador con buzón interno (outbox):* en vez de anotar la venta en el libro y luego cruzar la calle para echar la carta al buzón (donde puedes tropezar a mitad de la calle), guardas la venta **y** dejas la carta en la bandeja de salida dentro del mismo libro contable; un repartidor lee la bandeja después, y el destinatario tacha el código único del sobre al abrirlo. (*Límite:* las mediciones en una computadora local muestran fallos lógicos y comportamiento bajo reintentos, pero no predicen latencia ni costes en redes reales con múltiples máquinas).
   - *Comprobación del estudiante:* explica con palabras sencillas qué pasaría si quitaras la cola y la caché: cuándo te conviene esa versión simple y a partir de qué problema medido merece pagar la complejidad extra.

## Recursos
- [PostgreSQL: transacciones](https://www.postgresql.org/docs/17/tutorial-transactions.html) — frontera de consistencia.
- [OpenTelemetry: señales](https://opentelemetry.io/docs/concepts/signals/) — observabilidad.
- [Pro Git](https://git-scm.com/book/en/v2) — colaboración y recuperación de historial.
