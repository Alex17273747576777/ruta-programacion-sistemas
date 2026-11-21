# Guía 02 · Lenguajes de sistemas comparados (Python, C, C++, Rust, Go y Zig)

> **Objetivo:** superar los cursos aislados por lenguaje entendiendo **por qué existen distintos lenguajes**, cómo gestionan la memoria y cuándo elegir cada uno con criterio técnico.

## 1. Mapa honesto de decisión

| Lenguaje | Gestión de memoria | Compilación / ejecución | Dónde brilla | Riesgo clásico |
|---|---|---|---|---|
| **Python** | Conteo de referencias + recolector de ciclos (GC) | Intérprete / bytecode | Prototipado, automatización, APIs, datos, pruebas rápidas | Uso alto de RAM/CPU en bucles intensivos; errores de tipo tardíos sin análisis estático |
| **C** | Manual (`malloc`/`free`) | Nativa directa (GCC/Clang) | Kernels, drivers, embebidos mínimos, ABI universal | *Use-after-free*, desbordamientos de buffer, punteros nulos |
| **C++** | RAII + punteros inteligentes (`unique_ptr`) o manual | Nativa optimizada | Motores gráficos, tiempo real, embebidos avanzados, audio/video | Complejidad del lenguaje y comportamiento indefinido si se rompe RAII |
| **Rust** | Propiedad y préstamo (*ownership/borrowing*) verificados al compilar | Nativa (LLVM) | Sistemas concurrentes seguros, CLI rápidas, servicios críticos | Curva inicial exigente con tiempos de vida (*lifetimes*) |
| **Go** | Recolector de basura concurrente de baja pausa | Nativa rápida en un solo binario | Servicios de red, APIs concurrentes, herramientas DevOps/CLI | Menos predecible en tiempo real duro o microcontroladores mínimos |
| **Zig** | Manual explícita mediante `Allocator` inyectado | Nativa + compilación cruzada trivial de C/Zig | Reemplazo limpio de C, toolchains embebidos, librerías sin ocultamientos | Ecosistema aún joven frente a C/Rust |

## 2. El mismo problema en tres modelos de memoria

Sumar una lista garantizando manejo seguro de errores:
- En **Python**: la memoria se libera sola; el foco es la legibilidad y usar `Decimal` / excepciones explícitas.
- En **C**: debes pasar longitud y puntero (`const int *arr, size_t len`) y nunca devolver memoria local de la pila (*stack*).
- En **Rust**: pasas un *slice* prestado (`&[i64]`) con `Option<i64>` / `checked_add`, y el compilador impide leer fuera de rango o liberar dos veces.

## 3. Comprueba qué genera un compilador sin instalar todo

Usa **[Compiler Explorer (Godbolt)](https://godbolt.org/)** para pegar 5 líneas en C, C++, Rust, Go o Zig y observar exactamente las instrucciones de máquina generadas con `-O2`.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** modelos de propiedad y tiempo de vida de la memoria (GC en Python/Go vs manual en C/Zig vs estática en Rust/RAII en C++) usando [Learn C++](https://www.learncpp.com/), [High Assurance Rust](https://highassurance.rs/) y [Tour of Go](https://go.dev/tour).
2. **Enseñarlo con palabras simples:** en un programa cada dato ocupa una mesa en la memoria. En **Python o Go** hay un camarero que recoge las mesas vacías cuando nadie las usa (cómodo, pero ocupa algo de tiempo). En **C o Zig** tú mismo pones y recoges cada mesa: es rapidísimo, pero si recoges una mesa mientras alguien sigue sentado, todo se rompe. En **Rust**, un portero revisa los planos antes de abrir el local para asegurarse de que nunca haya dos personas escribiendo en la misma hoja ni nadie sentándose en una mesa ya recogida.
3. **Identificar lagunas y volver a la fuente original:** cuando aparezca la duda «¿por qué *stack* (pila) es más rápido que *heap* (montón)?» o «¿qué es exactamente comportamiento indefinido (*Undefined Behavior*)?», regresa a [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) y [High Assurance Rust](https://highassurance.rs/) antes de escribir código de producción.
4. **Simplificar y revisar con analogías:** *analogía de la mochila y el almacén:* la pila (*stack*) es tu mochila: sacas y metes cosas en orden rápido y al terminar la función la mochila se vacía al instante; el montón (*heap*) es un trastero alquilado por teléfono donde caben objetos de cualquier tamaño, pero alguien tiene que acordarse de devolver la llave para que no se llene el edificio. (*Límite:* los recolectores de basura modernos en Go o JVM ya optimizan la ubicación en memoria mediante escape analysis, por lo que no toda creación de objeto va siempre al heap).

## Recursos activos FMHY.net

- [Learn C++](https://www.learncpp.com/) y [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Tour of Go](https://go.dev/tour)
- [High Assurance Rust](https://highassurance.rs/) y [Rust Learning](https://github.com/ctjhoa/rust-learning)
- [Compiler Explorer (Godbolt)](https://godbolt.org/)
- [Crafting Interpreters](https://www.craftinginterpreters.com/) y [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x)
