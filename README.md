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

## Etapas y proyectos ejecutables

| # | Etapa | Proyecto de referencia (ejecutable) | Avance verificable |
|---|---|---|---|
| 1 | [Fundamentos](etapas/01-fundamentos.md) | [`proyectos/01_fundamentos/`](proyectos/01_fundamentos/) (`calculadora.py`, `agenda.py`) | Entradas normales y erróneas se tratan explícitamente; `Decimal` y guardado JSON atómico con pruebas. |
| 2 | [Modelado y pruebas](etapas/02-modelado.md) | [`proyectos/02_modelado/`](proyectos/02_modelado/) (`biblioteca.py`) | Invariantes y pruebas de operaciones, fallos, reloj inyectado y límites. |
| 3 | [Datos y concurrencia](etapas/03-datos.md) | [`proyectos/03_datos/`](proyectos/03_datos/) (`inventario.py`, `schema_postgres.sql`) | Migraciones, rollback, idempotencia y prueba real de competencia con barrera. |
| 4 | [Redes y aplicaciones](etapas/04-redes.md) | [`proyectos/04_redes/`](proyectos/04_redes/) (`api_inventario.py`) | Servidor HTTP real, autorización por recurso, límites de entrada y pruebas de integración. |
| 5 | [Entrega y operación](etapas/05-operacion.md) | [`proyectos/05_operacion/`](proyectos/05_operacion/) (`operacion.py`) | Liveness vs readiness, logs sin secretos, respaldo y restauración verificada con SHA-256. |
| 6 | [Sistemas distribuidos](etapas/06-sistemas.md) | [`proyectos/06_sistemas/`](proyectos/06_sistemas/) (`pipeline_async.py`) | Outbox transaccional, consumidor idempotente, caché TTL, fallos inyectados y percentiles `p50`/`p95`. |

## Guías técnicas, CheatSheets, Quizzes y Recursos activos FMHY.net

Para cubrir en profundidad arquitectura de CPU, lenguajes de sistemas, Linux/contenedores y puente a electrónica/IoT/RTOS —incorporando los recursos activos verificados de **[FMHY.net](https://fmhy.net)** para superar un portal de artículos estáticos como `luisllamas.es`— este repositorio incluye:

- **Guías técnicas completas (con 4 pasos Feynman y simuladores activos):**
  - [Guía 01 · Binario, representación numérica y CPU](guias/01-binario-arquitectura-y-cpu.md)
  - [Guía 02 · Lenguajes de sistemas comparados (Python, C, C++, Rust, Go, Zig)](guias/02-lenguajes-de-sistemas.md)
  - [Guía 03 · Linux, Shell, Git y Contenedores](guias/03-linux-shell-git-y-contenedores.md)
  - [Guía 04 · Puente a Electrónica, Microcontroladores, IoT y RTOS](guias/04-embebidos-iot-y-rtos.md)
  - [Guía 05 · POO, Composición, Patrones y Arquitectura Limpia](guias/05-poo-patrones-y-arquitectura.md)
  - [Guía 06 · Redes, Nginx, Contenedores Docker/Podman y Despliegue](guias/06-redes-nginx-docker-y-despliegue.md)
  - [Guía 07 · Desarrollo Web, TypeScript, Event Loop y Seguridad en Navegador](guias/07-web-typescript-y-apis-modernas.md)
  - [Guía 08 · Control Automático (PID), Señales e IA Aplicada](guias/08-control-automatico-senales-e-ia-aplicada.md)
- **Laboratorios multi-lenguaje ejecutables (`laboratorios/`):**
  - [C99 memoria segura y overflow](laboratorios/c_memoria/buffer_seguro.c) · [C++20 RAII y `unique_ptr`](laboratorios/cpp_raii/raii_pool.cpp) · [Node.js Event Loop](laboratorios/node_event_loop/event_loop_orden.mjs) · [Simulador PID con anti-windup](laboratorios/control_pid/simulador_pid.py) · [Diagnóstico Bash estricto](laboratorios/bash_diagnostico/verificar_entorno.sh)
- **Hojas de referencia rápida orientadas a fallos reales (`cheatsheets/`):**
  - [Python y Decimal](cheatsheets/python-y-decimal.md) · [SQL y transacciones](cheatsheets/sql-y-transacciones.md) · [Git, Linux y Docker](cheatsheets/git-linux-y-docker.md) · [C, C++, Rust, Go y Zig](cheatsheets/c-cpp-rust-go-zig.md) · [Redes, HTTP y seguridad](cheatsheets/redes-http-y-seguridad.md) · [Regex, Binario y Nginx](cheatsheets/regex-binario-y-nginx.md) · [Embebidos, Arduino, ESP32 y RTOS](cheatsheets/embebidos-arduino-esp32-y-rtos.md) · [TypeScript, Web y CORS](cheatsheets/typescript-web-y-cors.md) · [Estructuras de datos y Big-O](cheatsheets/estructuras-datos-y-big-o.md)
- **Portal Web Interactivo y Playgrounds offline (`docs/index.html`):** abre [`docs/index.html`](docs/index.html) (o la versión publicada en [GitHub Pages](https://alex17273747576777.github.io/ruta-programacion-sistemas/)) para usar el lector integrado sin 404, 5 playgrounds en vivo (Binario/IEEE-754, Compuertas Lógicas & Half-Adder, Regex/`chmod`, Simulador PID, Quiz Feynman de 30 preguntas) y buscador FMHY.net.
- **Quiz CLI verificable:** ejecuta `python3 quizzes/quiz_cli.py` (o `python3 quizzes/quiz_cli.py --listar`) para evaluar tu comprensión con explicación Feynman paso a paso.
- **Catálogo curado de recursos activos en FMHY.net:** [`recursos/fmhy-activos.md`](recursos/fmhy-activos.md) (verificado HTTP `200`/`3xx` el 2026-11-21).
- **Comparativa de diseño y alcance:** [`docs/COMPARATIVA-LUISLLAMAS-Y-FMHY.md`](docs/COMPARATIVA-LUISLLAMAS-Y-FMHY.md).

## Cómo ejecutar todas las pruebas locales

```bash
python3 tests/verificar_feynman.py
python3 tests/verificar_portal.py
python3 tests/verificar_enlaces_fmhy.py
python3 -m unittest discover -s proyectos -v
python3 -m unittest discover -s laboratorios -v
python3 -m unittest discover -s quizzes -v
```

## Regla común de evaluación

Una entrega incluye README con dependencias/versiones, comandos reproducibles, datos sintéticos, decisiones y límites; código y pruebas; evidencia real de ejecución; una explicación de fallos; y la **ficha Feynman completa (4 pasos)** sobre el concepto central de la etapa. Puntúa cinco áreas 0–2: **funcionalidad**, **pruebas**, **seguridad/datos**, **operabilidad**, **explicación Feynman**. 0 = ausente o falla; 1 = parcial (o explicación con jerga sin completar los 4 pasos); 2 = criterios de la etapa reproducidos y los 4 pasos Feynman completos. Avanza con al menos 8/10 y sin 0 en pruebas, seguridad/datos ni explicación Feynman. La etapa 1 adapta seguridad a no subir datos reales ni ejecutar comandos desconocidos. Una autoevaluación no sustituye revisión independiente.

## Recursos y alcance

Los recursos están vinculados a una necesidad concreta en cada etapa. El tutorial oficial de Python **presupone nociones de programación**: usa los ejemplos paso a paso de la etapa 1 como puente y vuelve a la documentación cuando el vocabulario resulte familiar. Las páginas externas pueden cambiar; consulta su propia licencia y fecha, sin copiar material de terceros como propio. Esta ruta se publica como material propio, no afirma haber ejecutado los proyectos de cada estudiante.
