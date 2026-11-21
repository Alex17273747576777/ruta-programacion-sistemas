#!/usr/bin/env python3
"""Genera docs/index.html (portal interactivo autocontenido sin dependencias externas)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


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


def construir_html() -> str:
    preguntas = json.loads((RAIZ / "quizzes" / "banco_preguntas.json").read_text(encoding="utf-8"))
    recursos = extraer_recursos_fmhy()

    preguntas_json = json.dumps(preguntas, ensure_ascii=False)
    recursos_json = json.dumps(recursos, ensure_ascii=False)

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
  .wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 1rem; }}
  h1, h2, h3 {{ margin-top: 0; }}
  nav {{
    display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem;
  }}
  .tab-btn {{
    background: var(--panel); color: var(--text); border: 1px solid var(--line);
    padding: .55rem .9rem; border-radius: .5rem; cursor: pointer; font-weight: 600;
  }}
  .tab-btn.active {{ background: var(--accent); color: #082f49; border-color: var(--accent); }}
  main {{ padding: 1.5rem 0 3rem; }}
  section.panel {{ display: none; }}
  section.panel.active {{ display: block; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
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
  .opt-btn {{
    display: block; width: 100%; text-align: left; margin: .4rem 0;
    background: #0b1220; color: var(--text); border: 1px solid var(--line);
    border-radius: .5rem; padding: .6rem .8rem; cursor: pointer;
  }}
  .opt-btn.ok {{ border-color: var(--ok); background: #14532d55; }}
  .opt-btn.bad {{ border-color: var(--err); background: #7f1d1d55; }}
  .feynman-box {{
    margin-top: .75rem; padding: .75rem; border-left: 3px solid var(--accent);
    background: #0b1220; border-radius: 0 .5rem .5rem 0;
  }}
  table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
  th, td {{ border-bottom: 1px solid var(--line); padding: .5rem; text-align: left; }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <span class="badge">Método Richard Feynman completo (4 pasos) · Recursos activos FMHY.net</span>
    <h1>De Principiante a Ingeniería de Sistemas</h1>
    <p style="color:var(--muted);margin:.25rem 0 0">
      6 etapas con proyectos probados en Python/SQL/HTTP · 6 guías técnicas · 7 cheatsheets · Playgrounds sin dependencias · Quiz interactivo ({len(preguntas)} preguntas).
    </p>
    <nav>
      <button class="tab-btn active" onclick="showTab('roadmap', this)">Roadmap y Proyectos</button>
      <button class="tab-btn" onclick="showTab('binario', this)">Playground Binario / IEEE-754</button>
      <button class="tab-btn" onclick="showTab('regex', this)">Playground Regex &amp; chmod</button>
      <button class="tab-btn" onclick="showTab('quiz', this)">Quiz Feynman ({len(preguntas)})</button>
      <button class="tab-btn" onclick="showTab('fmhy', this)">Catálogo FMHY ({len(recursos)})</button>
    </nav>
  </div>
</header>

<main class="wrap">
  <section id="roadmap" class="panel active">
    <h2>1. Las 6 etapas ejecutables + 6 guías + 7 cheatsheets</h2>
    <div class="grid">
      <div class="card"><span class="badge">Etapa 1</span><h3>Fundamentos</h3><p>Calculadora exacta con <code>Decimal</code> (sin <code>eval</code>) y agenda JSON atómica (<code>os.replace</code>).</p><p><a href="../etapas/01-fundamentos.md">Etapa 01</a> · <a href="../proyectos/01_fundamentos/">Código + Tests</a></p></div>
      <div class="card"><span class="badge">Etapa 2</span><h3>Modelado y Pruebas</h3><p>Biblioteca de préstamos con dominio desacoplado, reloj inyectable e invariantes estrictas.</p><p><a href="../etapas/02-modelado.md">Etapa 02</a> · <a href="../proyectos/02_modelado/">Código + Tests</a></p></div>
      <div class="card"><span class="badge">Etapa 3</span><h3>Datos y Concurrencia</h3><p>Inventario transaccional sin stock negativo bajo carreras reales con barrera e idempotencia.</p><p><a href="../etapas/03-datos.md">Etapa 03</a> · <a href="../proyectos/03_datos/">Código + SQL</a></p></div>
      <div class="card"><span class="badge">Etapa 4</span><h3>Redes y Seguridad</h3><p>API HTTP real con autenticación, autorización por recurso (<code>403</code>) y límites de entrada.</p><p><a href="../etapas/04-redes.md">Etapa 04</a> · <a href="../proyectos/04_redes/">Código + Tests</a></p></div>
      <div class="card"><span class="badge">Etapa 5</span><h3>Operación</h3><p>Liveness vs Readiness, logs sin secretos, respaldo SQLite Backup API y restauración SHA-256.</p><p><a href="../etapas/05-operacion.md">Etapa 05</a> · <a href="../proyectos/05_operacion/">Código + Tests</a></p></div>
      <div class="card"><span class="badge">Etapa 6</span><h3>Sistemas Distribuidos</h3><p>Transactional Outbox, consumidor idempotente ante caídas, caché TTL y percentiles p50/p95.</p><p><a href="../etapas/06-sistemas.md">Etapa 06</a> · <a href="../proyectos/06_sistemas/">Código + Tests</a></p></div>
    </div>
    <h2 style="margin-top:1.5rem">2. Guías de Arquitectura, Lenguajes, Linux y Hardware</h2>
    <div class="grid">
      <div class="card"><h3>Guía 01 · Binario y CPU</h3><p>Complemento a dos, IEEE-754, syscalls, NandGame y CPU Land.</p><a href="../guias/01-binario-arquitectura-y-cpu.md">Abrir guía</a></div>
      <div class="card"><h3>Guía 02 · Lenguajes de Sistemas</h3><p>Python, C, C++, Rust, Go y Zig comparados en memoria y concurrencia.</p><a href="../guias/02-lenguajes-de-sistemas.md">Abrir guía</a></div>
      <div class="card"><h3>Guía 03 · Linux, Git y Contenedores</h3><p>Shell segura, procesos, systemd, Git y Podman.</p><a href="../guias/03-linux-shell-git-y-contenedores.md">Abrir guía</a></div>
      <div class="card"><h3>Guía 04 · Embebidos, IoT y RTOS</h3><p>Arduino/ESP32/Raspberry Pi, UART/I2C/SPI, MQTT y simuladores Wokwi/Falstad.</p><a href="../guias/04-embebidos-iot-y-rtos.md">Abrir guía</a></div>
      <div class="card"><h3>Guía 05 · POO y Arquitectura</h3><p>Composición vs herencia, puertos/repositorios y diseño sin sobreingeniería.</p><a href="../guias/05-poo-patrones-y-arquitectura.md">Abrir guía</a></div>
      <div class="card"><h3>Guía 06 · Nginx, Docker y Despliegue</h3><p>TLS, proxy inverso, builds multicapa y seguridad operativa.</p><a href="../guias/06-redes-nginx-docker-y-despliegue.md">Abrir guía</a></div>
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

function showTab(id, btn) {{
  document.querySelectorAll('section.panel').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
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

calcBinario(); runRegex(); runChmod(); renderQuiz(); renderFmhy();
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
