#include <limits.h>
#include <stddef.h>
#include <stdio.h>

/* Suma segura de enteros con signo: devuelve 0 si OK, -1 si overflow o NULL. */
int sumar_seguro(int a, int b, int *salida) {
    if (salida == NULL) {
        return -1;
    }
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) {
        return -1;
    }
    *salida = a + b;
    return 0;
}

/* Copia acotada garantizando terminador nulo sin leer ni escribir fuera de rango. */
int copiar_acotado(const char *origen, char *destino, size_t cap) {
    size_t i = 0;
    if (origen == NULL || destino == NULL || cap == 0) {
        return -1;
    }
    while (i + 1 < cap && origen[i] != '\0') {
        destino[i] = origen[i];
        i++;
    }
    destino[i] = '\0';
    return (origen[i] == '\0') ? 0 : -1;
}

int main(void) {
    int res = 0;
    char buf[8];

    if (sumar_seguro(20, 22, &res) != 0 || res != 42) {
        return 1;
    }
    if (sumar_seguro(INT_MAX, 1, &res) == 0) {
        return 2;
    }
    if (copiar_acotado("sistemas", buf, sizeof(buf)) == 0) {
        return 3; /* "sistemas" tiene 8 chars + '\0' = 9, no cabe en 8 */
    }
    if (copiar_acotado("ok-c", buf, sizeof(buf)) != 0) {
        return 4;
    }
    printf("C_OK res=%d buf=%s\n", res, buf);
    return 0;
}
