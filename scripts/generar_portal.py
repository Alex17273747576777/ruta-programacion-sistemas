#!/usr/bin/env python3
"""Genera docs/index.html (portal interactivo autocontenido sin dependencias externas ni enlaces rotos)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPO_BLOB = "https://github.com/Alex17273747576777/ruta-programacion-sistemas/blob/main"


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
                out.append("<table><thead><tr>" + "".join(f"<th>{_inline_md(c)}</th>" for c in celdas) + "</tr></thead><tbody>")
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
            out.append(f"<li>{_inline_md(re.sub(r'^[-*]\\s+', '', linea))}</li>")
            continue
        if re.match(r"^\d+\.\s+", linea):
            if en_ul:
                out.append("</ul>")
                en_ul = False
            if not en_ol:
                out.append("<ol>")
                en_ol = True
            out.append(f"<li>{_inline_md(re.sub(r'^\\d+\\.\\s+', '', linea))}</li>")
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
            modulos.append(
                {
                    "id": rel,
                    "grupo": grupo,
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
<title>Ruta de Programación y Sistemas · Feynman + Playgrounds + FMHY</title>
<style>
  :root {{
    --bg: #0f172a; --panel: #1e293b; --line: #334155;
    --text: #f1f5f9; --muted: #94a3b8; --accent: #38bdf8;
    --ok: #22c55e; --warn: #f59e0b; --err: #ef4444;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.55;
  }}
  header {{
    padding: 2rem 1.25rem; border-bottom: 1px solid var(--line);
    background: linear-gradient(135deg, #0f172a, #172554);
  }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 1rem; }}
  h1, h2, h3 {{ margin-top: 0; }}
  nav {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }}
  .tab-btn {{
    background: var(--panel); color: var(--text); border: 1px solid var(--line);
    padding: .55rem .9rem; border-radius: .5rem; cursor: pointer; font-weight: 600;
  }}
  .tab-btn.active {{ background: var(--accent); color: #082f49; border-color: var(--accent); }}
  main {{ padding: 1.5rem 0 3rem; }}
  section.panel {{ display: none; }}
  section.panel.active {{ display: block; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 1rem; }}
  .card {{
    background: var(--panel); border: 1px solid var(--line); border-radius: .75rem;
    padding: 1rem 1.15rem;
  }}
  .badge {{
    display: inline-block; font-size: .75rem; padding: .15rem .5rem; border-radius: 999px;
    background: #0ea5e922; color: var(--accent); border: 1px solid #38bdf844;
  }}
  input, textarea, select {{
    width: 100%; background: #0b1220; color: var(--text); border: 1px solid var(--line);
    border-radius: .5rem; padding: .55rem .7rem; font-family: ui-monospace, monospace;
  }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .9rem; }}
  a {{ color: var(--accent); }}
  .link-btn {{
    background: #0b1220; color: var(--accent); border: 1px solid var(--line);
    padding: .3rem .65rem; border-radius: .4rem; cursor: pointer; font-size: .85rem;
  }}
  .opt-btn {{
    display: block; width: 100%; text-align: left; margin: .4rem 0;
    background: #0b1220; color: var(--text); border: 1px solid var(--line);
    border-radius: .5rem; padding: .6rem .8rem; cursor: pointer;
  }}
  .opt-btn.ok {{ border-color: var(--ok); background: #14532d55; }}
  .opt-btn.bad {{ border-color: var(--err); background: #7f1d1d55; }}
  .feynman-box, blockquote {{
    margin: .75rem 0; padding: .75rem; border-left: 3px solid var(--accent);
    background: #0b1220; border-radius: 0 .5rem .5rem 0;
  }}
  pre {{ background: #0b1220; border: 1px solid var(--line); border-radius: .5rem; padding: .75rem; overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
  th, td {{ border-bottom: 1px solid var(--line); padding: .5rem; text-align: left; }}
  .lector-wrap {{ display: grid; grid-template-columns: 290px 1fr; gap: 1rem; }}
  @media (max-width: 820px) {{ .lector-wrap {{ grid-template-columns: 1fr; }} }}
  .doc-item {{
    display: block; width: 100%; text-align: left; background: #0b1220; color: var(--text);
    border: 1px solid var(--line); border-radius: .45rem; padding: .45rem .65rem; margin-bottom: .35rem; cursor: pointer;
  }}
  .doc-item.active {{ border-color: var(--accent); color: var(--accent); }}
  .bit-btn {{
    padding: .5rem 1rem; font-weight: 700; border-radius: .5rem; cursor: pointer;
    border: 1px solid var(--line); background: #0b1220; color: var(--text);
  }}
  .bit-btn.on {{ background: var(--ok); color: #052e16; border-color: var(--ok); }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <span class="badge">Método Richard Feynman completo (4 pasos) · Recursos activos FMHY.net</span>
    <h1>De Principiante a Ingeniería de Sistemas</h1>
    <p style="color:var(--muted);margin:.25rem 0 0">
      6 etapas con proyectos probados · 5 laboratorios (C99, C++20, Node, PID, Bash) · {len(modulos)} módulos integrados · 5 Playgrounds sin dependencias · Quiz ({len(preguntas)} preguntas).
    </p>
    <nav>
      <button class="tab-btn active" onclick="showTab('roadmap', this)">Roadmap y Código</button>
      <button class="tab-btn" onclick="showTab('lector', this)">Lector Completo ({len(modulos)})</button>
      <button class="tab-btn" onclick="showTab('binario', this)">Binario / IEEE-754</button>
      <button class="tab-btn" onclick="showTab('logica', this)">Compuertas &amp; Half-Adder</button>
      <button class="tab-btn" onclick="showTab('regex', this)">Regex &amp; chmod</button>
      <button class="tab-btn" onclick="showTab('pid', this)">Control PID</button>
      <button class="tab-btn" onclick="showTab('quiz', this)">Quiz ({len(preguntas)})</button>
      <button class="tab-btn" onclick="showTab('fmhy', this)">FMHY ({len(recursos)})</button>
    </nav>
  </div>
</header>

<main class="wrap">
  <section id="roadmap" class="panel active">
    <h2>1. Las 6 etapas con código probado en CI</h2>
    <div class="grid">
      <div class="card"><span class="badge">Etapa 1</span><h3>Fundamentos</h3><p>Calculadora exacta con <code>Decimal</code> (sin <code>eval</code>) y agenda JSON atómica (<code>os.replace</code>).</p><p><button class="link-btn" onclick="abrirModulo('etapas/01-fundamentos.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/01_fundamentos" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card"><span class="badge">Etapa 2</span><h3>Modelado y Pruebas</h3><p>Biblioteca de préstamos con dominio desacoplado, reloj inyectable e invariantes estrictas.</p><p><button class="link-btn" onclick="abrirModulo('etapas/02-modelado.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/02_modelado" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card"><span class="badge">Etapa 3</span><h3>Datos y Concurrencia</h3><p>Inventario transaccional sin stock negativo bajo carreras reales con barrera e idempotencia.</p><p><button class="link-btn" onclick="abrirModulo('etapas/03-datos.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/03_datos" target="_blank" rel="noopener">Código + SQL</a></p></div>
      <div class="card"><span class="badge">Etapa 4</span><h3>Redes y Seguridad</h3><p>API HTTP real con autenticación, autorización por recurso (<code>403</code>) y límites de entrada.</p><p><button class="link-btn" onclick="abrirModulo('etapas/04-redes.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/04_redes" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card"><span class="badge">Etapa 5</span><h3>Operación</h3><p>Liveness vs Readiness, logs sin secretos, respaldo SQLite Backup API y restauración SHA-256.</p><p><button class="link-btn" onclick="abrirModulo('etapas/05-operacion.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/05_operacion" target="_blank" rel="noopener">Código en GitHub</a></p></div>
      <div class="card"><span class="badge">Etapa 6</span><h3>Sistemas Distribuidos</h3><p>Transactional Outbox, consumidor idempotente ante caídas, caché TTL y percentiles p50/p95.</p><p><button class="link-btn" onclick="abrirModulo('etapas/06-sistemas.md')">Leer etapa</button> · <a href="{REPO_BLOB}/proyectos/06_sistemas" target="_blank" rel="noopener">Código en GitHub</a></p></div>
    </div>

    <h2 style="margin-top:1.5rem">2. Laboratorios multi-lenguaje ejecutables</h2>
    <div class="grid">
      <div class="card"><h3>C99 · Memoria y Overflow</h3><p>Suma segura contra desbordamiento y copia acotada sin lectura fuera de rango.</p><a href="{REPO_BLOB}/laboratorios/c_memoria/buffer_seguro.c" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>C++20 · RAII y <code>unique_ptr</code></h3><p>Liberación determinista de recursos incluso al lanzar excepciones.</p><a href="{REPO_BLOB}/laboratorios/cpp_raii/raii_pool.cpp" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Node.js · Event Loop</h3><p>Verificación en vivo de orden sincrónico → microtareas → macrotareas.</p><a href="{REPO_BLOB}/laboratorios/node_event_loop/event_loop_orden.mjs" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Control PID Discreto</h3><p>Simulador en Python con anti-windup y prueba de convergencia.</p><a href="{REPO_BLOB}/laboratorios/control_pid/simulador_pid.py" target="_blank" rel="noopener">Ver en GitHub</a></div>
      <div class="card"><h3>Bash Estricto</h3><p>Auditoría reproducible de entorno con <code>set -euo pipefail</code>.</p><a href="{REPO_BLOB}/laboratorios/bash_diagnostico/verificar_entorno.sh" target="_blank" rel="noopener">Ver en GitHub</a></div>
    </div>
  </section>

  <section id="lector" class="panel">
    <h2>Lector completo de Etapas, Guías y CheatSheets ({len(modulos)} módulos)</h2>
    <div class="lector-wrap">
      <div class="card">
        <input id="docFilter" placeholder="Filtrar módulo..." oninput="renderDocList()" style="margin-bottom:.75rem">
        <div id="docList"></div>
      </div>
      <div class="card">
        <p style="margin-top:0"><a id="docGhLink" href="{REPO_BLOB}" target="_blank" rel="noopener">Abrir fuente en GitHub</a></p>
        <div id="docViewer"></div>
      </div>
    </div>
  </section>

  <section id="binario" class="panel">
    <h2>Playground · Binario, Complemento a Dos e IEEE-754 (64 bits)</h2>
    <div class="card">
      <label for="numInput">Escribe un número entero o decimal (ej. <code>0.1</code>, <code>-42</code>, <code>255</code>):</label>
      <input id="numInput" value="0.1" oninput="calcBinario()" style="margin:.5rem 0 1rem">
      <div id="binOut" class="mono"></div>
    </div>
  </section>

  <section id="logica" class="panel">
    <h2>Playground · Compuertas Lógicas Digitales &amp; Half-Adder</h2>
    <div class="card">
      <p>Conmuta las entradas binarias <code>A</code> y <code>B</code> para observar compuertas básicas, la universal <code>NAND</code> y un medio sumador (<code>Suma = A XOR B</code>, <code>Acarreo = A AND B</code>):</p>
      <div style="display:flex;gap:.75rem;margin-bottom:1rem">
        <button id="btnA" class="bit-btn" onclick="toggleBit('A')">A = 0</button>
        <button id="btnB" class="bit-btn" onclick="toggleBit('B')">B = 0</button>
      </div>
      <div id="logicOut" class="mono"></div>
    </div>
  </section>

  <section id="regex" class="panel">
    <h2>Playground · Expresiones Regulares &amp; Permisos UNIX (chmod)</h2>
    <div class="grid">
      <div class="card">
        <h3>Probador Regex en vivo</h3>
        <label>Patrón:</label><input id="rxPat" value="^[A-Za-z0-9_-]{{3,16}}$" oninput="runRegex()" style="margin:.35rem 0">
        <label>Texto de prueba:</label><input id="rxTxt" value="sku-01" oninput="runRegex()" style="margin:.35rem 0">
        <div id="rxOut" class="mono" style="margin-top:.6rem"></div>
      </div>
      <div class="card">
        <h3>Calculadora chmod (octal ↔ simbólica)</h3>
        <label>Octal (3 dígitos 0-7):</label><input id="chOct" value="750" maxlength="3" oninput="runChmod()" style="margin:.35rem 0">
        <div id="chOut" class="mono" style="margin-top:.6rem"></div>
      </div>
    </div>
  </section>

  <section id="pid" class="panel">
    <h2>Playground · Simulador de Lazo Cerrado PID (con anti-windup)</h2>
    <div class="card">
      <div class="grid" style="margin-bottom:.75rem">
        <div><label>Setpoint: <b id="spVal">50</b></label><input type="range" id="spIn" min="10" max="90" value="50" oninput="runPid()"></div>
        <div><label>Kp: <b id="kpVal">2.4</b></label><input type="range" id="kpIn" min="0.2" max="8" step="0.2" value="2.4" oninput="runPid()"></div>
        <div><label>Ki: <b id="kiVal">1.2</b></label><input type="range" id="kiIn" min="0" max="4" step="0.1" value="1.2" oninput="runPid()"></div>
        <div><label>Kd: <b id="kdVal">0.15</b></label><input type="range" id="kdIn" min="0" max="2" step="0.05" value="0.15" oninput="runPid()"></div>
      </div>
      <div id="pidStats" class="mono" style="margin-bottom:.5rem"></div>
      <svg id="pidSvg" viewBox="0 0 600 220" style="width:100%;max-height:240px;background:#0b1220;border:1px solid var(--line);border-radius:.5rem"></svg>
    </div>
  </section>

  <section id="quiz" class="panel">
    <h2>Quiz Interactivo Feynman ({len(preguntas)} preguntas)</h2>
    <p id="quizScore" style="color:var(--muted)"></p>
    <div id="quizHost"></div>
  </section>

  <section id="fmhy" class="panel">
    <h2>Catálogo curado de recursos activos FMHY.net ({len(recursos)})</h2>
    <input id="fmhySearch" placeholder="Filtrar por tema, nombre o herramienta (ej. Rust, SQL, Wokwi, Linux)..." oninput="renderFmhy()" style="margin-bottom:1rem">
    <div class="card" style="overflow-x:auto">
      <table><thead><tr><th>Recurso</th><th>Categoría</th><th>Origen</th><th>Uso en la ruta</th></tr></thead><tbody id="fmhyBody"></tbody></table>
    </div>
  </section>
</main>

<script>
const PREGUNTAS = {preguntas_json};
const RECURSOS = {recursos_json};
const MODULOS = {modulos_json};
let moduloActual = MODULOS[0] ? MODULOS[0].id : '';

function showTab(id, btn) {{
  document.querySelectorAll('section.panel').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  if (btn) btn.classList.add('active');
}}

function abrirModulo(id) {{
  moduloActual = id;
  renderDocList();
  const lectorBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.textContent.startsWith('Lector'));
  showTab('lector', lectorBtn);
}}

function renderDocList() {{
  const q = document.getElementById('docFilter').value.trim().toLowerCase();
  const list = document.getElementById('docList');
  list.innerHTML = '';
  const filtrados = MODULOS.filter(m => !q || `${{m.grupo}} ${{m.titulo}} ${{m.id}}`.toLowerCase().includes(q));
  filtrados.forEach(m => {{
    const b = document.createElement('button');
    b.className = 'doc-item' + (m.id === moduloActual ? ' active' : '');
    b.textContent = `[${{m.grupo}}] ${{m.titulo}}`;
    b.onclick = () => {{ moduloActual = m.id; renderDocList(); }};
    list.appendChild(b);
  }});
  const actual = MODULOS.find(m => m.id === moduloActual) || filtrados[0];
  if (actual) {{
    document.getElementById('docViewer').innerHTML = actual.html;
    document.getElementById('docGhLink').href = actual.github;
  }}
}}

let bitA = 0, bitB = 0;
function toggleBit(which) {{
  if (which === 'A') bitA = bitA ? 0 : 1;
  else bitB = bitB ? 0 : 1;
  renderLogic();
}}
function renderLogic() {{
  const bA = document.getElementById('btnA'), bB = document.getElementById('btnB');
  bA.textContent = `A = ${{bitA}}`; bA.classList.toggle('on', bitA === 1);
  bB.textContent = `B = ${{bitB}}`; bB.classList.toggle('on', bitB === 1);
  const notA = bitA ? 0 : 1, andAB = bitA & bitB, orAB = bitA | bitB, xorAB = bitA ^ bitB, nandAB = andAB ? 0 : 1;
  document.getElementById('logicOut').innerHTML =
    `<table><thead><tr><th>Operación</th><th>Salida</th><th>Uso típico</th></tr></thead><tbody>` +
    `<tr><td>NOT A</td><td><b>${{notA}}</b></td><td>Inversor lógico</td></tr>` +
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
    `<line x1="0" y1="${{spY}}" x2="600" y2="${{spY}}" stroke="#f59e0b" stroke-dasharray="5,5" stroke-width="1.5"/>` +
    `<polyline fill="none" stroke="#38bdf8" stroke-width="2.5" points="${{poly}}"/>`;
  const pico = Math.max(...pts);
  document.getElementById('pidStats').textContent = `Final=${{pts[pts.length-1].toFixed(2)}} | Pico=${{pico.toFixed(2)}} | Error final=${{Math.abs(sp - pts[pts.length-1]).toFixed(2)}}`;
}}

const respuestas = new Map();
function renderQuiz() {{
  const host = document.getElementById('quizHost');
  host.innerHTML = '';
  PREGUNTAS.forEach((p, idx) => {{
    const card = document.createElement('div');
    card.className = 'card';
    card.style.marginBottom = '1rem';
    card.innerHTML = `<span class="badge">${{p.etapa}}</span><h3 style="margin:.4rem 0">${{idx + 1}}. ${{p.pregunta}}</h3>`;
    p.opciones.forEach((op, oi) => {{
      const b = document.createElement('button');
      b.className = 'opt-btn';
      b.textContent = `${{oi + 1}}) ${{op}}`;
      if (respuestas.has(p.id)) {{
        const elegida = respuestas.get(p.id);
        if (oi === p.correcta) b.classList.add('ok');
        else if (oi === elegida) b.classList.add('bad');
      }}
      b.onclick = () => {{ respuestas.set(p.id, oi); renderQuiz(); }};
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
  let ok = 0;
  PREGUNTAS.forEach(p => {{ if (respuestas.get(p.id) === p.correcta) ok++; }});
  document.getElementById('quizScore').textContent = `Respondidas: ${{respuestas.size}}/${{PREGUNTAS.length}} · Aciertos: ${{ok}}`;
}}

function renderFmhy() {{
  const q = document.getElementById('fmhySearch').value.trim().toLowerCase();
  const body = document.getElementById('fmhyBody');
  const filtrados = RECURSOS.filter(r => !q || `${{r.nombre}} ${{r.categoria}} ${{r.uso}}`.toLowerCase().includes(q));
  body.innerHTML = filtrados.map(r =>
    `<tr><td><a href="${{r.url}}" target="_blank" rel="noopener">${{r.nombre}}</a></td><td>${{r.categoria}}</td><td><code>${{r.origen}}</code></td><td>${{r.uso}}</td></tr>`
  ).join('');
}}

renderDocList(); renderLogic(); calcBinario(); runRegex(); runChmod(); runPid(); renderQuiz(); renderFmhy();
</script>
</body>
</html>
"""


def main() -> int:
    salida = RAIZ / "docs" / "index.html"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(construir_html(), encoding="utf-8")
    print(f"Generado {salida.relative_to(RAIZ)} ({len(salida.read_text(encoding='utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
