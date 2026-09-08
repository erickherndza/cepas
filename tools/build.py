#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generador estático del sitio CEPASI (sistema visual "Firegard": degradado
rojo-naranja, esquina cortada, fondo oscuro, tipografía industrial en
mayúsculas). Produce las 6 páginas .html en la raíz del proyecto a partir
de las funciones/plantillas de este archivo. El sitio final NO depende de
Python para funcionar: son archivos .html/.css/.js estáticos — este
script es solo la herramienta de autoría para mantener el header, footer
y demás bloques repetidos consistentes entre las 6 páginas.

Uso: python3 tools/build.py   (ejecutar desde la raíz del proyecto, o
desde cualquier lugar — la ruta de salida se calcula sola)."""

import json
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dominio canónico del sitio (ya referenciado en robots.txt/sitemap.xml antes
# de este cambio) — usado para <link rel="canonical">, Open Graph y JSON-LD.
# No depende de dónde esté servido hoy (GitHub Pages) para seguir siendo
# correcto una vez apuntado el dominio propio.
BASE_URL = "https://www.cepasird.com/"

NAV = [
    ("index.html", "Inicio"),
    ("nosotros.html", "Nosotros"),
    ("servicios.html", "Servicios"),
    ("proyectos.html", "Proyectos"),
    ("blog.html", "Blog"),
    ("contacto.html", "Contacto"),
]

WA_LINK = "https://wa.me/18092845807"
PHONE_1 = "809-284-5807"
PHONE_1_TEL = "8092845807"
PHONE_2 = "829-546-2313"
PHONE_2_TEL = "8295462313"
EMAIL = "cuerpodeevacuacion01@gmail.com"
# URL del Web App de Google Apps Script que recibe el formulario PSST con
# adjuntos (formulario-psst.html). Vacío = el formulario aún cae de vuelta
# al envío por mailto (sin adjuntos reales, solo lista de nombres de
# archivo). Una vez desplegado el script, pegar aquí la URL "…/exec" y
# volver a correr build.py — no requiere tocar el HTML ni el JS.
PSST_UPLOAD_ENDPOINT = ""
ADDRESS = "C/ 16, Esquina 19, Villa Aura, Santo Domingo Oeste, R.D."
IG = "https://www.instagram.com/seguridad_y_salud_ocupacional1/"
FB = "#"
YEAR = "2026"

HERO_IMG = "assets/img/hero-mantenimiento.jpg"
CAPACITACION_IMG = "assets/img/capacitacion-rcp.jpg"
BOTIQUIN_IMG = "assets/img/botiquin.jpg"
DEA_IMG = "assets/img/dea.jpg"

# Lucide dropped brand icons (facebook/instagram) — inline SVGs, stroke="none"
# so Tailwind's text-* color utilities and currentColor work like lucide icons.

def icon_facebook(cls):
    return f"""<svg viewBox="0 0 24 24" fill="currentColor" class="{cls}"><path d="M22 12.06C22 6.51 17.52 2 12 2S2 6.51 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.51 1.49-3.9 3.77-3.9 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.89h2.78l-.44 2.91h-2.34V22c4.78-.79 8.44-4.94 8.44-9.94z"/></svg>"""


def icon_instagram(cls):
    return f"""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>"""


def icon_badge(icon, size="w-12 h-12", icon_size="w-5 h-5", soft=False):
    cls = "icon-badge-soft" if soft else "icon-badge"
    return f'<div class="{cls} {size}"><i data-lucide="{icon}" class="{icon_size}"></i></div>'


def org_json_ld():
    """Datos estructurados Organization/ProfessionalService (schema.org),
    incluidos en TODAS las páginas. Ayuda tanto al SEO tradicional (Google
    Business/Knowledge Panel) como a motores de respuesta con IA (GEO) a
    identificar a CEPASI como entidad, su dirección, contacto y área de
    servicio. Datos tomados de las constantes ya usadas en topbar/footer —
    no se inventa ninguna cifra ni certificación."""
    same_as = [IG]
    if FB and FB != "#":
        same_as.append(FB)
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "CEPASI — Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial, S.R.L.",
        "alternateName": "CEPASI",
        "url": BASE_URL,
        "logo": BASE_URL + "assets/img/logo-cepasi.png",
        "image": BASE_URL + HERO_IMG,
        "telephone": f"+1{PHONE_1_TEL}",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "C/ 16, Esquina 19, Villa Aura",
            "addressLocality": "Santo Domingo Oeste",
            "addressCountry": "DO",
        },
        "areaServed": "República Dominicana",
        "priceRange": "$$",
        "sameAs": same_as,
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def head(title, description, canonical="", og_image=None, extra="", json_ld=""):
    canonical_url = BASE_URL + canonical if canonical else BASE_URL
    image_url = BASE_URL + (og_image or HERO_IMG)
    return f"""<!doctype html>
<html lang="es-DO">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical_url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_DO">
<meta property="og:site_name" content="CEPASI">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="{image_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image_url}">
<meta name="theme-color" content="#1A1A1A">
<link rel="icon" type="image/png" href="assets/img/logo-cepasi.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{
    theme: {{
      extend: {{
        colors: {{
          ink: '#1A1A1A',
          brandred: {{ DEFAULT: '#E63C24', dark: '#C7301A' }},
          brandorange: '#F79433',
          lime: '#CBE24B',
          navy: {{ DEFAULT: '#1F3B57', dark: '#152A3D', light: '#2C5075' }},
          beige: '#F5F3EF'
        }},
        fontFamily: {{
          heading: ['Barlow Condensed', 'sans-serif'],
          sans: ['Inter', 'sans-serif']
        }}
      }}
    }}
  }}
</script>
<link rel="stylesheet" href="assets/css/theme.css">
<link rel="stylesheet" href="assets/css/typography.css">
<link rel="stylesheet" href="assets/css/responsive.css">
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
{org_json_ld()}
{json_ld}
{extra}
</head>"""


def topbar():
    return f"""  <div class="hidden sm:block bg-ink text-white text-xs">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 flex items-center justify-between py-2">
      <div class="flex items-center gap-5">
        <a href="contacto.html#mapa" class="flex items-center gap-1.5 hover:text-brandorange transition">
          <i data-lucide="map-pin" class="w-3.5 h-3.5"></i>
          <span>{ADDRESS}</span>
        </a>
        <a href="tel:+1{PHONE_1_TEL}" class="hidden md:flex items-center gap-1.5 hover:text-brandorange transition">
          <i data-lucide="phone" class="w-3.5 h-3.5"></i>
          <span>{PHONE_1}</span>
        </a>
        <a href="mailto:{EMAIL}" class="hidden lg:flex items-center gap-1.5 hover:text-brandorange transition">
          <i data-lucide="mail" class="w-3.5 h-3.5"></i>
          <span>{EMAIL}</span>
        </a>
      </div>
      <div class="flex items-center gap-3">
        <a href="{FB}" aria-label="Facebook de CEPASI" class="hover:text-brandorange transition">{icon_facebook("w-3.5 h-3.5")}</a>
        <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram de CEPASI" class="hover:text-brandorange transition">{icon_instagram("w-3.5 h-3.5")}</a>
      </div>
    </div>
  </div>"""


def header(active):
    links = []
    mlinks = []
    for href, label in NAV:
        cls = "nav-active" if href == active else "text-ink hover:text-brandred"
        links.append(f'<a href="{href}" class="font-semibold text-sm {cls} transition">{label}</a>')
        mlinks.append(f'<a href="{href}" class="block py-3 px-1 border-b border-slate-100 font-semibold {cls}">{label}</a>')
    links_html = "\n          ".join(links)
    mlinks_html = "\n      ".join(mlinks)

    return f"""  <header id="site-header" class="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-100">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <a href="index.html" class="flex items-center gap-3 shrink-0">
          <img src="assets/img/logo-cepasi.png" alt="Logo CEPASI" class="w-12 h-12">
          <span class="font-heading font-extrabold text-xl md:text-2xl text-ink leading-none">CEPASI</span>
        </a>
        <nav class="hidden lg:flex items-center gap-8 flex-1 justify-center">
          {links_html}
        </nav>
        <div class="hidden lg:flex items-center gap-3 shrink-0">
          <a href="{WA_LINK}" target="_blank" rel="noopener" class="clip-br bg-gradient-brand hover:brightness-105 text-white font-bold text-sm uppercase tracking-wide px-6 py-3 transition shadow-sm">
            Solicitar Asesoría
          </a>
        </div>
        <button id="menu-toggle" aria-label="Abrir menú" class="lg:hidden p-2 text-ink">
          <i data-lucide="menu" id="icon-open" class="w-7 h-7"></i>
          <i data-lucide="x" id="icon-close" class="w-7 h-7 hidden"></i>
        </button>
      </div>
      <div id="mobile-menu" class="lg:hidden">
      {mlinks_html}
        <a href="{WA_LINK}" target="_blank" rel="noopener" class="mt-3 clip-br bg-gradient-brand text-white font-bold text-sm uppercase tracking-wide px-5 py-3 flex items-center justify-center gap-2">
          <i data-lucide="message-circle" class="w-4 h-4"></i> Solicitar Asesoría
        </a>
      </div>
    </div>
  </header>"""


def footer():
    quick_icons = ["house", "shield", "clipboard-list", "briefcase", "book-open", "phone"]
    quick_items = "".join(
        f'<li><a href="{href}" class="footer-link hover:text-white transition"><i data-lucide="{ic}" class="bullet-icon w-3.5 h-3.5"></i>{label}</a></li>'
        for (href, label), ic in zip(NAV, quick_icons)
    )
    servicio_links = [
        ("servicios.html#asesoria", "Asesoría y Consultoría"),
        ("servicios.html#capacitaciones", "Capacitaciones"),
        ("servicios.html#mantenimiento", "Mantenimiento y Taller"),
        ("servicios.html#equipos", "Equipos y Primeros Auxilios"),
    ]
    servicio_items = "".join(
        f'<li><a href="{href}" class="footer-link hover:text-white transition"><i data-lucide="chevron-right" class="bullet-icon w-3.5 h-3.5"></i>{label}</a></li>'
        for href, label in servicio_links
    )

    return f"""  <footer class="bg-ink text-slate-300">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 py-14 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
      <div class="lg:col-span-2">
        <div class="flex items-center gap-3 mb-4">
          <img src="assets/img/logo-cepasi.png" alt="Logo CEPASI" class="w-12 h-12">
          <span class="font-heading font-extrabold text-xl text-white">CEPASI</span>
        </div>
        <p class="text-sm leading-relaxed max-w-sm">Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial, S.R.L. Asesoría, capacitación, mantenimiento y equipos para que su empresa cumpla el Reglamento 522-06 y proteja lo que más importa: su gente.</p>
        <div class="flex items-center gap-3 mt-5">
          <a href="{FB}" aria-label="Facebook de CEPASI" class="w-9 h-9 rounded-full bg-white flex items-center justify-center text-ink hover:text-brandred transition">{icon_facebook("w-4 h-4")}</a>
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram de CEPASI" class="w-9 h-9 rounded-full bg-white flex items-center justify-center text-ink hover:text-brandred transition">{icon_instagram("w-4 h-4")}</a>
        </div>
      </div>
      <div>
        <h4 class="font-heading font-semibold text-white mb-4 text-lg">Enlaces rápidos</h4>
        <ul class="space-y-2.5 text-sm">{quick_items}</ul>
      </div>
      <div>
        <h4 class="font-heading font-semibold text-white mb-4 text-lg">Servicios</h4>
        <ul class="space-y-2.5 text-sm">{servicio_items}</ul>
      </div>
      <div>
        <h4 class="font-heading font-semibold text-white mb-4 text-lg">Contacto</h4>
        <ul class="space-y-3 text-sm">
          <li class="flex items-start gap-2"><i data-lucide="map-pin" class="w-4 h-4 mt-0.5 shrink-0 text-brandorange"></i>{ADDRESS}</li>
          <li class="flex items-center gap-2"><i data-lucide="phone" class="w-4 h-4 shrink-0 text-brandorange"></i>{PHONE_1} · {PHONE_2}</li>
          <li class="flex items-center gap-2"><i data-lucide="mail" class="w-4 h-4 shrink-0 text-brandorange"></i>{EMAIL}</li>
        </ul>
      </div>
    </div>
    <div class="border-t border-white/10">
      <div class="max-w-7xl mx-auto px-4 lg:px-8 py-5 text-xs text-slate-400 text-center">
        © {YEAR} CEPASI. Todos los derechos reservados.
      </div>
    </div>
  </footer>

  <a href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp"
     class="wa-pulse fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-[#25D366] text-white flex items-center justify-center shadow-lg hover:scale-105 transition">
    <i data-lucide="message-circle" class="w-7 h-7"></i>
  </a>"""


def page(title, description, active, body, page_scripts="", canonical="", og_image=None, json_ld=""):
    return f"""{head(title, description, canonical=canonical, og_image=og_image, json_ld=json_ld)}
<body class="bg-white font-sans text-slate-700">
{topbar()}
{header(active)}
{body}
{footer()}
{page_scripts}
  <script src="assets/js/nav.js"></script>
  <script src="assets/js/slider.js"></script>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def write(name, content):
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Reusable UI fragments
# ---------------------------------------------------------------------------

def section_hero(eyebrow, headline, subheadline, bg=HERO_IMG, bg_alt=""):
    return f"""  <section class="relative overflow-hidden">
    <div class="absolute inset-0">
      <img src="{bg}" alt="{bg_alt}" class="w-full h-full object-cover">
      <div class="absolute inset-0 bg-ink/85"></div>
    </div>
    <div class="relative max-w-7xl mx-auto px-4 lg:px-8 py-20 md:py-28 text-center">
      <span class="eyebrow eyebrow-dot text-brandorange font-semibold text-xs uppercase tracking-widest">{eyebrow}</span>
      <h1 class="font-heading font-extrabold text-4xl md:text-6xl text-white mt-4 mb-5 max-w-3xl mx-auto leading-[1.05]">{headline}</h1>
      <p class="text-slate-200 max-w-2xl mx-auto text-base md:text-lg leading-relaxed">{subheadline}</p>
    </div>
  </section>"""


def wa_link_for(message):
    """Enlace de WhatsApp con mensaje prellenado (para CTAs de servicios
    específicos)."""
    return f"{WA_LINK}?text={quote(message)}"


def cta_band(headline, text, wa_label="Contactar por WhatsApp", bg=HERO_IMG, wa_link=WA_LINK):
    return f"""  <section class="relative overflow-hidden">
    <div class="absolute inset-0">
      <img src="{bg}" alt="" class="w-full h-full object-cover">
      <div class="absolute inset-0 bg-ink/90"></div>
    </div>
    <div class="relative max-w-4xl mx-auto px-4 lg:px-8 py-16 md:py-20 text-center text-white">
      <h2 class="font-heading font-bold text-3xl md:text-4xl mb-3">{headline}</h2>
      <p class="text-white/85 max-w-2xl mx-auto mb-9 text-base md:text-lg">{text}</p>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-8">
        <a href="{wa_link}" target="_blank" rel="noopener" class="clip-br bg-gradient-brand hover:brightness-105 text-white font-bold uppercase tracking-wide text-sm px-7 py-4 inline-flex items-center gap-2 transition">
          <i data-lucide="message-circle" class="w-5 h-5"></i> {wa_label}
        </a>
        <a href="tel:+1{PHONE_1_TEL}" class="flex items-center gap-3 group">
          {icon_badge("phone", size="w-14 h-14", icon_size="w-6 h-6")}
          <span class="text-left">
            <span class="block text-xs text-white/60 uppercase tracking-wide">Llámenos ahora</span>
            <span class="block font-heading font-bold text-2xl group-hover:text-brandorange transition">{PHONE_1}</span>
          </span>
        </a>
      </div>
    </div>
  </section>"""


def feature_list_section(eyebrow, title, items, image, image_alt, bg="", reverse=False, badge_size="w-14 h-14"):
    """Imagen a un lado + lista vertical con ícono circular en degradado
    (patrón "Por qué elegirnos" de Firegard). Reutilizado en Inicio y
    Nosotros."""
    rows = "\n".join(f"""        <div class="flex gap-5">
          {icon_badge(icon, size=badge_size, icon_size="w-6 h-6")}
          <div>
            <h4 class="font-heading font-bold text-lg text-ink leading-snug">{t}</h4>
            <p class="text-sm text-slate-600 leading-relaxed mt-1">{d}</p>
          </div>
        </div>""" for icon, t, d in items)

    img_block = f"""      <div class="{'lg:order-2' if not reverse else 'lg:order-1'}">
        <img src="{image}" alt="{image_alt}" class="clip-tr w-full h-[420px] md:h-[480px] object-cover">
      </div>"""
    text_block = f"""      <div class="{'lg:order-1' if not reverse else 'lg:order-2'}">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">{eyebrow}</span>
        <h2 class="font-heading font-bold text-3xl md:text-4xl text-ink mt-3 mb-8">{title}</h2>
        <div class="space-y-7">
{rows}
        </div>
      </div>"""
    cols = [text_block, img_block] if not reverse else [img_block, text_block]
    return f"""  <section class="py-16 md:py-24 {bg}">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 grid lg:grid-cols-2 gap-14 lg:gap-20 items-center">
{chr(10).join(cols)}
    </div>
  </section>"""


# ---------------------------------------------------------------------------
# INDEX
# ---------------------------------------------------------------------------

SLIDES = [
    {
        "eyebrow": "Seguridad industrial &amp; salud ocupacional en R.D.",
        "prefix": "Seguridad Industrial y Salud Ocupacional",
        "emph": "en la que su empresa puede confiar",
        "sub": "En CEPASI diseñamos, implementamos y capacitamos en los sistemas de prevención, evacuación y primeros auxilios que su empresa necesita para cumplir con el Reglamento 522-06 y, sobre todo, para proteger lo más importante: la vida de su equipo.",
        "img": HERO_IMG,
        "alt": "Técnico de CEPASI realizando mantenimiento a un extintor",
        "cta1": ("Solicitar asesoría gratuita", WA_LINK, True),
        "cta2": ("Ver nuestros servicios", "servicios.html", False),
    },
    {
        "eyebrow": "Capacitaciones y Formación Técnica",
        "prefix": "Capacitaciones y",
        "emph": "Formación Técnica",
        "sub": "Primeros auxilios, brigadas de emergencia, simulacros de evacuación, Comité Mixto de SST y más.",
        "img": CAPACITACION_IMG,
        "alt": "Capacitación práctica de primeros auxilios y RCP por el equipo de CEPASI",
        "cta1": ("Solicitar asesoría gratuita", WA_LINK, True),
        "cta2": ("Ver capacitaciones", "servicios.html#capacitaciones", False),
    },
    {
        "eyebrow": "Equipos de Emergencia y Primeros Auxilios",
        "prefix": "Equipos de Emergencia y",
        "emph": "Primeros Auxilios",
        "sub": "Botiquines, camillas, señalética industrial y sistemas contra incendios listos para instalar.",
        "img": BOTIQUIN_IMG,
        "alt": "Botiquín de primeros auxilios equipado CEPASI",
        "cta1": ("Solicitar asesoría gratuita", WA_LINK, True),
        "cta2": ("Ver equipos", "servicios.html#equipos", False),
    },
]


def build_slide(s, index, active):
    def cta(label, href, primary):
        target = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        if primary:
            return f'<a href="{href}"{target} class="clip-br bg-gradient-brand hover:brightness-105 text-white font-bold uppercase tracking-wide text-sm px-7 py-4 inline-flex items-center justify-center gap-2 transition shadow-lg">{label} <i data-lucide="message-circle" class="w-5 h-5"></i></a>'
        return f'<a href="{href}"{target} class="border-2 border-white/70 text-white font-bold uppercase tracking-wide text-sm px-7 py-4 inline-flex items-center justify-center gap-2 hover:bg-white/10 transition">{label} <i data-lucide="arrow-right" class="w-5 h-5"></i></a>'

    return f"""    <div class="slide{' active' if active else ''}" data-slide>
      <div class="absolute inset-0">
        <img src="{s['img']}" alt="{s['alt']}" class="w-full h-full object-cover">
        <div class="absolute inset-0 bg-gradient-to-r from-ink/95 via-ink/80 to-ink/40"></div>
      </div>
      <div class="relative max-w-7xl mx-auto px-4 lg:px-8 pt-24 pb-32 md:pt-32 md:pb-48">
        <div class="max-w-2xl">
          <span class="eyebrow eyebrow-dot text-brandorange font-semibold text-xs uppercase tracking-widest">{s['eyebrow']}</span>
          <h1 class="font-heading font-extrabold text-4xl md:text-6xl text-white mt-4 mb-6 leading-[1.05]">{s['prefix']} <span class="text-gradient">{s['emph']}</span></h1>
          <p class="text-slate-200 text-base md:text-lg leading-relaxed mb-8 max-w-xl">{s['sub']}</p>
          <div class="flex flex-col sm:flex-row gap-4">
            {cta(*s['cta1'])}
            {cta(*s['cta2'])}
          </div>
        </div>
      </div>
    </div>"""


def build_hero_slider():
    slides_html = "\n".join(build_slide(s, i, i == 0) for i, s in enumerate(SLIDES))
    dots = "\n".join(f'<button class="slider-dot{" active" if i == 0 else ""}" aria-label="Ir a la diapositiva {i+1}"></button>' for i in range(len(SLIDES)))
    return f"""  <section id="hero-slider" class="relative hero-clip overflow-hidden">
{slides_html}
    <button data-slide-prev aria-label="Anterior" class="absolute left-3 md:left-5 top-1/2 -translate-y-1/2 z-20 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center backdrop-blur transition">
      <i data-lucide="chevron-left" class="w-5 h-5"></i>
    </button>
    <button data-slide-next aria-label="Siguiente" class="absolute right-3 md:right-5 top-1/2 -translate-y-1/2 z-20 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center backdrop-blur transition">
      <i data-lucide="chevron-right" class="w-5 h-5"></i>
    </button>
    <div class="absolute bottom-8 md:bottom-10 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2">
      {dots}
    </div>
  </section>"""


def build_index():
    hero = build_hero_slider()

    trust = """  <section class="bg-ink -mt-1">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 py-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-white">
        <div class="flex items-center gap-3">
          <div class="icon-badge w-10 h-10 shrink-0"><i data-lucide="clipboard-check" class="w-4 h-4"></i></div>
          <span class="text-sm font-medium">Asesoría técnica</span>
        </div>
        <div class="flex items-center gap-3">
          <div class="icon-badge w-10 h-10 shrink-0"><i data-lucide="award" class="w-4 h-4"></i></div>
          <span class="text-sm font-medium">Capacitación certificada</span>
        </div>
        <div class="flex items-center gap-3">
          <div class="icon-badge w-10 h-10 shrink-0"><i data-lucide="package-check" class="w-4 h-4"></i></div>
          <span class="text-sm font-medium">Venta e instalación de equipos</span>
        </div>
        <div class="flex items-center gap-3">
          <div class="icon-badge w-10 h-10 shrink-0"><i data-lucide="scale" class="w-4 h-4"></i></div>
          <span class="text-sm font-medium">Cumplimiento del Reglamento 522-06</span>
        </div>
      </div>
    </div>
  </section>"""

    collage = f"""  <section class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 grid lg:grid-cols-2 gap-16 lg:gap-24 items-center">
      <div class="relative mt-8 mb-10 sm:mr-10">
        <img src="{HERO_IMG}" alt="Técnico de CEPASI realizando mantenimiento a un extintor" class="clip-tr w-full h-[420px] object-cover">
        <img src="{CAPACITACION_IMG}" alt="Capacitación de primeros auxilios de CEPASI" class="hidden sm:block absolute -bottom-10 -right-10 w-44 h-52 object-cover rounded-sm shadow-xl border-4 border-white">
        <div class="absolute -top-8 -left-6 bg-ink text-white rounded-sm px-6 py-5 shadow-xl">
          <p class="font-heading font-extrabold text-3xl text-brandorange stat-pending inline-block pb-1">[Número]</p>
          <p class="text-xs uppercase tracking-wide text-white/80 mt-1">años de experiencia</p>
        </div>
      </div>
      <div>
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Quiénes somos</span>
        <h2 class="font-heading font-bold text-3xl md:text-4xl text-ink mt-3 mb-6">Prevención real, entrenada y sostenida en el tiempo</h2>
        <p class="text-slate-600 leading-relaxed mb-4">En República Dominicana, la seguridad industrial dejó de ser un gasto opcional para convertirse en una obligación legal y, ante todo, en un acto de responsabilidad con las personas. CEPASI acompaña a empresas, instituciones y hogares en cada etapa de ese proceso: desde el análisis de riesgo y el diseño del plan de emergencia, hasta la capacitación de sus equipos y el mantenimiento de los sistemas contra incendios que ya tienen instalados.</p>
        <p class="text-slate-600 leading-relaxed mb-8">No vendemos equipos sueltos ni cursos aislados. Construimos con usted una cultura de prevención sólida, medible y conforme a la normativa vigente.</p>
        <div class="grid sm:grid-cols-2 gap-6">
          <div class="flex gap-4">
            {icon_badge("shield-check", size="w-12 h-12")}
            <div>
              <h4 class="font-heading font-bold text-ink">Cumplimiento real</h4>
              <p class="text-sm text-slate-600 mt-1">Alineados al Reglamento 522-06.</p>
            </div>
          </div>
          <div class="flex gap-4">
            {icon_badge("users", size="w-12 h-12")}
            <div>
              <h4 class="font-heading font-bold text-ink">Un solo equipo</h4>
              <p class="text-sm text-slate-600 mt-1">De la asesoría a la ejecución.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>"""

    why = feature_list_section(
        "¿Por qué elegir CEPASI?",
        "Cuatro razones por las que las empresas confían en nosotros",
        [
            ("layers", "Experiencia integral, no fragmentada", "Un solo equipo que analiza el riesgo, diseña el plan, capacita a su personal, instala el equipo y le da mantenimiento después. Sin intermediarios ni soluciones a medias."),
            ("shield-check", "Cumplimiento normativo real", "Trabajamos alineados al Reglamento 522-06 de Seguridad y Salud en el Trabajo, para que su empresa esté preparada tanto ante una inspección como ante una emergencia real."),
            ("shield-plus", "Cobertura completa: personas y activos", "Protegemos a las personas (primeros auxilios, brigadas, DEA) y protegemos la infraestructura (extintores, detección de incendios, señalética), porque la seguridad completa exige ambas cosas."),
            ("truck", "Servicio a domicilio y en planta", "Recargamos y damos mantenimiento a sus extintores donde usted esté, y llevamos las capacitaciones directamente a sus instalaciones."),
        ],
        DEA_IMG,
        "Desfibrilador externo automático (DEA) de CEPASI",
        bg="bg-beige",
        reverse=True,
    )

    servicios = [
        (None, "clipboard-list", "Asesoría y Consultoría", "Especializada", "servicios.html#asesoria"),
        (CAPACITACION_IMG, "graduation-cap", "Capacitaciones y", "Formación Técnica", "servicios.html#capacitaciones"),
        (HERO_IMG, "wrench", "Mantenimiento, Taller y", "Equipamiento", "servicios.html#mantenimiento"),
        (BOTIQUIN_IMG, "package", "Equipos de Emergencia y", "Primeros Auxilios", "servicios.html#equipos"),
    ]

    def portfolio_card(image, icon, line1, line2, link):
        bg_layer = (
            f'<img src="{image}" alt="{line1} {line2}" class="img-card-photo absolute inset-0 w-full h-full object-cover">'
            if image else
            f'<div class="img-card-photo absolute inset-0 bg-gradient-to-br from-ink to-navy flex items-center justify-center"><i data-lucide="{icon}" class="w-16 h-16 text-white/30"></i></div>'
        )
        return f"""        <a href="{link}" class="img-card clip-tr relative h-80 block overflow-hidden group">
          {bg_layer}
          <div class="absolute inset-0 bg-gradient-to-t from-ink via-ink/40 to-transparent"></div>
          <div class="absolute bottom-0 left-0 right-0 p-6">
            {icon_badge(icon, size="w-11 h-11", icon_size="w-5 h-5")}
            <h3 class="font-heading font-bold text-xl text-white mt-4 leading-tight">{line1}<br>{line2}</h3>
            <span class="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-brandorange mt-2 opacity-0 group-hover:opacity-100 transition">Ver más <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i></span>
          </div>
        </a>"""

    serv_cards = "\n".join(portfolio_card(*s) for s in servicios)

    services_section = f"""  <section id="servicios-resumen" class="py-16 md:py-24 bg-beige">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Nuestros servicios</span>
        <h2 class="font-heading font-bold text-3xl md:text-4xl text-ink mt-3">Todo lo que su empresa necesita para prevenir y cumplir</h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
{serv_cards}
      </div>
      <div class="text-center mt-10">
        <a href="servicios.html" class="inline-flex items-center gap-2 text-ink font-bold uppercase tracking-wide text-sm hover:text-brandred transition">Ver todos los servicios <i data-lucide="arrow-right" class="w-4 h-4"></i></a>
      </div>
    </div>
  </section>"""

    stats = f"""  <section class="bg-ink py-16">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center text-white">
        <div>
          <i data-lucide="building-2" class="w-7 h-7 text-brandorange mx-auto mb-3"></i>
          <p class="font-heading font-extrabold text-3xl stat-pending inline-block pb-1">[Número]</p>
          <p class="text-sm text-slate-300 mt-2">empresas asesoradas en seguridad industrial</p>
        </div>
        <div>
          <i data-lucide="users" class="w-7 h-7 text-brandorange mx-auto mb-3"></i>
          <p class="font-heading font-extrabold text-3xl stat-pending inline-block pb-1">[Número]</p>
          <p class="text-sm text-slate-300 mt-2">personas capacitadas en primeros auxilios y evacuación</p>
        </div>
        <div>
          <i data-lucide="calendar" class="w-7 h-7 text-brandorange mx-auto mb-3"></i>
          <p class="font-heading font-extrabold text-3xl stat-pending inline-block pb-1">[Número]</p>
          <p class="text-sm text-slate-300 mt-2">años de experiencia en el sector</p>
        </div>
        <div>
          <i data-lucide="map-pin" class="w-7 h-7 text-brandorange mx-auto mb-3"></i>
          <p class="font-heading font-extrabold text-xl pb-1">Santo Domingo</p>
          <p class="text-sm text-slate-300 mt-2">y <span class="stat-pending">[zonas de servicio]</span></p>
        </div>
      </div>
    </div>
  </section>"""

    cta = cta_band(
        "Su empresa no puede improvisar cuando de seguridad se trata",
        "Hablemos de su plan de seguridad, sus certificaciones pendientes o el mantenimiento de sus equipos contra incendios. Nuestro equipo técnico le responde directamente por WhatsApp o teléfono.",
    )

    body = "\n".join([hero, trust, collage, why, services_section, stats, cta])
    write("index.html", page(
        "CEPASI | Seguridad Industrial y Salud Ocupacional en República Dominicana",
        "CEPASI: asesoría, capacitación, mantenimiento y venta de equipos de seguridad industrial y primeros auxilios en R.D., alineados al Reglamento 522-06.",
        "index.html",
        body,
        canonical="index.html",
    ))


# ---------------------------------------------------------------------------
# NOSOTROS
# ---------------------------------------------------------------------------

def build_nosotros():
    hero = section_hero(
        "Nosotros",
        "Somos el equipo detrás de la seguridad de su empresa",
        "CEPASI — Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial — nace con un propósito claro: que ninguna empresa dominicana tenga que enfrentar una emergencia sin estar preparada.",
    )

    quienes = f"""  <section class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 grid lg:grid-cols-2 gap-16 items-center">
      <div class="order-2 lg:order-1">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Quiénes somos</span>
        <h2 class="font-heading font-bold text-3xl md:text-4xl text-ink mt-3 mb-6">Prevención real, entrenada y sostenida en el tiempo</h2>
        <p class="text-slate-600 leading-relaxed mb-4">CEPASI es una empresa dominicana especializada en seguridad industrial y salud ocupacional, dedicada al análisis de riesgos de incendio, al diseño de rutas de evacuación, a la capacitación en primeros auxilios y al mantenimiento de equipos de emergencia. Trabajamos con empresas de distintos sectores para que la prevención deje de ser una casilla que se marca por cumplimiento, y se convierta en una práctica real, entrenada y sostenida en el tiempo.</p>
        <p class="text-slate-600 leading-relaxed">Desde nuestra base en Villa Aura, Santo Domingo Oeste, damos servicio a empresas, instituciones y hogares en toda la región, combinando la asesoría técnica con la implementación práctica: capacitamos a su personal, instalamos y damos mantenimiento a sus equipos, y lo acompañamos en el cumplimiento del Reglamento 522-06 de Seguridad y Salud en el Trabajo.</p>
      </div>
      <div class="order-1 lg:order-2">
        <img src="{CAPACITACION_IMG}" alt="Capacitación práctica de primeros auxilios y RCP por el equipo de CEPASI" class="clip-tr w-full h-[420px] object-cover">
      </div>
    </div>
  </section>"""

    mision_vision = f"""  <section class="py-16 md:py-24 bg-beige">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 grid md:grid-cols-2 gap-6">
      <div class="bg-white rounded-sm border border-slate-100 shadow-sm p-8 card-lift">
        {icon_badge("target", size="w-14 h-14", icon_size="w-6 h-6")}
        <h3 class="font-heading font-bold text-2xl text-ink mt-5 mb-3">Misión</h3>
        <p class="text-slate-600 leading-relaxed">Proteger vidas y activos a través de servicios integrales de seguridad industrial, salud ocupacional y atención de emergencias, brindando a empresas e instituciones las herramientas técnicas, la capacitación y el equipamiento necesarios para prevenir, responder y cumplir con la normativa vigente.</p>
      </div>
      <div class="bg-white rounded-sm border border-slate-100 shadow-sm p-8 card-lift">
        {icon_badge("eye", size="w-14 h-14", icon_size="w-6 h-6")}
        <h3 class="font-heading font-bold text-2xl text-ink mt-5 mb-3">Visión</h3>
        <p class="text-slate-600 leading-relaxed">Ser la empresa de referencia en seguridad industrial y gestión de emergencias en República Dominicana, reconocida por la calidad técnica de sus asesorías, la seriedad de sus capacitaciones y su compromiso constante con la vida y la prevención.</p>
      </div>
    </div>
  </section>"""

    guia = feature_list_section(
        "Lo que nos guía",
        "Los principios detrás de cada servicio",
        [
            ("shield-alert", "Prevención antes que reacción", "Diseñamos sistemas para que la emergencia no llegue a ocurrir, y si ocurre, que su equipo sepa exactamente qué hacer."),
            ("ruler", "Rigor técnico", "Cada análisis de riesgo, cada plan de emergencia y cada capacitación se basa en normativa vigente y buenas prácticas del sector, no en plantillas genéricas."),
            ("handshake", "Acompañamiento continuo", "No entregamos un documento y desaparecemos. Damos seguimiento, mantenimiento y actualización a los sistemas que implementamos."),
            ("heart", "Compromiso con las personas", "Detrás de cada botiquín, cada extintor y cada simulacro hay una razón: que las personas lleguen a casa seguras."),
        ],
        HERO_IMG,
        "Técnico de CEPASI realizando mantenimiento a un extintor",
    )

    cumplimiento = f"""  <section class="py-16 md:py-24 bg-navy text-white">
    <div class="max-w-5xl mx-auto px-4 lg:px-8">
      <div class="flex flex-col md:flex-row items-start gap-8">
        {icon_badge("badge-check", size="w-16 h-16", icon_size="w-8 h-8")}
        <div>
          <span class="eyebrow eyebrow-dot text-brandorange font-semibold text-xs uppercase tracking-widest">Cumplimiento normativo</span>
          <h2 class="font-heading font-bold text-3xl md:text-4xl mt-3 mb-5">Alineados al Reglamento 522-06</h2>
          <p class="text-slate-200 leading-relaxed">Toda nuestra oferta de asesoría y capacitación está alineada con el Reglamento 522-06 de Seguridad y Salud en el Trabajo de la República Dominicana. Ayudamos a su empresa a cumplir con sus obligaciones legales en materia de SST: desde el Manual de Seguridad y Salud en el Trabajo hasta la conformación del Comité Mixto de Seguridad y Salud Ocupacional, pasando por los planes de emergencia y las capacitaciones obligatorias de su personal.</p>
        </div>
      </div>
    </div>
  </section>"""

    cta = cta_band(
        "Su empresa no puede improvisar cuando de seguridad se trata",
        "Hablemos de su plan de seguridad, sus certificaciones pendientes o el mantenimiento de sus equipos contra incendios. Nuestro equipo técnico le responde directamente por WhatsApp o teléfono.",
    )

    body = "\n".join([hero, quienes, mision_vision, guia, cumplimiento, cta])
    write("nosotros.html", page(
        "Nosotros | CEPASI — Seguridad Industrial y Salud Ocupacional",
        "Conozca a CEPASI: misión, visión, valores y compromiso con el cumplimiento del Reglamento 522-06 de Seguridad y Salud en el Trabajo en República Dominicana.",
        "nosotros.html",
        body,
        canonical="nosotros.html",
    ))


# ---------------------------------------------------------------------------
# SERVICIOS
# ---------------------------------------------------------------------------

def service_item(icon, slug, title, desc):
    return f"""        <a href="servicio-{slug}.html" class="bg-white rounded-sm border border-slate-100 p-6 card-lift flex gap-4 group hover:border-brandorange/40 transition">
          {icon_badge(icon, size="w-11 h-11", icon_size="w-5 h-5", soft=True)}
          <div>
            <h4 class="font-heading font-semibold text-ink mb-1.5 leading-snug tracking-normal normal-case">{title}</h4>
            <p class="text-sm text-slate-600 leading-relaxed">{desc}</p>
            <span class="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-brandred mt-3 opacity-0 group-hover:opacity-100 transition">Ver detalles <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i></span>
          </div>
        </a>"""


def category_block(anchor, number, title, intro, items, image=None, image_alt="", reverse=False, bg=""):
    items_html = "\n".join(service_item(it["icon"], it["slug"], it["title"], it["desc"]) for it in items)
    img_col = ""
    text_span = "md:col-span-7" if image else "md:col-span-12"
    if image:
        img_col = f"""      <div class="md:col-span-5 {'md:order-2' if not reverse else 'md:order-1'}">
        <img src="{image}" alt="{image_alt}" class="clip-tr w-full h-full min-h-[280px] object-cover">
      </div>"""
    text_col = f"""      <div class="{text_span} {'md:order-1' if not reverse else 'md:order-2'}">
        <div class="flex items-center gap-4 mb-4">
          <span class="w-10 h-10 rounded-full bg-gradient-brand text-white font-heading font-bold text-base flex items-center justify-center shrink-0">{number}</span>
          <h2 class="font-heading font-bold text-3xl md:text-4xl text-ink">{title}</h2>
        </div>
        <p class="text-slate-600 leading-relaxed mb-8 max-w-2xl">{intro}</p>
        <div class="grid sm:grid-cols-2 gap-4">
{items_html}
        </div>
      </div>"""
    cols = [text_col, img_col] if not reverse else [img_col, text_col]
    grid = "\n".join(c for c in cols if c)
    return f"""  <section id="{anchor}" class="py-16 md:py-24 {bg}">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="grid md:grid-cols-12 gap-10 items-start">
{grid}
      </div>
    </div>
  </section>"""


def _svc(icon, slug, title, desc, estandares=None, extra_cta=None, detalle=None, incluye=None, faq=None):
    return {
        "icon": icon, "slug": slug, "title": title, "desc": desc,
        "estandares": estandares or [], "extra_cta": extra_cta,
        # Contenido ampliado para SEO/GEO de cada página de detalle:
        # "detalle" = 1-2 párrafos de desarrollo del tema, "incluye" = lista
        # de entregables/alcance, "faq" = lista de (pregunta, respuesta) que
        # alimenta tanto la sección visible como el JSON-LD FAQPage.
        "detalle": detalle or [],
        "incluye": incluye or [],
        "faq": faq or [],
    }


# Cada entrada de "estandares" es (norma_u_organismo, dato_verificado, fuente).
# Investigado y cotejado contra al menos dos fuentes cuando fue posible (ver
# notas de verificación del proceso de investigación); son referencias
# informativas de organismos técnicos externos, no certificaciones de CEPASI.
#
# "detalle", "incluye" y "faq" son contenido editorial propio (no normativa
# citada) — desarrollan cada servicio para SEO/GEO sin inventar cifras,
# certificaciones de CEPASI ni afirmaciones que requieran una fuente externa.

SERVICE_CATEGORIES = [
    {
        "anchor": "asesoria", "number": "1", "title": "Asesoría y Consultoría Especializada",
        "intro": "Antes de capacitar o instalar un solo equipo, hay que entender el riesgo. Nuestro equipo de consultoría evalúa su empresa a fondo y traduce esa evaluación en documentos y planes claros, aplicables y alineados con la ley dominicana.",
        "image": None, "image_alt": "", "reverse": False, "bg": "",
        "items": [
            _svc("shield-check", "asesoria-integral-sst", "Asesoría y consultoría integral en Seguridad Industrial y Salud Ocupacional", "Acompañamiento experto para que su empresa identifique sus riesgos, priorice sus inversiones en seguridad y cumpla con sus obligaciones en materia de SST.", [
                ("ISO 45001:2018", "Especifica los requisitos de un sistema de gestión de la seguridad y salud en el trabajo: liderazgo, participación de los trabajadores e identificación de peligros.", "ISO"),
                ("Reglamento 522-06, Art. 8.1", "Obliga a todo empleador a elaborar un Programa de Seguridad y Salud en el Trabajo y renovarlo ante el Ministerio de Trabajo cada 3 años.", "Ministerio de Trabajo, R.D."),
                ("OIT, Convenios 155 y 187", "Convenios fundamentales de la OIT que establecen el marco de política nacional en SST y la promoción de sistemas de gestión.", "OIT"),
            ],
            detalle=[
                "La asesoría integral es el punto de partida antes de invertir en capacitación o equipos: evaluamos el estado real de su empresa frente al Reglamento 522-06, identificamos los riesgos presentes en cada área y le entregamos una hoja de ruta clara, con prioridades y plazos realistas, en lugar de una lista genérica de recomendaciones.",
                "Está pensada tanto para empresas que empiezan de cero en materia de seguridad y salud ocupacional como para las que ya tienen algunos elementos en marcha pero necesitan ordenar su cumplimiento, prepararse ante una inspección del Ministerio de Trabajo o simplemente confirmar que están haciendo lo correcto.",
            ],
            incluye=[
                "Diagnóstico inicial de cumplimiento en materia de SST",
                "Identificación y priorización de riesgos por área de trabajo",
                "Hoja de ruta de cumplimiento con plazos realistas",
                "Acompañamiento continuo, no solo un informe puntual",
                "Orientación para presentarse ante inspecciones del Ministerio de Trabajo",
            ],
            faq=[
                ("¿Mi empresa está obligada a tener un programa de SST?", "Sí. El Reglamento 522-06 obliga a todo empleador dominicano a elaborar y mantener un Programa de Seguridad y Salud en el Trabajo, sin importar el tamaño de la empresa."),
                ("¿Cuánto tiempo toma una asesoría integral?", "Depende del tamaño y la complejidad de la operación: una primera evaluación de riesgo puede completarse en pocos días, mientras que la implementación completa del programa suele tomar varias semanas."),
                ("¿La asesoría incluye la elaboración de documentos?", "Sí, la asesoría integral incluye el diseño de los documentos, procedimientos y planes que su empresa necesita para cumplir, no solo recomendaciones generales."),
            ]),
            _svc("file-text", "manual-sst", "Diseño del Manual de Seguridad y Salud en el Trabajo (SST)", "Elaboramos el manual oficial de su empresa, adaptado a su actividad, sus instalaciones y los riesgos específicos de su operación, en conformidad con el Reglamento 522-06.", [
                ("Reglamento 522-06, Resolución 04-2007", "Define 20 elementos básicos obligatorios de todo programa de SST: análisis de accidentes, entrenamiento, preparación para emergencias, entre otros.", "Ministerio de Trabajo, R.D."),
                ("Reglamento 522-06, Art. 8.2", "Cualquier cambio de maquinaria, productos o métodos de trabajo obliga a actualizar el programa y solicitar una nueva evaluación de riesgos.", "Ministerio de Trabajo, R.D."),
                ("ISO 45001:2018", "Exige mantener información documentada de la política, los objetivos y los procedimientos del sistema de gestión de SST.", "ISO"),
            ], extra_cta=("Completar formulario de informaciones para su Manual de SST", "formulario-psst.html"),
            detalle=[
                "El Manual de Seguridad y Salud en el Trabajo es el documento central de cumplimiento ante el Reglamento 522-06: reúne la política de SST de su empresa, los riesgos identificados, los procedimientos de control y el plan de preparación ante emergencias, en el formato que exige el Ministerio de Trabajo.",
                "Lo elaboramos a partir de la información real de su empresa —personal, instalaciones, equipos, productos químicos— recopilada a través de nuestro formulario en línea, para que el manual refleje su operación tal como es, y no una plantilla genérica.",
            ],
            incluye=[
                "Elaboración de los elementos básicos exigidos por la Resolución 04-2007",
                "Política y objetivos de SST adaptados a su empresa",
                "Procedimientos de identificación y control de riesgos",
                "Plan de preparación y respuesta ante emergencias",
                "Documento listo para presentar ante el Ministerio de Trabajo",
            ],
            faq=[
                ("¿Cada cuánto hay que renovar el Manual de SST?", "El Reglamento 522-06 exige renovarlo ante el Ministerio de Trabajo cada 3 años, o antes si cambian los procesos, la maquinaria o los productos utilizados."),
                ("¿Qué información necesita CEPASI para elaborar mi manual?", "Datos generales de la empresa, personal, inventario de equipos, productos químicos utilizados y organigrama, entre otros — puede enviárnoslos a través de nuestro formulario en línea."),
                ("¿El manual sirve para cualquier tipo de empresa?", "Sí, se adapta a la actividad económica, el tamaño y los riesgos específicos de cada empresa, desde oficinas hasta plantas industriales."),
            ]),
            _svc("search", "analisis-de-riesgo", "Elaboración de análisis de riesgo corporativos e industriales", "Identificamos los peligros presentes en sus instalaciones —incendios, eléctricos, estructurales, operativos— y entregamos un informe técnico con recomendaciones concretas de mitigación.", [
                ("ISO 31000:2018", "Norma internacional que estructura la gestión de riesgos en identificación, análisis, evaluación y tratamiento del riesgo.", "ISO"),
                ("Reglamento 522-06, Art. 7", "Obliga al empleador a evitar los riesgos en su origen, controlar los que no se puedan evitar y sustituir lo riesgoso por alternativas de menor riesgo.", "Ministerio de Trabajo, R.D."),
                ("OSHA 29 CFR 1910.132(d)", "Exige evaluar el lugar de trabajo para identificar peligros y certificar por escrito que dicha evaluación fue realizada.", "OSHA, EE. UU."),
            ],
            detalle=[
                "El análisis de riesgo es el paso técnico que sostiene todo lo demás: recorremos sus instalaciones, identificamos los peligros de incendio, eléctricos, estructurales y operativos presentes, y evaluamos su probabilidad e impacto para priorizar qué atender primero.",
                "El resultado es un informe técnico con recomendaciones de mitigación concretas —no una lista de observaciones sin orden—, que además sirve como base documental para el Manual de SST, el plan de emergencia y cualquier trámite ante el Ministerio de Trabajo.",
            ],
            incluye=[
                "Recorrido técnico de todas las áreas de la instalación",
                "Identificación de riesgos de incendio, eléctricos, estructurales y operativos",
                "Evaluación de probabilidad e impacto por tipo de riesgo",
                "Informe técnico con recomendaciones de mitigación priorizadas",
                "Base documental para el Manual de SST y el plan de emergencia",
            ],
            faq=[
                ("¿Con qué frecuencia se debe repetir un análisis de riesgo?", "Se recomienda repetirlo cada vez que cambien las condiciones de la instalación —maquinaria, productos, distribución de planta— y de forma periódica según lo defina el programa de SST de su empresa."),
                ("¿El análisis de riesgo es obligatorio?", "El Reglamento 522-06 obliga a evitar los riesgos en su origen y a controlar los que no se puedan evitar, lo cual requiere primero identificarlos mediante un análisis técnico."),
                ("¿Aplica solo a plantas industriales?", "No, también se realiza en oficinas, centros comerciales, colegios y otras instalaciones donde haya personal y público."),
            ]),
            _svc("map", "planes-de-emergencia", "Elaboración y estructuración de planes de emergencia para empresas y viviendas", "Diseñamos rutas de evacuación, puntos de encuentro y protocolos de actuación claros, tanto para instalaciones corporativas como para el hogar.", [
                ("OSHA 29 CFR 1910.38", "Un plan de acción de emergencia debe incluir procedimientos de evacuación, rutas de salida asignadas, conteo de personal y funciones de rescate.", "OSHA, EE. UU."),
                ("NFPA 1660 (heredero de NFPA 1600)", "Estándar internacional de referencia para programas de gestión de emergencias, continuidad y crisis en cualquier tipo de organización.", "NFPA"),
                ("Reglamento 522-06", "Incluye la preparación para emergencias como uno de los elementos obligatorios de todo programa de seguridad y salud en el trabajo.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "Un plan de emergencia traduce el análisis de riesgo en acciones concretas: quién hace qué, por dónde se evacúa, dónde se reúne el personal y cómo se actúa según el tipo de emergencia —incendio, sismo, huracán u otra situación crítica.",
                "Diseñamos el plan tanto para instalaciones corporativas como para viviendas, siempre con el mismo rigor técnico, adaptando roles, rutas y protocolos a la realidad de cada espacio y de las personas que lo ocupan.",
            ],
            incluye=[
                "Diseño de rutas de evacuación y puntos de encuentro",
                "Definición de roles y responsabilidades ante una emergencia",
                "Protocolos específicos por tipo de riesgo (incendio, sismo, huracán)",
                "Recomendaciones de señalización para cada ruta y salida",
                "Plan adaptado a empresas, instituciones y viviendas",
            ],
            faq=[
                ("¿Un plan de emergencia sirve sin capacitar al personal?", "No. El plan solo es efectivo si el personal lo conoce y lo practica; por eso recomendamos acompañarlo de capacitación y simulacros de evacuación."),
                ("¿También hacen planes de emergencia para el hogar?", "Sí, aplicamos el mismo enfoque técnico a residencias y edificios, considerando rutas de salida, puntos de encuentro y roles dentro de la familia."),
                ("¿Qué tipos de emergencia cubre el plan?", "Incendios, evacuaciones, sismos, huracanes y otras situaciones críticas relevantes para la actividad y ubicación de su empresa o vivienda."),
            ]),
        ],
        "proceso": [
            ("search", "Diagnóstico inicial", "Evaluamos su empresa, sus instalaciones y su nivel actual de cumplimiento frente al Reglamento 522-06."),
            ("file-text", "Propuesta técnica", "Definimos junto a usted el alcance, los documentos y los plazos realistas para avanzar."),
            ("pencil-ruler", "Elaboración", "Desarrollamos el análisis, el manual o el plan correspondiente, adaptado a su operación real."),
            ("handshake", "Entrega y seguimiento", "Le entregamos la documentación y damos seguimiento a su implementación en el tiempo."),
        ],
    },
    {
        "anchor": "capacitaciones", "number": "2", "title": "Capacitaciones y Formación Técnica",
        "intro": "Un plan de emergencia solo funciona si las personas saben ejecutarlo. Formamos a su personal —y, si lo desea, a su familia— para que sepan actuar con calma y eficacia ante cualquier situación de riesgo.",
        "image": CAPACITACION_IMG, "image_alt": "Capacitación de primeros auxilios y RCP impartida por CEPASI", "reverse": False, "bg": "bg-beige",
        "items": [
            _svc("activity", "primeros-auxilios", "Primeros auxilios básicos y avanzados", "Formación práctica para reconocer y atender emergencias médicas mientras llega ayuda especializada.", [
                ("AHA / ILCOR, Guías 2025", "En adultos, recomiendan compresiones torácicas de 100 a 120 por minuto, a una profundidad de 5 a 6 cm, con relación de 30:2.", "American Heart Association"),
                ("Reglamento 522-06, Resolución 09-26 (2026)", "Exige un responsable de primeros auxilios capacitado por cada 50 trabajadores de turno, con recapacitación cada 2 años.", "Ministerio de Trabajo, R.D."),
                ("Reglamento 522-06", "Exige un puesto de primeros auxilios dedicado en centros de trabajo con 100 o más trabajadores.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "Nuestra capacitación en primeros auxilios básicos y avanzados es práctica antes que teórica: los participantes practican con maniquíes y ejercicios de simulación el manejo de heridas, quemaduras, fracturas, atragantamiento y pérdida de conciencia, además de reanimación cardiopulmonar (RCP).",
                "Es la base de cualquier programa de SST, y el Reglamento 522-06 la vincula directamente con la figura del responsable de primeros auxilios que toda empresa debe designar y mantener capacitado.",
            ],
            incluye=[
                "Manejo de heridas, quemaduras y fracturas",
                "Reanimación cardiopulmonar (RCP) básica",
                "Atención de atragantamiento y pérdida de conciencia",
                "Uso correcto del botiquín de primeros auxilios",
                "Recomendación de frecuencia de recapacitación",
            ],
            faq=[
                ("¿Cada cuánto debe recapacitarse el responsable de primeros auxilios?", "El Reglamento 522-06 exige recapacitación cada 2 años para el responsable de primeros auxilios designado por la empresa."),
                ("¿Cuántos responsables de primeros auxilios necesita mi empresa?", "La norma exige al menos un responsable capacitado por cada 50 trabajadores de turno."),
                ("¿La capacitación es teórica o práctica?", "Es principalmente práctica, con ejercicios de simulación para que el personal gane confianza real ante una emergencia."),
            ]),
            _svc("siren", "manejo-de-emergencias", "Capacitación integral para el manejo de emergencias en las empresas", "Preparamos a su personal para responder de forma coordinada ante incendios, evacuaciones y otras situaciones críticas.", [
                ("NFPA 1660 (heredero de NFPA 1600)", "Exige evaluar las necesidades de entrenamiento y ejecutar un programa progresivo de ejercicios, desde simulacros de gabinete hasta simulacros a escala completa.", "NFPA"),
                ("ISO 22320:2018", "Norma internacional de referencia para la coordinación entre los actores involucrados en la respuesta a un incidente.", "ISO"),
                ("Reglamento 522-06", "Incluye la preparación para emergencias entre los elementos obligatorios de todo programa de seguridad y salud en el trabajo.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "Responder bien a una emergencia no depende solo de tener un plan escrito, sino de que cada persona sepa qué rol cumple en el momento crítico. Esta capacitación prepara a supervisores y personal clave para coordinar la respuesta ante incendios, evacuaciones y otras situaciones críticas dentro de su empresa.",
                "Trabajamos con ejercicios progresivos —desde simulacros de gabinete hasta ejercicios a escala completa— para que la coordinación entre áreas, brigada y liderazgo funcione en la práctica y no solo sobre el papel.",
            ],
            incluye=[
                "Identificación de roles ante una emergencia",
                "Protocolos de comunicación interna durante la crisis",
                "Coordinación con brigada de emergencia y personal clave",
                "Ejercicios de gabinete y simulacros progresivos",
                "Retroalimentación y ajustes al plan tras cada ejercicio",
            ],
            faq=[
                ("¿Quién debe recibir esta capacitación?", "Se recomienda para supervisores, encargados de área y todo el personal con funciones de respuesta dentro del plan de emergencia."),
                ("¿Incluye simulacros?", "Sí, la formación integra ejercicios progresivos, desde simulacros de gabinete hasta ejercicios a escala completa."),
                ("¿Se coordina con los cuerpos de bomberos o socorro?", "Reforzamos los protocolos de coordinación interna de su empresa; la comunicación formal con cuerpos externos depende de los canales que usted ya tenga establecidos."),
            ]),
            _svc("house", "prevencion-empresas-hogares", "Organización y prevención de emergencias en empresas y hogares", "Estructuramos protocolos de prevención adaptados tanto al entorno corporativo como al residencial.", [
                ("Reglamento 522-06", "Exige que toda empresa cuente con un Comité Mixto de SST (15 o más trabajadores) o un Coordinador de Seguridad y Salud en las de menor tamaño.", "Ministerio de Trabajo, R.D."),
                ("Reglamento 522-06", "Exige que todo programa de SST contemple señalización de seguridad, control de riesgos y entrenamiento del personal y la administración.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "No toda empresa necesita el mismo nivel de estructura: una empresa con 15 o más trabajadores requiere un Comité Mixto de SST, mientras que una más pequeña necesita al menos un coordinador de seguridad. Estructuramos y capacitamos según lo que corresponde a cada tamaño de organización.",
                "El mismo enfoque técnico se adapta al hogar: identificamos los riesgos del entorno residencial y organizamos protocolos de prevención simples, pensados para que cualquier miembro de la familia pueda seguirlos.",
            ],
            incluye=[
                "Diagnóstico de riesgos según el tipo de entorno (empresa u hogar)",
                "Protocolos de prevención adaptados a cada caso",
                "Recomendaciones de señalización y control de riesgos",
                "Orientación sobre comité o coordinador de SST según el tamaño de la empresa",
                "Capacitación del personal administrativo y operativo",
            ],
            faq=[
                ("¿Qué diferencia hay entre prevención en empresa y en hogar?", "El enfoque técnico es el mismo, pero los riesgos, roles y recursos disponibles cambian; adaptamos el protocolo a cada entorno."),
                ("¿Aplica a empresas pequeñas?", "Sí. Aunque el Comité Mixto de SST es obligatorio desde 15 trabajadores, toda empresa —sin importar su tamaño— debe contar con un coordinador de seguridad y salud."),
                ("¿Se puede combinar con otras capacitaciones?", "Sí, suele combinarse con primeros auxilios, simulacros de evacuación y formación de brigadas."),
            ]),
            _svc("door-open", "simulacros-de-evacuacion", "Ejecución de simulacros de evacuación", "Ponemos a prueba los planes de emergencia en condiciones reales, para corregir a tiempo lo que no funciona.", [
                ("OSHA 29 CFR 1910.38", "Exige documentar el plan de acción de emergencia y ejecutar simulacros con la frecuencia que el propio plan establezca.", "OSHA, EE. UU."),
                ("Reglamento 522-06", "Exige mantener libres y señalizadas las vías y salidas de evacuación, con puertas que abran en el sentido de la salida.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "Un plan de emergencia que nunca se ha probado es, en la práctica, un documento sin verificar. El simulacro pone a prueba las rutas, los tiempos de respuesta y la reacción real del personal, y suele revelar obstáculos u omisiones que no se ven en el papel.",
                "Planificamos el escenario según el objetivo —entrenar o evaluar—, cronometramos la evacuación y entregamos un informe con hallazgos concretos para corregir antes de que ocurra una emergencia real.",
            ],
            incluye=[
                "Planificación del escenario y aviso según el tipo de simulacro",
                "Ejecución cronometrada de la evacuación",
                "Verificación de rutas, salidas y puntos de encuentro",
                "Conteo de personal y evaluación de tiempos de respuesta",
                "Informe con hallazgos y recomendaciones de mejora",
            ],
            faq=[
                ("¿Con qué frecuencia se deben hacer simulacros?", "La frecuencia debe establecerse en el propio plan de emergencia de la empresa; lo recomendable es realizarlos de forma periódica y no solo una vez."),
                ("¿El simulacro se avisa con anticipación?", "Puede planificarse avisado o sorpresivo según el objetivo: los avisados sirven para entrenar, los sorpresivos para evaluar la respuesta real."),
                ("¿Qué se entrega después del simulacro?", "Un informe con los tiempos de evacuación, los hallazgos sobre rutas u obstáculos, y recomendaciones concretas de mejora."),
            ]),
            _svc("users", "comite-mixto-sst", "Formación de Comité Mixto de SST", "Capacitamos a los integrantes del Comité Mixto de Seguridad y Salud en el Trabajo, tal como lo exige el Reglamento 522-06.", [
                ("Reglamento 522-06, Art. 6.1", "Toda empresa con 15 o más trabajadores debe constituir un Comité Mixto de Seguridad y Salud en el Trabajo.", "Ministerio de Trabajo, R.D."),
                ("Reglamento 522-06, Art. 6.4.2", "El comité debe reunirse al menos una vez al mes y remitir las actas a la Dirección General de Higiene y Seguridad Industrial.", "Ministerio de Trabajo, R.D."),
                ("OIT, Convenio 155 (1981)", "Respalda internacionalmente la cooperación entre empleadores y trabajadores mediante comités paritarios de seguridad y salud.", "OIT"),
            ],
            detalle=[
                "El Comité Mixto de Seguridad y Salud en el Trabajo es la instancia que exige el Reglamento 522-06 para que empleador y trabajadores gestionen juntos la prevención dentro de la empresa. Capacitamos a sus integrantes titulares y suplentes en el marco legal, sus funciones y su forma de operar.",
                "Más allá de la capacitación puntual, orientamos al comité sobre la periodicidad de sus reuniones, la elaboración de actas y su reporte a la Dirección General de Higiene y Seguridad Industrial, para que funcione de forma continua y no solo en el papel.",
            ],
            incluye=[
                "Explicación del marco legal del Comité Mixto (Reglamento 522-06)",
                "Capacitación de los integrantes titulares y suplentes",
                "Definición de funciones y responsabilidades del comité",
                "Orientación sobre actas y reportes a la Dirección de Higiene y Seguridad",
                "Recomendaciones para el funcionamiento continuo del comité",
            ],
            faq=[
                ("¿A partir de cuántos trabajadores es obligatorio el Comité Mixto?", "El Reglamento 522-06 lo exige en empresas con 15 o más trabajadores."),
                ("¿Con qué frecuencia debe reunirse el comité?", "Al menos una vez al mes, remitiendo las actas correspondientes a la Dirección General de Higiene y Seguridad Industrial."),
                ("¿Quién puede formar parte del comité?", "Está integrado de forma paritaria por representantes del empleador y de los trabajadores, según lo establece la normativa."),
            ]),
            _svc("shield", "brigadas-de-emergencia", "Formación y entrenamiento de Brigadas de Emergencia", "Preparamos brigadas internas capaces de liderar la evacuación, el combate inicial de incendios y la atención de primeros auxilios dentro de su empresa.", [
                ("NFPA 600", "Establece los requisitos mínimos de organización, entrenamiento y equipamiento de brigadas de emergencia/incendio en instalaciones industriales y comerciales.", "NFPA"),
                ("OSHA 29 CFR 1910.156", "Exige capacitación de la brigada acorde a sus funciones, con entrenamiento al menos anual y refuerzo trimestral para quienes hacen extinción estructural interior.", "OSHA, EE. UU."),
            ],
            detalle=[
                "La brigada de emergencia es el primer nivel de respuesta dentro de su empresa: actúa en los minutos antes de que llegue ayuda especializada, liderando la evacuación, atendiendo primeros auxilios y combatiendo un conato de incendio con los extintores disponibles.",
                "Seleccionamos y entrenamos a sus integrantes según las funciones que asumirán, y recomendamos un programa de refuerzo periódico para que las habilidades no se pierdan con el tiempo.",
            ],
            incluye=[
                "Selección y organización de los integrantes de la brigada",
                "Entrenamiento en liderazgo de evacuación",
                "Combate inicial de incendios con extintores portátiles",
                "Atención básica de primeros auxilios dentro de la empresa",
                "Programa de refuerzo periódico de la brigada",
            ],
            faq=[
                ("¿Cuántas personas debe tener una brigada de emergencia?", "Depende del tamaño de la instalación y la cantidad de personal; se recomienda contar con brigadistas distribuidos en las distintas áreas y turnos."),
                ("¿Con qué frecuencia se debe reentrenar a la brigada?", "Se recomienda un entrenamiento anual como mínimo, con refuerzos más frecuentes para quienes tienen funciones de combate de incendios."),
                ("¿La brigada reemplaza a los bomberos?", "No. La brigada actúa en los primeros minutos mientras llega ayuda especializada; no sustituye la intervención de los cuerpos de bomberos."),
            ]),
            _svc("zap", "uso-de-dea", "Capacitación en uso de Desfibriladores Externos Automáticos (DEA)", "Entrenamiento en el manejo correcto del DEA para actuar en los primeros minutos —los más críticos— de una emergencia cardíaca.", [
                ("AHA, Cadena de Supervivencia", "Sitúa la desfibrilación temprana con DEA como uno de los eslabones más determinantes para la sobrevivencia ante un paro cardíaco.", "American Heart Association"),
                ("Reglamento 522-06, Resolución 09-26 (2026)", "Incorpora la disposición de desfibriladores externos automáticos entre los requisitos de respuesta a emergencias laborales.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "Ante un paro cardíaco súbito, cada minuto sin desfibrilación reduce las probabilidades de sobrevivencia. Esta capacitación enseña a reconocer la emergencia y a usar el DEA de forma correcta y segura, combinándolo con RCP dentro de la cadena de supervivencia.",
                "El equipo está diseñado para guiar al usuario paso a paso con instrucciones de voz, pero la práctica supervisada es lo que da al personal la confianza para actuar sin dudar en el momento real.",
            ],
            incluye=[
                "Reconocimiento de un paro cardíaco súbito",
                "Uso correcto y seguro del desfibrilador externo automático",
                "Combinación de RCP y DEA en la cadena de supervivencia",
                "Práctica con equipo de entrenamiento",
                "Recomendaciones sobre ubicación y mantenimiento del DEA",
            ],
            faq=[
                ("¿Es difícil usar un DEA?", "El equipo está diseñado para guiar al usuario paso a paso con instrucciones de voz; la capacitación refuerza la confianza para actuar sin dudar."),
                ("¿Mi empresa necesita tener un DEA?", "Cada vez más empresas lo incorporan como parte de su respuesta a emergencias; consulte con nuestro equipo si su actividad y tamaño lo recomiendan."),
                ("¿Quién debe recibir esta capacitación?", "Se recomienda para el personal de primeros auxilios, los brigadistas y cualquier colaborador dispuesto a actuar ante una emergencia cardíaca."),
            ]),
            _svc("truck", "manejo-de-montacargas", "Operación y manejo seguro de montacargas", "Certificación práctica para operadores, reduciendo accidentes en zonas de carga y almacén.", [
                ("OSHA 29 CFR 1910.178(l)", "Exige formación teórica, práctica y una evaluación de desempeño antes de autorizar a un operador de montacargas.", "OSHA, EE. UU."),
                ("OSHA 29 CFR 1910.178(l)(4)(iii)", "El desempeño de cada operador certificado debe reevaluarse al menos una vez cada 3 años.", "OSHA, EE. UU."),
            ],
            detalle=[
                "El montacargas es uno de los equipos con mayor riesgo de accidente en almacenes y zonas de carga si el operador no está debidamente formado. Combinamos teoría, práctica supervisada y una evaluación real de desempeño antes de considerar autorizado a un operador.",
                "Adaptamos la capacitación al tipo de montacargas y a las condiciones reales del almacén de su empresa, en lugar de un contenido genérico desconectado de su operación diaria.",
            ],
            incluye=[
                "Fundamentos teóricos de operación segura de montacargas",
                "Práctica supervisada de maniobras y carga",
                "Evaluación de desempeño individual del operador",
                "Identificación de riesgos en zonas de carga y almacén",
                "Recomendación de reevaluación periódica del operador",
            ],
            faq=[
                ("¿Cada cuánto debe recertificarse un operador de montacargas?", "Se recomienda reevaluar el desempeño de cada operador certificado al menos una vez cada 3 años, o antes si cambia de equipo o hay un incidente."),
                ("¿Cualquier persona puede operar un montacargas?", "No. Debe recibir formación teórica, práctica y una evaluación de desempeño antes de ser autorizado a operar el equipo."),
                ("¿La capacitación se adapta al tipo de montacargas de mi empresa?", "Sí, se ajusta al equipo específico y a las condiciones reales del almacén o zona de carga."),
            ]),
            _svc("plug-zap", "seguridad-electrica-industrial", "Seguridad eléctrica e industrial", "Formación en prevención de riesgos eléctricos e industriales para personal técnico y operativo.", [
                ("NFPA 70E", "Establece las prácticas de trabajo seguras frente a choque eléctrico y arco eléctrico (arc flash) en el entorno laboral.", "NFPA"),
                ("NFPA 70E", "Exige un análisis de riesgo de arco eléctrico que determine la energía incidente y la categoría de equipo de protección personal requerida.", "NFPA"),
            ],
            detalle=[
                "Los riesgos eléctricos son de los que menos aviso dan antes de causar un accidente grave. Esta capacitación forma a personal técnico, de mantenimiento y operativo en el reconocimiento de riesgos eléctricos e industriales y en las prácticas de trabajo seguro frente a choque y arco eléctrico.",
                "Se cubre también el uso correcto del equipo de protección personal eléctrico y los procedimientos de bloqueo y etiquetado (LOTO) antes de intervenir cualquier equipo o instalación energizada.",
            ],
            incluye=[
                "Identificación de riesgos eléctricos en el entorno industrial",
                "Prácticas de trabajo seguro frente a choque y arco eléctrico",
                "Uso correcto del equipo de protección personal eléctrico",
                "Procedimientos de bloqueo y etiquetado (LOTO)",
                "Recomendaciones para personal técnico y operativo",
            ],
            faq=[
                ("¿A quién va dirigida esta capacitación?", "A personal técnico, de mantenimiento y operativo que trabaja cerca de tableros, paneles o instalaciones eléctricas."),
                ("¿Qué es el riesgo de arco eléctrico?", "Es la liberación repentina de energía durante una falla eléctrica, que puede causar quemaduras graves; la capacitación enseña a reconocerlo y prevenirlo."),
                ("¿Incluye el uso de equipo de protección personal?", "Sí, se cubre la selección y el uso correcto del EPP adecuado según el nivel de riesgo eléctrico."),
            ]),
            _svc("flask-conical", "manejo-de-msds", "Manejo básico de Hojas de Datos de Seguridad de Materiales (MSDS) y materiales peligrosos", "Capacitación para interpretar correctamente las hojas MSDS y manipular sustancias peligrosas con seguridad.", [
                ("OSHA 29 CFR 1910.1200 / SGA-GHS de la ONU", "Exige que las hojas de datos de seguridad (SDS) sigan un formato estandarizado de 16 secciones.", "OSHA / ONU"),
                ("SGA-GHS de la ONU", "Establece 9 pictogramas de peligro estandarizados para etiquetas y hojas de seguridad, cubriendo peligros físicos, para la salud y ambientales.", "ONU"),
            ],
            detalle=[
                "Trabajar con productos químicos sin saber interpretar su hoja de seguridad es un riesgo silencioso. Enseñamos a su personal a leer correctamente las hojas MSDS/SDS, reconocer los pictogramas de peligro y aplicar las medidas de manipulación, almacenamiento y transporte correspondientes.",
                "También cubrimos qué hacer ante un derrame o una exposición accidental, y cómo mantener actualizado el inventario de sustancias químicas de su empresa conforme cambian sus procesos o proveedores.",
            ],
            incluye=[
                "Interpretación de las secciones de la hoja de seguridad (SDS)",
                "Reconocimiento de los pictogramas de peligro del SGA-GHS",
                "Manipulación, almacenamiento y transporte seguro de sustancias",
                "Protocolos ante derrames o exposición accidental",
                "Recomendaciones para mantener actualizado el inventario de químicos",
            ],
            faq=[
                ("¿Qué es una hoja MSDS o SDS?", "Es el documento estandarizado que describe los peligros, el manejo seguro y la respuesta ante emergencias de un producto químico."),
                ("¿Mi empresa debe tener las MSDS de todos sus productos?", "Sí, toda empresa que use o almacene sustancias químicas debe mantener disponibles las hojas de seguridad correspondientes."),
                ("¿La capacitación incluye el etiquetado de los productos?", "Sí, se cubren los pictogramas y el etiquetado estandarizado según el Sistema Globalmente Armonizado (SGA-GHS) de la ONU."),
            ]),
            _svc("cloud-lightning", "riesgos-fenomenos-naturales", "Prevención de riesgos ante fenómenos naturales (huracanes y terremotos)", "Protocolos de preparación y respuesta ante eventos naturales frecuentes en la región.", [
                ("Ley 147-02 (R.D.)", "Crea el Sistema Nacional para la Prevención, Mitigación y Respuesta ante Desastres y el Centro de Operaciones de Emergencia (COE).", "Ley 147-02, R.D."),
                ("NFPA 1660 (heredero de NFPA 1600)", "Reconocido como estándar de referencia para programas de gestión de emergencias ante todo tipo de riesgo.", "NFPA"),
                ("OSHA", "Recomienda identificar zonas seguras dentro del lugar de trabajo y practicar regularmente los planes de evacuación ante sismos.", "OSHA, EE. UU."),
            ],
            detalle=[
                "República Dominicana está expuesta tanto a huracanes como a sismos, y cada fenómeno requiere protocolos distintos. Formamos a su personal en la identificación de zonas seguras dentro de sus instalaciones y en la actuación correcta ante cada tipo de evento.",
                "El objetivo es que, llegado el momento, su empresa no tenga que improvisar: que sepa cuándo activar el plan, cómo coordinarse internamente y cómo alinearse con el Sistema Nacional de Prevención y Respuesta ante Desastres.",
            ],
            incluye=[
                "Identificación de zonas seguras dentro de las instalaciones",
                "Protocolos de actuación ante huracanes y tormentas",
                "Protocolos de actuación ante sismos y terremotos",
                "Orientación sobre el Sistema Nacional de Prevención y Respuesta (COE)",
                "Práctica periódica de los planes ante fenómenos naturales",
            ],
            faq=[
                ("¿Qué debo hacer antes de la temporada ciclónica?", "Revisar y actualizar el plan de emergencia, verificar rutas y puntos de encuentro, y capacitar al personal en los protocolos correspondientes."),
                ("¿Existe una entidad que coordine la respuesta a desastres en R.D.?", "Sí, el Centro de Operaciones de Emergencia (COE), creado bajo la Ley 147-02, coordina la respuesta nacional ante desastres."),
                ("¿Esta capacitación aplica también a sismos?", "Sí, se cubren protocolos específicos tanto para huracanes como para terremotos, dos de los fenómenos naturales más relevantes en la región."),
            ]),
            _svc("flame", "prevencion-control-incendios", "Prevención y control de incendios", "Formación teórico-práctica en el uso de extintores y en la actuación temprana ante un conato de incendio.", [
                ("NFPA 10", "Clasifica los incendios en 5 clases según el material combustible —A, B, C, D y K— como base para seleccionar el extintor correcto.", "NFPA"),
                ("OSHA 29 CFR 1910.157", "Exige capacitación general sobre extintores portátiles al momento de la contratación y al menos una vez al año.", "OSHA, EE. UU."),
            ],
            detalle=[
                "Un extintor solo sirve si la persona que lo toma sabe usarlo en los primeros segundos de un conato de incendio. Esta capacitación combina teoría —clasificación de fuegos y selección del extintor correcto— con práctica real de manejo del equipo.",
                "Reforzamos también la decisión más importante: cuándo actuar y cuándo evacuar. Un conato mal atendido, o atendido con el extintor equivocado, puede agravar la situación en segundos.",
            ],
            incluye=[
                "Clasificación de los tipos de fuego (A, B, C, D y K)",
                "Selección del extintor correcto según el riesgo",
                "Práctica real de uso de extintores portátiles",
                "Actuación ante un conato de incendio",
                "Recomendaciones para la capacitación anual del personal",
            ],
            faq=[
                ("¿Con qué frecuencia debe capacitarse al personal en uso de extintores?", "Se recomienda al momento de la contratación y, como mínimo, una vez al año."),
                ("¿Todos los extintores sirven para cualquier tipo de fuego?", "No. Cada extintor está diseñado para clases de fuego específicas; usar el incorrecto puede agravar la situación."),
                ("¿La capacitación incluye práctica real con fuego controlado?", "Incluye práctica con extintores en condiciones controladas y seguras, adaptada a las instalaciones disponibles."),
            ]),
        ],
        "proceso": [
            ("clipboard-check", "Evaluación de necesidades", "Identificamos qué formación requiere su personal según su actividad, sus riesgos y sus obligaciones normativas."),
            ("calendar-check", "Planificación", "Coordinamos fecha, lugar y grupo de participantes junto a su empresa, sin interrumpir su operación."),
            ("users-round", "Capacitación práctica", "Impartimos la formación con ejercicios prácticos y casos reales, no solo teoría en un salón."),
            ("badge-check", "Certificación y refuerzo", "Entregamos constancia de participación y recomendamos la frecuencia de recapacitación según cada tema."),
        ],
    },
    {
        "anchor": "mantenimiento", "number": "3", "title": "Mantenimiento, Taller y Equipamiento",
        "intro": "Un extintor vencido o un detector de humo sin batería son fallas invisibles hasta el momento en que más se necesitan. Nuestro taller especializado se encarga de que sus sistemas contra incendios estén siempre operativos.",
        "image": HERO_IMG, "image_alt": "Técnico de CEPASI dando mantenimiento a un extintor en taller", "reverse": True, "bg": "",
        "items": [
            _svc("wrench", "recarga-mantenimiento-extintores", "Recargas y mantenimiento preventivo/correctivo de extintores", "Inspección, recarga y reparación de extintores para garantizar que funcionen cuando se les necesite.", [
                ("NFPA 10", "Exige inspección visual mensual y un mantenimiento anual completo realizado por un técnico certificado.", "NFPA"),
                ("NFPA 10", "Fija la prueba hidrostática cada 5 años para extintores de agua, espuma, CO2 y agente húmedo, y cada 12 años para los de polvo químico seco.", "NFPA"),
                ("NORDOM 759", "Norma dominicana que regula la selección, inspección, mantenimiento y prueba de extintores portátiles.", "INDOCAL, R.D."),
            ],
            detalle=[
                "Un extintor no revisado es una falla invisible: por fuera puede lucir intacto y por dentro haber perdido presión, tener el agente compactado o el cilindro corroído. Nuestro servicio de mantenimiento preventivo y correctivo revisa, recarga y repara sus extintores para que respondan cuando de verdad se les necesite.",
                "Trabajamos con la periodicidad que exige la norma —inspección visual, mantenimiento anual completo y prueba hidrostática cuando corresponde— y le dejamos cada equipo etiquetado con la fecha de servicio, para que su empresa tenga trazabilidad de todo su inventario.",
            ],
            incluye=[
                "Inspección visual y funcional del extintor",
                "Recarga con el agente extintor correspondiente",
                "Reparación de partes dañadas o desgastadas",
                "Prueba hidrostática cuando corresponde según el tipo",
                "Etiquetado y registro de la fecha del servicio",
            ],
            faq=[
                ("¿Cada cuánto debo recargar un extintor?", "La recarga se realiza tras cada uso y, adicionalmente, según el mantenimiento anual completo que exige la norma."),
                ("¿Qué es la prueba hidrostática?", "Es una prueba de presión que verifica la integridad del cilindro; se exige cada 5 años en la mayoría de los tipos y cada 12 años en los de polvo químico seco."),
                ("¿Cómo sé si mi extintor necesita mantenimiento?", "Señales como manómetro fuera de rango, corrosión, sello roto o falta de inspección reciente indican que necesita revisión."),
            ]),
            _svc("truck", "taller-recarga-a-domicilio", "Taller especializado de recarga a domicilio", "Vamos hasta su empresa o su hogar a recargar y dar mantenimiento a sus extintores, sin que tenga que trasladarlos.", [
                ("NFPA 10", "Exige que el mantenimiento anual y la recarga tras cualquier uso sean ejecutados por personal certificado, con procedimientos específicos según el tipo de agente.", "NFPA"),
                ("NORDOM 759", "Norma dominicana equivalente que aplica a la recarga y prueba de extintores portátiles en el país.", "INDOCAL, R.D."),
            ],
            detalle=[
                "No siempre es práctico desmontar y trasladar todos los extintores de una empresa hasta un taller. Por eso llevamos el servicio hasta su empresa o su hogar, con el mismo procedimiento y los mismos estándares que aplicaríamos en nuestras instalaciones.",
                "Es especialmente útil para empresas con varios puntos de extintores distribuidos en distintas áreas o pisos, donde reunirlos todos para un traslado significaría dejar zonas sin protección mientras tanto.",
            ],
            incluye=[
                "Atención directa en su empresa o vivienda",
                "Recarga y mantenimiento realizado por personal certificado",
                "Reparación de válvulas, mangueras y componentes",
                "Entrega con etiquetado y fecha de servicio actualizada",
                "Sin necesidad de trasladar los equipos hasta un taller",
            ],
            faq=[
                ("¿En qué zonas ofrecen el servicio a domicilio?", "Contáctenos por WhatsApp o teléfono para confirmar la cobertura en su zona."),
                ("¿El servicio a domicilio tiene el mismo estándar que el taller?", "Sí, se aplican los mismos procedimientos y estándares de mantenimiento que en nuestro taller."),
                ("¿Pueden atender varios extintores de una vez?", "Sí, es habitual atender todo el inventario de extintores de una empresa en una sola visita."),
            ]),
            _svc("flame-kindling", "venta-de-extintores", "Venta de extintores (ABC, CO2, Halotron, tipo K y sistemas automáticos)", "Le asesoramos sobre el tipo de extintor correcto según el riesgo de cada área de su instalación.", [
                ("NFPA 10", "Clasifica los extintores según el tipo de fuego que combaten: ABC (fosfato monoamónico), CO2, agentes limpios como Halotron y agente húmedo para cocinas (Clase K).", "NFPA"),
                ("UL 711 / UL 299 / UL 2129", "Normas de listado UL que rigen la construcción, los materiales y el rating de cada extintor.", "UL Solutions"),
                ("NORDOM 567", "Norma dominicana que define las clases de fuego usadas para seleccionar el agente extintor correcto.", "INDOCAL, R.D."),
            ],
            detalle=[
                "Comprar un extintor sin evaluar el riesgo del área donde se va a instalar es uno de los errores más comunes: un extintor equivocado puede no combatir el tipo de fuego que realmente puede ocurrir ahí. Evaluamos cada zona de su instalación —oficinas, cocina, cuarto eléctrico, almacén— antes de recomendar el tipo correcto.",
                "Ofrecemos extintores ABC, CO2, agentes limpios como Halotron y tipo K para cocinas, además de sistemas automáticos para riesgos específicos que requieren protección constante sin intervención humana.",
            ],
            incluye=[
                "Evaluación del tipo de riesgo por área (eléctrico, líquidos, cocina, etc.)",
                "Recomendación del extintor correcto: ABC, CO2, Halotron o tipo K",
                "Venta de sistemas automáticos para riesgos específicos",
                "Instalación y señalización del punto de extintor",
                "Registro para su próximo mantenimiento programado",
            ],
            faq=[
                ("¿Qué extintor necesito para mi oficina?", "Generalmente un extintor multipropósito tipo ABC cubre la mayoría de los riesgos comunes de oficina; lo confirmamos según su evaluación específica."),
                ("¿Qué diferencia hay entre un extintor ABC y uno de CO2?", "El ABC usa polvo químico y sirve para fuegos sólidos, líquidos y eléctricos; el de CO2 es ideal para equipos electrónicos sensibles porque no deja residuo."),
                ("¿Venden extintores para cocinas industriales?", "Sí, ofrecemos extintores tipo K, diseñados específicamente para fuegos con aceites y grasas de cocina."),
            ]),
            _svc("radio-tower", "deteccion-de-incendios", "Instalación de sistemas de detección de incendios y detectores de humo", "Diseño e instalación de sistemas de detección temprana adaptados a sus instalaciones.", [
                ("NFPA 72", "Establece un régimen de pruebas escalonado —mensual, trimestral, semestral y anual— para paneles, detectores y dispositivos de notificación.", "NFPA"),
                ("NORDOM 901", "Norma dominicana sobre alarmas de incendio y señalización, basada explícitamente en NFPA 72.", "INDOCAL, R.D."),
            ],
            detalle=[
                "La detección temprana es lo que convierte un incendio en un conato controlable, en lugar de una emergencia mayor. Diseñamos e instalamos sistemas de detección de humo y alarma adaptados al tamaño y la distribución real de su instalación.",
                "Configuramos los dispositivos de notificación para que la alarma se active en toda la instalación o por zonas, según lo que tenga más sentido para su operación, y probamos el sistema completo antes de dejarlo en funcionamiento.",
            ],
            incluye=[
                "Diseño del sistema según el tipo y tamaño de la instalación",
                "Instalación de detectores de humo y paneles de control",
                "Configuración de dispositivos de notificación y alarma",
                "Pruebas de funcionamiento tras la instalación",
                "Recomendaciones de mantenimiento periódico del sistema",
            ],
            faq=[
                ("¿Cada cuánto se deben probar los detectores de humo?", "Se recomienda un régimen escalonado: pruebas mensuales, trimestrales, semestrales y anuales según el tipo de dispositivo."),
                ("¿Instalan sistemas en empresas pequeñas y grandes?", "Sí, adaptamos el diseño desde una oficina pequeña hasta una planta industrial de mayor escala."),
                ("¿El sistema se conecta a una alarma general?", "Sí, se configura para activar dispositivos de notificación —sirenas, luces— en toda la instalación o por zonas."),
            ]),
            _svc("lightbulb", "lamparas-de-emergencia", "Suministro e instalación de lámparas de emergencia", "Iluminación de emergencia para garantizar rutas de evacuación visibles ante un corte eléctrico.", [
                ("NFPA 101 (Life Safety Code)", "Exige que la iluminación de emergencia en rutas de salida provea un mínimo de 90 minutos de autonomía y se active en menos de 10 segundos.", "NFPA"),
                ("UL 924", "Norma de listado que exige que el equipo sostenga la carga al menos 90 minutos, con prueba funcional mensual y prueba de duración completa anual.", "UL Solutions"),
            ],
            detalle=[
                "Durante un corte eléctrico, la diferencia entre una evacuación ordenada y una confusa suele estar en la iluminación. Evaluamos qué pasillos, escaleras y salidas de su instalación requieren lámparas de emergencia y las instalamos donde realmente hacen falta.",
                "Cada lámpara se prueba para confirmar que se activa en segundos y que mantiene la autonomía necesaria hasta completar la evacuación, y recomendamos un calendario simple de pruebas para mantenerlas operativas.",
            ],
            incluye=[
                "Evaluación de rutas de evacuación que requieren iluminación",
                "Suministro de lámparas de emergencia certificadas",
                "Instalación en pasillos, escaleras y salidas",
                "Prueba de autonomía y encendido automático",
                "Recomendaciones de prueba mensual y anual",
            ],
            faq=[
                ("¿Cuánto tiempo debe durar encendida una lámpara de emergencia?", "Se recomienda un mínimo de 90 minutos de autonomía tras un corte eléctrico."),
                ("¿En qué zonas es obligatorio instalarlas?", "Principalmente en rutas de evacuación, escaleras y salidas donde la iluminación normal pueda fallar durante una emergencia."),
                ("¿Requieren mantenimiento?", "Sí, se recomienda una prueba funcional mensual y una prueba de duración completa al menos una vez al año."),
            ]),
        ],
        "proceso": [
            ("clipboard-list", "Inspección", "Revisamos el estado actual de sus extintores y sistemas contra incendios en planta."),
            ("search-check", "Diagnóstico", "Determinamos qué requiere recarga, reparación, reemplazo o una instalación nueva."),
            ("wrench", "Servicio técnico", "Ejecutamos la recarga, reparación o instalación en su planta o a domicilio, según el caso."),
            ("calendar-clock", "Registro y próxima revisión", "Etiquetamos el servicio realizado y programamos el siguiente mantenimiento."),
        ],
    },
    {
        "anchor": "equipos", "number": "4", "title": "Equipos de Emergencia y Primeros Auxilios",
        "intro": "Equipamos a su empresa o su hogar con los productos que marcan la diferencia en los primeros minutos de una emergencia: botiquines completos, camillas, señalética normativa y sistemas contra incendios.",
        "image": BOTIQUIN_IMG, "image_alt": "Botiquín de primeros auxilios equipado CEPASI", "reverse": False, "bg": "bg-beige",
        "items": [
            _svc("briefcase-medical", "botiquines-equipados", "Botiquines de primeros auxilios equipados", "Disponibles para 25, 50 y 100 personas, en gabinete de metal, plástico o bolso de tela, según el espacio y las necesidades de su empresa.", [
                ("ANSI/ISEA Z308.1-2021", "Clasifica los botiquines en Clase A (riesgo general) y Clase B (mayor riesgo, incluye férulas y torniquetes).", "ANSI/ISEA"),
                ("Reglamento 522-06, Resolución 09-26 (2026)", "Clasifica los botiquines dominicanos en Tipo A, B y C según el nivel de riesgo, y exige un responsable capacitado por cada 50 trabajadores de turno.", "Ministerio de Trabajo, R.D."),
                ("OSHA 29 CFR 1910.151(b)", "Exige suministros de primeros auxilios adecuados y de fácil acceso, citando a ANSI Z308.1 como referencia de contenido mínimo.", "OSHA, EE. UU."),
            ],
            detalle=[
                "El botiquín es, en muchos casos, la primera respuesta ante un accidente laboral, y su contenido debe corresponder al nivel de riesgo real de la empresa, no ser genérico. Ofrecemos botiquines para 25, 50 y 100 personas, clasificados según el tipo de riesgo, en gabinete de metal, plástico o bolso de tela.",
                "Le ayudamos a definir cuántos botiquines necesita y dónde ubicarlos según la distribución de su personal, y orientamos sobre la reposición periódica del contenido para que nunca esté incompleto cuando más se necesite.",
            ],
            incluye=[
                "Botiquines para 25, 50 y 100 personas",
                "Gabinete de metal, plástico o bolso de tela según el espacio",
                "Contenido clasificado según el nivel de riesgo (Tipo A, B o C)",
                "Ubicación recomendada según la cantidad de personal",
                "Orientación sobre reposición y actualización periódica del contenido",
            ],
            faq=[
                ("¿Qué tamaño de botiquín necesita mi empresa?", "Depende de la cantidad de personal y del nivel de riesgo de la actividad; lo evaluamos junto a usted antes de recomendar el tipo."),
                ("¿Es obligatorio tener un botiquín en la empresa?", "Sí, y en centros de trabajo con 100 o más trabajadores se exige además un puesto de primeros auxilios dedicado."),
                ("¿El botiquín viene listo para usar?", "Sí, se entrega equipado y clasificado según el nivel de riesgo correspondiente a su empresa."),
            ]),
            _svc("bed", "camillas-de-trauma", "Camillas de trauma para emergencias", "Incluyen inmovilizadores de cuello, arnés y sujeciones, listas para una respuesta rápida ante una lesión.", [
                ("Declaración conjunta NAEMSP/ACS-COT/ACEP (2018)", "Recomienda el uso de collarín cervical junto con camilla para mantener la alineación neutra durante el traslado del paciente.", "NAEMSP"),
                ("Reglamento 522-06, Resolución 09-26 (2026)", "Incluye camillas y collarines cervicales entre el equipamiento exigido en los puestos de primeros auxilios.", "Ministerio de Trabajo, R.D."),
            ],
            detalle=[
                "Ante una lesión física —una caída, un golpe, un accidente en zona de carga— mover a la persona de forma incorrecta puede agravar el daño. Nuestras camillas de trauma incluyen inmovilizador de cuello, arnés y sujeciones para un traslado seguro hasta que llegue ayuda especializada.",
                "Recomendamos su ubicación dentro de la instalación según las zonas de mayor riesgo físico, y su uso correcto se refuerza con nuestra capacitación en primeros auxilios.",
            ],
            incluye=[
                "Camilla rígida para traslado seguro del paciente",
                "Inmovilizador de cuello (collarín cervical)",
                "Arnés y sujeciones para fijar al paciente",
                "Recomendaciones de ubicación dentro de la instalación",
                "Orientación sobre su uso correcto junto a primeros auxilios",
            ],
            faq=[
                ("¿Por qué es importante usar collarín junto con la camilla?", "Ayuda a mantener la alineación neutra de la columna durante el traslado, reduciendo el riesgo de agravar una lesión."),
                ("¿Qué empresas deben tener camilla de trauma?", "Se recomienda especialmente en entornos con mayor riesgo de accidentes físicos, como plantas industriales, almacenes y zonas de construcción."),
                ("¿La camilla viene con capacitación de uso?", "Puede combinarse con nuestra capacitación de primeros auxilios para que el personal sepa usarla correctamente."),
            ]),
            _svc("signpost", "senaletica-industrial", "Señalética de seguridad industrial", "Rutas de evacuación, zonas de reunión, ubicación de extintores, riesgo eléctrico, prohibición de fumar y botiquines, con la señalización normativa que su empresa necesita.", [
                ("ISO 7010", "Estandariza internacionalmente los símbolos gráficos de seguridad, basados en los colores y formas definidos en ISO 3864.", "ISO"),
                ("ISO 3864", "Fija el significado de los colores de seguridad: rojo (prohibición/equipo contra incendios), amarillo (advertencia), verde (condición segura/salidas) y azul (acción obligatoria).", "ISO"),
                ("OSHA 29 CFR 1910.145 / ANSI Z535", "Normas de referencia en EE. UU. para la señalización general del lugar de trabajo.", "OSHA / ANSI"),
            ],
            detalle=[
                "La señalética no es un detalle decorativo: en una emergencia real, es lo que guía a las personas hacia la salida sin dudar. Diseñamos e instalamos la señalización de rutas de evacuación, zonas de reunión, ubicación de extintores, riesgo eléctrico, prohibición de fumar y puntos de botiquín que su empresa necesita.",
                "Seguimos los colores y símbolos gráficos de seguridad estandarizados internacionalmente, para que la señalización sea reconocible tanto por su personal como por cualquier visitante.",
            ],
            incluye=[
                "Señalización de rutas de evacuación y salidas de emergencia",
                "Identificación de zonas de reunión",
                "Señalización de ubicación de extintores y equipos contra incendios",
                "Señales de riesgo eléctrico y prohibición de fumar",
                "Identificación de puntos de botiquín y primeros auxilios",
            ],
            faq=[
                ("¿Qué colores usa la señalización de seguridad?", "Rojo para prohibición y equipo contra incendios, amarillo para advertencia, verde para condición segura y salidas, y azul para acción obligatoria."),
                ("¿La señalética se adapta a normas internacionales?", "Sí, seguimos los símbolos gráficos estandarizados en ISO 7010 y los colores definidos en ISO 3864."),
                ("¿Pueden señalizar toda mi instalación de una vez?", "Sí, evaluamos la instalación completa y definimos el paquete de señalización necesario para cada área."),
            ]),
            _svc("droplets", "gabinetes-y-mangueras", "Gabinetes y mangueras para sistemas contra incendios", "Equipamiento completo para sistemas fijos contra incendios en instalaciones industriales y comerciales.", [
                ("NFPA 14", "Clasifica los sistemas de gabinetes y mangueras en Clase I (uso exclusivo de bomberos), Clase II (uso de ocupantes entrenados) y Clase III (combinada).", "NFPA"),
                ("NFPA 14", "La manguera preinstalada para uso de ocupantes (Clase II) es típicamente de 1½\" de diámetro y hasta 100 pies de longitud.", "NFPA"),
            ],
            detalle=[
                "En instalaciones industriales y comerciales de mayor tamaño, los extintores portátiles no siempre bastan: los sistemas de gabinetes y mangueras dan una capacidad de respuesta mayor y sostenida ante un incendio en desarrollo.",
                "Suministramos e instalamos el sistema según la clase que corresponda a su instalación —de uso exclusivo de bomberos, de ocupantes entrenados o combinada— y señalizamos cada punto para que sea fácil de ubicar en una emergencia.",
            ],
            incluye=[
                "Suministro de gabinetes contra incendio",
                "Mangueras preinstaladas según la clase del sistema",
                "Instalación conforme al tipo de ocupación de la instalación",
                "Señalización del punto del gabinete",
                "Recomendaciones de inspección y mantenimiento periódico",
            ],
            faq=[
                ("¿Qué diferencia hay entre un sistema Clase I, II y III?", "La Clase I es de uso exclusivo de bomberos, la Clase II está pensada para ocupantes entrenados, y la Clase III combina ambos usos."),
                ("¿Qué instalaciones necesitan gabinetes y mangueras?", "Principalmente edificaciones industriales y comerciales de mayor tamaño, según lo determine el análisis de riesgo de la instalación."),
                ("¿Requieren mantenimiento como los extintores?", "Sí, se recomienda inspección y mantenimiento periódico para garantizar que estén operativos ante una emergencia."),
            ]),
        ],
        "proceso": [
            ("clipboard-list", "Evaluación de necesidades", "Analizamos el espacio, la cantidad de personal y el nivel de riesgo de cada área."),
            ("list-checks", "Selección del equipo", "Recomendamos el tipo y la cantidad adecuados para su empresa o su hogar."),
            ("truck", "Entrega e instalación", "Suministramos e instalamos el equipo donde corresponde, con la señalización necesaria."),
            ("book-open-check", "Orientación de uso", "Explicamos el uso correcto del equipo y la reposición o el mantenimiento periódico."),
        ],
    },
]


def build_servicios():
    hero = section_hero(
        "Servicios",
        "Soluciones completas en seguridad industrial, de la asesoría a la ejecución",
        "Agrupamos nuestros servicios en cuatro áreas para que su empresa encuentre, en un mismo lugar, todo lo que necesita para prevenir, cumplir y responder ante una emergencia.",
    )

    quicknav = """  <div class="bg-white border-b border-slate-100 sticky top-20 z-40">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 py-3 flex flex-wrap gap-x-6 gap-y-2 text-sm font-semibold justify-center">
      <a href="#asesoria" class="text-ink hover:text-brandred transition">Asesoría y Consultoría</a>
      <a href="#capacitaciones" class="text-ink hover:text-brandred transition">Capacitaciones</a>
      <a href="#mantenimiento" class="text-ink hover:text-brandred transition">Mantenimiento y Taller</a>
      <a href="#equipos" class="text-ink hover:text-brandred transition">Equipos y Primeros Auxilios</a>
    </div>
  </div>"""

    category_sections = [
        category_block(
            cat["anchor"], cat["number"], cat["title"], cat["intro"], cat["items"],
            image=cat["image"], image_alt=cat["image_alt"], reverse=cat["reverse"], bg=cat["bg"],
        )
        for cat in SERVICE_CATEGORIES
    ]

    cta = cta_band(
        "¿No sabe qué necesita su empresa?",
        "Solicite una evaluación gratuita y nuestro equipo técnico le recomendará exactamente lo que su operación requiere para cumplir y estar preparada.",
        wa_label="Solicitar evaluación gratuita",
    )

    body = "\n".join([hero, quicknav] + category_sections + [cta])
    write("servicios.html", page(
        "Servicios | CEPASI — Asesoría, Capacitación, Mantenimiento y Equipos",
        "Conozca los servicios de CEPASI: asesoría y consultoría SST, capacitaciones, mantenimiento de extintores y venta de equipos de emergencia y primeros auxilios.",
        "servicios.html",
        body,
        canonical="servicios.html",
    ))


# ---------------------------------------------------------------------------
# SERVICIO (detalle individual — una página por cada uno de los 25 servicios)
# ---------------------------------------------------------------------------

def servicio_hero(category, item):
    crumbs = f"""      <nav class="text-xs text-slate-300 flex items-center gap-2 justify-center mb-6 flex-wrap">
        <a href="index.html" class="hover:text-brandorange transition">Inicio</a>
        <i data-lucide="chevron-right" class="w-3 h-3"></i>
        <a href="servicios.html" class="hover:text-brandorange transition">Servicios</a>
        <i data-lucide="chevron-right" class="w-3 h-3"></i>
        <a href="servicios.html#{category['anchor']}" class="hover:text-brandorange transition">{category['title']}</a>
        <i data-lucide="chevron-right" class="w-3 h-3"></i>
        <span class="text-white">{item['title']}</span>
      </nav>"""
    bg = category["image"] or HERO_IMG
    extra_cta_html = ""
    if item.get("extra_cta"):
        cta_label, cta_href = item["extra_cta"]
        extra_cta_html = f"""
      <a href="{cta_href}" class="clip-br bg-gradient-brand hover:brightness-105 text-white font-bold uppercase tracking-wide text-sm px-7 py-4 inline-flex items-center gap-2 transition mt-8">
        <i data-lucide="clipboard-list" class="w-5 h-5"></i> {cta_label}
      </a>"""
    return f"""  <section class="relative overflow-hidden">
    <div class="absolute inset-0">
      <img src="{bg}" alt="" class="w-full h-full object-cover">
      <div class="absolute inset-0 bg-ink/90"></div>
    </div>
    <div class="relative max-w-4xl mx-auto px-4 lg:px-8 py-16 md:py-20 text-center">
{crumbs}
      {icon_badge(item['icon'], size="w-16 h-16 mx-auto", icon_size="w-7 h-7")}
      <span class="eyebrow eyebrow-dot text-brandorange font-semibold text-xs uppercase tracking-widest mt-5 inline-block">{category['title']}</span>
      <h1 class="font-heading font-extrabold text-3xl md:text-5xl text-white mt-3 mb-5 leading-[1.1]">{item['title']}</h1>
      <p class="text-slate-200 max-w-2xl mx-auto text-base md:text-lg leading-relaxed">{item['desc']}</p>{extra_cta_html}
    </div>
  </section>"""


def servicio_contexto(category):
    return f"""  <section class="py-14 md:py-20">
    <div class="max-w-3xl mx-auto px-4 lg:px-8 text-center">
      <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Sobre esta categoría</span>
      <h2 class="font-heading font-bold text-2xl md:text-3xl text-ink mt-3 mb-5">{category['title']}</h2>
      <p class="text-slate-600 leading-relaxed">{category['intro']}</p>
    </div>
  </section>"""


def servicio_detalle_section(item):
    if not item.get("detalle"):
        return ""
    paras = "\n".join(f'      <p class="text-slate-600 leading-relaxed mb-4 last:mb-0">{p}</p>' for p in item["detalle"])
    return f"""  <section class="py-14 md:py-20 bg-beige">
    <div class="max-w-3xl mx-auto px-4 lg:px-8">
      <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">En qué consiste</span>
      <h2 class="font-heading font-bold text-2xl md:text-3xl text-ink mt-3 mb-6">{item['title']}, explicado</h2>
{paras}
    </div>
  </section>"""


def servicio_incluye_section(item):
    if not item.get("incluye"):
        return ""
    rows = "\n".join(f"""        <li class="flex gap-3">
          <i data-lucide="check" class="w-5 h-5 text-brandred shrink-0 mt-0.5"></i>
          <span class="text-slate-600 leading-relaxed">{i}</span>
        </li>""" for i in item["incluye"])
    return f"""  <section class="py-14 md:py-20">
    <div class="max-w-3xl mx-auto px-4 lg:px-8">
      <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Alcance del servicio</span>
      <h2 class="font-heading font-bold text-2xl md:text-3xl text-ink mt-3 mb-8">¿Qué incluye este servicio?</h2>
      <ul class="space-y-4">
{rows}
      </ul>
    </div>
  </section>"""


def servicio_proceso_section(category):
    steps = category.get("proceso") or []
    if not steps:
        return ""
    cards = "\n".join(f"""        <div class="bg-white rounded-sm border border-slate-100 p-6 card-lift">
          {icon_badge(icon, size="w-12 h-12", icon_size="w-5 h-5", soft=True)}
          <span class="block text-xs font-bold uppercase tracking-wide text-brandred mt-4">Paso {i}</span>
          <h3 class="font-heading font-bold text-lg text-ink mt-1 mb-2 leading-snug">{title}</h3>
          <p class="text-sm text-slate-600 leading-relaxed">{desc}</p>
        </div>""" for i, (icon, title, desc) in enumerate(steps, start=1))
    return f"""  <section class="py-14 md:py-20 bg-beige">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-10">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Nuestro proceso</span>
        <h2 class="font-heading font-bold text-2xl md:text-3xl text-ink mt-3">Cómo trabajamos</h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
{cards}
      </div>
    </div>
  </section>"""


def servicio_faq_section(item):
    if not item.get("faq"):
        return ""
    rows = "\n".join(f"""        <details class="group bg-white rounded-sm border border-slate-100 p-5 card-lift">
          <summary class="flex items-center justify-between gap-4 cursor-pointer font-heading font-semibold text-ink list-none">
            {q}
            <i data-lucide="plus" class="w-4 h-4 text-brandred shrink-0 group-open:hidden"></i>
            <i data-lucide="minus" class="w-4 h-4 text-brandred shrink-0 hidden group-open:block"></i>
          </summary>
          <p class="text-sm text-slate-600 leading-relaxed mt-3">{a}</p>
        </details>""" for q, a in item["faq"])
    return f"""  <section class="py-14 md:py-20">
    <div class="max-w-3xl mx-auto px-4 lg:px-8">
      <div class="text-center mb-10">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Dudas frecuentes</span>
        <h2 class="font-heading font-bold text-2xl md:text-3xl text-ink mt-3">Preguntas frecuentes</h2>
      </div>
      <div class="space-y-4">
{rows}
      </div>
    </div>
  </section>"""


def servicio_json_ld(category, item):
    """JSON-LD combinado (Service + BreadcrumbList + FAQPage si aplica) para
    la página de detalle de un servicio — ayuda tanto al SEO tradicional
    (rich results de Google) como a motores de respuesta con IA (GEO), que
    citan directamente el contenido estructurado de preguntas y respuestas."""
    canonical_url = BASE_URL + f"servicio-{item['slug']}.html"
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": item["title"],
        "name": item["title"],
        "description": item["desc"],
        "provider": {"@type": "ProfessionalService", "name": "CEPASI"},
        "areaServed": "República Dominicana",
        "url": canonical_url,
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE_URL + "index.html"},
            {"@type": "ListItem", "position": 2, "name": "Servicios", "item": BASE_URL + "servicios.html"},
            {"@type": "ListItem", "position": 3, "name": category["title"], "item": BASE_URL + f"servicios.html#{category['anchor']}"},
            {"@type": "ListItem", "position": 4, "name": item["title"], "item": canonical_url},
        ],
    }
    blocks = [service, breadcrumb]
    if item.get("faq"):
        blocks.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in item["faq"]
            ],
        })
    return "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)


def servicio_normativa(item):
    if not item.get("estandares"):
        return ""
    rows = "\n".join(f"""        <div class="flex gap-4">
          <i data-lucide="check-circle-2" class="w-5 h-5 text-brandorange shrink-0 mt-0.5"></i>
          <p class="text-slate-200 leading-relaxed text-sm"><span class="font-heading font-semibold text-white">{norma}:</span> {dato} <span class="text-slate-400">({fuente})</span></p>
        </div>""" for norma, dato, fuente in item["estandares"])
    return f"""  <section class="py-14 md:py-20 bg-navy text-white">
    <div class="max-w-3xl mx-auto px-4 lg:px-8">
      <span class="eyebrow eyebrow-dot text-brandorange font-semibold text-xs uppercase tracking-widest">Normativa y estándares de referencia</span>
      <h2 class="font-heading font-bold text-2xl md:text-3xl mt-3 mb-8">Buenas prácticas reconocidas internacionalmente</h2>
      <div class="space-y-5">
{rows}
      </div>
      <p class="text-xs text-slate-400 mt-8 leading-relaxed">Referencias informativas de organismos técnicos y normativos externos (NFPA, OSHA, ISO, ANSI, OIT, Ministerio de Trabajo de la República Dominicana, entre otros), investigadas y verificadas para orientar las mejores prácticas del sector. No implican certificación de CEPASI por dichos organismos.</p>
    </div>
  </section>"""


def servicio_relacionados(category, current_slug):
    others = [it for it in category["items"] if it["slug"] != current_slug]
    if not others:
        return ""
    cards = "\n".join(service_item(it["icon"], it["slug"], it["title"], it["desc"]) for it in others)
    return f"""  <section class="py-14 md:py-20 bg-beige">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-10">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">También en {category['title']}</span>
        <h2 class="font-heading font-bold text-2xl md:text-3xl text-ink mt-3">Otros servicios de esta categoría</h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{cards}
      </div>
      <div class="text-center mt-10">
        <a href="servicios.html#{category['anchor']}" class="inline-flex items-center gap-2 text-ink font-bold uppercase tracking-wide text-sm hover:text-brandred transition">Ver todos los servicios <i data-lucide="arrow-right" class="w-4 h-4"></i></a>
      </div>
    </div>
  </section>"""


def build_servicio_detalle(category, item):
    hero = servicio_hero(category, item)
    contexto = servicio_contexto(category)
    detalle = servicio_detalle_section(item)
    incluye = servicio_incluye_section(item)
    proceso = servicio_proceso_section(category)
    normativa = servicio_normativa(item)
    faq = servicio_faq_section(item)
    relacionados = servicio_relacionados(category, item["slug"])
    cta = cta_band(
        "¿Le interesa este servicio?",
        "Cuéntenos sobre su empresa y nuestro equipo técnico le explicará cómo aplicarlo a su caso, sin compromiso.",
        wa_label="Consultar por WhatsApp",
        wa_link=wa_link_for(f"Hola, quisiera más información sobre el servicio de {item['title']}."),
    )
    body = "\n".join([hero, contexto, detalle, incluye, proceso, normativa, faq, relacionados, cta])
    write(f"servicio-{item['slug']}.html", page(
        f"{item['title']} | CEPASI República Dominicana",
        item["desc"],
        "servicios.html",
        body,
        canonical=f"servicio-{item['slug']}.html",
        og_image=category["image"] or HERO_IMG,
        json_ld=servicio_json_ld(category, item),
    ))


def build_servicios_detalle():
    for category in SERVICE_CATEGORIES:
        for item in category["items"]:
            build_servicio_detalle(category, item)


# ---------------------------------------------------------------------------
# PROYECTOS
# ---------------------------------------------------------------------------

def build_proyectos():
    hero = section_hero(
        "Proyectos",
        "Empresas que ya confían en CEPASI",
        "Cada proyecto es distinto: el riesgo de una planta industrial no es el de una torre de oficinas ni el de un colegio. Estos son algunos ejemplos del tipo de trabajo que realizamos.",
    )

    note = """  <div class="max-w-4xl mx-auto px-4 lg:px-8 -mt-6 relative z-10">
    <div class="bg-amber-50 border border-amber-200 text-amber-800 text-sm rounded-xl p-4 flex gap-3">
      <i data-lucide="info" class="w-5 h-5 shrink-0 mt-0.5"></i>
      <p><span class="font-semibold">Nota para el cliente:</span> los tres proyectos a continuación son ejemplos de estructura (placeholder). Deben sustituirse por casos reales de CEPASI, con autorización del cliente para usar su nombre, logo y fotos. Edite <code class="bg-amber-100 px-1 rounded">assets/js/proyectos-data.js</code> para reemplazarlos — no requiere tocar el HTML.</p>
    </div>
  </div>"""

    filters = """  <div class="max-w-7xl mx-auto px-4 lg:px-8 pt-10 flex flex-wrap gap-3 justify-center">
    <button data-filter="todos" class="bg-gradient-brand text-white text-sm font-bold uppercase tracking-wide px-5 py-2 rounded-full transition">Todos</button>
    <button data-filter="industrial" class="bg-white text-ink text-sm font-bold uppercase tracking-wide px-5 py-2 rounded-full border border-slate-200 transition">Industrial</button>
    <button data-filter="corporativo" class="bg-white text-ink text-sm font-bold uppercase tracking-wide px-5 py-2 rounded-full border border-slate-200 transition">Corporativo / Oficinas</button>
    <button data-filter="mantenimiento" class="bg-white text-ink text-sm font-bold uppercase tracking-wide px-5 py-2 rounded-full border border-slate-200 transition">Mantenimiento</button>
  </div>"""

    grid = """  <section class="py-10 md:py-16">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div id="proyectos-grid" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8"></div>
    </div>
  </section>"""

    cta = cta_band(
        "¿Quiere que su empresa sea el próximo caso de éxito?",
        "Solicite una evaluación gratuita y descubra qué necesita su operación para prevenir, cumplir y responder ante una emergencia.",
        wa_label="Solicitar evaluación",
    )

    body = "\n".join([hero, note, filters, grid, cta])
    write("proyectos.html", page(
        "Proyectos | CEPASI — Casos de seguridad industrial en R.D.",
        "Ejemplos del tipo de proyectos que CEPASI realiza en seguridad industrial, salud ocupacional y mantenimiento contra incendios en República Dominicana.",
        "proyectos.html",
        body,
        page_scripts='  <script src="assets/js/proyectos-data.js"></script>',
        canonical="proyectos.html",
    ))


# ---------------------------------------------------------------------------
# BLOG
# ---------------------------------------------------------------------------

def build_blog():
    hero = section_hero(
        "Blog",
        "Prevención, en palabras simples",
        "Compartimos guías prácticas, actualizaciones normativas y consejos de seguridad industrial para que la prevención llegue más allá de nuestros clientes directos.",
    )

    note = """  <div class="max-w-4xl mx-auto px-4 lg:px-8 -mt-6 relative z-10">
    <div class="bg-amber-50 border border-amber-200 text-amber-800 text-sm rounded-xl p-4 flex gap-3">
      <i data-lucide="info" class="w-5 h-5 shrink-0 mt-0.5"></i>
      <p><span class="font-semibold">Nota para el cliente:</span> los tres artículos a continuación son ejemplos de título y resumen (placeholder), pensados para orientar el tono y los temas del blog. El contenido completo debe ser redactado y publicado más adelante en <code class="bg-amber-100 px-1 rounded">assets/js/blog-data.js</code>.</p>
    </div>
  </div>"""

    grid = """  <section class="py-10 md:py-16">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div id="blog-grid" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8"></div>
    </div>
  </section>"""

    newsletter = f"""  <section class="py-16 bg-navy">
    <div class="max-w-2xl mx-auto px-4 lg:px-8 text-center text-white">
      {icon_badge("mail", size="w-14 h-14 mx-auto", icon_size="w-6 h-6")}
      <h2 class="font-heading font-bold text-3xl mt-5 mb-3">Suscribirse para recibir nuevos artículos</h2>
      <p class="text-slate-300 mb-6">Reciba nuestras guías de prevención y actualizaciones normativas apenas se publiquen.</p>
      <form id="newsletter-form" class="flex flex-col sm:flex-row gap-3">
        <input type="email" required placeholder="Su correo electrónico" class="flex-1 rounded-sm px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brandorange">
        <button type="submit" class="btn-lime px-7 py-3 uppercase tracking-wide text-sm">Suscribirme</button>
      </form>
      <p id="newsletter-feedback" class="hidden mt-4 text-sm text-brandorange font-medium"></p>
    </div>
  </section>"""

    body = "\n".join([hero, note, grid, newsletter])
    write("blog.html", page(
        "Blog | CEPASI — Guías de seguridad industrial y prevención",
        "Guías prácticas, actualizaciones normativas y consejos de seguridad industrial y primeros auxilios para empresas dominicanas.",
        "blog.html",
        body,
        page_scripts='  <script src="assets/js/blog-data.js"></script>',
        canonical="blog.html",
    ))


# ---------------------------------------------------------------------------
# FORMULARIO PSST (informaciones para el Programa/Manual de Seguridad y
# Salud en el Trabajo — mismos campos que el documento interno que el
# cliente usa hoy para recopilar esta información por correo).
# ---------------------------------------------------------------------------

def _f_input(name, label, kind="text", span=1, placeholder="", group=""):
    return f"""        <div class="sm:col-span-{span}">
          <label class="block text-sm font-medium text-ink mb-1.5">{label}</label>
          <input type="{kind}" name="{name}" data-label="{label}" placeholder="{placeholder}" class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange">
        </div>"""


def _f_textarea(name, label, span=2, rows=3, placeholder="", group=""):
    return f"""        <div class="sm:col-span-{span}">
          <label class="block text-sm font-medium text-ink mb-1.5">{label}</label>
          <textarea name="{name}" data-label="{label}" rows="{rows}" placeholder="{placeholder}" class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange"></textarea>
        </div>"""


def _f_file(name, label, multiple=False, accept="", span=1, hint=""):
    hint_html = f'<p class="text-xs text-slate-400 mt-1">{hint}</p>' if hint else ""
    return f"""        <div class="sm:col-span-{span}">
          <label class="block text-sm font-medium text-ink mb-1.5">{label}</label>
          <label data-file-drop class="flex flex-col items-center justify-center gap-1.5 border-2 border-dashed border-slate-300 rounded-sm px-4 py-6 text-center cursor-pointer hover:border-brandorange transition">
            <i data-lucide="upload" class="w-5 h-5 text-slate-400"></i>
            <span class="text-sm text-slate-500">Haga clic o arrastre {"los archivos" if multiple else "el archivo"} aquí</span>
            <input type="file" name="{name}" data-label="{label}" data-file-input {"multiple" if multiple else ""} accept="{accept}" class="hidden">
          </label>
          <div data-file-list class="mt-2 space-y-1.5"></div>
          {hint_html}
        </div>"""


def _f_group(title, fields_html):
    return f"""      <fieldset data-group="{title}" class="border-t border-slate-100 pt-8 mt-8 first:border-0 first:mt-0 first:pt-0">
        <legend class="font-heading font-bold text-lg text-ink mb-5 px-0">{title}</legend>
        <div class="grid sm:grid-cols-2 gap-5">
{fields_html}
        </div>
      </fieldset>"""


def build_formulario_psst():
    hero = section_hero(
        "Programa de Seguridad y Salud en el Trabajo",
        "Formulario de informaciones para su Manual de SST",
        "Complete estos datos para que nuestro equipo pueda elaborar el Manual de Seguridad y Salud en el Trabajo de su empresa, en conformidad con el Reglamento 522-06. Al final, el formulario generará un correo con toda esta información lista para enviarnos.",
    )

    identidad = f"""  <section class="bg-beige">
    <div class="max-w-4xl mx-auto px-4 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-center gap-6 sm:gap-10 text-center sm:text-left">
      <div class="flex items-center gap-3">
        {icon_badge("map-pin", size="w-11 h-11", icon_size="w-5 h-5", soft=True)}
        <div>
          <p class="text-xs uppercase tracking-wide text-slate-500">Estas informaciones serán procesadas por</p>
          <p class="font-heading font-bold text-ink">CEPASI — {ADDRESS}</p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        {icon_badge("phone", size="w-11 h-11", icon_size="w-5 h-5", soft=True)}
        <div>
          <p class="text-xs uppercase tracking-wide text-slate-500">Teléfono / WhatsApp</p>
          <p class="font-heading font-bold text-ink">{PHONE_1} · {PHONE_2}</p>
        </div>
      </div>
    </div>
  </section>"""

    grupo_general = _f_group("Datos generales de la empresa", "\n".join([
        _f_input("nombre_empresa", "Nombre de la empresa"),
        _f_input("razon_social", "Razón social de la empresa"),
        _f_input("rnc", "RNC"),
        _f_input("rnl", "RNL"),
        _f_input("actividad_economica", "Actividad económica de la empresa"),
        _f_input("fecha_fundacion", "Fecha de fundación de la empresa", placeholder="dd/mm/aaaa"),
        _f_input("direccion_empresa", "Dirección de la empresa", span=2),
        _f_input("telefono_empresa", "Teléfono", kind="tel"),
        _f_input("correo_empresa", "Dirección de correo electrónico", kind="email"),
        _f_input("horario_operativo", "Horario de trabajo operativo"),
        _f_input("horario_administrativo", "Horario de trabajo administrativo"),
    ]))

    grupo_personal = _f_group("Personal de la empresa", "\n".join([
        _f_input("cantidad_empleados", "Cantidad de empleados de la empresa", kind="number"),
        _f_input("empleados_masculino", "Cantidad de empleados — masculino", kind="number"),
        _f_input("empleados_femenino", "Cantidad de empleados — femenino", kind="number"),
        _f_input("admin_masculino", "Personal administrativo — masculino", kind="number"),
        _f_input("admin_femenino", "Personal administrativo — femenino", kind="number"),
        _f_input("operativo_masculino", "Personal operativo — masculino", kind="number"),
        _f_input("operativo_femenino", "Personal operativo — femenino", kind="number"),
    ]))

    grupo_responsables = _f_group("Responsables y representantes (nombre y cédula)", "\n".join([
        _f_input("gerente_general", "Gerente General"),
        _f_input("coordinador_sst", "Coordinador de Seguridad y Salud en el Trabajo"),
        _f_input("representante_propietario", "Representante o propietario de la empresa"),
        _f_input("aplicador_comite", "Aplicador que formará parte del Comité de SST"),
        _f_input("encargado_programa", "Encargado del programa de SST (nombre, apellido y cédula)", span=2),
    ]))

    grupo_empresa = _f_group("Sobre la empresa", "\n".join([
        _f_textarea("descripcion_empresa", "Descripción o reseña de la empresa"),
        _f_textarea("mision_vision_valores", "Misión, visión y valores"),
    ]))

    grupo_inventario = _f_group("Inventario y equipamiento", "\n".join([
        _f_textarea("listado_vehiculos", "Listado de vehículos (marca, modelo, año y cantidad)"),
        _f_textarea("listado_herramientas", "Listado de herramientas de trabajo (marca, modelo y cantidad)"),
        _f_textarea("listado_epp", "Listado de equipos de protección personal (marca y modelo)"),
        _f_textarea("productos_quimicos", "Nombre de los productos químicos que utilizan"),
        _f_textarea("listado_maquinas", "Listado de máquinas y equipos —marca y modelo— (si aplica)"),
        _f_textarea("listado_puestos", "Listado de puestos de trabajo administrativos y operativos"),
    ]))

    archivos_html = "\n".join([
        _f_file("logo_empresa", "Logo de la empresa", accept="image/*"),
        _f_file("organigrama", "Organigrama de la empresa", accept="image/*,.pdf"),
        _f_file("ficha_quimicos", "Ficha técnica de los productos químicos", multiple=True, accept="image/*,.pdf"),
        _f_file("plano_piso", "Plano por piso, en PDF", accept=".pdf"),
        _f_file("fotos_equipos", "Fotos de los equipos utilizados para el trabajo o servicio", multiple=True, accept="image/*"),
        _f_file("fotos_epp", "Fotos de los equipos de protección personal", multiple=True, accept="image/*"),
        _f_file("fotos_vehiculos", "Fotos de los vehículos", multiple=True, accept="image/*"),
        _f_file("fotos_herramientas", "Fotos de las herramientas", multiple=True, accept="image/*"),
        _f_input("ubicacion_geografica", "Ubicación geográfica (enlace de Google Maps)", span=2, placeholder="También puede enviárnosla por WhatsApp"),
    ])
    grupo_adjuntos = f"""      <fieldset data-group="Documentos y fotos" class="border-t border-slate-100 pt-8 mt-8">
        <legend class="font-heading font-bold text-lg text-ink mb-2 px-0">Documentos y fotos</legend>
        <p class="text-sm text-slate-600 mb-5">Adjunte aquí el logo, el organigrama, las fichas técnicas, el plano y las fotos. Puede seleccionar varios archivos por categoría.</p>
        <div class="grid sm:grid-cols-2 gap-5">
{archivos_html}
        </div>
        <p id="psst-file-total" class="text-xs text-slate-500 mt-5">Total seleccionado: 0 MB</p>
      </fieldset>"""

    grupo_notas = _f_group("Observaciones adicionales", _f_textarea("notas", "¿Algo más que debamos saber?", rows=4))

    form_section = f"""  <section class="py-16 md:py-24">
    <div class="max-w-4xl mx-auto px-4 lg:px-8">
      <form id="psst-form">
{grupo_general}
{grupo_personal}
{grupo_responsables}
{grupo_empresa}
{grupo_inventario}
{grupo_adjuntos}
{grupo_notas}
        <div class="mt-10 border-t border-slate-100 pt-8">
          <button type="submit" class="clip-br bg-gradient-brand hover:brightness-105 text-white font-bold uppercase tracking-wide text-sm px-7 py-4 inline-flex items-center gap-2 transition">
            <i data-lucide="send" class="w-4 h-4"></i> Enviar informaciones a CEPASI
          </button>
          <p id="psst-help" class="text-xs text-slate-500 mt-3">Se enviará junto con los archivos adjuntados arriba a {EMAIL}.</p>
          <p id="psst-feedback" class="hidden mt-4 text-sm text-ink bg-beige rounded-sm p-3"></p>
        </div>
      </form>
    </div>
  </section>"""

    body = "\n".join([hero, identidad, form_section])
    write("formulario-psst.html", page(
        "Formulario PSST | CEPASI — Informaciones para su Manual de SST",
        "Complete este formulario con las informaciones que CEPASI necesita para elaborar el Manual de Seguridad y Salud en el Trabajo (SST) de su empresa.",
        "servicios.html",
        body,
        page_scripts=f'  <script>window.PSST_UPLOAD_ENDPOINT = "{PSST_UPLOAD_ENDPOINT}";</script>',
        canonical="formulario-psst.html",
    ))


# ---------------------------------------------------------------------------
# CONTACTO
# ---------------------------------------------------------------------------

def build_contacto():
    hero = section_hero(
        "Contacto",
        "Hablemos de la seguridad de su empresa",
        "Ya sea que necesite una asesoría inicial, una capacitación para su equipo o el mantenimiento de sus extintores, nuestro equipo está listo para atenderle.",
    )

    servicio_options = [
        "Asesoría y consultoría",
        "Capacitaciones",
        "Mantenimiento de extintores",
        "Equipos y señalética",
        "Otro",
    ]
    options_html = "\n            ".join(f'<option value="{o}">{o}</option>' for o in servicio_options)

    form_section = f"""  <section class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 lg:px-8 grid lg:grid-cols-5 gap-12">
      <div class="lg:col-span-3">
        <span class="eyebrow eyebrow-dot text-brandred font-semibold text-xs uppercase tracking-widest">Escríbanos</span>
        <h2 class="font-heading font-bold text-3xl md:text-4xl text-ink mt-3 mb-4">Cuéntenos qué necesita</h2>
        <p class="text-slate-600 leading-relaxed mb-8 max-w-xl">Cuéntenos brevemente qué necesita —una evaluación de riesgo, una capacitación, mantenimiento de equipos o una cotización— y le responderemos a la brevedad. También puede escribirnos directamente por WhatsApp para una atención más rápida.</p>

        <form id="contact-form" class="grid sm:grid-cols-2 gap-5">
          <div class="sm:col-span-1">
            <label class="block text-sm font-medium text-ink mb-1.5">Nombre completo</label>
            <input type="text" name="nombre" required class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange">
          </div>
          <div class="sm:col-span-1">
            <label class="block text-sm font-medium text-ink mb-1.5">Empresa (opcional)</label>
            <input type="text" name="empresa" class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange">
          </div>
          <div class="sm:col-span-1">
            <label class="block text-sm font-medium text-ink mb-1.5">Teléfono</label>
            <input type="tel" name="telefono" required class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange">
          </div>
          <div class="sm:col-span-1">
            <label class="block text-sm font-medium text-ink mb-1.5">Correo electrónico</label>
            <input type="email" name="correo" class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange">
          </div>
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-ink mb-1.5">¿Qué servicio le interesa?</label>
            <select name="servicio" class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange">
            {options_html}
            </select>
          </div>
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-ink mb-1.5">Mensaje</label>
            <textarea name="mensaje" rows="4" required class="w-full rounded-sm border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brandorange"></textarea>
          </div>
          <div class="sm:col-span-2">
            <button type="submit" class="clip-br bg-gradient-brand hover:brightness-105 text-white font-bold uppercase tracking-wide text-sm px-7 py-4 inline-flex items-center gap-2 transition">
              <i data-lucide="send" class="w-4 h-4"></i> Enviar mensaje
            </button>
            <p id="form-feedback" class="hidden mt-4 text-sm text-ink bg-beige rounded-sm p-3"></p>
          </div>
        </form>
      </div>

      <div class="lg:col-span-2">
        <div class="bg-ink text-white rounded-sm p-8">
          <h3 class="font-heading font-bold text-2xl mb-6">CEPASI</h3>
          <p class="text-xs text-slate-300 mb-6 uppercase tracking-wide">Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial, S.R.L.</p>
          <ul class="space-y-4 text-sm mb-8">
            <li class="flex items-start gap-3"><i data-lucide="map-pin" class="w-5 h-5 text-brandorange mt-0.5 shrink-0"></i>{ADDRESS}</li>
            <li class="flex items-center gap-3"><i data-lucide="phone" class="w-5 h-5 text-brandorange shrink-0"></i>{PHONE_1} · {PHONE_2}</li>
            <li class="flex items-center gap-3"><i data-lucide="mail" class="w-5 h-5 text-brandorange shrink-0"></i>{EMAIL}</li>
          </ul>
          <div class="flex flex-col sm:flex-row gap-3">
            <a href="{WA_LINK}" target="_blank" rel="noopener" class="flex-1 clip-br bg-gradient-brand hover:brightness-105 text-white font-bold uppercase tracking-wide text-sm px-5 py-3.5 inline-flex items-center justify-center gap-2 transition">
              <i data-lucide="message-circle" class="w-4 h-4"></i> WhatsApp
            </a>
            <a href="tel:+1{PHONE_1_TEL}" class="flex-1 inline-flex items-center justify-center gap-2 border-2 border-white/70 text-white font-bold uppercase tracking-wide text-sm px-5 py-3.5 hover:bg-white/10 transition">
              <i data-lucide="phone" class="w-4 h-4"></i> Llamar
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>"""

    mapa = f"""  <section id="mapa" class="pb-16 md:pb-24">
    <div class="max-w-7xl mx-auto px-4 lg:px-8">
      <div class="clip-tr overflow-hidden shadow-lg border border-slate-100">
        <iframe class="map-frame w-full h-[420px]" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q={ADDRESS.replace(' ', '+').replace(',', '%2C')}&output=embed">
        </iframe>
      </div>
    </div>
  </section>"""

    closing = """  <section class="bg-ink">
    <div class="max-w-4xl mx-auto px-4 lg:px-8 py-12 text-center text-slate-200">
      <p class="text-lg leading-relaxed">La seguridad de su empresa no puede esperar a la próxima emergencia. Contáctenos hoy y demos el primer paso hacia un entorno más seguro y conforme a la ley.</p>
    </div>
  </section>"""

    body = "\n".join([hero, form_section, mapa, closing])
    write("contacto.html", page(
        "Contacto | CEPASI — Seguridad Industrial y Salud Ocupacional",
        "Contacte a CEPASI para una evaluación gratuita: asesoría, capacitación, mantenimiento de extintores y equipos de emergencia en Santo Domingo, R.D.",
        "contacto.html",
        body,
        canonical="contacto.html",
    ))


def build_sitemap():
    urls = [
        ("index.html", "1.0"),
        ("nosotros.html", "0.8"),
        ("servicios.html", "0.9"),
        ("proyectos.html", "0.6"),
        ("blog.html", "0.6"),
        ("contacto.html", "0.8"),
        ("formulario-psst.html", "0.4"),
    ]
    for category in SERVICE_CATEGORIES:
        for item in category["items"]:
            urls.append((f"servicio-{item['slug']}.html", "0.5"))

    entries = "\n".join(
        f'  <url><loc>https://www.cepasird.com/{path}</loc><priority>{priority}</priority></url>'
        for path, priority in urls
    )
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
    write("sitemap.xml", content)


if __name__ == "__main__":
    os.makedirs(ROOT, exist_ok=True)
    build_index()
    build_nosotros()
    build_servicios()
    build_servicios_detalle()
    build_proyectos()
    build_blog()
    build_formulario_psst()
    build_contacto()
    build_sitemap()
    print("DONE")
