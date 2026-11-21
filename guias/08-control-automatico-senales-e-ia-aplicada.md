# Guía 08 · Control Automático (PID), Señales e IA Aplicada con Límites Medibles

> **Objetivo:** cerrar el puente hacia ingeniería de control, señales e inteligencia artificial aplicada con simulaciones reproducibles en Python y sin cajas negras mágicas.

## 1. Control automático: lazo abierto vs lazo cerrado (PID)

- **Lazo abierto:** aplicas una potencia fija esperando acertar (como una tostadora por tiempo: si el pan estaba congelado, sale frío).
- **Lazo cerrado (PID):** mides la salida real con un sensor, calculas el error $e(t) = \text{objetivo} - \text{medida}$, y ajustas la acción sumando tres términos:
  - **Proporcional ($K_p$):** empuja según el error actual (demasiado alto provoca oscilaciones).
  - **Integral ($K_i$):** corrige el error pequeño acumulado en el tiempo (requiere *anti-windup* para no saturar).
  - **Derivativo ($K_d$):** frena cuando te acercas rápido al objetivo (sensible al ruido del sensor).

## 2. Muestreo de señales e IA aplicada con rigor

1. **Muestreo (Nyquist):** para reconstruir una señal de frecuencia máxima $f_{\max}$ debes muestrear al menos a más de $2 f_{\max}$ (en la práctica, 5–10× para control limpio).
2. **IA / Aprendizaje automático responsable:** divide datos en entrenamiento/validación/prueba **antes** de normalizar para evitar fuga de datos (*data leakage*); mide falsos positivos y coste de latencia antes de desplegar un modelo pesado donde basta una regla determinista.

## 3. Simulador ejecutable en este repositorio

Ejecuta y prueba la simulación discreta real de un controlador PID con *anti-windup* en [`laboratorios/control_pid/simulador_pid.py`](../laboratorios/control_pid/simulador_pid.py):

```bash
python3 -m unittest laboratorios/control_pid/test_pid.py -v
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** realimentación negativa, función de los términos P, I y D (incluido *anti-windup*), teorema de muestreo y evaluación honesta de modelos mediante [PhET](https://phet.colorado.edu/), [Academo](https://academo.org/) y [Fast.ai](https://course.fast.ai/).
2. **Enseñarlo con palabras simples:** conducir por una carretera sin mirar por el parabrisas es **lazo abierto**; mirar las líneas del carril y corregir el volante es **lazo cerrado**. La parte **P** gira según cuánto te saliste ahora; la **I** recuerda si llevas rato inclinado hacia la derecha por el viento lateral; y la **D** suaviza el giro cuando notas que ya vuelves rápido al centro para no pasarte al carril contrario.
3. **Identificar lagunas y volver a la fuente original:** cuando un controlador empiece a oscilar sin parar o la integral crezca hasta bloquear el actuador cuando el motor ya está al 100% (*integral windup*), revisa [`laboratorios/control_pid/simulador_pid.py`](../laboratorios/control_pid/simulador_pid.py) y simula frecuencias/ondas en [PhET](https://phet.colorado.edu/) y [Academo](https://academo.org/).
4. **Simplificar y revisar con analogías:** *analogía de la ducha con agua caliente:* si abres el grifo al máximo cuando sientes agua fría y no esperas a notar el cambio (retardo del tubo), te quemas y luego vuelves a cerrar de golpe hasta quedarte helado (oscilación por exceso de $K_p$ sin $K_d$). En inteligencia artificial, evaluar un modelo con las mismas preguntas del examen que ya estudió (*data leakage*) equivale a creer que un alumno sabe matemáticas porque memorizó la hoja de respuestas. (*Límite:* un modelo lineal discreto en Python muestra la dinámica básica del PID, pero no modela rozamientos no lineales ni retardos cambiantes de un sistema físico real).

## Recursos activos FMHY.net

- [PhET Interactive Simulations](https://phet.colorado.edu/) — simulaciones interactivas de física, ondas, circuitos y muestreo.
- [Academo](https://academo.org/) — herramientas interactivas visuales de señales, audio, espectros y matemáticas.
- [3Blue1Brown](https://www.3blue1brown.com/) — intuición matemática rigurosa de cálculo, álgebra lineal y redes neuronales.
- [Fast.ai](https://course.fast.ai/) — aprendizaje automático práctico orientado a medición real y código reproducible.
