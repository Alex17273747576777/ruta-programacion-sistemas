# Guía 09 · Ingeniería de Sistemas Expertos, Motores de Inferencia y Lógica Difusa

> **Nivel:** De novato a profesional (núcleo del **Máster en Ingeniería de Sistemas Expertos**).  
> **Laboratorio asociado:** [`laboratorios/sistema_experto/motor_inferencia.py`](../laboratorios/sistema_experto/motor_inferencia.py)

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** Un **Sistema Experto (SE)** emula el razonamiento de un especialista humano en un dominio acotado **separando el conocimiento del mecanismo de inferencia**. Se compone de cinco piezas: **Base de Conocimiento (KB)** con reglas `SI antecedentes ENTONCES consecuente [CF]` y ontologías (`RDF`/`OWL`); **Base de Hechos / Memoria de Trabajo (WM)**; **Motor de Inferencia** (*Forward Chaining* guiado por datos y *Backward Chaining* guiado por metas, con **refracción** y algoritmo **Rete**); **Módulo de Explicación (*Why* / *How*)**; y manejo de incertidumbre con **Factores de Certeza MYCIN** (`CF_comb = CF1 + CF2 * (1 - CF1)` para `CF1, CF2 > 0`) y **Lógica Difusa (Zadeh / Mamdani)** mediante fusificación, reglas `MIN`/`MAX` y defusificación por centroide.
2. **Enseñarlo con palabras simples:** En vez de enterrar cientos de `if/else` rígidos dentro del código, guardas las normas del especialista en un manual limpio (*Base de Conocimiento*), anotas los síntomas observados hoy en una pizarra (*Memoria de Trabajo*) y dejas que un detective automático (*Motor de Inferencia*) cruce ambos. Con **encadenamiento hacia adelante**, lee los síntomas y deduce todo lo que implican; con **encadenamiento hacia atrás**, parte de una sospecha concreta (*meta*) y revisa solo las pistas necesarias para probarla o descartarla. Para no decir *"seguro 100 %"* cuando hay duda, sumamos pistas con Factores de Certeza sin pasar de `1.0`, y para variables continuas (*humedad*, *temperatura*) usamos Lógica Difusa.
3. **Identificar lagunas y volver a la fuente original:** Las tres lagunas más frecuentes al pasar de novato a ingeniero de sistemas expertos son: (a) olvidar la **refracción**, provocando bucles infinitos al redisparar una misma regla sobre los mismos hechos; (b) sumar `CF` aritméticamente (`0.6 + 0.7 = 1.3`, inválido fuera de `[-1, +1]`); y (c) creer que un LLM reemplaza al motor simbólico en entornos críticos, cuando el enfoque robusto **neuro-simbólico** usa el LLM para extraer hechos estructurados y el motor simbólico para inferir con trazabilidad determinista. Para comprobarlo en código ejecutable, revisa [`laboratorios/sistema_experto/motor_inferencia.py`](../laboratorios/sistema_experto/motor_inferencia.py) y [`laboratorios/sistema_experto/test_sistema_experto.py`](../laboratorios/sistema_experto/test_sistema_experto.py).
4. **Simplificar y revisar con analogías claras:** La analogía clásica es la del **detective con su reglamento** o la del **cocinero**: *Forward Chaining* abre la nevera, ve qué ingredientes hay (*hechos*) y descubre qué platos puede preparar (*conclusiones*); *Backward Chaining* decide preparar lasaña (*meta*) y verifica qué ingredientes le faltan o cómo fabricarlos paso a paso. *Límite de la analogía:* en una receta normal la presencia de un ingrediente es binaria (hay o no hay), mientras que en un sistema experto real conviven **grados de certeza (`CF`)**, **conjuntos difusos solapados** (ducha tibia = `70 %` tibia + `30 %` fría), **prioridades de conflicto** y **trazas formales auditables** (*How/Why*).

---

## Arquitectura y estrategia de diseño (de novato a profesional)

| Componente | Función exacta | Antipatrones a evitar |
| :--- | :--- | :--- |
| **Base de Conocimiento** | Reglas `IF-THEN`, restricciones y ontologías (`RDF`/`OWL`) | Mezclar reglas de negocio con UI, SQL o controladores HTTP |
| **Memoria de Trabajo** | Hechos observados + hechos derivados en la sesión | Mutar hechos sin registrar procedencia (*How*) ni marca de tiempo |
| **Motor Forward** | Monitoreo continuo, eventos en streaming, alertas | Re-evaluar sin refracción (bucle infinito) |
| **Motor Backward** | Diagnóstico dirigido, verificación de cumplimiento | Recursión sin conjunto `visitados` (desbordamiento de pila) |
| **Incertidumbre MYCIN** | `CF ∈ [-1, +1]`, combinación asintótica | Confundir `CF` con probabilidad bayesiana estricta |
| **Controlador Difuso** | Fusificación → Reglas Mamdani → Defusificación centroide | Conjuntos sin solapamiento (zonas muertas) |
| **Neuro-Simbólico** | LLM extrae entidades → Motor simbólico valida y decide | Dejar decisiones normativas sin verificación de reglas |
