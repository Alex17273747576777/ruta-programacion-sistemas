# Guía 03 · Linux, Shell, Git y Contenedores en la práctica

> **Objetivo:** dominar las herramientas reales donde corre el 95% de los servidores y sistemas embebidos Linux, sin copiar comandos ciegamente.

## 1. Cuatro pilares operativos verificables

1. **Procesos, archivos y permisos en Linux:** todo en Linux sigue el modelo de archivos, descriptores (`stdin=0`, `stdout=1`, `stderr=2`) y permisos (`rwx` para dueño, grupo y otros). Usa `ps aux`, `ss -tulpn`, `df -h`, `journalctl` para diagnosticar antes de adivinar.
2. **Shell segura y componible:** usa `set -euo pipefail`, comillas dobles en variables (`"$ruta"`), y encadena herramientas pequeñas (`grep`, `awk`, `jq`, `find`) en vez de editar a mano.
3. **Git como grafo inmutable:** una rama es solo un puntero móvil a un commit; nunca uses `git push --force` en ramas compartidas ni subas `.env`, claves o copias privadas.
4. **Contenedores (Docker / Podman):** un contenedor no es una máquina virtual completa: comparte el kernel del host y aísla espacios de nombres (*namespaces*) y límites de recursos (*cgroups*).

## 2. Comandos de comprobación inmediata

```bash
# Ver árbol de procesos y puertos escuchando en Linux
ps -eo pid,ppid,comm --forest | head -n 20
ss -tuln

# Comprobar que un script bash no tiene errores básicos ni variables sin comillas
bash -n tu_script.sh
```

## Método Richard Feynman (4 pasos obligatorios)

1. **Seleccionar y estudiar el concepto:** separación entre kernel compartido y espacio de usuario aislado (contenedores vs VMs), gestión de servicios con `systemd` y modelo de commits/ramas en Git mediante [Linux Journey](https://labex.io/linuxjourney), [systemd-by-example](https://systemd-by-example.com/) y [Learn Git Branching](https://learngitbranching.js.org/).
2. **Enseñarlo con palabras simples:**
   - Una **máquina virtual** es construir otra casa entera con sus propios cimientos y caldera dentro de tu terreno. Un **contenedor** es alquilar un apartamento amueblado dentro del mismo edificio: cada inquilino tiene su llave y sus muebles (bibliotecas y archivos), pero todos comparten la misma caldera central (el kernel Linux).
   - **Git** no guarda copias duplicadas de toda tu carpeta cada vez: saca una foto de tu proyecto y la encadena con una flecha hacia la foto anterior; crear una rama es solo poner un marcapáginas con nombre en una foto concreta.
3. **Identificar lagunas y volver a la fuente original:** cuando no entiendas por qué cambiar un binario de Linux dentro de un contenedor sigue viendo la misma hora o kernel del host, o por qué `chmod 777` rompe la seguridad aunque «haga funcionar» un script, vuelve a [ArchWiki](https://wiki.archlinux.org/) y [Missing Semester (MIT)](https://missing.csail.mit.edu/).
4. **Simplificar y revisar con analogías:** *analogía de la cocina compartida y el libro de recetas:* los contenedores son estaciones de cocina con su propia despensa y utensilios etiquetados que comparten un mismo fogón central; si la cocina se queda sin gas (el kernel falla), todas las estaciones se apagan. Y `systemd` es el jefe de sala que vigila qué estaciones deben encenderse al abrir el restaurante y en qué orden. (*Límite:* por compartir el kernel, un contenedor Linux no puede ejecutar nativamente un kernel de Windows sin virtualización).

## Recursos activos FMHY.net

- [ArchWiki](https://wiki.archlinux.org/) y [Linux Command Library](https://linuxcommandlibrary.com/)
- [Linux Journey](https://labex.io/linuxjourney) y [Bash Academy](https://guide.bash.academy/)
- [systemd-by-example](https://systemd-by-example.com/)
- [Learn Git Branching](https://learngitbranching.js.org/) y [Oh My Git!](https://ohmygit.org/)
- [Podman](https://podman.io/) y [Crontab Guru](https://crontab.guru/)
- [DevOps Exercises](https://github.com/bregman-arie/devops-exercises) y [90DaysOfDevOps](https://github.com/MichaelCade/90DaysOfDevOps)
