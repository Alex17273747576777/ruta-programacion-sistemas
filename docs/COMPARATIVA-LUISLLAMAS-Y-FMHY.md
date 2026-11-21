# Comparativa técnica: `ruta-programacion-sistemas` vs `luisllamas.es` + `FMHY.net`

Este documento explica con honestidad qué hace bien [`luisllamas.es`](https://www.luisllamas.es/), qué aporta [`fmhy.net`](https://fmhy.net/), y por qué este repositorio está diseñado para **superar el formato de blog/portal tradicional** en rigor verificable, práctica reproducible y comprensión real.

## Comparativa punto por punto

| Dimensión | `luisllamas.es` | `fmhy.net` | `ruta-programacion-sistemas` (este repo) |
|---|---|---|---|
| **Formato de aprendizaje** | Artículos enciclopédicos, roadmaps visuales, snippets, cheatsheets y quizzes web estáticos. | Índice masivo curado por categorías (cursos, herramientas, simuladores, docs), sin progresión por proyectos propios. | **Ruta progresiva en 6 etapas + 6 guías técnicas + portal web interactivo (`docs/index.html`)**, cada una con **contratos verificables**, implementación de referencia y pruebas automatizadas en CI. |
| **Código ejecutable y verificación** | Ejemplos cortos aislados en artículos; no hay una suite de tests que valide un sistema entero de extremo a extremo. | Enlaza proyectos externos; no provee suite unificada propia. | **6 proyectos reales ejecutables** (`proyectos/01` a `06`) con 12 tests unitarios, prueba de concurrencia real con barrera, servidor HTTP real, backup/restore SHA-256 y outbox idempotente. |
| **Pedagogía y comprensión** | Explicaciones claras por artículo, pero sin mecanismo obligatorio que detecte lagunas del estudiante. | No impone método de estudio. | **Método Richard Feynman obligatorio en sus 4 pasos completos** (estudio en fuente primaria → explicación sin jerga → lagunas y vuelta a fuente → analogía con límites) verificado por `tests/verificar_feynman.py` en CI. |
| **Cobertura de sistemas, lenguajes y hardware** | Muy fuerte en amplitud (Arduino, ESP32, Raspberry Pi, C++, C#, Python, Rust, Go, Zig, Linux, Docker, RTOS, binario). | Aporta los mejores simuladores activos (`Wokwi`, `Falstad`, `HDLBits`, `Godbolt`, `NandGame`, `CPU Land`, `Protocol Explorer`, `systemd-by-example`, `Regex101`, `Play with Docker`). | Integra esa misma amplitud (**binario/CPU, C/C++/Rust/Go/Zig, POO/Arquitectura, Linux/Bash/Git/Nginx/Docker, Raspberry Pi/Arduino/ESP32/RTOS**) conectada con los **simuladores activos verificados de FMHY.net**, evitando cursos superficiales aislados. |
| **Hojas rápidas (CheatSheets)** | Muchas cheatsheets de sintaxis suelta. | Enlaza `Devhints`, `DevDocs`, `Linux Command Library`. | **7 cheatsheets orientadas a fallos y verificación** (`cheatsheets/`), cada una con trampa típica, comando de comprobación y ficha Feynman de 4 pasos. |
| **Quizzes y Playgrounds** | Quizzes y playgrounds web por tema. | Enlaza juegos y sandboxes externos (`FutureCoder`, `SQLBolt`, `Learn Git Branching`, `Wokwi`). | **Portal autocontenido (`docs/index.html`)** con 3 playgrounds offline (Binario/IEEE-754, Regex/`chmod`, Quiz Feynman) + **Evaluador CLI ejecutable y testeado** (`quizzes/quiz_cli.py`, 20 preguntas). |
| **Mantenimiento y transparencia** | Sitio cerrado mantenido por un autor. | Índice abierto actualizado continuamente por la comunidad (`fmhy/edit`). | Repositorio abierto verificable en GitHub Actions (`verificar_feynman.py`, `verificar_enlaces_fmhy.py`, pruebas de las 6 etapas y quizzes). |

## Dónde aporta valor adicional `luisllamas.es` (y cómo se integra sin perder rigor)

`luisllamas.es` destaca como consulta rápida en español para electrónica básica, pinouts concretos de Arduino/ESP32 y primeros contactos con múltiples lenguajes. En lugar de copiar su contenido, esta ruta lo supera al:

1. Exigir **invariantes medibles** en cada proyecto (por ejemplo, que dos salidas concurrentes nunca produzcan stock negativo, o que una agenda no sobrescriba un JSON corrupto).
2. Integrar **simuladores interactivos gratuitos y activos de FMHY.net** (`NandGame`, `Wokwi`, `Falstad`, `HDLBits`, `Protocol Explorer`, `Learn Git Branching`, `Select Star SQL`) para practicar sin hardware costoso antes de pasar al mundo físico.
3. Unir software, base de datos, redes, Linux/operación y puente a sistemas embebidos bajo un **único método de estudio auditable** (Richard Feynman en 4 pasos).
