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

  var ruhe = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var feinzeiger = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Hero: Überschrift Zeile für Zeile einblenden
  requestAnimationFrame(function () { b.classList.add('geladen'); });

  // Zähler in der Fakten-Leiste
  var zaehler = d.querySelectorAll('[data-zaehler]');
  if (zaehler.length && 'IntersectionObserver' in window && !ruhe) {
    var zo = new IntersectionObserver(function (e) {
      e.forEach(function (x) {
        if (!x.isIntersecting) return;
        var el = x.target, ziel = +el.getAttribute('data-zaehler'), t0 = null;
        var schritt = function (t) { t0 = t0 || t; var p = Math.min((t - t0) / 1400, 1); el.textContent = Math.round(ziel * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(schritt); };
        requestAnimationFrame(schritt); zo.unobserve(el);
      });
    }, { threshold: .6 });
    zaehler.forEach(function (el) { el.textContent = '0'; zo.observe(el); });
  }

  // Leitsatz: Wörter füllen sich beim Scrollen mit Farbe
  var aussage = d.querySelector('[data-woerter]');
  if (aussage) {
    aussage.innerHTML = aussage.textContent.trim().split(/\s+/).map(function (w) { return '<span>' + w + '</span>'; }).join(' ');
    var woerter = aussage.querySelectorAll('span');
  }

  // Parallax für große Bilder
  var parallax = ruhe ? [] : d.querySelectorAll('[data-parallax]');

  // Kopf: beim Runterscrollen ausblenden, beim Hochscrollen zeigen
  var kopfEl = d.querySelector('.kopf'), letzteY = window.scrollY;

  var tick = false;
  function beimScrollen() {
    var y = window.scrollY, h = window.innerHeight;
    if (woerter) {
      var r = aussage.getBoundingClientRect();
      var anteil = Math.min(Math.max((h * .85 - r.top) / (r.height + h * .45), 0), 1);
      var n = Math.round(anteil * woerter.length);
      woerter.forEach(function (w, i) { w.classList.toggle('an', i < n); });
    }
    parallax.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > h) return;
      var v = (r.top + r.height / 2 - h / 2) * -0.12;
      el.style.transform = 'translate3d(0,' + v.toFixed(1) + 'px,0) scale(1.12)';
    });
    if (kopfEl && !b.classList.contains('navi-offen')) {
      kopfEl.classList.toggle('kopf-weg', y > letzteY && y > 400);
    }
    letzteY = y; tick = false;
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(beimScrollen); } }, { passive: true });
  beimScrollen();

  // Leistungskarten: Lichtkegel folgt der Maus
  if (feinzeiger && !ruhe) {
    d.querySelectorAll('.leistung-karte, .kachel').forEach(function (k) {
      k.addEventListener('pointermove', function (e) {
        var r = k.getBoundingClientRect();
        k.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        k.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
    // Knöpfe: leichter Magnet-Effekt
    d.querySelectorAll('.knopf').forEach(function (k) {
      k.addEventListener('pointermove', function (e) {
        var r = k.getBoundingClientRect();
        k.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * .18).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * .25).toFixed(1) + 'px)';
      });
      k.addEventListener('pointerleave', function () { k.style.transform = ''; });
    });
  }

  // Kontaktformular: Versand per PHP, sonst (Vorschau) Mailprogramm
  var form = d.querySelector('.formular');
  if (form) {
    var meldung = form.querySelector('.formular-meldung'), knopf = form.querySelector('button[type=submit]');
    form.elements['zeit'].value = String(Date.now());
    var zeige = function (t, f) { meldung.textContent = t; meldung.className = 'formular-meldung ' + (f ? 'fehler' : 'erfolg'); };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var pf = ['name', 'telefon', 'email', 'anliegen'];
      for (var i = 0; i < pf.length; i++) { var f = form.elements[pf[i]]; if (!f.value.trim()) { f.focus(); return zeige('Bitte füllen Sie alle Pflichtfelder (*) aus.', true); } }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.elements['email'].value)) { form.elements['email'].focus(); return zeige('Bitte prüfen Sie die E-Mail-Adresse.', true); }
      if (!form.elements['datenschutz'].checked) return zeige('Bitte stimmen Sie der Datenschutzerklärung zu.', true);
      knopf.disabled = true; zeige('Wird gesendet …', false);
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { if ((r.headers.get('content-type') || '').indexOf('json') < 0) throw new Error('kein-php'); return r.json(); })
        .then(function (j) { knopf.disabled = false; if (j.ok) { form.reset(); zeige(j.text, false); } else zeige(j.text, true); })
        .catch(function () {
          knopf.disabled = false;
          var daten = new FormData(form), link = form.querySelector('.mail-rueckfall');
          var text = ['Anliegen: ' + daten.get('anliegen'), 'Name: ' + daten.get('name'), 'Telefon: ' + daten.get('telefon'), 'E-Mail: ' + daten.get('email'), 'Wunschzeit: ' + daten.get('wunschzeit'), '', daten.get('nachricht')].join('\n');
          zeige('Der Online-Versand ist gerade nicht möglich. Ihr Mailprogramm öffnet sich mit Ihren Angaben.', true);
          window.location.href = link.getAttribute('href') + '&body=' + encodeURIComponent(text);
        });
    });
  }
})();
