# CheatSheet · Python, Tipos Exactos y Persistencia Segura

| Qué necesitas | Patrón seguro | Error clásico que evita |
|---|---|---|
| Dinero / decimales exactos | `Decimal("0.1") + Decimal("0.2")` | `0.1 + 0.2 == 0.30000000000000004` |
| Parsear entrada matemática | Operaciones explícitas o `ast.literal_eval` | Ejecución arbitraria con `eval()` |
| Máximo de lista | `mayor = xs[0]` tras validar `if not xs:` | Inicializar `mayor = 0` con negativos |
| Guardar JSON sin corrupción | Escribir temporal en mismo dir + `os.fsync` + `os.replace` | Archivo truncado a la mitad si cae el proceso |
| Pruebas reproducibles | `unittest` con reloj/repositorio inyectado | Tests acoplados a hora del sistema o red externa |

## Comprobación rápida

```bash
python3 -c 'from decimal import Decimal; assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")'
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** tipos exactos (`Decimal`) y escritura atómica (`os.replace`) en la documentación oficial de Python.
2. **Enseñarlo con palabras simples:** las comillas guardan letras, los enteros guardan cuentas exactas y `Decimal` guarda centavos sin redondeos escondidos; escribir primero en una hoja aparte evita romper tu archivo bueno si falla a mitad de camino.
3. **Identificar lagunas y volver a la fuente original:** si dudas por qué `os.replace` falla entre discos distintos o qué hace `flush()` frente a `fsync()`, consulta `docs.python.org/3/library/os.html`.
4. **Simplificar y revisar con analogías:** *analogía del borrador y el original:* nunca taches sobre el contrato firmado; escribe el borrador nuevo completo en la misma carpeta y cámbialo de golpe cuando esté terminado. (*Límite:* `os.replace` garantiza cambio atómico de puntero, no protege contra disco dañado físicamente sin respaldo externo).
