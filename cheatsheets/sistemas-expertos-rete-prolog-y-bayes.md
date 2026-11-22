# CheatSheet · Prolog (Unificación), Rete, Ontologías OWL y Bayes

> Referencia rápida del **Máster en Ingeniería de Sistemas Expertos** · Ver [Guía 10](../guias/10-logica-primer-orden-unificacion-y-resolucion.md) y [Guía 11](../guias/11-algoritmo-rete-ontologias-owl-y-redes-bayesianas.md).

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** Elegir la herramienta simbólica o probabilística correcta entre **LPO/Prolog**, **motores Rete**, **ontologías OWL** y **Redes Bayesianas**, y validar su base de reglas con V&V.
2. **Enseñarlo con palabras simples:** Usa **Prolog/Unificación** cuando necesitas consultar relaciones con variables; usa **Rete** cuando miles de eventos disparan reglas en tiempo real; usa **OWL** cuando necesitas un diccionario formal compartido; y usa **Redes Bayesianas** cuando cada pista cambia matemáticamente la probabilidad de varias causas posibles.
3. **Identificar lagunas y volver a la fuente original:** Nunca uses probabilidades inventadas sin calibrar ni desactives el *occurs check* si recibes términos anidados desconocidos. Tampoco asumas que un grafo RDF/OWL rechaza un dato faltante como falso: bajo Mundo Abierto solo significa *"desconocido hasta nuevo axioma"*.
4. **Simplificar y revisar con analogías claras:** Es la **caja de herramientas de un taller aeronáutico**: no usas un martillo para medir presión hidráulica ni un calibrador para atornillar. *Analogía operativa:* Prolog es un detective que prueba hipótesis; Rete es un panel de alarmas cableado por dependencias; Bayes es un actuario calculando riesgo exacto. *Límite de la analogía:* un sistema híbrido real combina varias piezas bajo una capa común de pruebas automatizadas (V&V).

---

## Tabla de decisión rápida

| Necesidad del sistema | Tecnología adecuada | Algoritmo clave | Riesgo principal |
| :--- | :--- | :--- | :--- |
| Consultar relaciones con variables y recursión | Lógica de 1er Orden / Prolog | Unificación de Robinson + SLD | Bucles sin límite de profundidad / sin *occurs check* |
| Evaluar >200 reglas ante flujo continuo de hechos | Motor de Producción (CLIPS / Drools) | Red Rete (memoria alfa + beta) | Explosión de combinaciones en nodos beta |
| Vocabulario formal interoperable y jerarquías | RDF / RDFS / OWL 2 | Razonador Description Logic | Confundir Mundo Abierto (OWA) con SQL (Mundo Cerrado) |
| Diagnóstico probabilístico con causas múltiples | Red Bayesiana (DAG) | Regla de Bayes / Eliminación de variables | Tablas CPT exponenciales si un nodo tiene muchos padres |
| Auditar reglas antes de pasar a producción | V&V estático + pruebas unitarias | Análisis de conflicto, subsunción y ciclos | Falsos positivos si hay prioridades explícitas no modeladas |

## Fórmula clave · Teorema de Bayes en diagnóstico

```text
P(Causa | Evidencia) = [ P(Evidencia | Causa) * P(Causa) ] / P(Evidencia)
```

En una red `Causa -> Síntoma_1`, `Causa -> Síntoma_2`, los síntomas son condicionalmente independientes dada la `Causa`:

```text
P(C, S1, S2) = P(C) * P(S1 | C) * P(S2 | C)
```
