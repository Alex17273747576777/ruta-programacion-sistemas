# De principiante a ingeniería de sistemas: ruta basada en proyectos

Una ruta para construir y explicar software confiable, no una certificación ni una promesa de empleo. Cada etapa termina en un proyecto evaluable y ejercicios con criterios explícitos. Puedes usar Python y PostgreSQL como camino de referencia, o sustituir herramientas si mantienes los contratos y las pruebas. Los ejercicios de seguridad son exclusivamente para entornos propios o autorizados.

## Cómo empezar de cero

1. Instala una versión mantenida de Python 3 y Git desde sus sitios oficiales. Abre una terminal; comprueba `python3 --version` y `git --version`. En Windows usa `py` si corresponde. Nunca pegues comandos que no entiendes.
2. Crea una carpeta de práctica y un repositorio Git local. No subas claves, respaldos personales ni datos de terceros. Usa datos ficticios.
3. Para cada actividad aplica de forma completa el **método de Richard Feynman** (4 pasos): (1) estudia el concepto en la fuente oficial; (2) explícalo por escrito con palabras simples, sin jerga, como si se lo enseñaras a un niño; (3) anota dónde te trabaste o dudaste (tus lagunas) y vuelve a la fuente original para cerrarlas; (4) simplifica y reescribe usando una analogía cotidiana clara. Luego implementa, añade pruebas para el caso normal y el fallo, y ejecuta de nuevo desde cero.
4. Haz cada etapa en orden. Si repruebas un criterio, corrige y vuelve a medir; no compares tu ritmo con otro. Sin fechas ficticias ni cantidad de líneas como indicador de capacidad.

## Norma obligatoria: Método de Richard Feynman (4 pasos)

En toda la ruta —desde explicar qué es una variable hasta defender un sistema distribuido— es obligatorio completar los **cuatro pasos** sin saltarse ninguno:

1. **Seleccionar y estudiar el concepto:** elegir el tema concreto de la etapa y estudiarlo desde las fuentes confiables enlazadas al final de cada módulo.
2. **Enseñarlo por escrito con palabras simples:** explicarlo sin jerga técnica innecesaria, con frases cortas, como a alguien que empieza de cero.
3. **Identificar lagunas y volver a la fuente original:** cuando aparezca una explicación confusa o un «porque sí», marcar la laguna, volver a la documentación primaria y completar lo que faltaba.
4. **Simplificar y revisar con analogías:** reescribir la explicación integrando lo corregido, apoyándose en analogías claras (declarando dónde deja de aplicarse la analogía) hasta lograr fluidez real.

## Etapas

| # | Etapa | Producto | Avance verificable |
|---|---|---|---|
| 1 | [Fundamentos](etapas/01-fundamentos.md) | Calculadora y agenda CLI | Entradas normales y erróneas se tratan explícitamente; persiste y recupera datos. |
| 2 | [Modelado y pruebas](etapas/02-modelado.md) | Biblioteca de préstamos | Invariantes y pruebas de operaciones, fallos y límites. |
| 3 | [Datos y concurrencia](etapas/03-datos.md) | Inventario transaccional | Migraciones, rollback y pruebas de competencia contra base real. |
| 4 | [Redes y aplicaciones](etapas/04-redes.md) | API de inventario | Contrato HTTP, autenticación/autorización y pruebas de integración. |
| 5 | [Entrega y operación](etapas/05-operacion.md) | Servicio observable | CI, empaquetado, restauración ensayada y respuesta a incidentes. |
| 6 | [Sistemas distribuidos](etapas/06-sistemas.md) | API + cola + caché + worker | Idempotencia, fallos inyectados, métricas y defensa de decisiones. |

## Regla común de evaluación

Una entrega incluye README con dependencias/versiones, comandos reproducibles, datos sintéticos, decisiones y límites; código y pruebas; evidencia real de ejecución; una explicación de fallos; y la **ficha Feynman completa (4 pasos)** sobre el concepto central de la etapa. Puntúa cinco áreas 0–2: **funcionalidad**, **pruebas**, **seguridad/datos**, **operabilidad**, **explicación Feynman**. 0 = ausente o falla; 1 = parcial (o explicación con jerga sin completar los 4 pasos); 2 = criterios de la etapa reproducidos y los 4 pasos Feynman completos. Avanza con al menos 8/10 y sin 0 en pruebas, seguridad/datos ni explicación Feynman. La etapa 1 adapta seguridad a no subir datos reales ni ejecutar comandos desconocidos. Una autoevaluación no sustituye revisión independiente.

## Recursos y alcance

Los recursos están vinculados a una necesidad concreta en cada etapa. El tutorial oficial de Python **presupone nociones de programación**: usa los ejemplos paso a paso de la etapa 1 como puente y vuelve a la documentación cuando el vocabulario resulte familiar. Las páginas externas pueden cambiar; consulta su propia licencia y fecha, sin copiar material de terceros como propio. Esta ruta se publica como material propio, no afirma haber ejecutado los proyectos de cada estudiante.
