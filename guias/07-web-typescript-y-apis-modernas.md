# Guía 07 · Desarrollo Web, TypeScript, Event Loop y Seguridad en Navegador

> **Objetivo:** entender cómo funciona realmente el navegador (DOM, Event Loop asíncrono, `fetch`, CORS, CSP y tipado estático con TypeScript) para construir interfaces robustas sin depender de frameworks mágicos.

## 1. Cuatro mecanismos que todo desarrollador web debe explicar

1. **Event Loop en JavaScript:** JavaScript ejecuta tu código en un único hilo principal (*call stack*). Las operaciones lentas (`fetch`, temporizadores) se delegan al navegador y sus callbacks vuelven por la cola de microtareas (`Promise.then`) y macrotareas (`setTimeout`).
2. **TypeScript como contrato en compilación:** los tipos de TypeScript se borran al compilar a JavaScript. Sirven para detectar errores antes de desplegar, pero **no validan en ejecución** el JSON que llega desde una API externa.
3. **CORS (*Cross-Origin Resource Sharing*):** no es un escudo del servidor contra `curl`; es una regla del navegador que impide a una web ajena leer respuestas de otro origen salvo que el servidor envíe cabeceras explícitas (`Access-Control-Allow-Origin`).
4. **CSP y XSS:** nunca insertes texto de usuario con `innerHTML`; usa `textContent` o plantillas seguras y cabecera `Content-Security-Policy` para bloquear scripts inyectados.

## 2. Comprobación práctica sin dependencias

```bash
node -e '
console.log("1: sincrónico inicio");
setTimeout(() => console.log("4: macrotarea setTimeout"), 0);
Promise.resolve().then(() => console.log("3: microtarea Promise"));
console.log("2: sincrónico fin");
'
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** modelo de concurrencia por Event Loop (microtareas vs macrotareas), límites de TypeScript frente a validación en tiempo de ejecución, y políticas del mismo origen (CORS/XSS) en [MDN](https://developer.mozilla.org/) y [JavaScript.info](https://javascript.info/).
2. **Enseñarlo con palabras simples:** el navegador es como un camarero muy rápido que trabaja solo en una barra: nunca se queda parado esperando a que hierva el agua de un café (`fetch`); apunta el pedido, sigue atendiendo a la fila (*call stack*), revisa primero las notas urgentes pegadas en el timbre (*microtareas / Promesas*) y luego los recados normales (*macrotareas / temporizadores*).
3. **Identificar lagunas y volver a la fuente original:** cuando veas que un `JSON` malformado rompe tu app en TypeScript en producción o no entiendas por qué `curl` recibe `200 OK` mientras el navegador bloquea la respuesta por CORS, vuelve a [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) y [MDN: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) para comprobar el preflight `OPTIONS` y la validación en frontera.
4. **Simplificar y revisar con analogías:** *analogía del traductor previo y el guardia del edificio:* **TypeScript** es el corrector ortográfico antes de imprimir el menú: evita erratas en tus propios platos, pero no revisa lo que trae el camión de reparto de afuera (el JSON de red). **CORS** es el portero del edificio que solo deja que otro vecino lea tus cartas si tú firmaste una autorización explícita. (*Límite:* aunque CORS proteja al navegador, cualquier script externo fuera del navegador puede llamar a tu servidor directamente, por lo que la autenticación y autorización real siempre deben vivir en el backend).

## Recursos activos FMHY.net

- [MDN](https://developer.mozilla.org/) y [Web.dev Learn](https://web.dev/learn) — referencia primaria de HTML, CSS, DOM, Web APIs y rendimiento.
- [The Odin Project](https://www.theodinproject.com/) y [FullStackOpen](https://fullstackopen.com/en/) — rutas completas basadas en proyectos reales de frontend y backend.
- [JavaScript.info](https://javascript.info/) y [Eloquent JavaScript](https://eloquentjavascript.net/) — profundidad real en asincronía, cierres y Event Loop.
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) y [Patterns.dev](https://www.patterns.dev/) — tipado seguro y patrones web modernos.
