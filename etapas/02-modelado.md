# 2 · Modelado, módulos y pruebas

## Objetivo
Separar reglas de negocio de entrada/salida. Un modelo es un mapa: conserva lo necesario para decidir sin fingir que representa cada detalle del mundo. Explica composición frente a herencia y elige la opción más sencilla que satisfaga el problema.

## Proyecto: biblioteca de préstamos
Modela `Libro`, `Usuario` y `Prestamo`; un ejemplar tiene ID único y puede estar disponible o prestado a un único usuario. Permite alta, préstamo, devolución y búsqueda; no borres el historial de préstamos. Separa reglas puras, persistencia e interfaz. Prueba con `unittest` o framework equivalente.

**Invariantes:** no préstamo doble; no devolución de préstamo cerrado; ID de ejemplar y usuario existente; una operación inválida no cambia estado; fechas explícitas y reloj inyectable en pruebas. Una clase no basta para garantizarlo: los cambios de estado deben pasar por operaciones comprobadas.

## Ejercicios y criterios

1. Presta libro A a U1 y luego a U2: segunda operación falla y A sigue prestado a U1.
2. Devuelve dos veces: segunda devolución falla sin crear un préstamo ni cambiar el historial.
3. Inyecta un reloj fijo y calcula atraso con fecha límite: antes y en fecha, 0; un día después, 1. Declara zona/convención de fecha.
4. Compara igualdad de dos IDs y de dos objetos distintos que comparten nombre. El ID determina identidad, no el título.
5. Escribe un test que falle ante una implementación que omite validar usuario; demuestra que al corregirla pasa. No uses una prueba que solo verifique que no hay excepción.
6. Sustituye repositorio por doble en memoria; prueba reglas sin disco. Explica qué NO prueba el doble (integración con archivo/base).

## Entrega y avance
Al menos ocho tests unitarios, dos de integración de persistencia, un dibujo de dependencias y la **ficha Feynman completa (4 pasos)** sobre separación de reglas, identidad por ID y límites de los dobles de prueba. Ejecuta suite desde limpio y conserva su salida. Demuestra invariantes anteriores y explica una limitación del diseño. Aplica rúbrica común.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** separación entre reglas del problema y entrada/salida, identidad por clave única frente a nombre repetido, y dobles de prueba en memoria, consultando las secciones de clases y `unittest` en Python.
2. **Enseñarlo con palabras simples (sin jerga):**
   - Las reglas de la biblioteca son como las normas de un juego de mesa: dicen «no puedes prestar la misma ficha a dos personas a la vez». Que el juego se juegue en papel, en consola o en una pantalla no cambia las reglas; si mezclas las normas dentro de los botones de la pantalla, cada vez que cambies de pantalla rompes el juego.
   - Dos personas pueden llamarse igual («Ana Pérez»), así que usar el nombre para saber quién es quién confunde préstamos. Por eso cada socio y cada libro llevan un número de carné único que nunca cambia.
3. **Identificar lagunas y volver a la fuente original:**
   - *Laguna típica:* «Si mis pruebas en memoria pasan todas, ¿por qué puede fallar al guardar en archivo o base real?» y «¿Por qué un objeto puede cambiar de datos por dentro sin pasar por las reglas si dejo sus campos abiertos?»
   - *Regreso a la fuente:* vuelve a [Python `unittest` (`unittest.mock` / aislamiento)](https://docs.python.org/3/library/unittest.html) y [Python: clases](https://docs.python.org/3/tutorial/classes.html) para distinguir qué valida una prueba en memoria (lógica pura) de lo que solo prueba una ejecución real contra disco (permisos, formato JSON, bloqueos), y cómo controlar mutaciones mediante operaciones explícitas.
4. **Simplificar y revisar con analogías:**
   - *Analogía del árbitro y la libreta:* el dominio es el árbitro que decide si el préstamo es legal; el disco es la libreta donde se apunta el marcador. Un ensayo en memoria sustituye la libreta por notas rápidas para probar rápido si el árbitro pita bien las faltas, pero **no demuestra** que la libreta tenga hojas suficientes ni que el bolígrafo escriba bajo la lluvia.
   - *Comprobación del estudiante:* explica en cinco líneas simples, sin usar la palabra «encapsulación» ni «inyección de dependencias», por qué tu reloj de prueba se pasa como parámetro y qué deja sin probar el doble en memoria.

## Recursos y práctica activa (fuentes oficiales + FMHY.net)
- Implementación y pruebas de referencia: [`proyectos/02_modelado/`](../proyectos/02_modelado/) (`python3 -m unittest proyectos/02_modelado/test_etapa02.py -v`).
- Guía complementaria: [Guía 02 · Lenguajes de sistemas comparados](../guias/02-lenguajes-de-sistemas.md) y [CheatSheet C/C++/Rust/Go/Zig](../cheatsheets/c-cpp-rust-go-zig.md).
- [Python: clases](https://docs.python.org/3/tutorial/classes.html) — objetos, alcance y métodos.
- [Python unittest](https://docs.python.org/3/library/unittest.html) — aislamiento y aserciones.
- [Pro Git: ramas](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) — cambios revisables.
- **Recursos activos de [FMHY.net](https://fmhy.net/educational):** [Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans), [Awesome Low Level Design](https://github.com/ashishps1/awesome-low-level-design), [Crafting Interpreters](https://www.craftinginterpreters.com/), [Big-O Cheatsheet](https://www.bigocheatsheet.com/) y [Learn Git Branching](https://learngitbranching.js.org/).
