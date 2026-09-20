#!/usr/bin/env python3
"""Convert interview Q&A Markdown into HTML under site/."""
from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

SKIP_PARTS = {".venv", "site", "node_modules"}

NAV = [
    ("Start", [
        ("index.html", "Overview"),
        ("00-levels.html", "12y architect path"),
    ]),
    ("Q&A", [
        ("01-database.html", "Database"),
        ("02-frontend.html", "Frontend"),
        ("03-backend.html", "Backend"),
        ("04-aws-azure.html", "AWS vs Azure"),
        ("05-angular.html", "Angular (100)"),
        ("06-dsa-leetcode.html", "DSA (optional)"),
        ("07-enterprise.html", "Real apps (Netflix…)"),
        ("08-sql-coding.html", "SQL (architect)"),
        ("09-ai.html", "AI (basics→2026)"),
        ("10-mobile.html", "RN / Android / iOS"),
    ]),
]


def html_name(rel: Path) -> str:
    if rel.as_posix() == "README.md":
        return "index.html"
    if rel.name == "README.md":
        return f"{rel.parent.as_posix().replace('/', '-')}.html"
    stem = rel.with_suffix("").as_posix().replace("/", "-")
    return f"{stem}.html"


def collect_markdown() -> list[Path]:
    files = []
    for p in ROOT.rglob("*.md"):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        files.append(p)
    return sorted(files)


def rewrite_links(md: str, src: Path, mapping: dict[str, str]) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def repl(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        path_only, frag = href, ""
        if "#" in href:
            path_only, frag = href.split("#", 1)
            frag = "#" + frag
        if not path_only.endswith(".md"):
            return m.group(0)
        target = (src.parent / path_only).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        html = mapping.get(rel)
        if not html and path_only.endswith("/README.md"):
            html = path_only[: -len("/README.md")].replace("/", "-") + ".html"
        if not html:
            return m.group(0)
        return f"[{label}]({html}{frag})"

    return pattern.sub(repl, md)


def mermaid_fence_to_div(md: str) -> str:
    def repl(m: re.Match) -> str:
        body = m.group(1).strip()
        return f'\n<div class="mermaid">\n{body}\n</div>\n'

    return re.sub(r"```mermaid\n(.*?)```", repl, md, flags=re.S)


def page_title(rel: Path, md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return rel.stem


def render_html(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script>
  (function () {{
    var s = location.pathname.split("/").filter(Boolean)[0];
    if (s === "frontend" || s === "dbnotes" || s === "backend" || s === "interview" || s === "ai") {{
      document.write('<base href="/' + s + '/">');
    }}
  }})();
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Interview Q&A</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<div class="layout">
  <aside class="sidebar" id="nav"></aside>
  <main>
{body}
  </main>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script src="assets/app.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: "neutral" }});</script>
</body>
</html>
"""


def write_app_js() -> None:
    lines = ["const NAV = ["]
    for group, items in NAV:
        lines.append(f'  {{ group: {group!r}, items: [')
        for href, label in items:
            lines.append(f'    {{ href: {href!r}, label: {label!r} }},')
        lines.append("  ]},")
    lines.append("];")
    lines.append("""
function bookPrefix() {
  const seg = location.pathname.split("/").filter(Boolean)[0];
  if (seg === "frontend" || seg === "dbnotes" || seg === "backend" || seg === "interview" || seg === "ai") return "/" + seg + "/";
  return "";
}

function pageHref(file) {
  return bookPrefix() + String(file).replace(/^\\.\\//, "");
}

function currentPage() {
  const parts = location.pathname.split("/").filter(Boolean);
  let last = parts[parts.length - 1] || "index.html";
  if (last === "frontend" || last === "dbnotes" || last === "backend" || last === "interview" || last === "ai") return "index.html";
  if (last === "README.md" && parts.length >= 2) return parts[parts.length - 2] + ".html";
  if (last.endsWith(".md")) return last.replace(/\\.md$/, ".html");
  return last || "index.html";
}

function rewriteNotebookLinks() {
  const prefix = bookPrefix();
  document.querySelectorAll("main a[href]").forEach((a) => {
    const raw = a.getAttribute("href");
    if (!raw || raw.startsWith("http") || raw.startsWith("#") || raw.startsWith("mailto:")) return;
    let href = raw;
    const readme = href.match(/^(?:\\.\\/)?([^/]+)\\/README\\.md(#.*)?$/i);
    if (readme) href = readme[1] + ".html" + (readme[2] || "");
    else if (/\\.md($|#)/i.test(href) && !href.startsWith("/")) {
      href = href.replace(/\\.md($|#)/i, ".html$1").replace(/\\//g, "-");
    }
    if (prefix && !href.startsWith("/") && !href.startsWith("http")) {
      a.setAttribute("href", prefix + href.replace(/^\\.\\//, ""));
    } else if (href !== raw) {
      a.setAttribute("href", href);
    }
  });
}

function renderNav() {
  const mount = document.getElementById("nav");
  if (!mount) return;
  const page = currentPage();
  const brand = document.createElement("a");
  brand.className = "brand";
  brand.href = pageHref("index.html");
  brand.textContent = "Interview Q&A";
  const sub = document.createElement("div");
  sub.className = "brand-sub";
  sub.textContent = "DB · Frontend · Backend · Cloud";
  const search = document.createElement("input");
  search.className = "nav-search";
  search.placeholder = "Filter pages…";
  search.setAttribute("aria-label", "Filter pages");
  mount.append(brand, sub, search);

  const wrap = document.createElement("div");
  wrap.id = "nav-links";
  NAV.forEach((g) => {
    const label = document.createElement("div");
    label.className = "nav-group";
    label.textContent = g.group;
    wrap.append(label);
    g.items.forEach((item) => {
      const a = document.createElement("a");
      a.className = "nav-link" + (item.href === page ? " active" : "");
      a.href = pageHref(item.href);
      a.textContent = item.label;
      a.dataset.label = (item.label + " " + g.group).toLowerCase();
      wrap.append(a);
    });
  });
  mount.append(wrap);
  search.addEventListener("input", () => {
    const q = search.value.toLowerCase().trim();
    wrap.querySelectorAll("a.nav-link").forEach((a) => {
      a.style.display = a.dataset.label.includes(q) ? "" : "none";
    });
  });
}

function wrapCode() {
  document.querySelectorAll("main pre").forEach((pre) => {
    if (pre.parentElement.classList.contains("code-wrap")) return;
    if (pre.classList.contains("mermaid")) return;
    const wrap = document.createElement("div");
    wrap.className = "code-wrap";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.type = "button";
    btn.textContent = "Copy";
    btn.addEventListener("click", async () => {
      await navigator.clipboard.writeText(pre.innerText);
      btn.textContent = "Copied";
      setTimeout(() => (btn.textContent = "Copy"), 1200);
    });
    wrap.appendChild(btn);
  });
}

function markExternal() {
  document.querySelectorAll("main a[href^='http']").forEach((a) => {
    a.classList.add("ext");
    a.target = "_blank";
    a.rel = "noopener noreferrer";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  rewriteNotebookLinks();
  renderNav();
  wrapCode();
  markExternal();
});
""")
    (SITE / "assets" / "app.js").write_text("\n".join(lines))


def main() -> None:
    files = collect_markdown()
    mapping = {p.relative_to(ROOT).as_posix(): html_name(p.relative_to(ROOT)) for p in files}
    md_engine = markdown.Markdown(extensions=["extra", "sane_lists", "toc", "smarty"])
    SITE.mkdir(exist_ok=True)
    n = 0
    for src in files:
        rel = src.relative_to(ROOT)
        raw = src.read_text()
        title = page_title(rel, raw)
        text = rewrite_links(raw, src, mapping)
        text = mermaid_fence_to_div(text)
        md_engine.reset()
        body = md_engine.convert(text)
        out = SITE / html_name(rel)
        out.write_text(render_html(title, body))
        n += 1
        print(f"  {rel} -> {out.name}")
    write_app_js()
    inject_index_jumps()
    write_legacy_redirects()
    print(f"\nWrote {n} HTML pages into {SITE}")


INDEX_JUMP = """
<div class="jump-grid">
  <a class="card" href="00-levels.html"><strong>12y architect path</strong><span>How to study this repo at EA / L7 depth.</span></a>
  <a class="card" href="07-enterprise.html"><strong>Real apps</strong><span>Netflix, commerce, Zerodha, ChatGPT, claims — reason → stack.</span></a>
  <a class="card" href="09-ai.html"><strong>AI Q&A</strong><span>RAG, agents, evals, practical vs bubble.</span></a>
  <a class="card" href="01-database.html"><strong>Database</strong><span>MVCC, indexes, HA, NoSQL, CDC.</span></a>
  <a class="card" href="02-frontend.html"><strong>Frontend</strong><span>CSR/SSR, MFE, CWV, store, sockets.</span></a>
  <a class="card" href="03-backend.html"><strong>Backend</strong><span>Java/Go/Node, sagas, BFF, Redis, JWT.</span></a>
  <a class="card" href="04-aws-azure.html"><strong>AWS vs Azure</strong><span>Same job, two names.</span></a>
  <a class="card" href="05-angular.html"><strong>Angular</strong><span>100 Q&A: signals, RxJS, SSR, tests.</span></a>
  <a class="card" href="10-mobile.html"><strong>Mobile</strong><span>RN / Android / iOS — store trains, push, offline.</span></a>
</div>
"""

LEGACY_REDIRECTS = {}


def inject_index_jumps() -> None:
    path = SITE / "index.html"
    html = path.read_text()
    needle = "</h1>"
    if needle not in html or "jump-grid" in html:
        return
    html = html.replace(needle, needle + INDEX_JUMP, 1)
    path.write_text(html)


def write_legacy_redirects() -> None:
    for name, target in LEGACY_REDIRECTS.items():
        title = name.replace(".html", "")
        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>Moved — {title}</title>
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<div class="layout">
  <aside class="sidebar" id="nav"></aside>
  <main>
    <p class="kicker">Moved</p>
    <h1>This page moved</h1>
    <p class="lede">The lab pages now live in the generated notebook. Continue to <a href="{target}">{target}</a>.</p>
  </main>
</div>
<script src="assets/app.js"></script>
</body>
</html>
"""
        (SITE / name).write_text(body)
        print(f"  redirect {name} -> {target}")


if __name__ == "__main__":
    main()
