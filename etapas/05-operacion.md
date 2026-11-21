# 5 · Entrega, seguridad y operación

## Objetivo
Convertir código funcional en servicio recuperable. Un test verde se parece a un chequeo médico: ayuda, pero no garantiza salud en todos los escenarios. Un backup que nunca se restaura es una hipótesis, no evidencia de recuperación.

## Proyecto: entrega reproducible y operación
Empaqueta la API anterior, fija versiones y ejecuta pruebas en CI para cada cambio. Define configuración por entorno, un usuario de BD con permisos mínimos y logs estructurados sin secretos. Añade health checks diferenciando proceso vivo de capacidad de atender solicitudes. Añade una guía para migrar, respaldar, restaurar y revertir.

**Contrato:** desde un checkout limpio se levantan app y base de prueba, migran y pasan tests; una prueba deliberadamente rota hace fallar CI; un backup se restaura en base nueva y sus registros esperados se comparan; error de conexión no se presenta como éxito.

## Ejercicios y criterios

1. Haz fallar un test de forma intencional en una rama y observa CI rojo; corrige y observa verde. Conserva enlaces o logs sin secretos.
2. Ejecuta migración dos veces según la política documentada; segunda ejecución no debe corromper datos. Prueba también una actualización fallida.
3. Crea tres registros sintéticos, respalda, destruye solo la base temporal, restaura y compara identidad y contenido; registra duración y punto de recuperación.
4. Simula BD inaccesible: readiness falla y respuesta no confirma escritura; liveness depende de la política documentada, sin bucle de reinicios injustificado.
5. Revisa imágenes/dependencias y licencias con herramientas disponibles. Registra versión de bases y hallazgos; un escáner sin resultados no es prueba de ausencia de vulnerabilidades.
6. Escribe un mini postmortem por un fallo simulado: impacto, cronología, detección, mitigación, causa sustentada, acciones con responsables y verificación. Evita culpas y datos reales.

## Entrega y avance
CI y scripts, documentación operativa, salida real de restauración, prueba de incidente y la **ficha Feynman completa (4 pasos)** sobre CI reproducible, readiness vs liveness y restauración probada. El despliegue público no es obligatorio: si no se desplegó, decláralo. Aplicar rúbrica.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** integración continua reproducible, distinción entre proceso vivo (*liveness*) y proceso listo para servir (*readiness*), y respaldo comprobado mediante restauración real, con apoyo en OpenTelemetry y OWASP.
2. **Enseñarlo con palabras simples (sin jerga):**
   - Que un programa arranque en tu computadora no prueba que arranque en una máquina nueva sin tus carpetas ocultas: la prueba automática en una máquina limpia es como hornear la receta en una cocina vacía para ver si no olvidaste un ingrediente.
   - Una copia de seguridad que nunca has abierto para restaurar es como guardar una llave de repuesto sin haber probado si gira la cerradura: hasta el día del incendio no sabes si sirve.
3. **Identificar lagunas y volver a la fuente original:**
   - *Laguna típica:* «Si la app responde `OK` en `/health`, ¿por qué las peticiones de escritura fallan?» y «¿Por qué reiniciar la app cuando la base de datos está caída empeora el problema en vez de arreglarlo?»
   - *Regreso a la fuente:* consulta en [OpenTelemetry: señales](https://opentelemetry.io/docs/concepts/signals/) qué miden logs, métricas y trazas al diagnosticar dependencias caídas, y en la especificación de salud de servicios por qué *liveness* («¿el proceso está atascado?») y *readiness* («¿puede conectar con la base para recibir tráfico?») responden preguntas distintas.
4. **Simplificar y revisar con analogías:**
   - *Analogía de la tienda y la caja registradora:* *liveness* comprueba que el empleado esté despierto dentro de la tienda; *readiness* comprueba que la caja registradora tenga corriente para cobrar. Si se va la luz en el banco, despedir y volver a contratar al empleado cada 10 segundos (*reinicio por liveness*) no arregla la caja; solo hay que cerrar temporalmente la puerta al público (*readiness en rojo*) hasta que vuelva la conexión. (*Límite:* las pruebas de restauración en una base temporal pequeña no miden el tiempo de restauración con gigabytes reales de producción).
   - *Comprobación del estudiante:* explica a una persona no técnica qué pasó paso a paso en tu simulacro de restauración y por qué tu *readiness* no se marca sano sin base de datos.

## Recursos
- [OpenTelemetry: señales](https://opentelemetry.io/docs/concepts/signals/) — trazas, métricas y logs.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — amenazas y revisión.
