# CheatSheet · SQL, Integridad y Transacciones

| Necesidad | Patrón seguro | Error clásico que evita |
|---|---|---|
| Evitar inyección SQL | Consultas parametrizadas (`?` o `$1`) | Concatenar cadenas `f"... '{usuario}'"` |
| Descontar stock concurrente | `UPDATE ... SET cantidad = cantidad - ? WHERE id = ? AND cantidad >= ?` | Leer `SELECT` en app y restar después (*lost update*) |
| Evitar cobro/movimiento doble | Columna `clave_operacion TEXT UNIQUE` + `payload_hash` | Reintento de red que duplica descuento |
| Probar planes de consulta | `EXPLAIN QUERY PLAN ...` / `EXPLAIN ANALYZE` | Crear índices a ciegas sin medir |
| Integridad en SQLite | `PRAGMA foreign_keys = ON;` por conexión | Claves foráneas ignoradas por defecto en SQLite |

## Comprobación rápida

```bash
python3 -m unittest proyectos/03_datos/test_etapa03_concurrencia.py -v
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** atomicidad de sentencias SQL y restricciones en el motor (`CHECK`, `UNIQUE`, `FOREIGN KEY`).
2. **Enseñarlo con palabras simples:** la base de datos no es una hoja tonta; es un contador estricto que rechaza números negativos y comprueba el saldo en el mismo instante en que resta.
3. **Identificar lagunas y volver a la fuente original:** cuando dudes sobre niveles de aislamiento (*Read Committed* vs *Serializable*), vuelve a [PostgreSQL: aislamiento](https://www.postgresql.org/docs/17/transaction-iso.html) y [SQLBolt](https://sqlbolt.com/).
4. **Simplificar y revisar con analogías:** *analogía de la ventanilla única:* en lugar de preguntar cuánto queda, dar media vuelta y volver a pedir dos entradas, pides «dame dos si todavía hay dos» en una sola frase al taquillero. (*Límite:* las transacciones locales no cubren llamadas HTTP externas realizadas dentro de la misma función).
