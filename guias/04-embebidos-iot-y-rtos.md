# Guía 04 · Puente a Electrónica, Microcontroladores, IoT y RTOS

> **Objetivo:** conectar el software de sistemas con hardware real (Arduino, ESP32, Raspberry Pi, buses I2C/SPI/UART, MQTT y RTOS) usando **simuladores activos verificados de FMHY.net** antes de comprar una sola placa.

## 1. Qué cambia al programar hardware frente a una PC

1. **Sin sistema operativo (Bare Metal / Arduino):** un único bucle infinito (`loop()`) con interrupciones de hardware. Un `delay(1000)` bloquea toda la placa durante un segundo entero.
2. **Con RTOS (FreeRTOS / Zephyr en ESP32 o ARM):** múltiples tareas con prioridad, colas y semáforos compartiendo kilobytes de RAM; permite atender Wi-Fi/MQTT sin congelar la lectura de sensores.
3. **Linux embebido (Raspberry Pi):** corre un kernel Linux completo; ideal cuando necesitas Python, SQLite, contenedores o red compleja, pagando mayor consumo y arranque más lento.
4. **Seguridad física:** los pines GPIO suelen trabajar a **3.3 V** (ESP32, Raspberry Pi) o **5 V** (Arduino Uno). Mezclar voltajes sin divisor o conversor de nivel quema el chip.

## 2. Protocolos esenciales en una tabla rápida

| Protocolo | Tipo | Para qué se usa | Error típico |
|---|---|---|---|
| **UART / Serial** | Punto a punto (TX/RX) | Consola de depuración, GPS, módems | Cruzar TX con TX en vez de TX→RX o distinta velocidad (baudrate) |
| **I2C** | Bus con 2 hilos (SDA/SCL) + direcciones | Sensores de temperatura, pantallas OLED pequeñas | Olvidar resistencias *pull-up* o colisión de direcciones |
| **SPI** | Bus rápido (MOSI/MISO/SCK/CS) | Pantallas TFT, memorias SD, Ethernet | Confundir qué dispositivo tiene el pin CS en bajo |
| **MQTT** | Mensajería pub/sub sobre TCP/IP | Telemetría IoT entre sensores y servidor doméstico | Publicar sin TLS ni autenticación fuera de la red local |

## 3. Práctica inmediata sin hardware físico

1. Abre **[Wokwi](https://wokwi.com/)**, crea un circuito con ESP32 o Arduino Uno + LED + pulsador y sustituye `delay()` por temporización no bloqueante con `millis()`.
2. Abre **[Falstad](https://www.falstad.com/circuit/)** para observar en vivo cómo una resistencia limita la corriente de un LED y cómo un botón flotante necesita resistencia *pull-up*.
3. Si quieres diseñar lógica digital desde cero, resuelve los primeros niveles en **[HDLBits](https://hdlbits.01xz.net/)**.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** diferencia entre programación secuencial bloqueante (`delay`), programación por tiempo no bloqueante / interrupciones y un RTOS multitarea, además de buses básicos (UART/I2C/SPI) usando [Wokwi](https://wokwi.com/), [Last Minute Engineers](https://lastminuteengineers.com/) y [Pinout.xyz](https://pinout.xyz/).
2. **Enseñarlo con palabras simples:** si programas un microcontrolador usando `delay(5000)` para esperar cinco segundos antes de apagar una luz, es como ponerte tapones en los oídos y cerrar los ojos cinco segundos en mitad de una intersección: si alguien pulsa el botón de emergencia durante ese tiempo, ni te enteras. En cambio, mirar el reloj (`millis()`) o usar un RTOS es ir echando un ojo rápido al reloj mientras sigues atento a los botones y sensores.
3. **Identificar lagunas y volver a la fuente original:** cuando dudes sobre por qué un botón lee valores locos al soltarlo (pin flotante y rebote mecánico *debounce*) o por qué una tarea en FreeRTOS dispara un *watchdog reset* si nunca cede la CPU, consulta [Last Minute Engineers](https://lastminuteengineers.com/), [Falstad](https://www.falstad.com/circuit/) y la documentación oficial de FreeRTOS/ESP-IDF.
4. **Simplificar y revisar con analogías:** *analogía del cocinero y las tres cacerolas:* usar `delay()` es quedarse mirando la olla de la pasta cinco minutos sin cortar la cebolla ni responder al timbre; usar `millis()` es poner un temporizador en la pared y seguir picando mientras miras la hora cada segundo; un RTOS es tener un jefe de cocina que reparte turnos de milisegundos entre tres fogones prioritarios. (*Límite:* las simulaciones en Wokwi o Falstad validan lógica y cableado básico, pero no reproducen ruido electromagnético, caídas de batería ni tolerancias térmicas del mundo físico).

## Recursos activos FMHY.net

- [Wokwi](https://wokwi.com/) — simulador interactivo de Arduino, ESP32 y Raspberry Pi Pico.
- [Falstad Circuit Simulator](https://www.falstad.com/circuit/) — simulador visual de circuitos en tiempo real.
- [HDLBits](https://hdlbits.01xz.net/) — ejercicios verificables de diseño digital y Verilog.
- [KiCad](https://www.kicad.org/) — diseño libre de esquemáticos y PCB.
- [Pinout.xyz](https://pinout.xyz/) y [Awesome Raspberry Pi](https://github.com/thibmaek/awesome-raspberry-pi)
- [Awesome Electronics](https://github.com/kitspace/awesome-electronics) y [Last Minute Engineers](https://lastminuteengineers.com/)
- [How To Mechatronics](https://howtomechatronics.com/)
