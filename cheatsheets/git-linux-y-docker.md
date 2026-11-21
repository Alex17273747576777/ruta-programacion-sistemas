# CheatSheet · Git, Linux Shell y Contenedores

| Herramienta | Orden útil | Qué verifica o previene |
|---|---|---|
| **Git** | `git status -sb && git diff --staged` | Revisar exactamente qué entra antes de `commit` |
| **Git seguro** | `git switch -c feat/tema` | Trabajar cambios complejos sin ensuciar `main` |
| **Bash estricto** | `set -euo pipefail` + `bash -n script.sh` | Detener ante errores ocultos y variables vacías |
| **Procesos / Red** | `ss -tuln` / `ps -eo pid,ppid,comm --forest` | Ver puertos reales y jerarquía de procesos |
| **Contenedores** | `podman run --rm --read-only ...` | Ejecutar servicios con privilegios mínimos y sin daemon raíz |

## Comprobación rápida

```bash
git status -sb && python3 --version && git --version
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** punteros de rama en Git, descriptores estándar en Linux y aislamiento de contenedores mediante [Learn Git Branching](https://learngitbranching.js.org/) y [ArchWiki](https://wiki.archlinux.org/).
2. **Enseñarlo con palabras simples:** una rama en Git es solo una etiqueta pegada a una foto del proyecto; `stdin/stdout/stderr` son tres tubos por donde entran datos, salen resultados y salen errores por separado.
3. **Identificar lagunas y volver a la fuente original:** si no recuerdas la diferencia entre `git reset --soft` y `--hard` o entre redirección `>` y tubería `|`, vuelve a [Pro Git](https://git-scm.com/book/en/v2) y [Linux Command Library](https://linuxcommandlibrary.com/).
4. **Simplificar y revisar con analogías:** *analogía de los tubos etiquetados:* enviar errores por `stderr` y datos por `stdout` es como tener un conducto para el producto terminado y otro para los avisos de avería: así quien conecta otra máquina detrás no mezcla una alarma con un ingrediente. (*Límite:* programas externos mal diseñados a veces imprimen errores en `stdout` y rompen las tuberías).
