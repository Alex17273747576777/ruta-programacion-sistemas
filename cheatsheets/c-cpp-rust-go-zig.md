# CheatSheet · C, C++, Rust, Go y Zig (Sistemas)

| Lenguaje | Regla de oro en memoria | Compilación / prueba rápida |
|---|---|---|
| **C** | Toda reserva (`malloc`) tiene dueño único y tamaño explícito | `cc -Wall -Wextra -Werror -fsanitize=address prog.c` |
| **C++** | Prefiere `std::vector`, `std::string_view` y `std::unique_ptr` (RAII) | `c++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined` |
| **Rust** | Un escritor exclusivo (`&mut T`) o múltiples lectores (`&T`) | `cargo test` y `cargo clippy` |
| **Go** | Pasa `context.Context` y comprueba carreras con detector integrado | `go test -race ./...` |
| **Zig** | Ninguna asignación oculta: pasa `Allocator` explícito | `zig test archivo.zig` |

## Comprobación rápida en navegador

Usa **[Compiler Explorer (Godbolt)](https://godbolt.org/)** para comparar el código máquina de cualquiera de los cinco lenguajes sin instalar toolchains pesados.

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** reglas de seguridad de memoria y compilación con sanitizadores frente a comprobación estática en [High Assurance Rust](https://highassurance.rs/) y [Learn C++](https://www.learncpp.com/).
2. **Enseñarlo con palabras simples:** en C tú vigilas no pisar memoria ajena; con `-fsanitize=address` pones sensores en el suelo para que suene la alarma si pisas fuera; en Rust el arquitecto revisa los planos antes de construir para que ni siquiera exista la puerta equivocada.
3. **Identificar lagunas y volver a la fuente original:** cuando dudes por qué `go test -race` detecta carreras de datos en tiempo de ejecución mientras Rust las rechaza al compilar, vuelve a [Tour of Go](https://go.dev/tour) y [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
4. **Simplificar y revisar con analogías:** *analogía del detector de humos vs diseño ignífugo:* un sanitizador en C/C++ o `-race` en Go es un detector de humos que pita cuando ocurre el fallo en tus pruebas; el borrow checker de Rust es construir la cocina sin enchufes sobrecargables desde el plano. (*Límite:* `unsafe` en Rust y los casos no cubiertos por pruebas en Go/C aún exigen revisión humana).
