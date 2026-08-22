# Brief para Claude Code — MVP Website CEPASI

> Copia y pega este archivo completo como prompt/contexto para Claude Code. Incluye también el archivo `CEPASI_copy_website.md` en el mismo proyecto: ahí está todo el texto final de cada sección (Claude Code debe usarlo como fuente de verdad para los contenidos, no inventar copy nuevo).

## 1. Objetivo

Construir el **MVP del sitio web** de CEPASI (Cuerpo de Evacuación, Primeros Auxilios y Seguridad Industrial, S.R.L.), una empresa dominicana de seguridad industrial y salud ocupacional (B2B, con Reglamento 522-06 como eje de cumplimiento).

El sitio debe verse profesional, técnico y confiable — dirigido a gerentes de RRHH, seguridad industrial y dueños de empresa que necesitan cumplir normativa y proteger a su personal.

## 2. Referencia de diseño

Usar como referencia de **layout y patrones de UI** (no de contenido ni de rubro) esta landing:
`https://reintive.netlify.app/index-5`

De esa referencia, tomar:
- Header con barra superior de contacto + menú de navegación + iconos de redes sociales.
- Secciones tipo "grid de servicios" con cards (ícono, título, descripción corta, "Leer más").
- Sección de estadísticas/números destacados ("Por qué elegirnos").
- Grid de portafolio/proyectos con filtro por categoría.
- Sección de blog en cards (imagen, fecha, categoría, título, extracto).
- Sección de contacto con formulario + datos + mapa.
- Footer con info de empresa, enlaces rápidos y redes sociales.

**No replicar** de la referencia: la sección de precios (pricing), la convocatoria de talento, las barras de "habilidades %", ni el copy Lorem Ipsum — CEPASI no vende planes de suscripción ni necesita esas secciones.

**Agregar, aunque la referencia no lo tenga:**
- Botón flotante de WhatsApp visible en todas las páginas (esquina inferior derecha), especialmente en Home.
- Barra superior del header con dirección, teléfono y correo (ver sección 4).

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

## 5. Header (todas las páginas)

Barra superior (topbar), delgada, antes del menú principal:
- Ícono + dirección: C/ 16, Esquina 19, Villa Aura, Santo Domingo Oeste, R.D.
- Ícono + teléfono: 809-284-5807
- Ícono + correo: cuerpodeevacuacion01@gmail.com
- Iconos de redes sociales a la derecha: Facebook, Instagram (enlazando a las URLs de la sección 4)

Header principal (sticky al hacer scroll):
- Logo "CEPASI" (usar wordmark de texto si no hay logo gráfico aún)
- Menú: Inicio · Nosotros · Servicios · Proyectos · Blog · Contacto
- Botón CTA destacado: "Solicitar asesoría" (WhatsApp o ancla a #contacto)

## 6. Estructura de páginas y contenido

Usar el copy tal cual está en `CEPASI_copy_website.md` (documento ya aprobado con tono corporativo/técnico). Resumen de qué va en cada página/sección — el detalle completo de cada texto está en ese archivo:

### 6.1 Inicio (`/`)
- Hero con headline + subheadline + 2 CTAs ("Solicitar asesoría gratuita" / "Ver nuestros servicios")
- Trust bar (línea de íconos: Asesoría técnica · Capacitación certificada · Venta e instalación de equipos · Cumplimiento 522-06)
- Bloque de propuesta de valor (2 párrafos)
- 4 diferenciadores en cards ("¿Por qué elegir CEPASI?")
- Grid resumen de los 4 servicios (con ícono, título, descripción corta, botón "Ver más" → enlaza a /servicios#ancla)
- Banda de cifras/estadísticas (placeholders `[Número]` — dejar editable, no inventar cifras)
- CTA final con botón WhatsApp y botón de llamada
- **Botón flotante de WhatsApp** visible en toda la página

### 6.2 Nosotros (`/nosotros`)
- Hero de sección (headline + subheadline)
- Quiénes somos (2 párrafos)
- Misión / Visión (dos columnas o cards)
- "Lo que nos guía" — 4 valores en cards
- Bloque de cumplimiento del Reglamento 522-06 (puede llevar ícono de check/normativa)

### 6.3 Servicios (`/servicios`)
- Hero de sección
- 4 bloques (uno por categoría), cada uno como sección con ancla propia para poder linkear desde Home:
  1. Asesoría y Consultoría Especializada (4 servicios)
  2. Capacitaciones y Formación Técnica (12 servicios)
  3. Mantenimiento, Taller y Equipamiento (5 servicios)
  4. Equipos de Emergencia y Primeros Auxilios — ventas (4 líneas de producto)
- Cada servicio individual como card o ítem con ícono + título + descripción corta (texto exacto en el .md de copy)
- CTA de cierre: "¿No sabe qué necesita su empresa? Solicite una evaluación gratuita"

### 6.4 Proyectos (`/proyectos`)
- Hero de sección
- Grid de 3 "proyectos tipo" (placeholders, marcados como ejemplo — ver nota en el copy) con: nombre de empresa [placeholder], sector, alcance del proyecto, resultado
- Diseñar el componente para que sea fácil agregar más proyectos reales después (pensar en un array/lista de datos, no hardcodear si el stack lo permite)
- CTA de cierre

### 6.5 Blog (`/blog`)
- Hero de sección
- Grid de 3 "artículos tipo" (placeholder) con título, resumen, categoría
- Mismo criterio que Proyectos: estructura de datos reutilizable para agregar artículos reales después
- CTA de suscripción (puede ser solo un input de email + botón, sin backend funcional en el MVP)

### 6.6 Contacto (`/contacto`)
- Hero de sección
- Formulario: nombre, empresa (opcional), teléfono, correo, servicio de interés (select), mensaje
- Bloque de datos de contacto directo (dirección, teléfonos, correo) — igual que el header
- Botones grandes: "Escribir por WhatsApp" y "Llamar ahora"
- Mapa embebido de Google Maps con la dirección (usar iframe de Google Maps con la dirección de la sección 4)

### 6.7 Footer (todas las páginas)
- Logo/nombre CEPASI + una línea descriptiva corta
- Columna de enlaces rápidos (mismo menú del header)
- Columna de contacto (dirección, teléfono, correo)
- Iconos de redes sociales (Facebook, Instagram)
- Línea de copyright: "© [año actual] CEPASI. Todos los derechos reservados."

## 7. Guía de estilo visual

- **Paleta:** azul corporativo oscuro (tipo `#1F3B57`) como color primario, rojo de seguridad (tipo `#C0392B`) como acento para CTAs y alertas, fondo blanco/gris muy claro, texto gris oscuro para cuerpo.
- **Tipografía:** una sans-serif limpia y legible (ej. Inter, Poppins o similar), títulos en semibold/bold.
- **Iconografía:** íconos de seguridad industrial (casco, extintor, botiquín, cruz médica, señal de evacuación) — usar una librería tipo Lucide, Heroicons o Font Awesome.
- **Tono visual general:** confiable, técnico, no "creativo/agencia" — CEPASI vende seguridad, no diseño.

## 8. Checklist funcional del MVP

- [ ] Responsive en mobile, tablet y desktop
- [ ] Header con topbar de contacto + navegación + iconos sociales
- [ ] Botón flotante de WhatsApp en todas las páginas
- [ ] 6 páginas: Inicio, Nosotros, Servicios, Proyectos, Blog, Contacto
- [ ] Formulario de contacto funcional (o con fallback a WhatsApp/mailto)
- [ ] Mapa embebido en Contacto
- [ ] Meta tags básicos de SEO por página (title, description)
- [ ] Todo el copy tomado de `CEPASI_copy_website.md`, sin Lorem Ipsum
- [ ] Datos de contacto exactamente como en la sección 4 de este documento (no inventar cifras, direcciones ni teléfonos adicionales)
