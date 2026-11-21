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
Código, instrucciones, al menos seis pruebas automatizadas con `unittest`, un ejemplo de ejecución y la **ficha Feynman completa (4 pasos)** explicando tipos, flujo y guardado seguro. Demuestra ambas aplicaciones desde una carpeta nueva; aplica la rúbrica del README.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** tipos de dato (texto vs número decimal exacto `Decimal`), flujo condicional y reemplazo seguro de archivos JSON, apoyándote en el Tutorial oficial de Python.
2. **Enseñarlo con palabras simples (sin jerga):**
   - Para la computadora, `"2"` escrito entre comillas es un dibujo de un carácter (como una etiqueta pegada en una caja), mientras que `2` es una cantidad con la que puedes sumar y multiplicar. Si sumas dos etiquetas `"2" + "2"`, juntas los dibujos (`"22"`), no las cantidades (`4`).
   - Guardar en un archivo nuevo antes de borrar el viejo evita quedarte sin libreta si se va la luz a mitad de una frase: primero escribes la hoja limpia aparte y, solo cuando terminas, la cambias por la anterior.
3. **Identificar lagunas y volver a la fuente original:**
   - *Laguna típica:* «¿Por qué `0.1 + 0.2` da `0.30000000000000004` en Python si en papel da `0.3`?» y «¿Por qué cambiar un archivo en la misma carpeta es distinto a copiarlo desde otro disco?»
   - *Regreso a la fuente:* consulta en el [Tutorial oficial de Python (Floating Point Arithmetic / `decimal`)](https://docs.python.org/3/tutorial/floatingpoint.html) cómo la base binaria aproxima decimales y por qué `Decimal` conserva centavos exactos, y revisa `os.replace` frente a descarga a disco (`os.fsync`).
4. **Simplificar y revisar con analogías:**
   - *Analogía del dinero y la moneda:* usar flotantes binarios para dinero es como medir pesos exactos con una regla graduada en tercios: siempre sobra o falta un milímetro; `Decimal` es contar monedas enteras una por una.
   - *Analogía de la pizarra:* reemplazar de golpe sobre el archivo original es borrar la pizarra mientras alguien aún copia la tarea; escribir en una hoja temporal y colgarla encima solo cuando está completa garantiza que nunca quede media lista rota (aunque sin garantizar que el edificio no se quede sin luz antes de guardar en disco).
   - *Comprobación del estudiante:* reescribe estos cuatro pasos en tus propias palabras en el README de tu proyecto sin copiar definiciones técnicas.

## Recursos
- [Tutorial oficial de Python](https://docs.python.org/3/tutorial/) — consulta tipos, control de flujo y funciones; presupone nociones previas.
- [Pro Git](https://git-scm.com/book/en/v2) — capítulos 1–2, historial y commits. No subas secretos.
