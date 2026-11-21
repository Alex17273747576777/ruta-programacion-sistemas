# CheatSheet · TypeScript, Event Loop, CORS y Seguridad Web

| Concepto | Patrón correcto | Error clásico que evita |
|---|---|---|
| **Event Loop** | `Promise.then` (microtarea) corre antes que `setTimeout` | Asumir orden arbitrario en código asíncrono |
| **TypeScript en frontera** | Validar JSON externo con esquema/comprobación real | Creer que `interface Datos` valida en ejecución |
| **XSS en DOM** | Usar `elemento.textContent = texto` | Usar `elemento.innerHTML = entrada_usuario` |
| **CORS** | Configurar orígenes exactos en `Access-Control-Allow-Origin` | Creer que CORS bloquea peticiones desde `curl` o scripts |
| **Fetch con timeout** | `AbortController` + verificar `resp.ok` | Asumir que `fetch()` rechaza automáticamente HTTP `404`/`500` |

## Comprobación rápida

```bash
python3 -m unittest laboratorios/node_event_loop/test_node_lab.py -v
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** diferencia entre microtareas y macrotareas, borrado de tipos en TypeScript y manejo de errores en `fetch` usando [JavaScript.info](https://javascript.info/) y [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html).
2. **Enseñarlo con palabras simples:** `fetch()` solo te avisa de error si se cortó el cable de red; si el servidor respondió con un cartel de «404 no encontrado», la carta igual llegó a tu mano, así que debes mirar `resp.ok` antes de leerla como JSON bueno.
3. **Identificar lagunas y volver a la fuente original:** cuando veas que un `try { await fetch(...) }` deja pasar un `500` o un JSON inesperado rompe un componente TypeScript, vuelve a [MDN](https://developer.mozilla.org/) y [The Copenhagen Book](https://thecopenhagenbook.com/) para validar estados HTTP y entradas antes de usarlas.
4. **Simplificar y revisar con analogías:** *analogía del cartero y el sobre:* `fetch` promete avisarte cuando el cartero vuelva con respuesta; que el sobre traiga dentro «403 prohibido» sigue siendo una entrega exitosa del cartero (*Promise resuelta*), por lo que tú debes abrir y revisar el sello (`resp.ok`) antes de servir el contenido. (*Límite:* las cabeceras de seguridad CSP y CORS solo protegen navegadores compatibles, nunca sustituyen validación y autorización en el servidor).
