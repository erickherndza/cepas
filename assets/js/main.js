// CEPASI — main.js
// Formularios (contacto/newsletter), filtro de proyectos y render de las
// tarjetas de Proyectos/Blog desde assets/js/proyectos-data.js y
// blog-data.js. Ver nav.js (menú/scroll) y slider.js (hero) para el resto.

document.addEventListener('DOMContentLoaded', function () {
  // Contact form -> mailto + WhatsApp fallback (sin backend)
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var data = new FormData(form);
      var nombre = (data.get('nombre') || '').toString().trim();
      var empresa = (data.get('empresa') || '').toString().trim();
      var telefono = (data.get('telefono') || '').toString().trim();
      var correo = (data.get('correo') || '').toString().trim();
      var servicio = (data.get('servicio') || '').toString().trim();
      var mensaje = (data.get('mensaje') || '').toString().trim();

      var feedback = document.getElementById('form-feedback');
      if (!nombre || !telefono || !mensaje) {
        if (feedback) {
          feedback.textContent = 'Por favor complete al menos nombre, teléfono y mensaje.';
          feedback.classList.remove('hidden');
        }
        return;
      }

      var bodyLines = [
        'Nombre: ' + nombre,
        'Empresa: ' + (empresa || '—'),
        'Teléfono: ' + telefono,
        'Correo: ' + (correo || '—'),
        'Servicio de interés: ' + (servicio || '—'),
        '',
        mensaje
      ];
      var subject = 'Solicitud de contacto — ' + nombre;
      var mailto = 'mailto:cuerpodeevacuacion01@gmail.com' +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(bodyLines.join('\n'));

      var waText = 'Hola CEPASI, mi nombre es ' + nombre +
        (empresa ? ' (' + empresa + ')' : '') +
        '. Me interesa: ' + (servicio || 'una asesoría') +
        '. ' + mensaje;
      var waLink = 'https://wa.me/18092845807?text=' + encodeURIComponent(waText);

      if (feedback) {
        feedback.innerHTML = 'Gracias, ' + nombre.split(' ')[0] +
          '. Abriendo su cliente de correo… si prefiere, ' +
          '<a href="' + waLink + '" target="_blank" rel="noopener" class="underline font-semibold">escríbanos por WhatsApp</a>.';
        feedback.classList.remove('hidden');
      }

      window.location.href = mailto;
      form.reset();
    });
  }

  // Blog newsletter (sin backend funcional)
  var newsletter = document.getElementById('newsletter-form');
  if (newsletter) {
    newsletter.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('newsletter-feedback');
      if (msg) {
        msg.textContent = '¡Gracias por suscribirse! Le enviaremos nuestros próximos artículos.';
        msg.classList.remove('hidden');
      }
      newsletter.reset();
    });
  }

  // Render de proyectos desde assets/js/proyectos-data.js — tarjetas estilo
  // portafolio: imagen/degradado con esquina cortada + overlay + texto.
  var proyectosGrid = document.getElementById('proyectos-grid');
  if (proyectosGrid && window.PROYECTOS) {
    proyectosGrid.innerHTML = PROYECTOS.map(function (p) {
      return '' +
        '<article data-category="' + p.categoria + '" class="img-card group">' +
          '<div class="clip-tr relative h-56 overflow-hidden bg-gradient-to-br from-ink via-ink to-navy">' +
            '<div class="img-card-photo absolute inset-0 flex items-center justify-center opacity-30">' +
              '<i data-lucide="' + p.icono + '" class="w-24 h-24 text-white"></i>' +
            '</div>' +
            '<div class="absolute inset-0 bg-gradient-to-t from-ink via-ink/40 to-transparent"></div>' +
            '<span class="absolute top-4 left-4 bg-gradient-brand text-white text-xs font-bold uppercase tracking-wide px-3 py-1 rounded-full">' + p.categoriaLabel + '</span>' +
            '<div class="absolute bottom-4 left-4 right-4">' +
              '<h3 class="font-heading font-bold text-xl text-white leading-tight">' + p.empresa + '</h3>' +
              '<p class="text-xs text-white/80 mt-1">' + p.sector + ' · ' + p.ubicacion + '</p>' +
            '</div>' +
          '</div>' +
          '<div class="bg-white border border-t-0 border-slate-100 rounded-b-xl p-6 card-lift">' +
            '<p class="text-slate-600 text-sm leading-relaxed mb-4">' + p.descripcion + '</p>' +
            '<p class="text-sm text-slate-700 mb-2"><span class="font-semibold text-ink">Alcance:</span> ' + p.alcance.join(' · ') + '</p>' +
            '<p class="text-sm text-slate-700"><span class="font-semibold text-ink">Resultado:</span> ' + p.resultado + '</p>' +
          '</div>' +
        '</article>';
    }).join('');
    if (window.lucide) lucide.createIcons();
  }

  // Render de artículos desde assets/js/blog-data.js
  var blogGrid = document.getElementById('blog-grid');
  if (blogGrid && window.ARTICULOS) {
    blogGrid.innerHTML = ARTICULOS.map(function (a) {
      return '' +
        '<article class="img-card">' +
          '<div class="clip-tr relative h-44 overflow-hidden bg-gradient-to-br from-navy to-ink">' +
            '<div class="img-card-photo absolute inset-0 flex items-center justify-center opacity-30">' +
              '<i data-lucide="' + a.icono + '" class="w-16 h-16 text-white"></i>' +
            '</div>' +
            '<div class="absolute inset-0 bg-gradient-to-t from-ink/90 to-transparent"></div>' +
          '</div>' +
          '<div class="bg-white border border-t-0 border-slate-100 rounded-b-xl p-6 flex flex-col flex-1 card-lift">' +
            '<span class="text-xs font-bold uppercase tracking-wide text-brandred mb-2">' + a.categoria + '</span>' +
            '<h3 class="font-heading font-bold text-xl text-ink mb-2 leading-tight">' + a.titulo + '</h3>' +
            '<p class="text-slate-600 text-sm leading-relaxed flex-1">' + a.resumen + '</p>' +
            '<span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-brandred">Próximamente <i data-lucide="arrow-right" class="w-4 h-4"></i></span>' +
          '</div>' +
        '</article>';
    }).join('');
    if (window.lucide) lucide.createIcons();
  }

  // Proyectos: filtro por categoría
  var filterButtons = document.querySelectorAll('[data-filter]');
  if (filterButtons.length) {
    filterButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterButtons.forEach(function (b) {
          b.classList.remove('bg-gradient-brand', 'text-white');
          b.classList.add('bg-white', 'text-ink');
        });
        btn.classList.add('bg-gradient-brand', 'text-white');
        btn.classList.remove('bg-white', 'text-ink');

        var filter = btn.getAttribute('data-filter');
        document.querySelectorAll('[data-category]').forEach(function (card) {
          var match = filter === 'todos' || card.getAttribute('data-category') === filter;
          card.style.display = match ? '' : 'none';
        });
      });
    });
  }
});
