/* app.js Hauptseite Zahnzentrum Messerschmidt: Menü, Kopf beim Scrollen, Video-Schalter, sanftes Einblenden.
   Kein Framework, nichts von außen. */
(function () {
  'use strict';
  var d = document, b = d.body;
  d.documentElement.classList.add('js');
  d.querySelectorAll('[data-jahr]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  // Menü auf dem Handy
  var schalter = d.querySelector('.navi-schalter'), navi = d.querySelector('.hauptnavi');
  if (schalter && navi) {
    schalter.addEventListener('click', function () {
      var offen = navi.classList.toggle('offen');
      b.classList.toggle('navi-offen', offen);
      schalter.setAttribute('aria-expanded', offen ? 'true' : 'false');
      schalter.setAttribute('aria-label', offen ? 'Menü schließen' : 'Menü öffnen');
    });
  }

  // Startseite: Kopf ist über dem Video durchsichtig und wird beim Scrollen weiß
  var kopf = d.querySelector('.kopf-transparent');
  if (kopf) {
    var pruefen = function () { kopf.classList.toggle('kopf-transparent', window.scrollY < 60); };
    window.addEventListener('scroll', pruefen, { passive: true }); pruefen();
  }

  // Video: anhalten/abspielen; bei „Bewegung reduzieren“ gar nicht abspielen
  var video = d.querySelector('.hero-video'), vs = d.querySelector('.video-schalter');
  if (video) {
    var ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (ruhig) { video.removeAttribute('autoplay'); video.pause(); if (vs) vs.setAttribute('aria-pressed', 'true'); }
    if (vs) vs.addEventListener('click', function () {
      if (video.paused) { video.play(); vs.setAttribute('aria-pressed', 'false'); vs.setAttribute('aria-label', 'Video anhalten'); }
      else { video.pause(); vs.setAttribute('aria-pressed', 'true'); vs.setAttribute('aria-label', 'Video abspielen'); }
    });
  }

  // Sanftes Einblenden
  var ziele = d.querySelectorAll('.abschnitt .text-spalte, .bild-quer, .bild-hoch, .leistung-karte, .kachel, .person, .karte-glas, .abschnitt-kopf');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (e) {
      e.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('sichtbar'); io.unobserve(x.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    ziele.forEach(function (el) { el.classList.add('einblenden'); io.observe(el); });
  }
})();
