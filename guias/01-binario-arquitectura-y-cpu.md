# Guía 01 · Sistema binario, representación numérica y arquitectura de CPU

> **Objetivo:** entender qué ocurre debajo de Python, C o Rust cuando declaras un número, sumas decimales o ejecutas un programa en una CPU real.

## 1. De bits a números con signo y punto flotante

- **Enteros sin signo:** $n$ bits representan $0$ a $2^n - 1$ (en 8 bits: `0..255`).
- **Enteros con signo (complemento a dos):** el bit más significativo indica peso negativo ($-2^{n-1}$). En 8 bits el rango es `-128..127`. Ventaja: la misma circuitería sumadora sirve para positivos y negativos.
- **Punto flotante IEEE-754 (`float` en Python = `double` de 64 bits):** usa signo (1 bit), exponente (11 bits) y mantisa (52 bits). Al trabajar en base 2, fracciones como $1/10$ (`0.1`) son periódicas infinitas igual que $1/3$ en base 10 (`0.3333...`).
- **Regla práctica de ingeniería:** usa enteros de la unidad mínima (centavos, milisegundos) o `Decimal` para dinero/contabilidad; usa `float` para física, señales y gráficos.

## 2. Cómo ejecuta un programa la CPU (ciclo básico)

1. El sistema operativo mapea el ejecutable en memoria virtual y fija el contador de programa (*Program Counter*).
2. La CPU sigue el bucle **Fetch → Decode → Execute** leyendo instrucciones de memoria a través de cachés L1/L2/L3 y registros.
3. Un programa nunca habla directo con el disco o la red: pide ayuda al kernel mediante llamadas al sistema (*syscalls* como `read`, `write`, `socket`).

## 3. Comprobación en tu terminal (sin suposiciones)

```bash
python3 - << 'PY'
import struct
print("0.1 + 0.2 en IEEE-754:", repr(0.1 + 0.2))
print("Bits IEEE-754 de 0.1:", "".join(f"{b:08b}" for b in struct.pack("!d", 0.1)))
print("Entero -1 en complemento a dos (8 bits):", f"{(-1) & 0xFF:08b}")
PY
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** representación binaria, complemento a dos, IEEE-754 y ciclo instrucción/syscall en [CPU Land](https://cpu.land/) y [NandGame](https://nandgame.com/).
2. **Enseñarlo con palabras simples:** la computadora solo distingue dos estados eléctricos (apagado `0` y encendido `1`). Agrupando esos interruptores construye números, letras y órdenes. Como un interruptor solo entiende mitades (`1/2`, `1/4`, `1/8`), números decimales normales como `0.1` no caben exactos igual que `1/3` no cabe exacto en nuestra libreta decimal.
3. **Identificar lagunas y volver a la fuente original:** cuando aparezca la duda «¿por qué un contador de 8 bits tras `255` vuelve a `0` (*overflow*) o pasa a `-128` en complemento a dos?», vuelve a [From Nand to Tetris](https://www.nand2tetris.org/course) y a [IEEE-754 / Python Floating Point](https://docs.python.org/3/tutorial/floatingpoint.html) para trazar el acarreo bit a bit.
4. **Simplificar y revisar con analogías:** *analogía del odómetro del coche:* un registro de 8 bits es un cuentakilómetros con 8 ruedas de ceros y unos: cuando todas llegan al máximo y sumas `1`, dan la vuelta al principio; en complemento a dos, la mitad superior del dial se reserva para contar hacia atrás desde `-1`. (*Límite:* el binario exacto en CPU no es «aproximado» en enteros; la aproximación ocurre solo al representar fracciones base 10 en punto flotante binario).

## Recursos activos FMHY.net

- [NandGame](https://nandgame.com/) — construye una CPU desde compuertas NAND en el navegador.
- [From Nand to Tetris](https://www.nand2tetris.org/course) — curso completo hardware → ensamblador → sistema operativo.
- [CPU Land](https://cpu.land/) — funcionamiento interno de ELF, memoria virtual, paginación y syscalls.
- [CS50x](https://cs50.harvard.edu/x/) — fundamentos de bits, memoria y punteros en C.
