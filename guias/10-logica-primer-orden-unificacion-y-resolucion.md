# Guía 10 · Lógica de Primer Orden, Unificación y Resolución SLD (Prolog)

> Nivel: **Experto / Máster en Ingeniería de Sistemas Expertos** · Laboratorio asociado: [unificador_prolog.py](../laboratorios/sistemas_expertos_avanzados/unificador_prolog.py)

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** Pasar de la lógica proposicional (`cpu_100 -> alerta`) a la **Lógica de Primer Orden (LPO)** con predicados, variables y términos compuestos (`fallo(nodo_a, disco)`, `depende(servicio_x, nodo_a)`), ejecutando deducciones mediante el algoritmo de **unificación de Robinson** (con *occurs check*) y **resolución SLD** sobre cláusulas de Horn.
2. **Enseñarlo con palabras simples:** La lógica proposicional solo sabe manejar etiquetas sueltas y fijas; si tienes mil servidores, tendrías que escribir mil reglas repetidas. La Lógica de Primer Orden usa **plantillas con huecos (variables)** como `critico(S) :- depende(S, N), caido(N)`. **Unificar** es encajar una ficha concreta en la plantilla buscando qué valor debe tomar cada variable para que dos expresiones queden idénticas, sin crear bucles infinitos (`X = f(X)`, bloqueado por el *occurs check*). **Resolución SLD** es ir resolviendo metas de izquierda a derecha mediante búsqueda con vuelta atrás (*backtracking*) hasta que no queden submetas por probar.
3. **Identificar lagunas y volver a la fuente original:** Un error clásico en implementaciones ingenuas de Prolog es omitir el *occurs check* al unificar `X` con `lista(X)` por velocidad (`O(n)` frente a `O(1)`), lo que produce estructuras cíclicas infinitas y cuelgues silenciosos en motores de inferencia. Otra laguna habitual es olvidar la **renombración de variables** (*standardizing apart*) antes de aplicar una cláusula: si dos reglas usan la variable `X`, mezclar sus entornos corrompe la sustitución resultante.
4. **Simplificar y revisar con analogías claras:** Piensa en la unificación como un **contrato con espacios en blanco** donde dos partes rellenan sus huecos simultáneamente: si una dice `contrato(servidor_1, Y)` y la otra dice `contrato(X, puerto_5432)`, ambas coinciden en cuanto `X = servidor_1` e `Y = puerto_5432`. El *occurs check* equivale a prohibir escribir *"el Anexo A contiene el Contrato entero incluyendo el Anexo A"*, porque jamás podrías terminar de leerlo. *Límite de la analogía:* un contrato en papel no hace *backtracking*; la resolución SLD sí deshace asignaciones en una rama fallida para probar automáticamente la siguiente regla compatible.

---

## De proposiciones fijas a cláusulas de Horn

| Elemento | Ejemplo | Significado en el motor |
| :--- | :--- | :--- |
| **Átomo / Constante** | `nodo_1`, `5432` | Entidad concreta inmutable |
| **Variable** | `X`, `Servicio`, `N` | Incógnita por ligar durante la unificación |
| **Término compuesto** | `puerto(tcp, 443)` | Estructura anidada con functor y aridad (`puerto/2`) |
| **Hecho (cláusula unitaria)** | `caido(bd_primaria).` | Cláusula de Horn sin cuerpo (siempre verdadera) |
| **Regla** | `afectado(S) :- usa(S, B), caido(B).` | Cabeza verdadera si se prueban todas las submetas del cuerpo |

---

## Reglas prácticas de ingeniería

- Renombra siempre las variables de cada cláusula (`X -> X_1`) antes de unificar para aislar contextos de llamada.
- Activa el **occurs check** siempre que recibas términos externos no confiables o grafos simbólicos arbitrarios.
- Usa un límite explícito de profundidad en resolución SLD para prevenir recursión infinita ante reglas simétricas (`conecta(A, B) :- conecta(B, A)`).
- Complementa la teoría con la [Guía 09 · Motores de Inferencia y Lógica Difusa](09-sistemas-expertos-motores-inferencia-y-logica-difusa.md) y la [Guía 11 · Rete, Ontologías OWL y Redes Bayesianas](11-algoritmo-rete-ontologias-owl-y-redes-bayesianas.md).
