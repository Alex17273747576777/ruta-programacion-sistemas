# CheatSheet · Regex, Sistema Binario / Permisos UNIX y Nginx

| Área | Patrón / Orden | Qué resuelve o evita |
|---|---|---|
| **Regex segura** | `^[A-Za-z0-9_-]{3,32}$` | Ancla inicio/fin (`^...$`) y acota repeticiones para evitar *catastrophic backtracking* (ReDoS) |
| **Binario / Hex** | `0xFF == 0b11111111 == 255` | Conversión rápida de máscara de 8 bits (1 nibble hex = 4 bits) |
| **Permisos UNIX** | `chmod 750 script.sh` (`rwx r-x ---`) | Dueño=7 (`4+2+1`), Grupo=5 (`4+1`), Otros=0 (nunca `777` por pereza) |
| **Nginx Proxy** | `client_max_body_size 1m;` + `proxy_pass` | Corta cargas gigantes antes de saturar la aplicación |
| **Nginx Cabeceras** | `proxy_set_header X-Forwarded-Proto $scheme;` | Permite a la app saber si el cliente llegó por HTTPS |

## Comprobación rápida

```bash
python3 - << 'PY'
import re
assert re.fullmatch(r"[A-Za-z0-9_-]{3,32}", "sku-01")
assert int("0xFF", 16) == 0b11111111 == 255
print("Regex y binario OK")
PY
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** cuantificadores seguros en expresiones regulares, notación octal de permisos UNIX y directivas base de Nginx mediante [Regex101](https://regex101.com/), [RegexLearn](https://regexlearn.com/), [ExplainShell](https://explainshell.com/) y [Nginx Docs](https://nginx.org/en/docs/).
2. **Enseñarlo con palabras simples:**
   - Una **expresión regular** es una plantilla para revisar si un texto cumple un formato (como un código postal), pero si escribes comodines anidados sin límite (`(a+)+`), el buscador puede quedarse probando miles de millones de combinaciones con una sola frase larga.
   - Los **permisos en Linux** (`r=4, w=2, x=1`) son simplemente tres interruptores encendidos o apagados sumados para tres grupos: tú, tu equipo y los desconocidos.
3. **Identificar lagunas y volver a la fuente original:** cuando un patrón `.*` devuelva más texto del esperado (*greedy* vs *lazy* `.*?`) o cuando `nginx -t` falle por falta de punto y coma o ubicación de `proxy_pass`, prueba el patrón paso a paso en [Regex101](https://regex101.com/) y revisa [Nginx Docs](https://nginx.org/en/docs/).
4. **Simplificar y revisar con analogías:** *analogía de la cerradura de tres diales y el colador:* los permisos `750` son tres ruedas numéricas para dueño/grupo/resto; una regex es un colador con forma exacta: si dejas agujeros enormes (`.*`), cuela piedras, y si encadenas bucles dentro de bucles, atascas el colador con una palabra larga. (*Límite:* las expresiones regulares validan sintaxis de texto, no reemplazan un parser completo para HTML o JSON).
