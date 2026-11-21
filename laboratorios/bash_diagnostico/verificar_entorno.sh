#!/usr/bin/env bash
set -euo pipefail

# Diagnóstico mínimo reproducible de entorno de desarrollo y sistemas
for herramienta in python3 git bash; do
  if ! command -v "$herramienta" >/dev/null 2>&1; then
    echo "FALTA: $herramienta" >&2
    exit 1
  fi
done

echo "BASH_LAB_OK python3=$(python3 --version | awk '{print $2}')"
