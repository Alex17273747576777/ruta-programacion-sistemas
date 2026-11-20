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
Script de migración, instrucciones para base temporal, tests de integración y reporte del experimento concurrente. La base usada en pruebas debe ser desechable y configurada por variables, no credenciales en Git. Demuestra los seis criterios.

## Recursos
- [Tutorial PostgreSQL](https://www.postgresql.org/docs/17/tutorial.html) — consultas, integridad y transacciones; consulta la versión instalada.
- [PostgreSQL: aislamiento](https://www.postgresql.org/docs/17/transaction-iso.html) — anomalías y comportamiento del motor.
