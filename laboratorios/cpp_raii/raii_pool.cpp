#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

struct RecursoMedido {
    std::string nombre;
    int *contador_vivos;

    RecursoMedido(std::string n, int *contador)
        : nombre(std::move(n)), contador_vivos(contador) {
        (*contador_vivos)++;
    }

    ~RecursoMedido() {
        (*contador_vivos)--;
    }
};

static void operacion_con_excepcion(int *vivos) {
    auto r = std::make_unique<RecursoMedido>("conexion-db", vivos);
    if (*vivos != 1) {
        throw std::logic_error("Conteo inesperado dentro de scope");
    }
    throw std::runtime_error("Fallo simulado antes de cerrar manualmente");
}

int main() {
    int vivos = 0;
    try {
        operacion_con_excepcion(&vivos);
    } catch (const std::runtime_error &) {
        // Incluso tras excepción, RAII destruyó unique_ptr al salir del ámbito.
    }
    if (vivos != 0) {
        std::cerr << "FUGA: vivos=" << vivos << "\n";
        return 1;
    }
    std::cout << "CPP_RAII_OK vivos=" << vivos << "\n";
    return 0;
}
