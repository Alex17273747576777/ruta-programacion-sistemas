# 3 · Datos, SQL y concurrencia

## Objetivo
Guardar datos coherentes cuando varios procesos operan a la vez. Una transacción es una unidad de decisión: si falla una parte, el sistema no debe fingir que todo terminó. Las garantías concretas dependen de aislamiento y motor.

## Proyecto: inventario transaccional
PostgreSQL local y datos sintéticos. Crea productos (ID, SKU único, cantidad entera no negativa) y movimientos (ID, producto, delta, clave de operación única). Implementa alta, entrada, salida, consulta e historial. Una salida nunca produce negativo. Escribe migración y prueba de aplicación sobre base vacía. Usa parámetros SQL, no concatenación de entrada.

**Contrato:** producto con cantidad 3, dos salidas concurrentes de 2: solo una confirma; cantidad final 1 y un solo movimiento exitoso. Utiliza transacción y actualización condicional `UPDATE ... WHERE cantidad >= ... RETURNING` o bloqueo equivalente; registra el movimiento en la misma transacción. Una clave de operación repetida no debe volver a descontar.

## Ejercicios y criterios

1. Crea clave primaria, `UNIQUE` de SKU, `CHECK(cantidad >= 0)` y clave foránea. Demuestra que la base rechaza violaciones incluso sin la aplicación.
2. Prueba `BEGIN`, modifica y `ROLLBACK`: la cantidad original permanece y no hay movimiento. No llames prueba de rollback a un mock.
3. Ejecuta el contrato concurrente con dos conexiones reales y barrera; repítelo y verifica invariantes, no solo un orden de logs.
4. Repite misma clave de operación: resultado sin doble descuento; si la misma clave tiene contenido diferente, rechaza el conflicto.
5. Consulta productos y suma de movimientos; determina discrepancias. Crea un índice y compara `EXPLAIN` con datos de prueba; no prometas mejora sin medirla.
6. Fuerza error entre actualizar cantidad y registrar movimiento: confirma rollback de ambos. Identifica qué cambia si las dos escrituras se separan.

## Entrega y avance
Script de migración, instrucciones para base temporal, tests de integración, reporte del experimento concurrente y la **ficha Feynman completa (4 pasos)** sobre transacciones, bloqueos/condiciones atómicas e idempotencia. La base usada en pruebas debe ser desechable y configurada por variables, no credenciales en Git. Demuestra los seis criterios.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** atomicidad transaccional, condiciones de carrera al descontar inventario y claves de operación para evitar dobles descuentos, estudiados en el Tutorial y la guía de aislamiento de PostgreSQL.
2. **Enseñarlo con palabras simples (sin jerga):**
   - Imagina una caja con 3 entradas de cine y dos taquilleros mirando la caja al mismo tiempo. Si los dos cuentan «hay 3, así que vendo 2», entre ambos prometen 4 entradas cuando solo había 3.
   - Para evitarlo, la base de datos funciona como un turno único en la ventanilla: dice «solo resta 2 si todavía quedan 2 o más, y anota el recibo en el mismo paso». Si algo falla a mitad de camino, deshace todo como si nadie hubiera tocado la caja.
3. **Identificar lagunas y volver a la fuente original:**
   - *Laguna típica:* «¿Por qué leer `SELECT cantidad` en Python y luego hacer `UPDATE` falla bajo dos conexiones simultáneas, aunque una sola conexión siempre funcione?» y «¿Por qué un reintento con la misma clave no debe volver a restar?»
   - *Regreso a la fuente:* revisa [PostgreSQL: aislamiento de transacciones](https://www.postgresql.org/docs/17/transaction-iso.html) (fenómeno *lost update* / *read committed* vs `UPDATE ... WHERE cantidad >= ...` y restricciones `UNIQUE`) para comprobar por qué la condición debe evaluarse dentro de la propia sentencia en el motor.
4. **Simplificar y revisar con analogías:**
   - *Analogía del billete numerado y la puerta giratoria:* una transacción es una puerta giratoria donde entran juntos el descuento y el recibo: o cruzan los dos, o ambos se quedan afuera. La clave única de operación es el número de serie del ticket: si el cliente vuelve con la misma foto del recibo porque se cortó la llamada, la taquilla reconoce el número y le muestra el mismo recibo en vez de cobrarle otra vez. (*Límite de la analogía:* niveles de aislamiento distintos en bases diferentes cambian qué filas se bloquean).
   - *Comprobación del estudiante:* explica por escrito a alguien sin formación técnica qué ocurrió en tu prueba concurrente con dos conexiones reales y qué habría pasado si hubieras separado la resta del registro del movimiento.

## Recursos y práctica activa (fuentes oficiales + FMHY.net)
- Implementación y pruebas de concurrencia real: [`proyectos/03_datos/`](../proyectos/03_datos/) (`python3 -m unittest proyectos/03_datos/test_etapa03_concurrencia.py -v`) + [`schema_postgres.sql`](../proyectos/03_datos/schema_postgres.sql).
- Hoja rápida: [CheatSheet SQL y transacciones](../cheatsheets/sql-y-transacciones.md).
- [Tutorial PostgreSQL](https://www.postgresql.org/docs/17/tutorial.html) — consultas, integridad y transacciones; consulta la versión instalada.
- [PostgreSQL: aislamiento](https://www.postgresql.org/docs/17/transaction-iso.html) — anomalías y comportamiento del motor.
- **Recursos activos de [FMHY.net](https://fmhy.net/developer-tools):** [Select Star SQL](https://selectstarsql.com/), [SQLBolt](https://sqlbolt.com/), [SQL Noir](https://www.sqlnoir.com/), [DB Browser for SQLite](https://sqlitebrowser.org/), [DBeaver](https://dbeaver.io/), [DuckDB](https://duckdb.org/) y [ChartDB](https://chartdb.io/).
