# 1 · Fundamentos: instrucciones, decisiones y datos

## Objetivo
Explicar y usar variables, tipos, expresiones, condiciones, bucles, funciones, listas y diccionarios. Un programa es una receta precisa: si una instrucción es ambigua, la máquina no adivina. Primer paso: escribe en papel cómo sumar dos números y qué harás si uno no es número.

## Proyecto A: calculadora CLI
Pide dos números y una operación (`+`, `-`, `*`, `/`); muestra resultado o error sin traza. Usa `Decimal` para dinero y valida división por cero. No evalúes cadenas arbitrarias con `eval`.

**Contrato:** `2 + 3 → 5`; `1 / 0 → error` y continúa o termina con estado no exitoso; operación desconocida no modifica datos. Explica diferencia entre texto `"2"` y número 2.

## Proyecto B: agenda CLI
Agrega, busca, lista y elimina contactos sintéticos. Cada contacto tiene ID estable, nombre no vacío y teléfono como texto. Persiste JSON en archivo local; si no existe, inicia vacío; si está corrupto, informa y no lo sobrescribe. Guarda primero a archivo temporal en el mismo directorio y reemplaza el original tras terminar la escritura. Explica que reemplazo atómico y durabilidad ante apagón son propiedades distintas.

## Ejercicios y evaluación

1. **Paridad:** recibe entero y devuelve par/impar, incluyendo negativos. Comprobar `0`, `-3`, `8`; esperado par, impar, par.
2. **Suma de lista:** implementa bucle sin `sum`. `[] → 0`, `[1,-2,4] → 3`; explica inicialización y por qué se termina.
3. **Máximo:** determina máximo de lista no vacía; `[-5,-2] → -2`. Vacía: devuelve error explícito; no uses 0 como máximo inicial.
4. **Conteo:** cuenta palabras en `"sol luna sol"` → `{sol:2,luna:1}`. Documenta cómo tratas mayúsculas y puntuación; prueba cadena vacía.
5. **Validación:** nombre vacío o espacios debe rechazarse; un teléfono `"00123"` mantiene ceros. Comprueba entradas demasiado largas con un límite documentado.
6. **Persistencia:** crea dos contactos, cierra y vuelve a abrir; identifica los dos. Alimenta JSON truncado: debe rechazar sin perder la copia corrupta.

## Entrega y avance
Código, instrucciones, al menos seis pruebas automatizadas con `unittest` y un ejemplo de ejecución. Explica flujo, tipos y cómo manejar un error. Demuestra ambas aplicaciones desde una carpeta nueva; aplica la rúbrica del README.

## Recursos
- [Tutorial oficial de Python](https://docs.python.org/3/tutorial/) — consulta tipos, control de flujo y funciones; presupone nociones previas.
- [Pro Git](https://git-scm.com/book/en/v2) — capítulos 1–2, historial y commits. No subas secretos.
