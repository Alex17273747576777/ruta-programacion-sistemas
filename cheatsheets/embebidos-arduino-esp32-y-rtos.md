# CheatSheet · Embebidos, Arduino/ESP32, Buses y FreeRTOS

| Concepto | Regla práctica | Error clásico que evita |
|---|---|---|
| **Niveles lógicos** | ESP32 / Raspberry Pi = **3.3 V** · Arduino Uno = **5 V** | Conectar 5 V directo a un GPIO de 3.3 V y dañar el pin |
| **Tiempo no bloqueante** | `if (millis() - prev >= interval)` (resta sin desbordar) | Usar `delay(5000)` congelando botones y comunicaciones |
| **Botón limpio** | `INPUT_PULLUP` + *debounce* de 20–50 ms | Lecturas aleatorias por pin flotante y rebote mecánico |
| **UART / I2C / SPI** | UART: cruzar `TX↔RX` · I2C: resistencias *pull-up* | Conectar `TX↔TX` o olvidar compartir `GND` común entre placas |
| **FreeRTOS** | Pasar datos por `xQueueSend`, proteger con `Semaphore`, ceder con `vTaskDelay` | Disparar el *Watchdog Timer* en bucles sin espera |

## Comprobación en simulador sin placa física

Abre **[Wokwi](https://wokwi.com/)** o **[Falstad](https://www.falstad.com/circuit/)** para probar exactamente temporización con `millis()`, resistencias *pull-up* y comunicación serial antes de soldar o conectar cables reales.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** temporización no bloqueante con resta `millis() - anterior`, entradas *pull-up* y comunicación entre tareas RTOS usando [FreeRTOS Docs](https://www.freertos.org/Documentation/00-Overview), [ESP-IDF Docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/) y [Wokwi](https://wokwi.com/).
2. **Enseñarlo con palabras simples:** un pin de entrada sin resistencia conectada es como una veleta suelta al viento: si nadie la sujeta hacia arriba (`pull-up` a 3.3 V) o hacia abajo (`pull-down` a tierra), cualquier estática del aire hace creer al chip que alguien pulsó el botón. Y compartir el cable `GND` común entre dos placas es darles el mismo suelo para medir desde dónde cuenta el voltaje.
3. **Identificar lagunas y volver a la fuente original:** cuando dudes por qué `millis() - prev >= intervalo` sigue funcionando aunque el contador de 32 bits dé la vuelta a los ~49 días (aritmética sin signo módulo $2^{32}$), o por qué una interrupción (ISR) en FreeRTOS debe usar `FromISR` y nunca `printf`/`delay`, vuelve a [FreeRTOS Docs](https://www.freertos.org/Documentation/00-Overview) y [Last Minute Engineers](https://lastminuteengineers.com/).
4. **Simplificar y revisar con analogías:** *analogía del muelle en el timbre y la cinta métrica:* una resistencia *pull-up* es un muelle suave que mantiene el botón arriba cuando nadie lo toca; la resta `ahora - antes` en un reloj circular de 12 horas siempre da la diferencia real aunque hayas pasado de las 11 a la 1 (`1 - 11 = 2` en reloj de 12 h). (*Límite:* las interrupciones hardware deben hacer trabajo mínimo y delegar el resto a una bandera o cola para no perder otros eventos críticos).
