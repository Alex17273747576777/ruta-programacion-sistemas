# Guía 11 · Algoritmo Rete, Ontologías OWL, Redes Bayesianas y V&V

> Nivel: **Experto / Máster en Ingeniería de Sistemas Expertos** · Laboratorio asociado: [red_bayesiana_y_vv.py](../laboratorios/sistemas_expertos_avanzados/red_bayesiana_y_vv.py)

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** Escalar sistemas expertos a producción mediante el **algoritmo Rete** (evaluación incremental de reglas de producción), **ontologías formales RDF/RDFS/OWL** (conocimiento semántico bajo suposición de mundo abierto), **Redes Bayesianas** (inferencia probabilística exacta en grafos acíclicos dirigidos) y **Verificación y Validación (V&V)** de bases de conocimiento antes del despliegue.
2. **Enseñarlo con palabras simples:** Si tienes 5.000 reglas y cambia un solo dato, volver a revisar todas las reglas desde cero en cada paso es lentísimo. El algoritmo **Rete** guarda una memoria intermedia de qué condiciones ya cumplen los datos actuales y solo recalcula las reglas tocadas por el dato nuevo. Por otro lado, una **ontología OWL** define el vocabulario oficial y las jerarquías del dominio (por ejemplo, que todo *Servidor Crítico* es un *Nodo*, pero sin asumir que lo no escrito es falso: *Mundo Abierto*). Cuando el problema tiene incertidumbre estadística real y dependencias causales, las **Redes Bayesianas** reemplazan los pesos heurísticos por probabilidades condicionales exactas. Finalmente, **V&V** inspecciona la base de reglas antes de salir a producción para detectar reglas contradictorias, duplicadas o imposibles de disparar.
3. **Identificar lagunas y volver a la fuente original:** Una confusión frecuente es mezclar **Factores de Certeza MYCIN** con **Redes Bayesianas**: MYCIN asume independencia condicional heurística entre reglas y falla cuando existen causas comunes (*explaining away*), mientras que una Red Bayesiana modela explícitamente la estructura causal DAG y la **d-separación**. Otra laguna común es olvidar que en OWL rige la **Open World Assumption (OWA)**: si no consta que un usuario tenga permiso, OWL no lo declara falso automáticamente salvo que exista un axioma de disjunción o cierre explícito.
4. **Simplificar y revisar con analogías claras:** **Rete** es como una **hoja de cálculo bien diseñada**: cuando cambias la celda `B4`, no vuelve a multiplicar toda la contabilidad del año, solo recalcula las fórmulas que dependen de `B4`. Una **Red Bayesiana** es un **tablero de cañerías con llaves de probabilidad**: abrir o observar una evidencia cambia la presión exacta en los nodos conectados aguas abajo y aguas arriba (diagnóstico causal). *Límite de la analogía:* en Rete, cuando el orden de cambios es muy volátil, mantener las memorias alfa y beta consume RAM adicional a cambio de velocidad en CPU.

---

## Arquitectura comparada en Sistemas Expertos de Producción

| Componente | Problema que resuelve | Cuándo usarlo | Punto crítico de ingeniería |
| :--- | :--- | :--- | :--- |
| **Red Rete (alfa / beta)** | Evitar reevaluar todas las reglas en cada ciclo | Cientos o miles de reglas sobre memoria de trabajo cambiante | Uso de memoria en nodos beta si hay joins poco selectivos |
| **Ontologías RDF / OWL** | Taxonomías, herencia de clases y axiomas lógicos | Integración semántica, catálogos normativos, Grafos de Conocimiento | Mundo Abierto (OWA) y costo de razonadores DL (`O(exp)` en perfiles expresivos) |
| **Red Bayesiana (DAG)** | Incertidumbre causal con múltiples evidencias | Diagnóstico médico, riesgo técnico, análisis de causa raíz | Requiere tablas CPT bien calibradas y evitar ciclos |
| **V&V (Verificación / Validación)** | Calidad antes de producción | Toda base de conocimiento crítica o auditable | Detectar subsunción, conflicto directo, ciclos y reglas muertas |

---

## Reglas de Verificación Formal (V&V) que debes automatizar en CI

1. **Conflicto directo:** dos reglas comparten exactamente las mismas condiciones pero concluyen hechos incompatibles (o valores opuestos del mismo atributo).
2. **Redundancia / Subsunción:** la regla `R2` exige más condiciones que `R1` para concluir exactamente lo mismo (`R1` ya se habría disparado antes).
3. **Ciclos en encadenamiento:** `A -> B` y `B -> A` sin control de visitados ni monotonicidad.
4. **Reglas inalcanzables:** premisas que ni provienen de entradas observables ni son concluidas por ninguna otra regla.

Consulta la síntesis operativa en el [CheatSheet de Rete, Prolog y Redes Bayesianas](../cheatsheets/sistemas-expertos-rete-prolog-y-bayes.md) y el laboratorio [red_bayesiana_y_vv.py](../laboratorios/sistemas_expertos_avanzados/red_bayesiana_y_vv.py).
