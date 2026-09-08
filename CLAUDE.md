# CEPASI — Sitio web MVP

Contexto de proyecto para Claude Code. Léelo antes de tocar el sitio.

## Qué es esto

MVP del sitio web de **CEPASI** (Cuerpo de Evacuación, Primeros Auxilios y
Seguridad Industrial, S.R.L.), empresa dominicana de seguridad industrial y
salud ocupacional (B2B, Reglamento 522‑06 como eje de cumplimiento).

- **Repo:** https://github.com/erickherndza/cepas
- **Sitio en vivo (para compartir con el cliente):** https://erickherndza.github.io/cepas/
- **Deploy:** GitHub Pages sirve directo la rama `main`, carpeta raíz. Cada
  `git push` a `main` republica el sitio en 1–2 minutos. No hay CI ni build
  step — lo que está en `main` es exactamente lo que se sirve.

## Stack

HTML5 estático + Tailwind CSS (vía CDN, `tailwind.config` inline en cada
`<head>`) + JavaScript vanilla. Sin backend, sin framework, sin npm. Así lo
pidió el brief explícitamente: "fácil de desplegar y de mantener por el
cliente". No introduzcas un build step (Vite/Webpack/etc.) ni un framework
salvo que el cliente lo pida de forma explícita.

## Cómo editar el sitio

Las 6 páginas principales (`index.html`, `nosotros.html`, `servicios.html`,
`proyectos.html`, `blog.html`, `contacto.html`), más las **25 páginas de
detalle de servicio** (`servicio-<slug>.html`) y `formulario-psst.html`,
comparten header, topbar, footer y varios bloques (`section_hero`,
`cta_band`, `feature_list_section`, `category_block`, tarjetas de ícono,
etc.). **Ningún `.html` se edita a mano de forma independiente** — todos
los genera `tools/build.py`, que arma cada página a partir de esas
funciones/plantillas en Python.

**Regla de oro:** si el cambio toca algo que aparece en más de una página
(header, footer, nav, botón de WhatsApp, paleta, tipografía, un patrón de
sección reutilizado), edítalo en `tools/build.py`, no en los `.html`
directamente — si no, las páginas se desincronizan. Para cambios que solo
viven en una página (un párrafo específico de Nosotros, por ejemplo)
también se edita en `tools/build.py`, dentro de la función `build_*()`
correspondiente, y luego se regenera:

```bash
python3 tools/build.py   # reescribe TODOS los .html + sitemap.xml en la raíz
```

El script no tiene dependencias externas (solo `os`/`urllib.parse` de la
librería estándar) y calcula la ruta de salida solo — corre igual desde
cualquier directorio. También regenera `sitemap.xml` (incluye las 25
páginas de servicio automáticamente).

**Excepción — Proyectos y Blog:** esas dos páginas NO se editan en
`build.py` para agregar contenido real. Sus tarjetas se renderizan en el
navegador vía JS desde arreglos de datos:
- `assets/js/proyectos-data.js` → array `PROYECTOS`
- `assets/js/blog-data.js` → array `ARTICULOS`

Para agregar un proyecto o artículo real, se edita solo ese archivo
(agregar un objeto al array) — no requiere tocar HTML ni volver a correr
`build.py`. Los 3 registros actuales en cada uno son placeholders
explícitamente marcados como ejemplo (con nota visible en la página).

### Servicios y sus páginas de detalle

Los 25 servicios (agrupados en 4 categorías) viven en una sola estructura
de datos, `SERVICE_CATEGORIES` en `tools/build.py`, construida con el
helper `_svc(icon, slug, title, desc, estandares=None, extra_cta=None)`.
De ahí se generan tanto las tarjetas de `servicios.html` como cada
`servicio-<slug>.html` (`build_servicios_detalle()`) — **nunca dupliques
un servicio a mano en dos sitios**, todo sale de esa misma lista.

- `estandares`: lista de tuplas `(norma_u_organismo, dato, fuente)` que
  alimenta la sección "Normativa y estándares de referencia" (fondo
  `navy`) de cada página de detalle. Estos datos fueron investigados y
  cotejados contra fuentes reales (NFPA, OSHA, ISO, ANSI/ISEA, AHA/ILCOR,
  OIT, ONU-GHS, UL, NORDOM/INDOCAL, Reglamento 522-06) — **no inventar ni
  agregar un dato nuevo sin verificarlo en al menos una fuente confiable**
  (misma disciplina que `CEPASI_copy_website.md`). Se redactan como
  referencias externas informativas, nunca como "CEPASI está certificada
  por X" — la sección lleva un descargo explícito para eso.
- `extra_cta`: tupla opcional `(label, href)` para un botón extra en el
  hero de esa página de detalle. Hoy solo lo usa `manual-sst`, que enlaza
  a `formulario-psst.html`.

### Formulario PSST (`formulario-psst.html`)

Recolecta las informaciones que CEPASI necesita para elaborar el Manual
de Seguridad y Salud en el Trabajo de un cliente (mismos campos que su
documento interno "Informaciones para el PSST"). Se construye con los
helpers `_f_input` / `_f_textarea` / `_f_file` / `_f_group` — agregar o
quitar un campo es editar la lista correspondiente dentro de
`build_formulario_psst()` y volver a correr `build.py`; no hace falta
tocar `main.js` (el JS recorre los campos por `data-group`/`data-label`).

Los campos de archivo (`_f_file`) son recuadros reales de
arrastrar-y-soltar (logo, organigrama, fichas técnicas, plano en PDF,
fotos por categoría) con lista de seleccionados, opción de quitar uno a
uno y un total en MB (`initPsstFileDropzones` / `updatePsstFileTotal` en
`main.js`).

**Envío — pendiente de conectar backend:** el sitio sigue siendo estático
(sin servidor propio), así que un adjunto real solo puede viajar si algo
del lado servidor lo reenvía por correo. La constante
`PSST_UPLOAD_ENDPOINT` en `tools/build.py` (vacía hoy) está pensada para
la URL de un Google Apps Script Web App desplegado sobre la propia cuenta
de Gmail de CEPASI (`cuerpodeevacuacion01@gmail.com`) — gratis, sin
depender de un tercero, hasta ~50 MB de payload. En cuanto se despliegue
y se pegue esa URL en la constante (y se corra `build.py`), el formulario
empieza a enviar los archivos de verdad vía `fetch`/`FormData`
(`assets/js/main.js`, handler de `#psst-form`). Mientras `PSST_UPLOAD_ENDPOINT`
esté vacía, el formulario cae de vuelta a `mailto:` (como el resto del
sitio) y lista los nombres de los archivos elegidos en el cuerpo del
correo, para que el cliente los adjunte manualmente.

## Estructura

```
index.html, nosotros.html, servicios.html,   ← generados por tools/build.py
proyectos.html, blog.html, contacto.html
servicio-<slug>.html (× 25)                   ← generados por build_servicios_detalle()
formulario-psst.html                          ← generado por build_formulario_psst()
sitemap.xml                                   ← generado por build_sitemap() (incluye los 25 servicios)
tools/build.py                                ← generador (fuente de verdad de TODO el HTML)
assets/css/theme.css                          ← color, degradados, botones, tarjetas, íconos, animaciones
assets/css/typography.css                     ← fuentes, títulos en mayúsculas, eyebrow, nav activo
assets/css/responsive.css                     ← ajustes específicos de pantallas pequeñas
assets/js/nav.js                              ← menú móvil, sombra del header, init de íconos lucide
assets/js/slider.js                           ← slider del hero de Inicio (autoplay/flechas/puntos)
assets/js/main.js                             ← formularios (contacto, PSST), filtro de proyectos, render de datos
assets/js/proyectos-data.js                   ← contenido editable de Proyectos
assets/js/blog-data.js                        ← contenido editable de Blog
assets/img/                                   ← fotos reales optimizadas para web (ver abajo)
imagenes/                                     ← material original del cliente (fuente, sin optimizar)
logo-cepasi.png / logo_cepasi.png             ← logo real recortado de los flyers del cliente
CEPASI_MVP_brief.md, _1, _2                   ← briefs recibidos, en orden cronológico (_2 es el vigente)
CEPASI_copy_website.md                        ← fuente de verdad de TODO el copy — no inventar texto
```

## Sistema visual (vigente: brief `_2`, estilo "Firegard")

- **Colores:** degradado de marca rojo→naranja `#E63C24` → `#F79433`
  (`.bg-gradient-brand` / `.text-gradient`), fondo oscuro `#1A1A1A` (`ink`)
  en topbar/footer/bandas de cierre, verde lima `#CBE24B` como acento
  puntual (úsalo con moderación — ya se usa en el botón de suscripción del
  blog), azul institucional `#1F3B57` (`navy`) reservado para bloques de
  Nosotros / cumplimiento 522‑06, beige `#F5F3EF` para fondos de sección
  alternos.
- **Tipografía:** títulos en **Barlow Condensed** bold, en mayúsculas
  automáticas vía CSS (`h1–h4, .font-heading { text-transform: uppercase }`
  en `typography.css` — no hace falta escribir el texto en mayúsculas en
  `build.py`). Cuerpo en Inter.
- **Elemento distintivo — esquina cortada:** `.clip-tr` (corta la esquina
  superior derecha, para fotos/tarjetas de imagen) y `.clip-br` (corta la
  inferior derecha, para botones). Es EL detalle que define el look
  "Firegard" — consérvalo en cualquier tarjeta o botón nuevo que se agregue.
- **Íconos:** círculos `.icon-badge` (degradado rojo-naranja, para
  secciones destacadas) o `.icon-badge-soft` (gris claro + naranja, para
  listas densas como los 25 servicios). Librería: Lucide vía CDN
  (`data-lucide="nombre-en-kebab-case"` + `lucide.createIcons()` en
  `nav.js`). **Antes de usar un ícono nuevo, verifica que exista** — Lucide
  quitó los íconos de marca (`facebook`, `instagram` no existen: hay SVG
  inline a mano en `build.py`, funciones `icon_facebook()`/`icon_instagram()`)
  y renombró algunos (`home` → `house`).

## Decisiones y adaptaciones deliberadas (no son bugs, no "corregir" sin preguntar)

- **Logo real, no genérico:** el brief `_2` describía un ícono circular
  genérico (casco/escudo). Se optó por mantener el **logo real de CEPASI**
  (encontrado dentro de flyers en `imagenes/`, recortado en círculo) porque
  ya es un activo de marca aprobado — más fiel que inventar uno nuevo.
- **Sin barra de promo lima superior:** el brief la marcaba como opcional;
  se omitió para no alargar el header en 3 niveles.
- **Sin testimonios inventados:** el brief prohíbe explícitamente citas
  ficticias atribuidas a personas. No hay sección de testimonios.
- **Slider del hero (Inicio) reutiliza solo copy ya aprobado** de
  `CEPASI_copy_website.md` (headline principal + los resúmenes de
  Capacitaciones y Equipos de la sección "Nuestros servicios") — no se
  redactó texto nuevo para las diapositivas 2 y 3.
- **Reuso de fotos reales:** solo hay 4 fotos "grandes" utilizables del
  cliente sin marca de terceros (`hero-mantenimiento.jpg`,
  `capacitacion-rcp.jpg`, `botiquin.jpg`, `dea.jpg`) — se reutilizan a
  propósito en varias secciones/páginas. **Cuidado:** la carpeta
  `imagenes/` tiene varias fotos con logos de OTRAS empresas (ECOFIRE
  Express, AGA Fire, "FIRE 55", "Full Minería") — no usarlas en el sitio.
- **Cifras sin inventar:** la banda de estadísticas y la cifra de años de
  experiencia del bloque "Quiénes somos" muestran literalmente
  `[Número]` / `[zonas de servicio]` (clase `.stat-pending`, subrayado
  punteado) porque el cliente no ha dado datos reales — no reemplazar con
  números inventados.
- **Facebook pendiente:** el ícono de Facebook enlaza a `#` porque el
  cliente no ha dado la URL (brief, sección 4).
- **Normativa citada como referencia externa, no como certificación:** la
  sección "Normativa y estándares de referencia" de cada
  `servicio-<slug>.html` cita normas reales (NFPA, OSHA, ISO, etc.)
  investigadas y verificadas, pero deliberadamente NO afirma que CEPASI
  esté certificada por esos organismos — solo que son buenas prácticas
  del sector. Mantener ese descargo si se edita esa sección.
- **Formulario PSST sin envío de adjuntos "de verdad" todavía:** es
  intencional mientras `PSST_UPLOAD_ENDPOINT` esté vacía (ver arriba) —
  no es un bug, es el estado esperado hasta desplegar el Google Apps
  Script.

## Verificación / testing

No hay suite de tests. Para validar cambios visuales:

```bash
python3 -m http.server 8731        # servir el sitio localmente
# tomar screenshot con Chrome headless, ej.:
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1440,4600 --screenshot=/tmp/shot.png \
  http://localhost:8731/index.html
```

**Nota importante:** Chrome headless con `--screenshot` en este entorno
recorta/mide mal el layout en anchos **menores a ~500px** (confirmado con
reproducción mínima aislada, no es un bug del sitio) — para revisar mobile
real usa 600px como proxy razonable, o pide al usuario probar en un
navegador de verdad / conectar la extensión Claude in Chrome.

Antes de dar por buena una edición: correr `python3 tools/build.py`,
revisar que `git diff` solo muestre lo esperado, y tomar al menos una
captura desktop (1440) + una a 600px de las páginas afectadas. Un cambio
en un helper compartido (`category_block`, `service_item`, `_svc`,
`servicio_hero`, etc.) toca potencialmente las 25 `servicio-<slug>.html`
a la vez — revisa el `git status`/`git diff` completo, no solo la página
que pensabas cambiar.

## Pendiente técnico

- **Conectar `PSST_UPLOAD_ENDPOINT`:** desplegar el Google Apps Script Web
  App sobre la cuenta de Gmail de CEPASI (requiere acceso a
  `cuerpodeevacuacion01@gmail.com` o a otra cuenta de Google del
  cliente), pegar la URL `.../exec` resultante en esa constante de
  `tools/build.py` y correr `build.py`. Hasta entonces, `formulario-psst.html`
  funciona por `mailto:` sin adjuntar los archivos automáticamente (ver
  sección "Formulario PSST" arriba).

## Pendientes conocidos (del cliente, no técnicos)

- URL real de Facebook.
- Cifras reales para la banda de estadísticas y años de experiencia.
- Reemplazar los 3 proyectos y 3 artículos de blog placeholder por casos
  reales (editar `proyectos-data.js` / `blog-data.js`).
- Fotos propias de mejor resolución para hero/servicios si el cliente las
  tiene (hoy se usan las de `imagenes/` que estaban disponibles).
