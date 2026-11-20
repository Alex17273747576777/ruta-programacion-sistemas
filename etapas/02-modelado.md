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
Al menos ocho tests unitarios, dos de integración de persistencia, y un dibujo de dependencias. Ejecuta suite desde limpio y conserva su salida. Demuestra invariantes anteriores y explica una limitación del diseño. Aplica rúbrica común.

## Recursos
- [Python: clases](https://docs.python.org/3/tutorial/classes.html) — objetos, alcance y métodos.
- [Python unittest](https://docs.python.org/3/library/unittest.html) — aislamiento y aserciones.
- [Pro Git: ramas](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) — cambios revisables.
