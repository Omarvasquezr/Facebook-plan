#!/usr/bin/env python3
"""Genera los entregables del CV en dist/.

dist/web/      → para publicar en un hosting (web + fuentes + PDF descargables)
dist/allegati/ → para adjuntar al correo (HTML autónomo que funciona sin conexión + 2 PDF)

`python3 build.py --keep-pdfs` conserva los PDF existentes y prepara la web y el HTML autónomo.
`python3 build.py --deploy` además publica dist/web en https://omar-vasquez.vercel.app
"""
import base64, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
CHROME = shutil.which("chromium-browser") or shutil.which("chromium") or shutil.which("google-chrome")
PDFS = {"pc": "Omar-Vasquez-CV.pdf", "telefono": "Omar-Vasquez-CV-telefono.pdf"}


def inline_fonts(html: str) -> str:
    """Sustituye el enlace a fonts.css por @font-face con las fuentes en base64."""
    css = (ROOT / "fonts/fonts.css").read_text()
    def to_data(m):
        data = base64.b64encode((ROOT / "fonts" / m.group(1)).read_bytes()).decode()
        return f"url(data:font/woff2;base64,{data})"
    css = re.sub(r"url\('([^']+)'\)", to_data, css)
    return html.replace('<link rel="stylesheet" href="fonts/fonts.css">', f"<style>{css}</style>")


def print_pdf(variant: str, out: Path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={out}",
                    f"file://{ROOT / 'deck.html'}?v={variant}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    keep_pdfs = "--keep-pdfs" in sys.argv
    if keep_pdfs:
        missing = [name for name in PDFS.values() if not (ROOT / name).is_file()]
        if missing:
            sys.exit("Faltan los PDF que deben conservarse: " + ", ".join(missing))
    elif not CHROME:
        sys.exit("Falta Chromium/Chrome para generar los PDF.")
    # conservar el vínculo con el proyecto de Vercel entre builds
    link = DIST / "web" / ".vercel"
    saved = ROOT / ".vercel-link"
    if link.exists():
        shutil.rmtree(saved, ignore_errors=True); shutil.copytree(link, saved)
    shutil.rmtree(DIST, ignore_errors=True)
    web, mail = DIST / "web", DIST / "allegati"
    web.mkdir(parents=True); mail.mkdir()
    if saved.exists():
        shutil.copytree(saved, web / ".vercel")

    for variant, name in PDFS.items():
        if keep_pdfs:
            shutil.copy2(ROOT / name, mail / name)
        else:
            print_pdf(variant, mail / name)
        shutil.copy(mail / name, web / name)

    src = (ROOT / "index.html").read_text()
    (web / "index.html").write_text(src)
    shutil.copytree(ROOT / "fonts", web / "fonts")
    for resource in ("preferences.css", "preferences.js", "intro.css", "intro.js",
                     "favicon.svg", "favicon.ico", "favicon-32.png", "apple-touch-icon.png"):
        shutil.copy(ROOT / resource, web / resource)
    shutil.copytree(ROOT / "assets", web / "assets")

    # Adjunto: sin fuentes externas y sin el bloque de descarga (los PDF ya van en el correo)
    standalone = inline_fonts(src)
    standalone = standalone.replace('<link rel="stylesheet" href="preferences.css">',
                                    '<style>' + (ROOT / "preferences.css").read_text() + '</style>')
    standalone = standalone.replace('<script src="preferences.js"></script>',
                                    '<script>' + (ROOT / "preferences.js").read_text() + '</script>')
    standalone = standalone.replace('<link rel="stylesheet" href="intro.css">',
                                    '<style>' + (ROOT / "intro.css").read_text() + '</style>')
    standalone = standalone.replace('<script src="intro.js"></script>',
                                    '<script>' + (ROOT / "intro.js").read_text() + '</script>')
    # Iconos embebidos también en el adjunto para mantenerlo autónomo.
    for resource, mime in (("favicon.svg", "image/svg+xml"), ("favicon.ico", "image/x-icon"),
                           ("favicon-32.png", "image/png"), ("apple-touch-icon.png", "image/png")):
        data = base64.b64encode((ROOT / resource).read_bytes()).decode()
        standalone = standalone.replace(f'href="{resource}"', f'href="data:{mime};base64,{data}"')
    standalone = re.sub(r"\s*<!-- solo-web:inicio -->.*?<!-- solo-web:fin -->", "", standalone, flags=re.S)
    (mail / "Omar-Vasquez-CV.html").write_text(standalone)

    for f in sorted(DIST.rglob("*")):
        if f.is_file() and ".vercel" not in f.parts:
            print(f"{f.stat().st_size / 1024:8.0f} KB  {f.relative_to(DIST)}")

    if "--deploy" in sys.argv:
        subprocess.run(["npx", "--yes", "vercel", "deploy", "--prod", "--yes"], cwd=web, check=True)


if __name__ == "__main__":
    main()
