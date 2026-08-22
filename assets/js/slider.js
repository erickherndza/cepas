// CEPASI — slider.js
// Slider del hero de Inicio (#hero-slider). No hace nada en páginas que no
// tengan ese elemento, así que se puede incluir en todas las páginas sin
// costo. Autoplay + flechas + puntos, se pausa al pasar el mouse.

document.addEventListener('DOMContentLoaded', function () {
  var root = document.getElementById('hero-slider');
  if (!root) return;

  var slides = Array.prototype.slice.call(root.querySelectorAll('.slide'));
  var dots = Array.prototype.slice.call(root.querySelectorAll('.slider-dot'));
  var prevBtn = root.querySelector('[data-slide-prev]');
  var nextBtn = root.querySelector('[data-slide-next]');
  if (slides.length < 2) return;

  var current = 0;
  var AUTOPLAY_MS = 6500;
  var timer = null;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach(function (s, i) {
      s.classList.toggle('active', i === current);
    });
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i === current);
    });
  }

  function next() { show(current + 1); }
  function prev() { show(current - 1); }

  function play() {
    stop();
    timer = window.setInterval(next, AUTOPLAY_MS);
  }
  function stop() {
    if (timer) window.clearInterval(timer);
    timer = null;
  }

  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      show(i);
      play();
    });
  });
  if (nextBtn) nextBtn.addEventListener('click', function () { next(); play(); });
  if (prevBtn) prevBtn.addEventListener('click', function () { prev(); play(); });

  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', play);

  show(0);
  play();
});
