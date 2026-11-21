# CheatSheet · Estructuras de Datos, Complejidad Big-O y Caché CPU

| Estructura | Búsqueda promedio | Inserción | Cuándo elegirla en sistemas |
|---|---|---|---|
| **Array contiguo (`list`/`vector`)** | `O(1)` por índice / `O(n)` por valor | `O(1)` amortizado al final | Por defecto cuando iteras mucho: aprovecha caché L1/L2 contigua |
| **Tabla hash (`dict`/`HashMap`)** | `O(1)` amortizado | `O(1)` amortizado | Índices por ID, cachés, conjuntos de vistos (`set`) |
| **Cola / Deque (`collections.deque`)** | `O(1)` extremos | `O(1)` extremos | Colas FIFO sin desplazar todo el array (`list.pop(0)` es `O(n)`) |
| **Montículo (*Heap* / `heapq`)** | `O(1)` mínimo | `O(log n)` | Planificadores por prioridad, *timers* y *top-K* |
| **Árbol B / B+ (en disco / SQL)** | `O(log n)` pocas lecturas | `O(log n)` | Índices de PostgreSQL y SQLite por bloques de página |

## Comprobación rápida

```bash
python3 - << 'PY'
from collections import deque
q = deque(["t1", "t2"])
q.append("t3")
assert q.popleft() == "t1"
print("Deque FIFO O(1) OK")
PY
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** coste temporal y espacial (Big-O), diferencia entre complejidad asintótica y localidad de caché en memoria mediante [Big-O Cheatsheet](https://www.bigocheatsheet.com/) y [TeachYourselfCS](https://teachyourselfcs.com/).
2. **Enseñarlo con palabras simples:** quitar el primer elemento de una lista normal (`pop(0)`) obliga a mover una silla atrás a todas las demás personas de la fila (*O(n)*); usar una cola doble (`deque`) es mover solo el cartel de «primero de la fila» (*O(1)*). Y recorrer datos seguidos en un array es más rápido que saltar por punteros sueltos aunque ambos sean *O(n)*, porque la CPU lee bloques enteros vecinos.
3. **Identificar lagunas y volver a la fuente original:** cuando veas que un algoritmo teóricamente *O(n log n)* con muchos punteros pequeños va más lento que un vector contiguo en arrays pequeños, vuelve a [CPU Land](https://cpu.land/) y [Big-O Cheatsheet](https://www.bigocheatsheet.com/) para medir aciertos de caché y factores constantes reales.
4. **Simplificar y revisar con analogías:** *analogía del estante seguido frente a las notas por toda la casa:* leer un array contiguo es leer un libro página tras página en la misma mesa; seguir nodos enlazados por el heap es ir leyendo pistas pegadas en habitaciones distintas: aunque cuentes el mismo número de frases (*O(n)*), caminar entre habitaciones cuesta mucho más tiempo. (*Límite:* Big-O describe cómo crece el coste cuando $n$ se vuelve muy grande, no sustituye medir con datos reales cuando $n$ es pequeño).
