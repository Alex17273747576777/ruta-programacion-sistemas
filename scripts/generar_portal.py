#!/usr/bin/env python3
"""Genera docs/index.html (portal interactivo autocontenido sin dependencias externas ni enlaces rotos)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPO_BLOB = "https://github.com/Alex17273747576777/ruta-programacion-sistemas/blob/main"

NIVEL_POR_ARCHIVO = {
    "etapas/01-fundamentos.md": "novato",
    "etapas/02-modelado.md": "intermedio",
    "etapas/03-datos.md": "intermedio",
    "etapas/04-redes.md": "avanzado",
    "etapas/05-operacion.md": "avanzado",
    "etapas/06-sistemas.md": "avanzado",
    "guias/01-binario-arquitectura-y-cpu.md": "novato",
    "guias/02-lenguajes-de-sistemas.md": "intermedio",
    "guias/03-linux-shell-git-y-contenedores.md": "novato",
    "guias/04-embebidos-iot-y-rtos.md": "avanzado",
    "guias/05-poo-patrones-y-arquitectura.md": "intermedio",
    "guias/06-redes-nginx-docker-y-despliegue.md": "avanzado",
    "guias/07-web-typescript-y-apis-modernas.md": "intermedio",
    "guias/08-control-automatico-senales-e-ia-aplicada.md": "avanzado",
    "guias/09-sistemas-expertos-motores-inferencia-y-logica-difusa.md": "master",
    "guias/10-logica-primer-orden-unificacion-y-resolucion.md": "master",
    "guias/11-algoritmo-rete-ontologias-owl-y-redes-bayesianas.md": "master",
    "cheatsheets/c-cpp-rust-go-zig.md": "intermedio",
    "cheatsheets/embebidos-arduino-esp32-y-rtos.md": "avanzado",
    "cheatsheets/estructuras-datos-y-big-o.md": "intermedio",
    "cheatsheets/git-linux-y-docker.md": "novato",
    "cheatsheets/python-y-decimal.md": "novato",
    "cheatsheets/redes-http-y-seguridad.md": "avanzado",
    "cheatsheets/regex-binario-y-nginx.md": "intermedio",
    "cheatsheets/sistemas-expertos-ontologias-y-reglas.md": "master",
    "cheatsheets/sistemas-expertos-rete-prolog-y-bayes.md": "master",
    "cheatsheets/sql-y-transacciones.md": "intermedio",
    "cheatsheets/typescript-web-y-cors.md": "intermedio",
}

ETIQUETA_NIVEL = {
    "novato": "Novato",
    "intermedio": "Intermedio",
    "avanzado": "Avanzado",
    "master": "Experto / Máster",
}


def extraer_recursos_fmhy() -> list[dict[str, str]]:
    txt = (RAIZ / "recursos" / "fmhy-activos.md").read_text(encoding="utf-8")
    categoria = "General"
    items: list[dict[str, str]] = []
    for linea in txt.splitlines():
        if linea.startswith("## "):
            categoria = linea[3:].strip()
            continue
        if linea.startswith("| [") and " | " in linea:
            celdas = [c.strip() for c in linea.strip("|").split("|")]
            if len(celdas) >= 3:
                enlaces = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", celdas[0])
                for nombre, url in enlaces:
                    items.append(
                        {
                            "categoria": categoria,
                            "nombre": nombre,
                            "url": url,
                            "origen": celdas[1].strip("` "),
                            "uso": celdas[2],
                        }
                    )
    return items


def _inline_md(texto: str) -> str:
    esc = html.escape(texto)
    esc = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc)
    esc = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", esc)
    esc = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", esc)

    def _link(m: re.Match[str]) -> str:
        label, href = m.group(1), m.group(2)
        if href.startswith("http"):
            return f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'
        return f"<code>{label}</code>"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, esc)


def md_a_html(md: str) -> str:
    lineas = md.splitlines()
    out: list[str] = []
    en_code = False
    en_ul = False
    en_ol = False
    en_tabla = False

    def cerrar_listas() -> None:
        nonlocal en_ul, en_ol, en_tabla
        if en_ul:
            out.append("</ul>")
            en_ul = False
        if en_ol:
            out.append("</ol>")
            en_ol = False
        if en_tabla:
            out.append("</tbody></table>")
            en_tabla = False

    for linea in lineas:
        if linea.startswith("```"):
            cerrar_listas()
            if not en_code:
                out.append("<pre><code>")
                en_code = True
            else:
                out.append("</code></pre>")
                en_code = False
            continue
        if en_code:
            out.append(html.escape(linea))
            continue
        if not linea.strip():
            cerrar_listas()
            continue
        if linea.startswith("|") and "|" in linea[1:]:
            celdas = [c.strip() for c in linea.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in celdas):
                continue
            if not en_tabla:
                cerrar_listas()
                out.append(
                    "<table><thead><tr>"
                    + "".join(f"<th>{_inline_md(c)}</th>" for c in celdas)
                    + "</tr></thead><tbody>"
                )
                en_tabla = True
            else:
                out.append("<tr>" + "".join(f"<td>{_inline_md(c)}</td>" for c in celdas) + "</tr>")
            continue
        if re.match(r"^#{1,4}\s+", linea):
            cerrar_listas()
            nivel = len(linea) - len(linea.lstrip("#"))
            titulo = linea[nivel:].strip()
            out.append(f"<h{nivel}>{_inline_md(titulo)}</h{nivel}>")
            continue
        if linea.startswith("> "):
            cerrar_listas()
            out.append(f"<blockquote>{_inline_md(linea[2:])}</blockquote>")
            continue
        if re.match(r"^[-*]\s+", linea):
            if en_ol:
                out.append("</ol>")
                en_ol = False
            if not en_ul:
                out.append("<ul>")
                en_ul = True
            out.append(f"<li>{_inline_md(re.sub(r'^[-*]\s+', '', linea))}</li>")
            continue
        if re.match(r"^\d+\.\s+", linea):
            if en_ul:
                out.append("</ul>")
                en_ul = False
            if not en_ol:
                out.append("<ol>")
                en_ol = True
            out.append(f"<li>{_inline_md(re.sub(r'^\d+\.\s+', '', linea))}</li>")
            continue
        cerrar_listas()
        out.append(f"<p>{_inline_md(linea)}</p>")

    cerrar_listas()
    if en_code:
        out.append("</code></pre>")
    return "\n".join(out)


def cargar_modulos() -> list[dict[str, str]]:
    modulos: list[dict[str, str]] = []
    grupos = [
        ("Etapas", sorted((RAIZ / "etapas").glob("*.md"))),
        ("Guías", sorted((RAIZ / "guias").glob("*.md"))),
        ("CheatSheets", sorted((RAIZ / "cheatsheets").glob("*.md"))),
    ]
    for grupo, archivos in grupos:
        for arch in archivos:
            rel = str(arch.relative_to(RAIZ)).replace("\\", "/")
            texto = arch.read_text(encoding="utf-8")
            primera = next((l.lstrip("# ").strip() for l in texto.splitlines() if l.startswith("# ")), arch.stem)
            nivel = NIVEL_POR_ARCHIVO.get(rel, "intermedio")
            modulos.append(
                {
                    "id": rel,
                    "grupo": grupo,
                    "nivel": nivel,
                    "nivelEtiqueta": ETIQUETA_NIVEL[nivel],
                    "titulo": primera,
                    "github": f"{REPO_BLOB}/{rel}",
                    "html": md_a_html(texto),
                }
            )
    return modulos


def construir_html() -> str:
    preguntas = json.loads((RAIZ / "quizzes" / "banco_preguntas.json").read_text(encoding="utf-8"))
    recursos = extraer_recursos_fmhy()
    modulos = cargar_modulos()

    preguntas_json = json.dumps(preguntas, ensure_ascii=False)
    recursos_json = json.dumps(recursos, ensure_ascii=False)
    modulos_json = json.dumps(modulos, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ruta de Programación y Sistemas · Máster en Ingeniería de Sistemas Expertos</title>
<style>
  :root {{
    --bg: #0b101b;
    --bg-alt: #0f1726;
    --panel: #141e30;
    --line: #27354d;
    --text: #f3f6fb;
    --muted: #b0bfd4;
    --accent: #2dd4bf;
    --accent-ink: #042f2e;
    --amber: #fbbf24;
    --ok: #34d399;
    --warn: #f59e0b;
    --err: #f87171;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    background: radial-gradient(circle at top right, #13223b 0%, var(--bg) 52%);
    color: var(--text);
    line-height: 1.6;
  }}
  .skip-link {{
    position: absolute; left: -9999px; top: 0;
    background: var(--accent); color: var(--accent-ink); padding: .6rem 1rem; font-weight: 700;
  }}
  .skip-link:focus {{ left: .75rem; top: .75rem; z-index: 100; border-radius: .4rem; }}
  :focus-visible {{ outline: 2px solid var(--amber); outline-offset: 2px; }}
  header {{
    padding: 1.75rem 1.25rem 1.35rem;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(135deg, #0b101b 0%, #101f36 60%, #0d262b 100%);
  }}
  .wrap {{ max-width: 1200px; margin: 0 auto; padding: 0 1rem; }}
  h1, h2, h3 {{ margin-top: 0; letter-spacing: -.01em; }}
  nav {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }}
  .tab-btn {{
    background: var(--panel); color: var(--text); border: 1px solid var(--line);
    padding: .55rem .9rem; border-radius: .5rem; cursor: pointer; font-weight: 600;
  }}
  .tab-btn:hover {{ border-color: var(--accent); }}
  .tab-btn.active {{ background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }}
  main {{ padding: 1.5rem 0 3.5rem; }}
  section.panel {{ display: none; }}
  section.panel.active {{ display: block; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 1rem; }}
  .card {{
    background: var(--panel); border: 1px solid var(--line); border-radius: .75rem;
    padding: 1rem 1.15rem;
  }}
  .badge {{
    display: inline-block; font-size: .75rem; font-weight: 600; padding: .15rem .55rem; border-radius: 999px;
    background: #0d948826; color: #5eead4; border: 1px solid #2dd4bf55;
  }}
  .badge.master {{ background: #d9770626; color: #fcd34d; border-color: #fbbf2455; }}
  .badge.novato {{ background: #2563eb26; color: #93c5fd; border-color: #60a5fa55; }}
  .badge.avanzado {{ background: #7c3aed26; color: #d8b4fe; border-color: #a78bfa55; }}
  .progress-bar-wrap {{
    margin-top: .9rem; padding: .75rem 1rem; border-radius: .65rem;
    background: rgba(11, 16, 27, .75); border: 1px solid var(--line);
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .75rem;
  }}
  .bar-track {{
    flex: 1 1 240px; height: 10px; background: #090d16; border-radius: 999px; overflow: hidden;
    border: 1px solid var(--line);
  }}
  .bar-fill {{ height: 100%; width: 0%; background: linear-gradient(90deg, var(--accent), var(--amber)); transition: width .25s ease; }}
  .level-bar {{ display: flex; flex-wrap: wrap; gap: .45rem; margin: .75rem 0 1rem; }}
  .lvl-btn {{
    background: var(--bg-alt); color: var(--muted); border: 1px solid var(--line);
    padding: .35rem .75rem; border-radius: 999px; cursor: pointer; font-size: .85rem; font-weight: 600;
  }}
  .lvl-btn.active {{ background: var(--amber); color: #1c1917; border-color: var(--amber); }}
  input, textarea, select {{
    width: 100%; background: #090e18; color: var(--text); border: 1px solid var(--line);
    border-radius: .5rem; padding: .55rem .7rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .9rem; }}
  a {{ color: var(--accent); }}
  .link-btn {{
    background: #090e18; color: var(--accent); border: 1px solid var(--line);
    padding: .35rem .7rem; border-radius: .45rem; cursor: pointer; font-size: .85rem; font-weight: 600;
  }}
  .link-btn:hover {{ border-color: var(--accent); }}
  .link-btn.done {{ background: #064e3b; color: #a7f3d0; border-color: #10b981; }}
  .opt-btn {{
    display: block; width: 100%; text-align: left; margin: .4rem 0;
    background: #090e18; color: var(--text); border: 1px solid var(--line);
    border-radius: .5rem; padding: .6rem .8rem; cursor: pointer;
  }}
  .opt-btn.ok {{ border-color: var(--ok); background: #064e3b88; }}
  .opt-btn.bad {{ border-color: var(--err); background: #7f1d1d88; }}
  .feynman-box, blockquote {{
    margin: .75rem 0; padding: .75rem; border-left: 3px solid var(--accent);
    background: #090e18; border-radius: 0 .5rem .5rem 0;
  }}
  pre {{ background: #090e18; border: 1px solid var(--line); border-radius: .5rem; padding: .75rem; overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
  th, td {{ border-bottom: 1px solid var(--line); padding: .5rem; text-align: left; }}
  .lector-wrap {{ display: grid; grid-template-columns: 310px 1fr; gap: 1rem; }}
  @media (max-width: 820px) {{ .lector-wrap {{ grid-template-columns: 1fr; }} }}
  .doc-item {{
    display: block; width: 100%; text-align: left; background: #090e18; color: var(--text);
    border: 1px solid var(--line); border-radius: .45rem; padding: .5rem .65rem; margin-bottom: .35rem; cursor: pointer;
  }}
  .doc-item.active {{ border-color: var(--accent); color: var(--accent); }}
  .bit-btn {{
    padding: .5rem 1rem; font-weight: 700; border-radius: .5rem; cursor: pointer;
    border: 1px solid var(--line); background: #090e18; color: var(--text);
  }}
  .bit-btn.on {{ background: var(--ok); color: #052e16; border-color: var(--ok); }}
</style>
</head>
<body>
<a class="skip-link" href="#contenido-principal">Saltar al contenido</a>
<header>
  <div class="wrap">
    <span class="badge master">De Novato a Profesional · Máster en Ingeniería de Sistemas Expertos · Método Richard Feynman (4 pasos)</span>
    <h1>Ruta hacia la Ingeniería de Sistemas Expertos</h1>
    <p style="color:var(--muted);margin:.25rem 0 0">
      6 etapas con código probado · 7 laboratorios (C99, C++20, Node, PID, Motor Experto, LPO/Bayes/V&amp;V, Bash) · {len(modulos)} módulos integrados · 7 Playgrounds sin dependencias · Quiz ({len(preguntas)} preguntas).
    </p>
    <div class="progress-bar-wrap" aria-live="polite">
      <span id="globalProgressText" class="mono">Progreso local: 0 / {len(modulos)} módulos completados</span>
      <div class="bar-track" aria-hidden="true"><div id="globalProgressFill" class="bar-fill"></div></div>
      <button class="link-btn" onclick="resetProgreso()">Reiniciar progreso</button>
    </div>
    <nav aria-label="Secciones principales">
      <button class="tab-btn active" onclick="showTab('roadmap', this)">Roadmap por Nivel</button>
      <button class="tab-btn" onclick="showTab('lector', this)">Lector Completo ({len(modulos)})</button>
      <button class="tab-btn" onclick="showTab('experto', this)">Motor Experto</button>
      <button class="tab-btn" onclick="showTab('unificacion', this)">LPO &amp; Bayes (Máster)</button>
      <button class="tab-btn" onclick="showTab('binario', this)">Binario / IEEE-754</button>
      <button class="tab-btn" onclick="showTab('logica', this)">Compuertas &amp; Half-Adder</button>
      <button class="tab-btn" onclick="showTab('regex', this)">Regex &amp; chmod</button>
      <button class="tab-btn" onclick="showTab('pid', this)">Control PID</button>
      <button class="tab-btn" onclick="showTab('quiz', this)">Quiz ({len(preguntas)})</button>
      <button class="tab-btn" onclick="showTab('fmhy', this)">FMHY ({len(recursos)})</button>
    </nav>
  </div>
</header>

<main id="contenido-principal" class="wrap">
  <section id="roadmap" class="panel active">
    <h2>1. Itinerario escalonado (Novato → Intermedio → Avanzado → Máster)</h2>
    <div class="level-bar" id="roadmapLevels" role="group" aria-label="Filtrar itinerario por nivel">
      <button class="lvl-btn active" onclick="setNivelRoadmap('todos', this)">Todos</button>
      <button class="lvl-btn" onclick="setNivelRoadmap('novato', this)">Novato</button>
      <button class="lvl-btn" onclick="setNivelRoadmap('intermedio', this)">Intermedio</button>
      <button class="lvl-btn" onclick="setNivelRoadmap('avanzado', this)">Avanzado</button>
      <button class="lvl-btn" onclick="setNivelRoadmap('master', this)">Experto / Máster</button>
    </div>
    <div class="grid" id="roadmapGrid">
      <div class="card" data-nivel="novato"><span class="badge novato">Novato · Etapa 1</span><h3>Fundamentos</h3><p>Calculadora exacta con <code>Decimal</code> (sin <code>eval</code>) y agenda JSON atómica (<code>os.replace</code>).</p><p><button class="link-btn" onclick="abrirModulo('etapas/01-fundamentos.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/01_fundamentos" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="intermedio"><span class="badge">Intermedio · Etapa 2</span><h3>Modelado y Pruebas</h3><p>Biblioteca de préstamos con dominio desacoplado, reloj inyectable e invariantes estrictas.</p><p><button class="link-btn" onclick="abrirModulo('etapas/02-modelado.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/02_modelado" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="intermedio"><span class="badge">Intermedio · Etapa 3</span><h3>Datos y Concurrencia</h3><p>Inventario transaccional sin stock negativo bajo carreras reales con barrera e idempotencia.</p><p><button class="link-btn" onclick="abrirModulo('etapas/03-datos.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/03_datos" target="_blank" rel="noopener">Código + SQL</a></p></div>
      <div class="card" data-nivel="avanzado"><span class="badge avanzado">Avanzado · Etapa 4</span><h3>Redes y Seguridad</h3><p>API HTTP real con autenticación, autorización por recurso (<code>403</code>) y límites de entrada.</p><p><button class="link-btn" onclick="abrirModulo('etapas/04-redes.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/04_redes" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="avanzado"><span class="badge avanzado">Avanzado · Etapa 5</span><h3>Operación</h3><p>Liveness vs Readiness, logs sin secretos, respaldo SQLite Backup API y restauración SHA-256.</p><p><button class="link-btn" onclick="abrirModulo('etapas/05-operacion.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/05_operacion" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="avanzado"><span class="badge avanzado">Avanzado · Etapa 6</span><h3>Sistemas Distribuidos</h3><p>Transactional Outbox, consumidor idempotente ante caídas, caché TTL y percentiles p50/p95.</p><p><button class="link-btn" onclick="abrirModulo('etapas/06-sistemas.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/06_sistemas" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="master"><span class="badge master">Máster · Guía 09</span><h3>Motores de Inferencia y Lógica Difusa</h3><p>Encadenamiento adelante/atrás con explicación <em>How</em>, certeza MYCIN y controlador Mamdani.</p><p><button class="link-btn" onclick="abrirModulo('guias/09-sistemas-expertos-motores-inferencia-y-logica-difusa.md')">Leer Guía 09</button> · <a href="{REPO_BLOB}/laboratorios/sistema_experto/motor_inferencia.py" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="master"><span class="badge master">Máster · Guía 10</span><h3>Lógica de 1er Orden y Resolución SLD</h3><p>Unificación de Robinson con <em>occurs check</em>, cláusulas de Horn y <em>backtracking</em>.</p><p><button class="link-btn" onclick="abrirModulo('guias/10-logica-primer-orden-unificacion-y-resolucion.md')">Leer Guía 10</button> · <a href="{REPO_BLOB}/laboratorios/sistemas_expertos_avanzados/unificador_prolog.py" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card" data-nivel="master"><span class="badge master">Máster · Guía 11</span><h3>Rete, Ontologías OWL, Bayes y V&amp;V</h3><p>Redes alfa/beta, Mundo Abierto (OWA), inferencia bayesiana exacta y auditoría V&amp;V.</p><p><button class="link-btn" onclick="abrirModulo('guias/11-algoritmo-rete-ontologias-owl-y-redes-bayesianas.md')">Leer Guía 11</button> · <a href="{REPO_BLOB}/laboratorios/sistemas_expertos_avanzados/red_bayesiana_y_vv.py" target="_blank" rel="noopener">Código en GitHub</a></p></div>
    </div>

    <h2 style="margin-top:1.75rem">2. Laboratorios multi-lenguaje ejecutables</h2>
    <div class="grid">
      <div class="card"><h3>C99 · Memoria y Overflow</h3><p>Suma segura contra desbordamiento y copia acotada sin lectura fuera de rango.</p><a href="{REPO_BLOB}/laboratorios/c_memoria/buffer_seguro.c" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>C++20 · RAII y <code>unique_ptr</code></h3><p>Liberación determinista de recursos incluso al lanzar excepciones.</p><a href="{REPO_BLOB}/laboratorios/cpp_raii/raii_pool.cpp" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Node.js · Event Loop</h3><p>Verificación en vivo de orden sincrónico → microtareas → macrotareas.</p><a href="{REPO_BLOB}/laboratorios/node_event_loop/event_loop_orden.mjs" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Control PID Discreto</h3><p>Simulador en Python con anti-windup y prueba de convergencia.</p><a href="{REPO_BLOB}/laboratorios/control_pid/simulador_pid.py" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Motor de Inferencia (Máster SE)</h3><p>Forward &amp; Backward Chaining con explicación <em>How</em>, MYCIN CF y Lógica Difusa Mamdani.</p><a href="{REPO_BLOB}/laboratorios/sistema_experto/motor_inferencia.py" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>LPO, Red Bayesiana &amp; V&amp;V</h3><p>Unificación de Robinson, resolución SLD, probabilidad posterior DAG y detector de conflictos.</p><a href="{REPO_BLOB}/laboratorios/sistemas_expertos_avanzados/red_bayesiana_y_vv.py" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Bash Estricto</h3><p>Auditoría reproducible de entorno con <code>set -euo pipefail</code>.</p><a href="{REPO_BLOB}/laboratorios/bash_diagnostico/verificar_entorno.sh" target="_blank" rel="noopener">Ver en GitHub</a></div>
    </div>
  </section>

  <section id="lector" class="panel">
    <h2>Lector completo de Etapas, Guías y CheatSheets ({len(modulos)} módulos)</h2>
    <div class="level-bar" id="lectorLevels" role="group" aria-label="Filtrar módulos por nivel">
      <button class="lvl-btn active" onclick="setNivelLector('todos', this)">Todos</button>
      <button class="lvl-btn" onclick="setNivelLector('novato', this)">Novato</button>
      <button class="lvl-btn" onclick="setNivelLector('intermedio', this)">Intermedio</button>
      <button class="lvl-btn" onclick="setNivelLector('avanzado', this)">Avanzado</button>
      <button class="lvl-btn" onclick="setNivelLector('master', this)">Experto / Máster</button>
    </div>
    <div class="lector-wrap">
      <div class="card">
        <input id="docFilter" placeholder="Filtrar módulo..." aria-label="Filtrar módulo por texto" oninput="renderDocList()" style="margin-bottom:.75rem">
        <div id="docList"></div>
      </div>
      <div class="card">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem;margin-bottom:.75rem">
          <a id="docGhLink" href="{REPO_BLOB}" target="_blank" rel="noopener">Abrir fuente en GitHub</a>
          <button id="docCompleteBtn" class="link-btn" onclick="toggleModuloActual()">Marcar completado</button>
        </div>
        <div id="docViewer"></div>
      </div>
    </div>
  </section>

  <section id="experto" class="panel">
    <h2>Playground · Motor de Inferencia Simbólico (Forward/Backward + MYCIN CF)</h2>
    <div class="grid">
      <div class="card">
        <h3>1. Base de Hechos observados (Memoria de Trabajo)</h3>
        <p style="color:var(--muted);font-size:.9rem">Activa los síntomas observados y elige si deseas deducir todo (<em>Forward</em>) o probar una meta concreta (<em>Backward</em>):</p>
        <label style="display:flex;align-items:center;gap:.5rem;margin:.35rem 0"><input type="checkbox" id="hLatencia" checked onchange="runExperto()" style="width:auto"> <code>latencia_alta</code> (CF=0.90)</label>
        <label style="display:flex;align-items:center;gap:.5rem;margin:.35rem 0"><input type="checkbox" id="hPaquetes" checked onchange="runExperto()" style="width:auto"> <code>perdida_paquetes</code> (CF=1.00)</label>
        <label style="display:flex;align-items:center;gap:.5rem;margin:.35rem 0"><input type="checkbox" id="hCpu" checked onchange="runExperto()" style="width:auto"> <code>cpu_100</code> (CF=0.80)</label>
        <label style="display:flex;align-items:center;gap:.5rem;margin:.35rem 0"><input type="checkbox" id="hSwap" onchange="runExperto()" style="width:auto"> <code>sin_swap</code> (CF=0.90)</label>
        <label style="margin-top:.75rem;display:block">Meta para Encadenamiento hacia Atrás:</label>
        <select id="seMeta" onchange="runExperto()" style="margin-top:.35rem">
          <option value="alerta_incidente_p1">alerta_incidente_p1</option>
          <option value="congestion_red">congestion_red</option>
          <option value="saturacion_nodo">saturacion_nodo</option>
        </select>
      </div>
      <div class="card">
        <h3>2. Reglas de Producción (Base de Conocimiento)</h3>
        <ul class="mono" style="padding-left:1.1rem;font-size:.86rem">
          <li><b>R1:</b> SI <code>latencia_alta</code> Y <code>perdida_paquetes</code> → <code>congestion_red</code> (CF=0.80)</li>
          <li><b>R2:</b> SI <code>cpu_100</code> Y <code>sin_swap</code> → <code>saturacion_nodo</code> (CF=0.75)</li>
          <li><b>R3:</b> SI <code>congestion_red</code> → <code>alerta_incidente_p1</code> (CF=0.90)</li>
          <li><b>R4:</b> SI <code>saturacion_nodo</code> → <code>alerta_incidente_p1</code> (CF=0.85)</li>
        </ul>
        <div id="seOut" class="mono" style="margin-top:.75rem"></div>
      </div>
    </div>
  </section>

  <section id="unificacion" class="panel">
    <h2>Playground · Unificación LPO (Robinson) &amp; Red Bayesiana Exacta (Máster)</h2>
    <div class="grid">
      <div class="card">
        <h3>1. Unificador de Primer Orden (con Occurs Check)</h3>
        <p style="color:var(--muted);font-size:.9rem">Variables en <code>Mayúscula</code> (ej. <code>X</code>, <code>Servicio</code>); átomos en <code>minúscula</code>. Prueba <code>depende(X, lista(X))</code> para activar el <em>occurs check</em>.</p>
        <label>Término 1: <input id="uniT1" value="depende(api_pagos, nodo(Z, 5432))" oninput="runUnificacion()"></label>
        <label style="display:block;margin-top:.6rem">Término 2: <input id="uniT2" value="depende(Servicio, nodo(bd_1, Puerto))" oninput="runUnificacion()"></label>
        <div id="uniOut" class="mono" style="margin-top:.75rem"></div>
      </div>
      <div class="card">
        <h3>2. Red Bayesiana: <code>FallaDisco → Latencia ← PicoRed</code></h3>
        <p style="color:var(--muted);font-size:.9rem">Priors: <code>P(FallaDisco)=0.02</code>, <code>P(PicoRed)=0.05</code>. Observa el fenómeno <em>explaining away</em> al marcar <code>PicoRed</code>:</p>
        <label style="display:flex;align-items:center;gap:.5rem;margin:.35rem 0"><input type="checkbox" id="bayLatencia" checked onchange="runBayes()" style="width:auto"> Evidencia: <code>Latencia = Alta</code></label>
        <label style="display:flex;align-items:center;gap:.5rem;margin:.35rem 0"><input type="checkbox" id="bayPico" onchange="runBayes()" style="width:auto"> Evidencia: <code>PicoRed = Confirmado</code></label>
        <div id="bayOut" class="mono" style="margin-top:.75rem"></div>
      </div>
    </div>
  </section>

  <section id="binario" class="panel">
    <h2>Playground · Binario, Complemento a Dos e IEEE-754 (64 bits)</h2>
    <div class="card">
      <label for="numInput">Ingresa un entero o decimal (prueba <code>0.1</code>, <code>-42</code>, <code>255</code>):</label>
      <input id="numInput" value="0.1" oninput="calcBinario()" style="margin:.5rem 0 1rem">
      <div id="binOut" class="mono"></div>
    </div>
  </section>

  <section id="logica" class="panel">
    <h2>Playground · Compuertas Lógicas y Semisumador (Half-Adder)</h2>
    <div class="card">
      <p style="color:var(--muted);margin-top:0">Pulsa las entradas digitales A y B para ver las compuertas básicas y la suma binaria del Half-Adder:</p>
      <div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:1rem">
        <button id="btnA" class="bit-btn on" onclick="toggleBit('A')">Entrada A = 1</button>
        <button id="btnB" class="bit-btn" onclick="toggleBit('B')">Entrada B = 0</button>
      </div>
      <div id="logicaOut" class="mono"></div>
    </div>
  </section>

  <section id="regex" class="panel">
    <h2>Playground · Regex Segura y Calculadora de Permisos <code>chmod</code></h2>
    <div class="grid">
      <div class="card">
        <h3>Validador Regex</h3>
        <label>Patrón: <input id="rxPat" value="^[a-z0-9_.-]+@[a-z0-9.-]+\\.[a-z]{{2,}}$" oninput="runRegex()"></label>
        <label style="display:block;margin-top:.6rem">Texto de prueba: <input id="rxTxt" value="ingenieria@sistemas.dev" oninput="runRegex()"></label>
        <p id="rxOut" class="mono" style="margin-top:.75rem"></p>
      </div>
      <div class="card">
        <h3>Permisos Unix (<code>chmod</code>)</h3>
        <label>Octal (3 dígitos): <input id="chOct" value="750" maxlength="3" oninput="runChmod()"></label>
        <p id="chOut" class="mono" style="margin-top:.75rem"></p>
      </div>
    </div>
  </section>

  <section id="pid" class="panel">
    <h2>Playground · Simulador de Lazo Cerrado PID (con Anti-Windup)</h2>
    <div class="card">
      <div class="grid">
        <label>Setpoint: <span id="spVal">60</span><input type="range" id="spIn" min="20" max="100" value="60" oninput="runPid()"></label>
        <label>Kp: <span id="kpVal">2.0</span><input type="range" id="kpIn" min="0.2" max="6" step="0.2" value="2.0" oninput="runPid()"></label>
        <label>Ki: <span id="kiVal">0.8</span><input type="range" id="kiIn" min="0" max="3" step="0.1" value="0.8" oninput="runPid()"></label>
        <label>Kd: <span id="kdVal">0.2</span><input type="range" id="kdIn" min="0" max="2" step="0.1" value="0.2" oninput="runPid()"></label>
      </div>
      <svg id="pidSvg" viewBox="0 0 600 220" style="width:100%;height:220px;background:#090e18;border:1px solid var(--line);border-radius:.5rem;margin-top:1rem"></svg>
      <p id="pidStats" class="mono" style="margin-top:.5rem"></p>
    </div>
  </section>

  <section id="quiz" class="panel">
    <h2>Quiz de Evaluación por Niveles ({len(preguntas)} preguntas · Explicación Feynman)</h2>
    <div class="level-bar" id="quizLevels" role="group" aria-label="Filtrar quiz por nivel">
      <button class="lvl-btn active" onclick="setNivelQuiz('todos', this)">Todas</button>
      <button class="lvl-btn" onclick="setNivelQuiz('novato', this)">Novato</button>
      <button class="lvl-btn" onclick="setNivelQuiz('intermedio', this)">Intermedio</button>
      <button class="lvl-btn" onclick="setNivelQuiz('avanzado', this)">Avanzado</button>
      <button class="lvl-btn" onclick="setNivelQuiz('master', this)">Experto / Máster</button>
    </div>
    <p id="quizScore" class="mono" style="color:var(--accent)"></p>
    <div id="quizHost"></div>
  </section>

  <section id="fmhy" class="panel">
    <h2>Catálogo FMHY.net verificado ({len(recursos)} recursos activos)</h2>
    <input id="fmhySearch" placeholder="Filtrar por tema o nombre..." aria-label="Filtrar recursos FMHY" oninput="renderFmhy()" style="margin-bottom:.75rem">
    <div class="card" style="overflow-x:auto">
      <table><thead><tr><th>Recurso</th><th>Categoría</th><th>Origen FMHY</th><th>Uso</th></tr></thead><tbody id="fmhyBody"></tbody></table>
    </div>
  </section>
</main>

<script>
const PREGUNTAS = {preguntas_json};
const RECURSOS = {recursos_json};
const MODULOS = {modulos_json};
const PROGRESO_KEY = 'ruta_sistemas_expertos_v1';

let moduloActualId = MODULOS[0].id;
let nivelRoadmap = 'todos';
let nivelLector = 'todos';
let nivelQuiz = 'todos';
const respuestas = new Map();

function cargarEstado() {{
  try {{
    const raw = localStorage.getItem(PROGRESO_KEY);
    if (!raw) return {{ completados: [], quiz: {{}} }};
    const obj = JSON.parse(raw);
    return {{
      completados: Array.isArray(obj.completados) ? obj.completados : [],
      quiz: obj.quiz && typeof obj.quiz === 'object' ? obj.quiz : {{}},
    }};
  }} catch (_e) {{
    return {{ completados: [], quiz: {{}} }};
  }}
}}

const estado = cargarEstado();
Object.entries(estado.quiz).forEach(([k, v]) => respuestas.set(k, v));

function guardarEstado() {{
  try {{
    const quizObj = {{}};
    respuestas.forEach((v, k) => {{ quizObj[k] = v; }});
    localStorage.setItem(PROGRESO_KEY, JSON.stringify({{ completados: estado.completados, quiz: quizObj }}));
  }} catch (_e) {{}}
  actualizarBarraProgreso();
}}

function actualizarBarraProgreso() {{
  const total = MODULOS.length;
  const done = estado.completados.filter(id => MODULOS.some(m => m.id === id)).length;
  const pct = total ? Math.round((done / total) * 100) : 0;
  document.getElementById('globalProgressText').textContent = `Progreso local: ${{done}} / ${{total}} módulos completados (${{pct}}%)`;
  document.getElementById('globalProgressFill').style.width = `${{pct}}%`;
}}

function resetProgreso() {{
  estado.completados = [];
  respuestas.clear();
  guardarEstado();
  renderDocList();
  mostrarModulo(moduloActualId);
  renderQuiz();
}}

function showTab(id, btn) {{
  document.querySelectorAll('section.panel').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  if (btn) btn.classList.add('active');
}}

function setNivelRoadmap(nivel, btn) {{
  nivelRoadmap = nivel;
  document.querySelectorAll('#roadmapLevels .lvl-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  document.querySelectorAll('#roadmapGrid .card').forEach(card => {{
    card.style.display = (nivel === 'todos' || card.dataset.nivel === nivel) ? 'block' : 'none';
  }});
}}

function setNivelLector(nivel, btn) {{
  nivelLector = nivel;
  document.querySelectorAll('#lectorLevels .lvl-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderDocList();
}}

function setNivelQuiz(nivel, btn) {{
  nivelQuiz = nivel;
  document.querySelectorAll('#quizLevels .lvl-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderQuiz();
}}

function abrirModulo(id) {{
  const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.textContent.startsWith('Lector'));
  showTab('lector', btn);
  mostrarModulo(id);
}}

function toggleModuloActual() {{
  const idx = estado.completados.indexOf(moduloActualId);
  if (idx >= 0) estado.completados.splice(idx, 1);
  else estado.completados.push(moduloActualId);
  guardarEstado();
  renderDocList();
  mostrarModulo(moduloActualId);
}}

function renderDocList() {{
  const q = document.getElementById('docFilter').value.trim().toLowerCase();
  const host = document.getElementById('docList');
  const filtrados = MODULOS.filter(m =>
    (nivelLector === 'todos' || m.nivel === nivelLector) &&
    (!q || `${{m.grupo}} ${{m.nivelEtiqueta}} ${{m.titulo}} ${{m.id}}`.toLowerCase().includes(q))
  );
  host.innerHTML = filtrados.map(m => {{
    const doneMark = estado.completados.includes(m.id) ? '✓ ' : '';
    return `<button class="doc-item ${{m.id === moduloActualId ? 'active' : ''}}" onclick="mostrarModulo('${{m.id}}')"><small style="color:var(--muted)">${{m.grupo}} · ${{m.nivelEtiqueta}}</small><br>${{doneMark}}${{m.titulo}}</button>`;
  }}).join('');
}}

function mostrarModulo(id) {{
  const mod = MODULOS.find(m => m.id === id) || MODULOS[0];
  moduloActualId = mod.id;
  document.getElementById('docGhLink').href = mod.github;
  document.getElementById('docViewer').innerHTML = mod.html;
  const doneBtn = document.getElementById('docCompleteBtn');
  const isDone = estado.completados.includes(mod.id);
  doneBtn.textContent = isDone ? '✓ Completado' : 'Marcar completado';
  doneBtn.classList.toggle('done', isDone);
  renderDocList();
}}

let bitA = 1, bitB = 0;
function toggleBit(cual) {{
  if (cual === 'A') bitA = 1 - bitA;
  else bitB = 1 - bitB;
  const bA = document.getElementById('btnA'), bB = document.getElementById('btnB');
  bA.textContent = `Entrada A = ${{bitA}}`; bA.classList.toggle('on', bitA === 1);
  bB.textContent = `Entrada B = ${{bitB}}`; bB.classList.toggle('on', bitB === 1);
  renderLogica();
}}

function renderLogica() {{
  const andAB = bitA & bitB, orAB = bitA | bitB, xorAB = bitA ^ bitB, nandAB = 1 - andAB;
  document.getElementById('logicaOut').innerHTML =
    `<table><thead><tr><th>Compuerta</th><th>Salida</th><th>Rol en circuito</th></tr></thead><tbody>` +
    `<tr><td>A AND B</td><td><b>${{andAB}}</b></td><td>Acarreo (Carry) del Half-Adder</td></tr>` +
    `<tr><td>A OR B</td><td><b>${{orAB}}</b></td><td>Disyunción inclusiva</td></tr>` +
    `<tr><td>A XOR B</td><td><b>${{xorAB}}</b></td><td>Suma (Sum) del Half-Adder (0+1=1, 1+1=0)</td></tr>` +
    `<tr><td>A NAND B</td><td><b>${{nandAB}}</b></td><td>Compuerta universal (construye cualquier circuito)</td></tr>` +
    `</tbody></table>` +
    `<p style="margin-top:.75rem"><b>Half-Adder (${{bitA}} + ${{bitB}}):</b> Suma = <code>${{xorAB}}</code>, Acarreo = <code>${{andAB}}</code> → Binario = <code>${{andAB}}${{xorAB}}</code> (${{bitA + bitB}} decimal)</p>`;
}}

function calcBinario() {{
  const raw = document.getElementById('numInput').value.trim();
  const out = document.getElementById('binOut');
  const n = Number(raw);
  if (!raw || Number.isNaN(n)) {{ out.textContent = 'Ingresa un número válido.'; return; }}
  const buf = new ArrayBuffer(8);
  const view = new DataView(buf);
  view.setFloat64(0, n, false);
  let bits64 = '';
  for (let i = 0; i < 8; i++) bits64 += view.getUint8(i).toString(2).padStart(8, '0');
  const signo = bits64[0], exp = bits64.slice(1, 12), mant = bits64.slice(12);
  let enteroHtml = '';
  if (Number.isInteger(n) && n >= -2147483648 && n <= 2147483647) {{
    const u8 = (n & 0xFF).toString(2).padStart(8, '0');
    const u16 = (n & 0xFFFF).toString(2).padStart(16, '0');
    const hex = (n >>> 0).toString(16).toUpperCase();
    enteroHtml = `<p><b>Entero:</b> 8-bit (c2): <code>${{u8}}</code> | 16-bit: <code>${{u16}}</code> | Hex 32-bit: <code>0x${{hex}}</code></p>`;
  }}
  out.innerHTML = enteroHtml +
    `<p><b>Valor exacto IEEE-754 en memoria:</b> <code>${{n.toPrecision(21)}}</code></p>` +
    `<p><b>Signo (1):</b> <code>${{signo}}</code> | <b>Exponente (11):</b> <code>${{exp}}</code></p>` +
    `<p><b>Mantisa (52):</b> <code>${{mant}}</code></p>`;
}}

function runRegex() {{
  const pat = document.getElementById('rxPat').value;
  const txt = document.getElementById('rxTxt').value;
  const out = document.getElementById('rxOut');
  try {{
    const rx = new RegExp(pat);
    const m = rx.exec(txt);
    out.innerHTML = m ? `<span style="color:var(--ok)">COINCIDE:</span> <code>${{m[0]}}</code>` : `<span style="color:var(--warn)">NO COINCIDE</span>`;
  }} catch (e) {{
    out.innerHTML = `<span style="color:var(--err)">Patrón inválido:</span> ${{e.message}}`;
  }}
}}

function runChmod() {{
  const oct = document.getElementById('chOct').value.trim();
  const out = document.getElementById('chOut');
  if (!/^[0-7]{{3}}$/.test(oct)) {{ out.textContent = 'Usa 3 dígitos octales entre 0 y 7 (ej. 750).'; return; }}
  const fmt = d => ((d & 4) ? 'r' : '-') + ((d & 2) ? 'w' : '-') + ((d & 1) ? 'x' : '-');
  const [u, g, o] = oct.split('').map(Number);
  out.innerHTML = `Simbólico: <code>${{fmt(u)}}${{fmt(g)}}${{fmt(o)}}</code> (Dueño=${{u}}, Grupo=${{g}}, Otros=${{o}})`;
}}

function runPid() {{
  const sp = Number(document.getElementById('spIn').value);
  const kp = Number(document.getElementById('kpIn').value);
  const ki = Number(document.getElementById('kiIn').value);
  const kd = Number(document.getElementById('kdIn').value);
  document.getElementById('spVal').textContent = sp;
  document.getElementById('kpVal').textContent = kp;
  document.getElementById('kiVal').textContent = ki;
  document.getElementById('kdVal').textContent = kd;
  let y = 0, integral = 0, prev = sp, dt = 0.1;
  const pts = [];
  for (let k = 0; k < 100; k++) {{
    const err = sp - y, der = (err - prev) / dt, ic = integral + err * dt;
    const raw = kp * err + ki * ic + kd * der;
    let u = raw;
    if (raw > 100) {{ u = 100; if (err < 0) integral = ic; }}
    else if (raw < -100) {{ u = -100; if (err > 0) integral = ic; }}
    else {{ integral = ic; }}
    y = y + dt * (-0.5 * y + 0.5 * u);
    prev = err;
    pts.push(y);
  }}
  const maxY = Math.max(sp * 1.25, ...pts, 10);
  const mapY = v => (205 - (v / maxY) * 185).toFixed(1);
  const poly = pts.map((v, i) => `${{(i * 6).toFixed(1)}},${{mapY(v)}}`).join(' ');
  const spY = mapY(sp);
  document.getElementById('pidSvg').innerHTML =
    `<line x1="0" y1="${{spY}}" x2="600" y2="${{spY}}" stroke="#fbbf24" stroke-dasharray="5,5" stroke-width="1.5"/>` +
    `<polyline fill="none" stroke="#2dd4bf" stroke-width="2.5" points="${{poly}}"/>`;
  const pico = Math.max(...pts);
  document.getElementById('pidStats').textContent = `Final=${{pts[pts.length-1].toFixed(2)}} | Pico=${{pico.toFixed(2)}} | Error final=${{Math.abs(sp - pts[pts.length-1]).toFixed(2)}}`;
}}

function renderQuiz() {{
  const host = document.getElementById('quizHost');
  host.innerHTML = '';
  const filtradas = PREGUNTAS.filter(p => nivelQuiz === 'todos' || p.nivel === nivelQuiz);
  filtradas.forEach((p, idx) => {{
    const card = document.createElement('div');
    card.className = 'card';
    card.style.marginBottom = '1rem';
    card.innerHTML = `<span class="badge">${{p.etapa}} · ${{p.nivel}}</span><h3 style="margin:.4rem 0">${{idx + 1}}. ${{p.pregunta}}</h3>`;
    p.opciones.forEach((op, oi) => {{
      const b = document.createElement('button');
      b.className = 'opt-btn';
      b.textContent = `${{oi + 1}}) ${{op}}`;
      if (respuestas.has(p.id)) {{
        const elegida = respuestas.get(p.id);
        if (oi === p.correcta) b.classList.add('ok');
        else if (oi === elegida) b.classList.add('bad');
      }}
      b.onclick = () => {{ respuestas.set(p.id, oi); guardarEstado(); renderQuiz(); }};
      card.appendChild(b);
    }});
    if (respuestas.has(p.id)) {{
      const fb = document.createElement('div');
      fb.className = 'feynman-box';
      fb.innerHTML = `<b>Explicación Feynman:</b> ${{p.explicacion_feynman}}`;
      card.appendChild(fb);
    }}
    host.appendChild(card);
  }});
  let ok = 0, respVista = 0;
  filtradas.forEach(p => {{
    if (respuestas.has(p.id)) {{
      respVista++;
      if (respuestas.get(p.id) === p.correcta) ok++;
    }}
  }});
  document.getElementById('quizScore').textContent = `Filtro actual: ${{respVista}}/${{filtradas.length}} respondidas · Aciertos: ${{ok}} (Total banco: ${{PREGUNTAS.length}})`;
}}

function renderFmhy() {{
  const q = document.getElementById('fmhySearch').value.trim().toLowerCase();
  const body = document.getElementById('fmhyBody');
  const filtrados = RECURSOS.filter(r => !q || `${{r.nombre}} ${{r.categoria}} ${{r.uso}}`.toLowerCase().includes(q));
  body.innerHTML = filtrados.map(r =>
    `<tr><td><a href="${{r.url}}" target="_blank" rel="noopener">${{r.nombre}}</a></td><td>${{r.categoria}}</td><td><code>${{r.origen}}</code></td><td>${{r.uso}}</td></tr>`
  ).join('');
}}

function combinarCF(a, b) {{
  if (a > 0 && b > 0) return a + b * (1 - a);
  if (a < 0 && b < 0) return a + b * (1 + a);
  const den = 1 - Math.min(Math.abs(a), Math.abs(b));
  return den === 0 ? 0 : (a + b) / den;
}}

function runExperto() {{
  const hechos = {{}};
  if (document.getElementById('hLatencia').checked) hechos.latencia_alta = 0.90;
  if (document.getElementById('hPaquetes').checked) hechos.perdida_paquetes = 1.00;
  if (document.getElementById('hCpu').checked) hechos.cpu_100 = 0.80;
  if (document.getElementById('hSwap').checked) hechos.sin_swap = 0.90;
  const reglas = [
    {{ id: 'R1', ant: ['latencia_alta', 'perdida_paquetes'], con: 'congestion_red', cf: 0.80 }},
    {{ id: 'R2', ant: ['cpu_100', 'sin_swap'], con: 'saturacion_nodo', cf: 0.75 }},
    {{ id: 'R3', ant: ['congestion_red'], con: 'alerta_incidente_p1', cf: 0.90 }},
    {{ id: 'R4', ant: ['saturacion_nodo'], con: 'alerta_incidente_p1', cf: 0.85 }},
  ];

  const mem = {{ ...hechos }};
  const disp = new Set();
  const trazaFwd = [];
  let cambio = true;
  while (cambio) {{
    cambio = false;
    for (const r of reglas) {{
      if (disp.has(r.id)) continue;
      if (r.ant.every(a => (mem[a] || 0) > 0)) {{
        const cfAnt = Math.min(...r.ant.map(a => mem[a]));
        const aporte = cfAnt * r.cf;
        disp.add(r.id);
        mem[r.con] = mem[r.con] !== undefined ? combinarCF(mem[r.con], aporte) : aporte;
        trazaFwd.push(`${{r.id}} → ${{r.con}} (CF=${{mem[r.con].toFixed(3)}})`);
        cambio = true;
      }}
    }}
  }}

  const meta = document.getElementById('seMeta').value;
  function probar(g, vis) {{
    if (hechos[g] !== undefined) return {{ ok: true, cf: hechos[g], pasos: [`Hecho base '${{g}}' (CF=${{hechos[g].toFixed(2)}})`] }};
    if (vis.has(g)) return {{ ok: false, cf: 0, pasos: [] }};
    const nextVis = new Set([...vis, g]);
    let cfAcc = null, pasos = [];
    for (const r of reglas.filter(x => x.con === g)) {{
      const subs = r.ant.map(a => probar(a, nextVis));
      if (subs.every(s => s.ok)) {{
        const cfAnt = Math.min(...subs.map(s => s.cf));
        const aporte = cfAnt * r.cf;
        cfAcc = cfAcc === null ? aporte : combinarCF(cfAcc, aporte);
        subs.forEach(s => pasos.push(...s.pasos));
        pasos.push(`${{r.id}} deduce '${{g}}' (CF=${{aporte.toFixed(3)}})`);
      }}
    }}
    return cfAcc !== null ? {{ ok: true, cf: cfAcc, pasos }} : {{ ok: false, cf: 0, pasos: [] }};
  }}
  const bwd = probar(meta, new Set());
  document.getElementById('seOut').innerHTML =
    `<p><b>Forward Chaining:</b> ${{trazaFwd.length ? trazaFwd.join(' | ') : 'Ninguna regla disparada'}}</p>` +
    `<p><b>Backward Chaining ('${{meta}}'):</b> ${{bwd.ok ? `<span style="color:var(--ok)">PROBADA (CF=${{bwd.cf.toFixed(3)}})</span>` : `<span style="color:var(--warn)">NO PROBADA</span>`}}</p>` +
    (bwd.pasos.length ? `<p style="color:var(--muted)"><b>Explicación (How):</b> ${{bwd.pasos.join(' → ')}}</p>` : '');
}}

function parseTerm(src) {{
  let i = 0;
  function skipWs() {{ while (i < src.length && /\\s/.test(src[i])) i++; }}
  function parseExpr() {{
    skipWs();
    const start = i;
    while (i < src.length && /[A-Za-z0-9_]/.test(src[i])) i++;
    const name = src.slice(start, i);
    if (!name) throw new Error('Se esperaba identificador');
    skipWs();
    if (src[i] === '(') {{
      i++;
      const args = [];
      skipWs();
      if (src[i] !== ')') {{
        while (true) {{
          args.push(parseExpr());
          skipWs();
          if (src[i] === ',') {{ i++; continue; }}
          if (src[i] === ')') break;
          throw new Error("Falta ',' o ')'");
        }}
      }}
      i++;
      return {{ kind: 'term', functor: name, args }};
    }}
    if (/^[A-Z_]/.test(name)) return {{ kind: 'var', name }};
    return {{ kind: 'term', functor: name, args: [] }};
  }}
  const res = parseExpr();
  skipWs();
  if (i !== src.length) throw new Error('Sobran caracteres al final');
  return res;
}}

function termToString(t, env) {{
  t = deref(t, env);
  if (t.kind === 'var') return t.name;
  return t.args.length ? `${{t.functor}}(${{t.args.map(a => termToString(a, env)).join(', ')}})` : t.functor;
}}

function deref(t, env) {{
  while (t.kind === 'var' && env[t.name]) t = env[t.name];
  return t;
}}

function occurs(vName, t, env) {{
  t = deref(t, env);
  if (t.kind === 'var') return t.name === vName;
  return t.args.some(a => occurs(vName, a, env));
}}

function unifyJs(a, b, env) {{
  a = deref(a, env);
  b = deref(b, env);
  if (a.kind === 'var' && b.kind === 'var' && a.name === b.name) return env;
  if (a.kind === 'var') {{
    if (occurs(a.name, b, env)) return null;
    return {{ ...env, [a.name]: b }};
  }}
  if (b.kind === 'var') {{
    if (occurs(b.name, a, env)) return null;
    return {{ ...env, [b.name]: a }};
  }}
  if (a.functor !== b.functor || a.args.length !== b.args.length) return null;
  let cur = env;
  for (let idx = 0; idx < a.args.length; idx++) {{
    cur = unifyJs(a.args[idx], b.args[idx], cur);
    if (!cur) return null;
  }}
  return cur;
}}

function runUnificacion() {{
  const out = document.getElementById('uniOut');
  try {{
    const t1 = parseTerm(document.getElementById('uniT1').value);
    const t2 = parseTerm(document.getElementById('uniT2').value);
    const sust = unifyJs(t1, t2, {{}});
    if (!sust) {{
      out.innerHTML = `<span style="color:var(--warn)">NO UNIFICAN</span> (choque de functor/aridad o bloqueo por <em>occurs check</em>)`;
      return;
    }}
    const pares = Object.keys(sust).map(k => `<code>${{k}} = ${{termToString(sust[k], sust)}}</code>`);
    out.innerHTML = `<span style="color:var(--ok)">UNIFICACIÓN EXITOSA:</span> ${{pares.length ? pares.join(' · ') : 'Términos idénticos sin sustituciones'}}`;
  }} catch (e) {{
    out.innerHTML = `<span style="color:var(--err)">Error de sintaxis:</span> ${{e.message}}`;
  }}
}}

function runBayes() {{
  const obsLat = document.getElementById('bayLatencia').checked;
  const obsPico = document.getElementById('bayPico').checked;
  const pFalla = 0.02, pPico = 0.05;
  const cptLat = (f, p) => (f && p) ? 0.98 : (f && !p) ? 0.85 : (!f && p) ? 0.80 : 0.01;
  let numF = 0, den = 0;
  for (const f of [true, false]) {{
    const pf = f ? pFalla : 1 - pFalla;
    for (const p of [true, false]) {{
      if (obsPico && !p) continue;
      const pp = p ? pPico : 1 - pPico;
      const pl = obsLat ? cptLat(f, p) : 1.0;
      const joint = pf * pp * pl;
      den += joint;
      if (f) numF += joint;
    }}
  }}
  const post = den > 0 ? (numF / den) : 0;
  document.getElementById('bayOut').innerHTML =
    `<p><b>P(FallaDisco = True | evidencia):</b> <span style="color:var(--accent)">${{(post * 100).toFixed(2)}}%</span></p>` +
    `<p style="color:var(--muted)">Sin observar PicoRed pero con Latencia Alta, la sospecha sobre FallaDisco sube a ~24.8%; al confirmar PicoRed=True, baja a ~2.44% (<em>explaining away</em>).</p>`;
}}

actualizarBarraProgreso();
mostrarModulo(MODULOS[0].id);
renderLogica();
calcBinario();
runRegex();
runChmod();
runPid();
renderQuiz();
renderFmhy();
runExperto();
runUnificacion();
runBayes();
</script>
</body>
</html>
"""


def main() -> int:
    destino = RAIZ / "docs" / "index.html"
    destino.write_text(construir_html(), encoding="utf-8")
    print(f"Generado {destino} ({destino.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
