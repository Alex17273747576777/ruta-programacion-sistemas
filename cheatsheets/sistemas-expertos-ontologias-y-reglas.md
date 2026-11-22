# CheatSheet · Sistemas Expertos, Ontologías y Reglas de Inferencia

> Referencia rápida del **Máster en Ingeniería de Sistemas Expertos**.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** Un motor de Sistemas Expertos desacopla **reglas/ontologías** (Base de Conocimientos) de **hechos observados** (Memoria de Trabajo) y del **Motor de Inferencia** (*Forward* guiado por datos, *Backward* guiado por metas, resolución de conflictos con algoritmo **Rete**). Maneja incertidumbre con **Factores de Certeza MYCIN** (`CF1 + CF2 * (1 - CF1)` si ambos > 0) y **Lógica Difusa Mamdani** (fusificación, reglas `MIN`/`MAX`, defusificación por centroide), además de conocimiento semántico con tripletas `RDF` (`Sujeto, Predicado, Objeto`) y `OWL`.
2. **Enseñarlo con palabras simples:** El **reglamento** vive separado del **árbitro**. Si anotas síntomas y deduces todo lo que implican, haces *Forward Chaining*; si partes de una sospecha y solo verificas lo necesario para probarla, haces *Backward Chaining*. La **refracción** impide repetir la misma regla sobre los mismos datos, y MYCIN suma pistas sin pasarse jamás de `1.0`.
3. **Identificar lagunas y volver a la fuente original:** Confundir `CF` con probabilidad bayesiana (`P(H|E)`), olvidar la detección de ciclos en búsqueda hacia atrás o dejar huecos entre conjuntos difusos (*bajo*, *medio*, *alto*) rompe la estabilidad del motor. Comprueba las fórmulas ejecutables en [`laboratorios/sistema_experto/motor_inferencia.py`](../laboratorios/sistema_experto/motor_inferencia.py).
4. **Simplificar y revisar con analogías claras:** *Forward* es una ficha médica completa que deduce todo automáticamente; *Backward* es una brújula que apunta a una sola enfermedad y pide solo las pruebas necesarias para confirmarla. *Límite de la analogía:* un médico real usa contexto clínico implícito, mientras el motor experto solo garantiza validez sobre las reglas y ontologías declaradas.

---

## Tabla de decisión rápida

| Situación real | Estrategia recomendada | Motivo |
| :--- | :--- | :--- |
| Sensores / logs en tiempo real | **Forward Chaining** (Rete) | Llegan hechos continuos y se requieren alertas inmediatas |
| Chatbot de soporte o diagnóstico | **Backward Chaining** (*Why/How*) | Parte de una hipótesis y solicita solo los datos faltantes |
| Múltiples evidencias inciertas | **MYCIN CF** o **Red Bayesiana** | Evita desbordar `[−1, 1]` al combinar pistas independientes |
| Variables físicas continuas | **Lógica Difusa Mamdani** | Transiciones suaves sin saltos bruscos de umbral |
| Texto no estructurado + normativa | **Arquitectura Neuro-Simbólica** | LLM extrae hechos → Motor simbólico valida con trazabilidad |
