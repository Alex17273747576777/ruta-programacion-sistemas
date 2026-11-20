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
CI y scripts, documentación operativa, salida real de restauración y prueba de incidente. El despliegue público no es obligatorio: si no se desplegó, decláralo. Aplicar rúbrica.

## Recursos
- [OpenTelemetry: señales](https://opentelemetry.io/docs/concepts/signals/) — trazas, métricas y logs.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — amenazas y revisión.
