# Brief para Claude Code — MVP Website CEPASI

> Copia y pega este archivo completo como prompt/contexto para Claude Code. Incluye también el archivo `CEPASI_copy_website.md` en el mismo proyecto: ahí está todo el texto final de cada sección (Claude Code debe usarlo como fuente de verdad para los contenidos, no inventar copy nuevo).

## 1. Objetivo

Construir el **MVP del sitio web** de CEPASI (Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial, S.R.L.), una empresa dominicana de seguridad industrial y salud ocupacional (B2B, con Reglamento 522-06 como eje de cumplimiento).

El sitio debe verse profesional, técnico e industrial — dirigido a gerentes de RRHH, seguridad industrial y dueños de empresa que necesitan cumplir normativa y proteger a su personal. El estilo visual debe sentirse como una empresa de seguridad/emergencias real, no como una agencia creativa.

## 2. Referencias de diseño (dos referencias, roles distintos)

### 2.1 Referencia de estructura de páginas — Reintive
`https://reintive.netlify.app/index-5`

Tomar de ahí únicamente el **inventario de secciones/páginas** (qué existe, no cómo se ve):
- Header con barra de contacto + navegación + redes sociales
- Grid de servicios en cards
- Sección de estadísticas
- Grid de portafolio/proyectos
- Blog en cards
- Contacto con formulario + datos + mapa
- Footer con columnas

**No usar su estilo visual** (esa referencia es genérica de agencia). El estilo visual real del sitio sale de la referencia de la sección 2.2.

**No replicar tampoco de Reintive:** pricing/planes, convocatoria de talento, barras de "habilidades %", copy Lorem Ipsum — CEPASI no vende suscripciones.

### 2.2 Referencia de estilo visual (la que manda) — Firegard
`https://demo.awaikenthemes.com/firegard/`

Este es un theme de una empresa de protección contra incendios: es el más cercano al rubro de CEPASI y **debe ser la referencia visual principal** (colores, tipografía, forma de botones, forma de las cards, fotografía). El detalle exacto capturado de sus screenshots está en la sección 7 (Guía de estilo visual) — Claude Code debe implementar esa guía, no adivinar el estilo.

Patrones de layout de Firegard a replicar (adaptados a las secciones de CEPASI, ver sección 6):
- Topbar oscura de dos niveles: barra de anuncio/promo arriba (opcional) + barra de contacto con teléfono/correo a la izquierda e iconos sociales a la derecha.
- Header principal blanco, logo a la izquierda, nav centrado, botón CTA con esquina cortada en diagonal (forma de "banderín"), en degradado rojo-naranja.
- Hero de pantalla completa con foto industrial de fondo oscurecida, headline enorme en mayúsculas con una palabra/frase resaltada en degradado, foto de una persona (con casco/EPP) superpuesta al lado derecho, botón CTA flotante sobre la imagen.
- Sección "Nosotros" tipo collage: imagen principal con esquina cortada + imagen secundaria superpuesta + tarjeta oscura con una cifra destacada ("30+ Años de experiencia") + video/imagen adicional, todo junto a un bloque de texto con 2 features en columnas e ícono circular.
- Sección "Por qué elegirnos" repetida con imagen a un lado + lista de puntos con ícono circular en degradado + título + descripción.
- Grid de servicios/proyectos como cards de imagen de fondo con esquina superior cortada, overlay oscuro degradado abajo, categoría + título superpuestos en la imagen.
- Sección de confianza/testimonios en 3 columnas, la del centro resaltada con fondo en degradado rojo-naranja.
- Banda de contacto de cierre: fondo oscuro con foto industrial, texto centrado, botón CTA + ícono circular de teléfono con el número al lado.
- Footer oscuro de 4 columnas: marca + redes sociales, enlaces rápidos (con íconos pequeños como viñeta en vez de puntos), info legal, contacto — barra inferior con copyright.

**Adaptar, no copiar literal:**
- CEPASI no vende productos por carrito, así que todos los botones tipo "Buy Now" de Firegard se traducen a CTAs de CEPASI: "Solicitar asesoría", "Escribir por WhatsApp", "Solicitar cotización" — mismo estilo visual de botón (degradado, esquina cortada o pill), otro texto.
- El ícono de "llama" del logo y de las viñetas del footer se reemplaza por un ícono propio de CEPASI (ver sección 7 — casco, escudo o cruz de emergencia), ya que CEPASI cubre más que incendios (evacuación, primeros auxilios, seguridad industrial en general).
- La sección de testimonios de Firegard usa citas ficticias atribuidas a un mismo texto repetido — **no reutilizar ese contenido de ejemplo tal cual**. Si se incluye una sección de confianza en el MVP, usar el formato "empresas que confían en nosotros" (logos placeholder) en vez de citas textuales inventadas atribuidas a personas reales, hasta que CEPASI entregue testimonios reales con su autorización.

**Agregar, aunque Firegard no lo tenga:**
- Botón flotante de WhatsApp visible en todas las páginas (esquina inferior derecha) — Firegard no lo incluye, pero es un requisito de CEPASI.

## 3. Stack técnico sugerido

MVP simple, rápido de desplegar y fácil de mantener por el cliente:

- **HTML5 + CSS3 (Tailwind CSS) + JavaScript vanilla**, o **Next.js/Astro** si se prefiere un stack de componentes — a criterio de Claude Code según lo que sea más rápido de entregar como MVP.
- Totalmente **responsive** (mobile-first; muchos clientes B2B lo revisan desde el teléfono).
- Sin backend por ahora: el formulario de contacto puede usar un servicio tipo Formspree/EmailJS o simplemente `mailto:` + WhatsApp como fallback (definir el más simple de implementar).
- Optimizado para SEO básico: metatags, títulos por página, alt en imágenes, sitemap.xml.
- Assets de imágenes: usar placeholders/stock relacionados a seguridad industrial, extintores, brigadas, primeros auxilios (el cliente reemplazará luego con fotos reales).

## 4. Datos de marca y contacto (usar exactamente así, sin inventar)

- **Nombre legal:** Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial, S.R.L.
- **Marca:** CEPASI
- **Dirección:** C/ 16, Esquina 19, Villa Aura, Santo Domingo Oeste, R.D.
- **Teléfonos / WhatsApp:** 809-284-5807 | 829-546-2313
- **Correo:** cuerpodeevacuacion01@gmail.com
- **Instagram:** https://www.instagram.com/seguridad_y_salud_ocupacional1/
- **Facebook:** *(pendiente — el cliente debe dar la URL; dejar el ícono enlazado a `#` o a la página de Facebook de CEPASI cuando la confirmen)*
- **WhatsApp click-to-chat (botón flotante):** `https://wa.me/18092845807` (usar el primer número con código de país 1 para R.D.)

## 5. Header (todas las páginas) — estilo Firegard

**Barra de anuncio (opcional, fondo lima/verde claro):** franja delgada arriba de todo, texto corto tipo "🔥 Solicita tu evaluación de riesgo gratis" + botón pequeño en pill lima. Opcional para el MVP; se puede omitir si se prefiere un header más corto.

**Topbar de contacto (fondo oscuro, texto blanco):**
- Izquierda: ícono teléfono + 809-284-5807, ícono correo + cuerpodeevacuacion01@gmail.com, ícono dirección + "Villa Aura, Sto. Dgo. Oeste" (versión corta; la dirección completa va en el footer y en Contacto)
- Derecha: iconos de redes sociales — Instagram, Facebook (enlazando a las URLs de la sección 4)

**Header principal (fondo blanco, sticky al hacer scroll):**
- Logo CEPASI: ícono circular en degradado rojo-naranja (casco o escudo, ver sección 7) + wordmark "CEPASI" en mayúsculas bold
- Menú centrado: Inicio · Nosotros · Servicios · Proyectos · Blog · Contacto
- Botón CTA a la derecha, estilo Firegard (degradado rojo-naranja, esquina inferior derecha cortada en diagonal): "Solicitar Asesoría"

## 6. Estructura de páginas y contenido

Usar el copy tal cual está en `CEPASI_copy_website.md` (documento ya aprobado con tono corporativo/técnico). Aquí se detalla qué va en cada sección **y cómo se ve** (adaptando los patrones de Firegard descritos en 2.2):

### 6.1 Inicio (`/`)
- **Hero:** fondo de foto industrial oscurecida (tuberías, planta, o brigada en acción) con overlay oscuro; eyebrow con punto de color + texto corto ("SEGURIDAD QUE PROTEGE VIDAS"); headline en mayúsculas grande con la última frase en degradado rojo-naranja (usar el headline ya escrito: "Seguridad Industrial y Salud Ocupacional en la que su empresa puede confiar"); subheadline; 2 botones (uno degradado tipo Firegard "Solicitar asesoría gratuita", uno outline/secundario "Ver nuestros servicios"); opcional: foto de un brigadista/técnico con casco superpuesta a la derecha, como en Firegard.
- **Trust bar:** línea de íconos justo debajo del hero (Asesoría técnica · Capacitación certificada · Venta e instalación de equipos · Cumplimiento 522-06).
- **Bloque "Nosotros" resumido (estilo collage Firegard):** imagen principal con esquina cortada + imagen secundaria superpuesta + tarjeta oscura con cifra destacada (placeholder `[Número] años de experiencia`, editable) + texto de propuesta de valor (los 2 párrafos del copy) + 2 mini-features con ícono circular.
- **"¿Por qué elegir CEPASI?":** imagen a un lado + los 4 diferenciadores como lista con ícono circular en degradado, título y descripción (estilo "Por qué elegirnos" de Firegard).
- **Grid de servicios:** 4 cards estilo portafolio (imagen de fondo, esquina cortada, overlay oscuro, categoría + título superpuestos) — una por cada categoría de servicio, con botón "Ver más" hacia `/servicios#ancla`.
- **CTA final:** banda oscura de cierre con foto de fondo, headline + texto, botón "Contactar por WhatsApp" + ícono circular de teléfono con "809-284-5807" al lado (igual que la banda de contacto de Firegard).
- **Botón flotante de WhatsApp** visible en toda la página.

### 6.2 Nosotros (`/nosotros`)
- Hero de sección (headline + subheadline, fondo oscuro con foto)
- Quiénes somos (2 párrafos)
- Misión / Visión en dos cards
- "Lo que nos guía" — los 4 valores como lista con ícono circular en degradado (mismo patrón que "Por qué elegirnos")
- Bloque de cumplimiento del Reglamento 522-06, con ícono de check/normativa

### 6.3 Servicios (`/servicios`)
- Hero de sección
- 4 bloques (uno por categoría), cada uno con ancla propia para poder linkear desde Home:
  1. Asesoría y Consultoría Especializada (4 servicios)
  2. Capacitaciones y Formación Técnica (12 servicios)
  3. Mantenimiento, Taller y Equipamiento (5 servicios)
  4. Equipos de Emergencia y Primeros Auxilios — ventas (4 líneas de producto)
- Cada servicio individual como card con ícono circular en degradado + título + descripción corta (texto exacto en el .md de copy) — no hace falta la esquina cortada aquí, mejor cards limpias tipo "feature list" para que se lea bien con tanto contenido.
- CTA de cierre: "¿No sabe qué necesita su empresa? Solicite una evaluación gratuita"

### 6.4 Proyectos (`/proyectos`)
- Hero de sección
- Grid de 3 "proyectos tipo" (placeholders, marcados como ejemplo) en cards estilo portafolio de Firegard: imagen con esquina cortada, overlay oscuro, categoría/sector + nombre de empresa `[placeholder]` superpuestos; al hacer clic o debajo, el detalle con alcance y resultado.
- Diseñar el componente para que sea fácil agregar más proyectos reales después (array/lista de datos, no hardcodear si el stack lo permite).
- CTA de cierre.

### 6.5 Blog (`/blog`)
- Hero de sección
- Grid de 3 "artículos tipo" (placeholder) en cards con imagen, categoría, título, extracto
- Mismo criterio que Proyectos: estructura de datos reutilizable para agregar artículos reales después
- CTA de suscripción (input de email + botón, sin backend funcional en el MVP)

### 6.6 Contacto (`/contacto`)
- Hero de sección
- Formulario: nombre, empresa (opcional), teléfono, correo, servicio de interés (select), mensaje
- Bloque de datos de contacto directo (dirección completa, teléfonos, correo) — igual que el header
- Botones grandes: "Escribir por WhatsApp" y "Llamar ahora" (estilo botón degradado + ícono circular de Firegard)
- Mapa embebido de Google Maps con la dirección (iframe con la dirección de la sección 4)

### 6.7 Footer (todas las páginas) — estilo Firegard
- Fondo oscuro (casi negro)
- Columna 1: logo CEPASI + línea descriptiva corta + iconos circulares de redes sociales (fondo blanco, ícono en color)
- Columna 2: enlaces rápidos (mismo menú del header), cada ítem con un pequeño ícono de viñeta (ej. escudo/casco pequeño en vez del punto genérico)
- Columna 3: info legal si aplica (Política de privacidad, Términos) — opcional en el MVP
- Columna 4: contacto (dirección completa, teléfono, correo)
- Barra inferior: "© [año actual] CEPASI. Todos los derechos reservados."

## 7. Guía de estilo visual (extraída de Firegard — es la que manda)

> Colores tomados por inspección visual de capturas del theme; son aproximados. Si se requiere pixel-perfect, ajustar con un eyedropper sobre las capturas antes de fijarlos en el design system.

**Paleta:**
- Degradado primario (CTAs, iconos destacados, texto de énfasis): rojo `#E63C24` → naranja `#F79433`, en diagonal (`135deg`)
- Verde lima / chartreuse (barra de promo opcional, algún botón secundario tipo "pill"): `#CBE24B` — usar con moderación, es un acento, no el color principal
- Fondo oscuro (topbar, footer, bandas de cierre, overlays de hero): `#1A1A1A` / casi negro
- Texto sobre fondo oscuro: blanco `#FFFFFF`, con acentos en naranja `#F7941E` para números/links destacados
- Texto de titulares sobre fondo claro: casi negro `#1A1A1A`
- Texto de cuerpo: gris `#6B7280`
- Fondos de sección alternos: blanco `#FFFFFF` y un beige/gris muy claro `#F5F3EF` (para dar variedad entre secciones, como en la sección de testimonios de Firegard)

**Nota de marca:** para CEPASI, mantener el degradado rojo-naranja como identidad (coherente con "seguridad/alerta/incendio"), pero es válido introducir un azul oscuro corporativo (`#1F3B57`, del brief de copy) como color de apoyo en textos institucionales (Nosotros, Reglamento 522-06) si se quiere diferenciar un poco de un theme genérico de "fire protection" — a discreción de diseño, no es un requisito duro.

**Tipografía:**
- Titulares: sans-serif bold/black, en mayúsculas, tracking ajustado (look "industrial/impactante") — usar un Google Font equivalente como **Poppins ExtraBold/Black**, **Archivo Black** o **Barlow Condensed Bold**.
- Navegación y cuerpo: sans-serif regular/medium más neutra y legible — **Poppins** o **Inter**, pesos 400–600.

**Forma / lenguaje visual distintivo (el detalle que más define el look de Firegard):**
- **Esquina cortada en diagonal ("clip corner"):** botones, cards de imagen (servicios, proyectos, blog) y algunas fotos tienen una esquina (normalmente la superior derecha o inferior derecha) cortada en 45°, dando una forma de "banderín/ticket". Implementar con `clip-path: polygon(...)` en CSS. Este es el elemento que más hay que replicar para que se sienta "Firegard".
- Botones primarios: degradado rojo-naranja, esquina cortada, texto blanco bold, a veces con una flecha "→" al final.
- Botones secundarios/pill: verde lima, completamente redondeados (pill), texto negro bold.
- Iconos: circulares, ya sea con fondo degradado + ícono en línea blanca, o fondo gris claro + ícono en línea naranja.
- Cards de imagen (servicios/proyectos): overlay oscuro degradado de abajo hacia arriba sobre la foto, texto blanco superpuesto en la parte inferior.
- Bloques de cifras destacadas: caja oscura sólida superpuesta sobre un collage de imágenes, número grande en naranja + texto blanco pequeño debajo.

**Iconografía temática:** en vez del ícono de llama de Firegard (muy específico a incendios), usar para CEPASI un ícono que represente seguridad integral: casco de seguridad, escudo con cruz, o figura de evacuación — consistente en logo, viñetas del footer y acentos decorativos.

**Tono visual general:** confiable, técnico, con la energía visual de "alerta/protección" que da el degradado rojo-naranja sobre fondo oscuro — no un look "creativo de agencia", sino de empresa de seguridad y respuesta a emergencias.

## 8. Checklist funcional del MVP

- [ ] Responsive en mobile, tablet y desktop
- [ ] Header de dos niveles (topbar de contacto + iconos sociales, header principal con nav y CTA con esquina cortada)
- [ ] Botón flotante de WhatsApp en todas las páginas
- [ ] 6 páginas: Inicio, Nosotros, Servicios, Proyectos, Blog, Contacto
- [ ] Estilo visual "Firegard" aplicado: degradado rojo-naranja, esquina cortada en botones/cards, fondo oscuro en topbar/footer/bandas de cierre, tipografía bold en mayúsculas para titulares
- [ ] Formulario de contacto funcional (o con fallback a WhatsApp/mailto)
- [ ] Mapa embebido en Contacto
- [ ] Meta tags básicos de SEO por página (title, description)
- [ ] Todo el copy tomado de `CEPASI_copy_website.md`, sin Lorem Ipsum
- [ ] Datos de contacto exactamente como en la sección 4 de este documento (no inventar cifras, direcciones, teléfonos ni testimonios)
