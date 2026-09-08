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

  // Formulario de informaciones para el Manual de SST (PSST). Recorre los
  // campos por data-group/data-label en vez de listarlos uno a uno, para
  // que agregar/quitar un campo en build.py no requiera tocar este
  // archivo. Si window.PSST_UPLOAD_ENDPOINT está configurado (URL de un
  // Google Apps Script Web App), envía el formulario con los archivos
  // reales adjuntos; si no, cae de vuelta a mailto (sin adjuntos reales,
  // solo el nombre de los archivos elegidos, como recordatorio).
  var psstForm = document.getElementById('psst-form');
  if (psstForm) {
    initPsstFileDropzones(psstForm);

    var psstHelp = document.getElementById('psst-help');
    var hasUploadEndpoint = !!(window.PSST_UPLOAD_ENDPOINT && window.PSST_UPLOAD_ENDPOINT.trim());
    if (psstHelp && !hasUploadEndpoint) {
      psstHelp.innerHTML = 'Se abrirá su cliente de correo con esta información. Los archivos elegidos arriba <strong>no se adjuntan automáticamente todavía</strong> — adjúntelos usted mismo a ese correo antes de enviarlo.';
    }

    psstForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var lines = [];
      psstForm.querySelectorAll('[data-group]').forEach(function (group) {
        lines.push('');
        lines.push('== ' + group.getAttribute('data-group') + ' ==');
        group.querySelectorAll('[data-label]').forEach(function (field) {
          var label = field.getAttribute('data-label');
          var value;
          if (field.type === 'file') {
            value = field.files && field.files.length
              ? Array.prototype.map.call(field.files, function (f) { return f.name; }).join(', ')
              : '— (sin seleccionar)';
          } else {
            value = (field.value || '').toString().trim() || '—';
          }
          lines.push(label + ': ' + value);
        });
      });

      var nombreEmpresaField = psstForm.querySelector('[name="nombre_empresa"]');
      var nombreEmpresa = nombreEmpresaField ? nombreEmpresaField.value.trim() : '';
      var subject = 'Informaciones PSST' + (nombreEmpresa ? ' — ' + nombreEmpresa : '');
      var feedback = document.getElementById('psst-feedback');

      if (hasUploadEndpoint) {
        var formData = new FormData(psstForm);
        formData.append('_subject', subject);
        if (feedback) {
          feedback.innerHTML = 'Enviando información y archivos a CEPASI…';
          feedback.classList.remove('hidden');
        }
        fetch(window.PSST_UPLOAD_ENDPOINT, { method: 'POST', body: formData })
          .then(function (res) { if (!res.ok) throw new Error('bad response'); return res; })
          .then(function () {
            if (feedback) feedback.innerHTML = 'Gracias — recibimos su información y los archivos adjuntos. Nuestro equipo se pondrá en contacto en breve.';
            psstForm.reset();
            initPsstFileDropzones(psstForm);
          })
          .catch(function () {
            if (feedback) feedback.innerHTML = 'No se pudo enviar automáticamente. Por favor escríbanos por <a href="https://wa.me/18092845807" target="_blank" rel="noopener" class="underline font-semibold">WhatsApp</a> o al correo cuerpodeevacuacion01@gmail.com.';
          });
        return;
      }

      var mailto = 'mailto:cuerpodeevacuacion01@gmail.com' +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n').trim());

      if (feedback) {
        feedback.innerHTML = 'Abriendo su cliente de correo con esta información. Antes de enviarlo, no olvide <strong>adjuntar</strong> los archivos que seleccionó arriba.';
        feedback.classList.remove('hidden');
      }

      window.location.href = mailto;
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

// Zonas de arrastrar-y-soltar del formulario PSST (formulario-psst.html):
// lista de archivos elegidos con opción de quitar uno a uno, arrastrar
// archivos sobre el recuadro, y un total de tamaño acumulado en MB para
// que el cliente note si se está acercando al límite de un correo.
var PSST_SOFT_LIMIT_MB = 20;

function initPsstFileDropzones(form) {
  form.querySelectorAll('[data-file-input]').forEach(function (input) {
    var dropLabel = input.closest('[data-file-drop]');
    var container = input.closest('div');
    var listEl = container && container.querySelector('[data-file-list]');

    function renderFiles() {
      if (!listEl) return;
      listEl.innerHTML = '';
      Array.prototype.forEach.call(input.files, function (file, idx) {
        var chip = document.createElement('div');
        chip.className = 'flex items-center justify-between gap-2 bg-beige rounded-sm px-3 py-1.5 text-xs text-ink';
        var sizeKb = Math.round(file.size / 1024);
        var nameSpan = document.createElement('span');
        nameSpan.className = 'truncate';
        nameSpan.textContent = file.name + ' (' + sizeKb + ' KB)';
        var removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'text-slate-400 hover:text-brandred shrink-0 font-bold px-1';
        removeBtn.setAttribute('aria-label', 'Quitar ' + file.name);
        removeBtn.textContent = '×';
        removeBtn.addEventListener('click', function () {
          var dt = new DataTransfer();
          Array.prototype.forEach.call(input.files, function (f, i) {
            if (i !== idx) dt.items.add(f);
          });
          input.files = dt.files;
          renderFiles();
          updatePsstFileTotal(form);
        });
        chip.appendChild(nameSpan);
        chip.appendChild(removeBtn);
        listEl.appendChild(chip);
      });
    }

    input.addEventListener('change', function () {
      renderFiles();
      updatePsstFileTotal(form);
    });

    if (dropLabel) {
      dropLabel.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropLabel.classList.add('border-brandorange');
      });
      dropLabel.addEventListener('dragleave', function () {
        dropLabel.classList.remove('border-brandorange');
      });
      dropLabel.addEventListener('drop', function (e) {
        e.preventDefault();
        dropLabel.classList.remove('border-brandorange');
        var incoming = e.dataTransfer.files;
        if (!incoming || !incoming.length) return;
        var dt = new DataTransfer();
        if (input.multiple) {
          Array.prototype.forEach.call(input.files, function (f) { dt.items.add(f); });
        }
        Array.prototype.forEach.call(incoming, function (f) { dt.items.add(f); });
        input.files = dt.files;
        renderFiles();
        updatePsstFileTotal(form);
      });
    }
  });
  updatePsstFileTotal(form);
}

function updatePsstFileTotal(form) {
  var totalEl = document.getElementById('psst-file-total');
  if (!totalEl) return;
  var total = 0;
  form.querySelectorAll('[data-file-input]').forEach(function (input) {
    Array.prototype.forEach.call(input.files, function (f) { total += f.size; });
  });
  var mb = total / (1024 * 1024);
  var overLimit = mb > PSST_SOFT_LIMIT_MB;
  totalEl.textContent = 'Total seleccionado: ' + mb.toFixed(1) + ' MB' +
    (overLimit ? ' — considere enviarlo en más de un correo o compartir las fotos por WhatsApp.' : '');
  totalEl.classList.toggle('text-brandred', overLimit);
  totalEl.classList.toggle('font-semibold', overLimit);
}
