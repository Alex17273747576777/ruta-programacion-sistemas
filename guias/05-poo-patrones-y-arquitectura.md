# Guía 05 · POO, Composición, Patrones y Arquitectura Limpia

> **Objetivo:** superar la memorización de diagramas UML y patrones por moda, entendiendo **cuándo un objeto o patrón simplifica el código** y cuándo introduce complejidad innecesaria.

## 1. Tres reglas prácticas de diseño

1. **Composición antes que herencia:** heredar acopla la clase hija a los detalles internos del padre; componer (inyectar un repositorio o un reloj como parámetro) permite cambiar piezas y probar sin tocar la lógica central.
2. **Invariantes en el borde y en las operaciones:** no expongas atributos mutables sin control; valida reglas en métodos con nombre claro (`prestar()`, `aplicar_movimiento()`).
3. **Patrones solo cuando resuelven una tensión real:**
   - **Repositorio / Puerto:** separa dominio puro de SQLite, PostgreSQL o archivos JSON.
   - **Estrategia / Reloj inyectable:** evita depender de `datetime.now()` dentro de pruebas unitarias.
   - **Outbox:** resuelve el corte entre base de datos y cola de mensajes sin prometer transacciones distribuidas mágicas.

## 2. Dónde comprobarlo en este repositorio

Observa [`proyectos/02_modelado/biblioteca.py`](../proyectos/02_modelado/biblioteca.py): `ServicioBiblioteca` no importa `sqlite3` ni `json`, sino un `Protocol` mínimo (`RepositorioBiblioteca`), por lo que la misma lógica se prueba en memoria en milisegundos y funciona igual sobre disco.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** composición frente a herencia, inversión de dependencias mediante interfaces/protocolos y patrones básicos en [Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans), [Refactoring Guru](https://refactoring.guru/) y [Awesome Low Level Design](https://github.com/ashishps1/awesome-low-level-design).
2. **Enseñarlo con palabras simples:** diseñar con **herencia** es decir «un coche eléctrico es una subclase de coche de gasolina»; cuando luego descubres que no tiene tubo de escape ni depósito, empiezas a tapar agujeros. Diseñar con **composición** es construir con piezas intercambiables: un chasis tiene un motor (de gasolina o eléctrico) y unas ruedas; si mañana cambias el motor de prueba por el motor real, el volante sigue funcionando igual.
3. **Identificar lagunas y volver a la fuente original:** cuando caigas en la trampa de crear cinco capas de interfaces para una sola función o confundas herencia múltiple con contratos de comportamiento, regresa a [`proyectos/02_modelado/biblioteca.py`](../proyectos/02_modelado/biblioteca.py) y [Refactoring Guru](https://refactoring.guru/) para comprobar si el patrón elimina duplicación real o solo añade archivos vacíos.
4. **Simplificar y revisar con analogías:** *analogía del enchufe universal frente al aparato soldado a la pared:* soldar una lámpara directo a los cables de la pared (acoplamiento duro) obliga a picar el muro para probar otra bombilla; usar un enchufe estándar (`Protocol` o interfaz mínima) deja cambiar la fuente de energía o el repositorio en segundos sin tocar la lámpara. (*Límite:* crear un enchufe para cada cable interno dentro de una función pequeña vuelve el sistema ilegible; solo sepáralo en las fronteras externas como disco, red, reloj o pagos).

## Recursos activos FMHY.net

- [Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans) — patrones explicados con lenguaje sencillo y ejemplos cotidianos.
- [Refactoring Guru](https://refactoring.guru/) — catálogo claro de patrones, olores de código y refactorizaciones con ejemplos comparados.
- [Awesome Low Level Design](https://github.com/ashishps1/awesome-low-level-design) — casos prácticos de diseño orientado a objetos y contratos.
- [Crafting Interpreters](https://www.craftinginterpreters.com/) — ejemplo real de arquitectura limpia sin sobreingeniería.
