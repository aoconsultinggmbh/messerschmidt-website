#!/usr/bin/env python3
"""
bauen.py – baut alle Seiten der Hauptseite Zahnzentrum Messerschmidt nach website/.

Aufruf im Projektordner:  python3 quelltexte/bauen.py
Nur Python-Standardbibliothek. Texte stehen hier und in inhalt_leistungen.py.
Regeln: Sie-Ansprache, keine Gedankenstriche, keine Heilversprechen, keine externen Dateien.
"""
import hashlib, html, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from inhalt_leistungen import LEISTUNGEN
from inhalt_ratgeber import RATGEBER

PROJEKT = Path(__file__).resolve().parent.parent
WEB = PROJEKT / "website"
DOMAIN = "https://zahnzentrum-messerschmidt.de"
# Vor dem Livegang auf https://zahnzentrum-messerschmidt-karriere.de umstellen:
KARRIERE = "https://messerschmidt-karriere.vorschau.ao-consult.de/"
TEL, TEL_LINK = "06131 86926", "tel:+49613186926"
MAIL = "info@zahnzentrum-messerschmidt.de"
WA = "https://wa.me/4915154321140"
FIRMA = "Zahnzentrum Messerschmidt"
ADRESSE = ("Parkstraße 33", "55130 Mainz-Laubenheim")
ROUTE = "https://www.google.com/maps/dir/?api=1&destination=Parkstra%C3%9Fe%2033%2C%2055130%20Mainz"
HEUTE = __import__("datetime").date.today().isoformat()
GEO = (49.95324, 8.31060)  # OpenStreetMap, Eintrag „Zahnzentrum Messerschmidt“, Parkstraße 33 (06.10.2026)

PRAXIS_SCHEMA = {
    "@context": "https://schema.org", "@type": ["Dentist", "MedicalClinic"], "@id": DOMAIN + "/#praxis",
    "name": "Zahnzentrum Messerschmidt", "alternateName": "Zahnarztpraxis Dr. Sabine Messerschmidt",
    "description": "Zahnarztpraxis in Mainz-Laubenheim mit eigenem Dentallabor: Prophylaxe, Parodontologie, Implantologie, Endodontie, ästhetische Zahnheilkunde, Kinderzahnheilkunde, Funktionsdiagnostik und Oralchirurgie.",
    "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo-quer.png", "image": DOMAIN + "/assets/img/og-bild.jpg",
    "telephone": "+49 6131 86926", "faxNumber": "+49 6131 86936", "email": "info@zahnzentrum-messerschmidt.de",
    "address": {"@type": "PostalAddress", "streetAddress": "Parkstraße 33", "postalCode": "55130", "addressLocality": "Mainz",
                "addressRegion": "Rheinland-Pfalz", "addressCountry": "DE"},
    "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
    "hasMap": "https://www.openstreetmap.org/?mlat=49.95324&mlon=8.31060#map=18/49.95324/8.31060",
    "areaServed": [{"@type": "City", "name": "Mainz"}, {"@type": "Place", "name": "Mainz-Laubenheim"}],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "20:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "16:00"}],
    "foundingDate": "1995", "isAcceptingNewPatients": None,
    "medicalSpecialty": ["Dentistry", "Periodontics", "Endodontics"],
    "availableService": [],
    "sameAs": ["https://www.instagram.com/zahnzentrum_messerschmidt/", "https://www.facebook.com/zahnzentrummesserschmidt/"],
}
PRAXIS_SCHEMA.pop("isAcceptingNewPatients")

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def brotkrumen_schema(teile):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + "/" + u} for i, (n, u) in enumerate(teile)]}

def brotkrumen_html(teile, praefix=""):
    links = []
    for i, (n, u) in enumerate(teile):
        if i == len(teile) - 1:
            links.append(f'<span aria-current="page">{html.escape(n)}</span>')
        else:
            links.append(f'<a href="{praefix}{u or "index.html"}">{html.escape(n)}</a>')
    return '<nav class="wrap brotkrumen" aria-label="Brotkrümelnavigation">' + ' <span aria-hidden="true">/</span> '.join(links) + '</nav>'


ICONS = {
 "zahnbuerste": '<path d="M14 34l14-14M24 16l8 8M30 10l8 8"/><path d="M27 13l8-8 8 8-8 8"/><path d="M6 42l8-8"/>',
 "stern": '<path d="M24 5l5.5 12 13 1.5-9.7 8.8 2.7 12.9L24 33.8 12.5 40.2l2.7-12.9L5.5 18.5l13-1.5z"/>',
 "zahnfleisch": '<path d="M14 8c-5 0-8 4-8 9 0 6 3 9 4 15 1 7 3 10 5 10s3-5 4-10c1-3 3-3 5-3s4 0 5 3c1 5 2 10 4 10s4-3 5-10c1-6 4-9 4-15 0-5-3-9-8-9-4 0-6 2-10 2s-6-2-10-2z"/><path d="M6 20c6 3 30 3 36 0"/>',
 "implantat": '<path d="M16 6h16c2 0 3 2 3 4 0 5-3 7-11 7s-11-2-11-7c0-2 1-4 3-4z"/><path d="M19 21h10M20 26h8M21 31h6M22 36h4M24 17v25"/>',
 "wurzel": '<path d="M14 6c-5 0-8 4-8 9 0 7 4 10 5 17 1 6 2 10 4 10 3 0 3-8 6-12 1-2 4-2 6 0 3 4 3 12 6 12 2 0 3-4 4-10 1-7 5-10 5-17 0-5-3-9-8-9-4 0-6 2-10 2S18 6 14 6z"/><path d="M19 22c2 3 2 8 1 12M29 22c-2 3-2 8-1 12"/>',
 "kind": '<circle cx="24" cy="14" r="7"/><path d="M12 42c0-8 5-14 12-14s12 6 12 14"/><path d="M21 13h.1M27 13h.1M21 17c2 1.5 4 1.5 6 0"/>',
 "kiefer": '<path d="M8 14c0 14 7 26 16 26s16-12 16-26"/><path d="M8 14c4-4 10-6 16-6s12 2 16 6"/><path d="M16 24h16"/>',
 "herz": '<path d="M24 40S6 29 6 17c0-6 4-10 9-10 4 0 7 2 9 6 2-4 5-6 9-6 5 0 9 4 9 10 0 12-18 23-18 23z"/>',
 "skalpell": '<path d="M8 40L32 16l6 6-24 24z"/><path d="M32 16l6-10 4 4-6 12"/>',
 "telefon": '<path d="M14 6l6 1 3 8-4 3a22 22 0 0 0 11 11l3-4 8 3 1 6c0 3-3 5-6 5C20 39 9 28 9 12c0-3 2-6 5-6z"/>',
 "uhr": '<circle cx="24" cy="24" r="18"/><path d="M24 13v11l7 5"/>',
 "ort": '<path d="M24 43s-14-13-14-24a14 14 0 0 1 28 0c0 11-14 24-14 24z"/><circle cx="24" cy="19" r="5"/>',
 "labor": '<path d="M18 6h12M20 6v12L9 38c-1 3 1 5 4 5h22c3 0 5-2 4-5L28 18V6"/><path d="M14 30h20"/>',
 "blatt": '<path d="M10 38C10 18 24 8 40 8c0 16-10 30-30 30z"/><path d="M10 38L28 20"/>',
 "pfeil": '<path d="M10 24h28M28 14l10 10-10 10"/>',
 "download": '<path d="M24 6v24M14 20l10 10 10-10"/><path d="M8 34v6h32v-6"/>',
}
def icon(n, cls="ikon"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>'

def bild(name, alt, w, h, cls="", lazy=True, praefix=""):
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    k = ' class="' + cls + '"' if cls else ""
    return (f'<picture{k}><source srcset="{praefix}assets/img/{name}.webp" type="image/webp">'
            f'<img src="{praefix}assets/img/{name}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}"{l}></picture>')

NAVI = [("leistungen.html", "Leistungen"), ("praxis.html", "Praxis"), ("team.html", "Team"),
        ("neu-bei-uns.html", "Neu bei uns"), ("ratgeber.html", "Ratgeber"), ("kontakt.html", "Kontakt")]
GOOGLE_BEWERTUNGEN = "https://www.google.com/maps/search/?api=1&query=Zahnzentrum%20Messerschmidt%20Parkstra%C3%9Fe%2033%20Mainz"
TERMIN = "kontakt.html#anfrage"

def version(datei):
    """Kurzer Fingerabdruck der Datei, damit Browser nach jeder Änderung die neue CSS/JS laden."""
    return hashlib.md5((WEB / datei).read_bytes()).hexdigest()[:8]

def kopf(titel, beschr, pfad, praefix="", hell_start=False, body_klasse="", schema=None, og_bild="og-bild.jpg", vorladen=None):
    canon = f"{DOMAIN}/{pfad}" if pfad else f"{DOMAIN}/"
    akt = ' aria-current="page"'
    navi = "".join(f'<a href="{praefix}{h}"{akt if (h == pfad or pfad.startswith(h[:-5] + "/")) else ""}>{t}</a>' for h, t in NAVI)
    klasse = "kopf kopf-transparent" if hell_start else "kopf"
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titel)}</title>
<meta name="description" content="{html.escape(beschr)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{html.escape(titel)}">
<meta property="og:description" content="{html.escape(beschr)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/img/{og_bild}">
<meta property="og:site_name" content="{FIRMA}">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="DE-RP"><meta name="geo.placename" content="Mainz-Laubenheim"><meta name="geo.position" content="{GEO[0]};{GEO[1]}"><meta name="ICBM" content="{GEO[0]}, {GEO[1]}">
{f'<link rel="preload" as="image" href="{praefix}{vorladen}">' if vorladen else ""}
<meta name="theme-color" content="#0b1f33">
<link rel="icon" href="{praefix}assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{praefix}assets/img/apple-touch-icon.png">
<link rel="preload" href="{praefix}assets/fonts/manrope-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{praefix}assets/css/einwilligung.css?v={version("assets/css/einwilligung.css")}">
<link rel="stylesheet" href="{praefix}assets/css/barrierefreiheit.css?v={version("assets/css/barrierefreiheit.css")}">
<link rel="stylesheet" href="{praefix}assets/css/stil.css?v={version("assets/css/stil.css")}">
{jsonld(PRAXIS_SCHEMA)}
{"".join(jsonld(x) for x in (schema or []))}
</head>
<body class="{body_klasse}">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="{klasse}">
  <div class="wrap kopf-zeile">
    <a class="logo" href="{praefix}index.html" aria-label="{FIRMA}, zur Startseite">
      <img class="logo-farbe" src="{praefix}assets/img/logo-quer.png" alt="{FIRMA}" width="650" height="116">
      <img class="logo-weiss" src="{praefix}assets/img/logo-quer-weiss.png" alt="" width="650" height="116">
    </a>
    <nav class="hauptnavi" id="navi" aria-label="Hauptnavigation">
      {navi}
      <a href="{KARRIERE}" rel="noopener" target="_blank">Karriere</a>
    </nav>
    <span class="offen-anzeige kopf-offen" data-sprechzeit aria-live="polite"></span>
    <a class="knopf knopf-klein kopf-knopf" href="{TEL_LINK}">{icon("telefon","ikon-klein")}<span>{TEL}</span></a>
    <button class="navi-schalter" aria-expanded="false" aria-controls="navi" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="inhalt">
'''

def fuss(praefix=""):
    leist = "".join(f'<li><a href="{praefix}leistungen/{l["slug"]}.html">{html.escape(l["kurz"])}</a></li>' for l in LEISTUNGEN)
    return f'''</main>
<footer class="fuss">
  <div class="wrap fuss-raster">
    <div class="fuss-marke">
      <img src="{praefix}assets/img/logo-quer-weiss.png" alt="{FIRMA}" width="650" height="116">
      <p>Zahnmedizin mit Liebe zum Detail in Mainz-Laubenheim.</p>
    </div>
    <div>
      <p class="fuss-titel">Kontakt</p>
      <p>{ADRESSE[0]}<br>{ADRESSE[1]}</p>
      <p><a href="{TEL_LINK}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
      <p><a href="{ROUTE}" rel="noopener" target="_blank">Route planen</a></p>
    </div>
    <div>
      <p class="fuss-titel">Sprechzeiten</p>
      <p><span class="offen-anzeige" data-sprechzeit></span></p>
      <p>Montag bis Donnerstag<br>8:00 bis 20:00 Uhr</p>
      <p>Freitag<br>8:00 bis 16:00 Uhr</p>
      <p class="fuss-notdienst">Zahnärztlicher Notdienst<br><a href="tel:+4961316246999">06131 6246-999</a></p>
    </div>
    <div>
      <p class="fuss-titel">Leistungen</p>
      <ul class="fuss-liste">{leist}</ul>
    </div>
    <div>
      <p class="fuss-titel">Für Patienten</p>
      <ul class="fuss-liste">
        <li><a href="{praefix}neu-bei-uns.html">Neu bei uns</a></li>
        <li><a href="{praefix}patienteninfos.html">Patienteninfos</a></li>
        <li><a href="{praefix}ratgeber.html">Ratgeber</a></li>
        <li><a href="{praefix}{TERMIN}">Termin anfragen</a></li>
        <li><a href="{GOOGLE_BEWERTUNGEN}" rel="noopener" target="_blank">Bewertungen auf Google</a></li>
        <li><a href="{praefix}barrierefreiheit.html">Barrierefreiheit</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap fuss-unten">
    <p>© <span data-jahr>2026</span> {FIRMA} · <a href="{praefix}impressum.html">Impressum</a> · <a href="{praefix}datenschutz.html">Datenschutz</a><span data-einwilligung-huelle> · <button type="button" class="ein-ausloeser" data-einwilligung-oeffnen>Cookie-Einstellungen</button></span> · <a href="{praefix}barrierefreiheit.html">Barrierefreiheit</a> · <a href="{KARRIERE}" rel="noopener" target="_blank">Karriere</a></p>
    <p><a href="https://www.instagram.com/zahnzentrum_messerschmidt/" rel="noopener" target="_blank">Instagram</a> · <a href="https://www.facebook.com/zahnzentrummesserschmidt/" rel="noopener" target="_blank">Facebook</a> · made by <a href="https://ao-consult.de" rel="noopener">AO Consulting</a></p>
  </div>
</footer>
<nav class="schnellleiste" aria-label="Schnellzugriff">
  <a href="{TEL_LINK}">{icon("telefon","ikon-klein")}<span>Anrufen</span></a>
  <a href="{ROUTE}" rel="noopener" target="_blank">{icon("ort","ikon-klein")}<span>Route</span></a>
  <a href="{praefix}{TERMIN}">{icon("uhr","ikon-klein")}<span>Termin</span></a>
</nav>
<script src="{praefix}assets/js/ao-konfiguration.js?v={version("assets/js/ao-konfiguration.js")}" defer></script>
<script src="{praefix}assets/js/einwilligung.js?v={version("assets/js/einwilligung.js")}" defer></script>
<script src="{praefix}assets/js/barrierefreiheit.js?v={version("assets/js/barrierefreiheit.js")}" defer></script>
<script src="{praefix}assets/js/app.js?v={version("assets/js/app.js")}" defer></script>
<script src="{praefix}assets/js/statistik.js" defer></script>
</body>
</html>
'''

def termin_band(praefix=""):
    return f'''
<section class="band band-dunkel">
  <div class="wrap band-zeile">
    <div>
      <p class="dachzeile dachzeile-hell">Termin vereinbaren</p>
      <h2>Wir sind gerne für Sie da.</h2>
      <p>Montag bis Donnerstag von 8 bis 20 Uhr, freitags von 8 bis 16 Uhr.</p>
    </div>
    <div class="knoepfe">
      <a class="knopf" href="{TEL_LINK}">{icon("telefon","ikon-klein")} {TEL}</a>
      <a class="knopf knopf-rand-hell" href="{praefix}{TERMIN}">Termin anfragen</a>
    </div>
  </div>
</section>'''

def seitenkopf(dach, titel, text, bildname=None, alt="", praefix=""):
    b = (f'<div class="seitenkopf-bild" data-parallax>{bild(bildname, alt, 2000, 1000, lazy=False, praefix=praefix)}</div>' if bildname else "")
    return f'''
<section class="seitenkopf{" mit-bild" if bildname else ""}">
  {b}
  <div class="wrap seitenkopf-text">
    <p class="dachzeile dachzeile-hell">{dach}</p>
    <h1>{titel}</h1>
    <p class="lead">{text}</p>
  </div>
</section>'''

def schreibe(pfad, inhalt):
    p = WEB / pfad
    p.parent.mkdir(parents=True, exist_ok=True)
    if "–" in inhalt or "—" in inhalt:
        sys.exit(f"FEHLER: Gedankenstrich in {pfad}")
    p.write_text(inhalt, encoding="utf-8")

DOWNLOADS = [("anmeldebogen-zahnzentrum-messerschmidt.pdf", "Anmeldebogen", "Ihre Kontaktdaten und Versicherung"),
             ("gesundheitsfragebogen-zahnzentrum-messerschmidt.pdf", "Gesundheitsfragebogen", "Angaben zu Erkrankungen, Medikamenten und Allergien"),
             ("allgemeine-informationen-zahnzentrum-messerschmidt.pdf", "Allgemeine Informationen", "Termine, Kosten und Behandlungsvertrag")]
def downloads_html(praefix=""):
    return '<ul class="downloads">' + "".join(
        f'<li><a href="{praefix}downloads/{d}" download>{icon("download","ikon-klein")}<span><strong>{t}</strong><small>{x} · PDF</small></span></a></li>'
        for d, t, x in DOWNLOADS) + "</ul>"

def ratgeber_karten(praefix=""):
    import datetime as dt
    return "".join(f'''<a class="ratgeber-karte" href="{praefix}ratgeber/{r["slug"]}.html"><span class="klein">{dt.date.fromisoformat(r["datum"]).strftime("%d.%m.%Y")} · {r["lesezeit"]} Min. Lesezeit</span><h3>{html.escape(r["titel"])}</h3><p>{html.escape(r["kurz"][:150].rsplit(" ",1)[0])} …</p><span class="mehr">Weiterlesen {icon("pfeil","ikon-pfeil")}</span></a>'''
                   for r in sorted(RATGEBER, key=lambda r: r["datum"], reverse=True))

START_FAQ = [
  ("Wo liegt das Zahnzentrum Messerschmidt?", "Das Zahnzentrum liegt in der Parkstraße 33 in 55130 Mainz-Laubenheim. Die Einfahrt erreichen Sie über die Hans-Zöller-Straße 114, Parkplätze gibt es direkt am Haus. Die Buslinien 61, 63 und 64 halten an der Haltestelle Hans-Zöller-Straße."),
  ("Wann hat die Praxis geöffnet?", "Montag bis Donnerstag von 8 bis 20 Uhr durchgehend und freitags von 8 bis 16 Uhr. Termine nach Vereinbarung unter 06131 86926."),
  ("Welche Leistungen bietet das Zahnzentrum an?", "Prophylaxe und professionelle Zahnreinigung, ästhetische Zahnheilkunde, Parodontologie, Zahnersatz und Implantate, Endodontie, Kinder- und Jugendzahnheilkunde, Funktionsdiagnostik bei CMD und Oralchirurgie. Zahnersatz fertigen wir im eigenen Dentallabor."),
  ("Ich habe Angst vor dem Zahnarzt. Was kann ich tun?", "Sagen Sie es uns bei der Terminvereinbarung. Wir planen mehr Zeit ein, erklären jeden Schritt und bieten auf Wunsch begleitend Akupunktur an."),
  ("Ab wann kann ich mit meinem Kind kommen?", "Sobald die ersten Milchzähne da sind. So lernt Ihr Kind die Praxis ganz entspannt kennen."),
  ("Was mache ich bei Zahnschmerzen am Wochenende?", "Außerhalb unserer Sprechzeiten erreichen Sie den zahnärztlichen Notdienst unter 06131 6246-999."),
]

# ---------------------------------------------------------------- Startseite
def startseite():
    karten = "".join(f'''
      <a class="leistung-karte" href="leistungen/{l["slug"]}.html">
        {icon(l["icon"])}
        <h3>{html.escape(l["kurz"])}</h3>
        <p>{html.escape(l["teaser"])}</p>
        <span class="mehr">Mehr erfahren {icon("pfeil","ikon-pfeil")}</span>
      </a>''' for l in LEISTUNGEN)
    s = kopf("Zahnarzt Mainz-Laubenheim | Zahnzentrum Messerschmidt",
             "Zahnzentrum Messerschmidt in Mainz-Laubenheim: Prophylaxe, Implantate, Parodontologie, Ästhetik, Kinderzahnheilkunde und eigenes Dentallabor. Mo bis Do bis 20 Uhr.",
             "", hell_start=True, body_klasse="startseite", vorladen="assets/video/hero-poster.jpg",
             schema=[{"@context": "https://schema.org", "@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": FIRMA, "inLanguage": "de-DE", "publisher": {"@id": DOMAIN + "/#praxis"}},
                     {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in START_FAQ]}])
    s += f'''
<section class="hero" aria-labelledby="hero-titel">
  <video class="hero-video" autoplay muted loop playsinline preload="metadata" poster="assets/video/hero-poster.jpg" aria-hidden="true">
    <source src="assets/video/hero.webm" type="video/webm">
    <source src="assets/video/hero.mp4" type="video/mp4">
  </video>
  <div class="hero-schleier"></div>
  <div class="wrap hero-inhalt">
    <p class="dachzeile dachzeile-hell">Zahnzentrum Messerschmidt · Mainz-Laubenheim</p>
    <h1 id="hero-titel"><span class="zeile"><span>Kompetenz</span></span><span class="zeile"><span>im Detail.</span></span></h1>
    <p class="hero-unterzeile">Moderne Zahnmedizin in einem hellen, eigens gebauten Haus. Für Ihr Lächeln, ein Leben lang.</p>
    <div class="knoepfe">
      <a class="knopf" href="{TERMIN}">Termin anfragen</a>
      <a class="knopf knopf-rand-hell" href="leistungen.html">Leistungen entdecken</a>
    </div>
  </div>
  <button class="video-schalter" type="button" aria-label="Video anhalten" aria-pressed="false"><span></span></button>
  <a class="hero-runter" href="#willkommen" aria-label="Weiter nach unten"></a>
</section>

<section class="fakten-leiste" aria-label="Auf einen Blick">
  <div class="wrap fakten-raster">
    <div><strong><span data-zaehler="30">30</span>+ Jahre</strong><span>in Mainz-Laubenheim</span></div>
    <div><strong><span data-zaehler="4">4</span> Zimmer</strong><span>modern ausgestattet</span></div>
    <div><strong>Eigenes Labor</strong><span>Zahnersatz aus dem Haus</span></div>
    <div><strong>Bis <span data-zaehler="20">20</span> Uhr</strong><span>Montag bis Donnerstag</span></div>
  </div>
</section>

<section id="willkommen" class="wrap abschnitt zwei">
  <div class="text-spalte">
    <p class="dachzeile">Willkommen</p>
    <h2>Zahnmedizin, wie wir sie uns selbst wünschen.</h2>
    <p>Unser Team um Zahnärztin Dr. Sabine Messerschmidt freut sich, Sie im Zahnzentrum zu begrüßen. Wir verbinden fachliche Kompetenz mit großer Sorgfalt, viel Engagement und einem Lächeln.</p>
    <p>Für uns stehen Sie als Mensch im Mittelpunkt. Deshalb nehmen wir uns Zeit für Beratung, erklären jeden Schritt und sorgen für eine angenehme Atmosphäre, vom ersten Milchzahn bis zum hochwertigen Zahnersatz.</p>
    <a class="mehr" href="team.html">Unser Team kennenlernen {icon("pfeil","ikon-pfeil")}</a>
  </div>
  <figure class="bild-hoch">{bild("start-sabine", "Dr. Sabine Messerschmidt, Zahnärztin und Praxisinhaberin", 900, 1125)}<figcaption>Dr. med. Sabine Messerschmidt<span>Zahnärztin, Praxisinhaberin</span></figcaption></figure>
</section>

<section class="aussage aussage-bild" aria-label="Unser Leitsatz">
  <div class="aussage-hg" data-parallax>{bild("start-haende", "", 1920, 1280)}</div>
  <div class="wrap"><p class="aussage-text" data-woerter>Bei uns steckt die Kompetenz im Detail. Kleine Teile ergeben das große Ganze: moderne Technik, erfahrene Zahnärztinnen und ein Team, das Sie mit einem Lächeln empfängt.</p></div>
</section>

<section class="abschnitt flaeche">
  <div class="wrap">
    <div class="abschnitt-kopf">
      <p class="dachzeile">Leistungen</p>
      <h2>Alles für gesunde und schöne Zähne.</h2>
      <p>Von der Vorsorge über Implantate bis zur Kinderzahnheilkunde. Unsere Zahnärztinnen bilden sich laufend fort, damit Sie von modernen Methoden profitieren.</p>
    </div>
    <div class="leistungen-raster">{karten}
    </div>
  </div>
</section>

<div class="laufband" aria-hidden="true"><div class="laufband-spur"><span>Prophylaxe</span><i aria-hidden="true">✦</i><span>Implantologie</span><i aria-hidden="true">✦</i><span>Parodontologie</span><i aria-hidden="true">✦</i><span>Ästhetik</span><i aria-hidden="true">✦</i><span>Endodontie</span><i aria-hidden="true">✦</i><span>Kinderzahnheilkunde</span><i aria-hidden="true">✦</i><span>Funktionsdiagnostik</span><i aria-hidden="true">✦</i><span>Oralchirurgie</span><i aria-hidden="true">✦</i><span>Eigenes Dentallabor</span><i aria-hidden="true">✦</i><span>Prophylaxe</span><i aria-hidden="true">✦</i><span>Implantologie</span><i aria-hidden="true">✦</i><span>Parodontologie</span><i aria-hidden="true">✦</i><span>Ästhetik</span><i aria-hidden="true">✦</i><span>Endodontie</span><i aria-hidden="true">✦</i><span>Kinderzahnheilkunde</span><i aria-hidden="true">✦</i><span>Funktionsdiagnostik</span><i aria-hidden="true">✦</i><span>Oralchirurgie</span><i aria-hidden="true">✦</i><span>Eigenes Dentallabor</span><i aria-hidden="true">✦</i></div></div>

<section class="abschnitt bild-band">
  <div class="bild-band-bild" data-parallax>{bild("start-haus", "Das Zahnzentrum Messerschmidt in der Parkstraße in Mainz-Laubenheim", 1600, 1067)}</div>
  <div class="wrap bild-band-text">
    <div class="karte-glas">
      <p class="dachzeile">Unsere Praxis</p>
      <h2>Ein Haus, gebaut für Ihr Wohlbefinden.</h2>
      <p>Unsere Praxis liegt in einem eigens dafür errichteten Niedrigenergiehaus. Große Fenster, helle Räume und eine eigene Solaranlage: Nachhaltigkeit ist uns wichtig, bei den Räumen genauso wie bei der Behandlung.</p>
      <a class="mehr" href="praxis.html">Die Praxis entdecken {icon("pfeil","ikon-pfeil")}</a>
    </div>
  </div>
</section>

<div class="laufband laufband-rueck" aria-hidden="true"><div class="laufband-spur"><span>Eigenes Dentallabor</span><i aria-hidden="true">✦</i><span>Kinderzahnheilkunde</span><i aria-hidden="true">✦</i><span>Implantologie</span><i aria-hidden="true">✦</i><span>Prophylaxe</span><i aria-hidden="true">✦</i><span>Oralchirurgie</span><i aria-hidden="true">✦</i><span>Ästhetik</span><i aria-hidden="true">✦</i><span>Parodontologie</span><i aria-hidden="true">✦</i><span>Funktionsdiagnostik</span><i aria-hidden="true">✦</i><span>Endodontie</span><i aria-hidden="true">✦</i><span>Eigenes Dentallabor</span><i aria-hidden="true">✦</i><span>Kinderzahnheilkunde</span><i aria-hidden="true">✦</i><span>Implantologie</span><i aria-hidden="true">✦</i><span>Prophylaxe</span><i aria-hidden="true">✦</i><span>Oralchirurgie</span><i aria-hidden="true">✦</i><span>Ästhetik</span><i aria-hidden="true">✦</i><span>Parodontologie</span><i aria-hidden="true">✦</i><span>Funktionsdiagnostik</span><i aria-hidden="true">✦</i><span>Endodontie</span><i aria-hidden="true">✦</i></div></div>

<section class="wrap abschnitt zwei umgekehrt">
  <div class="text-spalte">
    <p class="dachzeile">Angst vor dem Zahnarzt?</p>
    <h2>Bei uns dürfen Sie entspannt sein.</h2>
    <p>Sprechen Sie Ihre Sorgen schon bei der Terminvereinbarung an. Wir planen mehr Zeit ein, erklären jeden Schritt und sorgen für eine ruhige Atmosphäre. Auf Wunsch bieten wir begleitend Akupunktur an.</p>
    <a class="mehr" href="leistungen/stressfreier-besuch.html">Mehr für Angstpatienten {icon("pfeil","ikon-pfeil")}</a>
  </div>
  <figure class="bild-quer">{bild("start-angst", "Freundliche Mitarbeiterin am Empfang des Zahnzentrums", 1400, 933)}</figure>
</section>

<section class="abschnitt karriere-teaser">
  <div class="wrap zwei">
    <figure class="bild-quer">{bild("start-karriere", "Zahnärztin und Kollegin im hellen Behandlungszimmer", 1400, 933)}</figure>
    <div class="text-spalte">
      <p class="dachzeile dachzeile-hell">Karriere</p>
      <h2>Werden Sie Teil unseres Teams.</h2>
      <p>Wir suchen ZFA, ZMP und ZMF sowie Auszubildende. Es erwarten Sie nette Kolleginnen, moderne Räume und flexible Arbeitszeiten.</p>
      <a class="knopf knopf-hell" href="{KARRIERE}" rel="noopener" target="_blank">Zu den offenen Stellen</a>
    </div>
  </div>
</section>

<section class="abschnitt bewertungen bewertungen-bild">
  <div class="bewertungen-hg" data-parallax>{bild("start-luftbild", "", 1920, 1080)}</div>
  <div class="wrap bewertungen-zeile">
    <div>
      <p class="dachzeile dachzeile-hell">Bewertungen</p>
      <h2>Was unsere Patienten sagen.</h2>
      <p>Lesen Sie, wie andere Patienten ihren Besuch im Zahnzentrum erlebt haben. Und wenn Sie zufrieden waren: Ihre Bewertung hilft anderen Menschen bei der Suche nach einer Zahnarztpraxis.</p>
    </div>
    <div class="bewertungen-karte">
      <div class="sterne" aria-hidden="true">★★★★★</div>
      <p><strong>Zahnzentrum Messerschmidt auf Google</strong><br>Bewertungen lesen oder selbst eine abgeben</p>
      <a class="knopf" href="{GOOGLE_BEWERTUNGEN}" rel="noopener" target="_blank">Bewertungen auf Google</a>
      <p class="klein">Der Link öffnet Google Maps. Auf dieser Seite werden keine Inhalte von Google geladen.</p>
    </div>
  </div>
</section>

<section class="wrap abschnitt">
  <div class="abschnitt-kopf">
    <p class="dachzeile">Ratgeber</p>
    <h2>Wissen für gesunde Zähne.</h2>
  </div>
  <div class="ratgeber-raster">{ratgeber_karten("")}</div>
  <p style="margin-top:28px"><a class="mehr" href="ratgeber.html">Alle Artikel {icon("pfeil","ikon-pfeil")}</a></p>
</section>

<section class="wrap abschnitt zwei faq-start">
  <div class="text-spalte">
    <p class="dachzeile">Häufige Fragen</p>
    <h2>Gut zu wissen.</h2>
    <p>Die wichtigsten Antworten rund um Ihren Besuch im Zahnzentrum Messerschmidt in Mainz-Laubenheim.</p>
  </div>
  <div class="faq-liste">{"".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in START_FAQ)}</div>
</section>

<section class="wrap abschnitt kontakt-kurz">
  <div class="kontakt-kacheln">
    <div class="kachel">{icon("ort")}<h3>Anfahrt</h3><p>{ADRESSE[0]}<br>{ADRESSE[1]}<br>Einfahrt über die Hans-Zöller-Straße 114, Parkplätze direkt am Haus.</p><a class="mehr" href="kontakt.html#anfahrt">Anfahrt ansehen {icon("pfeil","ikon-pfeil")}</a></div>
    <div class="kachel">{icon("uhr")}<h3>Sprechzeiten</h3><p><span class="offen-anzeige" data-sprechzeit></span></p><p>Montag bis Donnerstag<br>8:00 bis 20:00 Uhr durchgehend<br>Freitag 8:00 bis 16:00 Uhr</p><a class="mehr" href="{TERMIN}">Termin anfragen {icon("pfeil","ikon-pfeil")}</a></div>
    <div class="kachel">{icon("telefon")}<h3>Kontakt</h3><p><a href="{TEL_LINK}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p><p class="klein">Notdienst außerhalb der Sprechzeiten:<br><a href="tel:+4961316246999">06131 6246-999</a></p><a class="mehr" href="kontakt.html#anfrage">Anfrage senden {icon("pfeil","ikon-pfeil")}</a></div>
  </div>
</section>
'''
    s += fuss()
    schreibe("index.html", s)

# ---------------------------------------------------------------- Leistungen
def leistungen():
    karten = "".join(f'''
      <a class="leistung-karte" href="leistungen/{l["slug"]}.html">
        {icon(l["icon"])}
        <h3>{html.escape(l["kurz"])}</h3>
        <p>{html.escape(l["teaser"])}</p>
        <span class="mehr">Mehr erfahren {icon("pfeil","ikon-pfeil")}</span>
      </a>''' for l in LEISTUNGEN)
    s = kopf("Zahnarzt-Leistungen Mainz | Zahnzentrum Messerschmidt",
             "Unsere Leistungen: Prophylaxe, Ästhetik, Parodontologie, Zahnersatz und Implantate, Endodontie, Kinderzahnheilkunde, Funktionsdiagnostik, Oralchirurgie.",
             "leistungen.html", schema=[brotkrumen_schema([("Startseite", ""), ("Leistungen", "leistungen.html")])])
    s += brotkrumen_html([("Startseite", ""), ("Leistungen", "leistungen.html")])
    s += seitenkopf("Leistungen", "Ihre Zahngesundheit hat oberste Priorität.",
                    "Wir verbinden Qualifikation mit moderner Technik. Unsere Zahnärztinnen haben Zusatzqualifikationen in Implantologie, Parodontologie, Endodontie, ästhetischer Zahnheilkunde und Akupunktur. Zahnersatz fertigen wir im eigenen Dentallabor.")
    s += f'''
<section class="wrap abschnitt">
  <h2 class="sr-only">Unsere Leistungen im Überblick</h2>
  <div class="leistungen-raster">{karten}
  </div>
  <div class="hinweis-box">
    <h2>Außerdem bei uns</h2>
    <ul class="haken-liste spalten">
      <li>Fluoridierung und Ernährungsberatung</li><li>Komposit-Füllungen in Zahnfarbe</li><li>Kronen, Brücken und Inlays aus Keramik oder Gold</li>
      <li>Laserbehandlung, zum Beispiel in der Parodontitistherapie</li><li>Akupunktur begleitend zur Behandlung</li><li>Aufbissschienen in Zusammenarbeit mit Meisterlaboren</li>
    </ul>
    <p>Sie vermissen etwas? Sprechen Sie uns gerne an.</p>
  </div>
</section>'''
    s += termin_band() + fuss()
    schreibe("leistungen.html", s)

    for i, l in enumerate(LEISTUNGEN):
        pfad = f'leistungen/{l["slug"]}.html'
        brot = [("Startseite", ""), ("Leistungen", "leistungen.html"), (l["kurz"], pfad)]
        abschn = "".join(f'<section class="text-block"><h2>{html.escape(t)}</h2><p>{html.escape(p)}</p></section>' for t, p in l["abschnitte"])
        ablauf = "".join(f'<li><strong>{html.escape(t)}</strong><span>{html.escape(x)}</span></li>' for t, x in l["ablauf"])
        fuer = "".join(f"<li>{html.escape(x)}</li>" for x in l["fuer_wen"])
        faq = "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in l["faq"])
        aerzt = [Z_NACH_SCHLUESSEL[k] for k in l["aerztinnen"]]
        aerzt_html = ("<section class=\"text-block\"><h2>Ihre Ansprechpartnerinnen</h2><ul class=\"aerztin-chips\">"
                      + "".join(f'<li><a href="../team.html#{z["key"]}"><strong>{html.escape(z["name"])}</strong><span>{html.escape(z["schwerpunkte"][0])}</span></a></li>' for z in aerzt)
                      + "</ul></section>") if aerzt else ""
        verwandt = "".join(f'<a class="verwandt-karte" href="{x["slug"]}.html">{icon(x["icon"],"ikon-klein")}<span>{html.escape(x["kurz"])}</span></a>'
                           for x in LEISTUNGEN if x["slug"] in l["verwandt"])
        andere = "".join(f'<li><a href="{x["slug"]}.html">{icon(x["icon"],"ikon-klein")}<span>{html.escape(x["kurz"])}</span></a></li>' for x in LEISTUNGEN if x is not l)
        schema = [brotkrumen_schema(brot),
                  {"@context": "https://schema.org", "@type": "MedicalWebPage", "@id": f"{DOMAIN}/{pfad}#seite", "url": f"{DOMAIN}/{pfad}",
                   "name": l["titel"], "description": l["beschreibung"], "inLanguage": "de-DE", "lastReviewed": HEUTE,
                   "about": {"@type": "MedicalProcedure", "name": l["titel"], "description": l["kurz_erklaert"]},
                   "publisher": {"@id": DOMAIN + "/#praxis"}, "isPartOf": {"@id": DOMAIN + "/#website"},
                   "mainEntity": {"@type": "Service", "name": l["titel"], "serviceType": l["kurz"], "provider": {"@id": DOMAIN + "/#praxis"},
                                  "areaServed": {"@type": "City", "name": "Mainz"}}},
                  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in l["faq"]]}]
        s = kopf(f'{l["seo"]} | {FIRMA}', l["beschreibung"], pfad, praefix="../", schema=schema)
        s += brotkrumen_html(brot, praefix="../")
        s += seitenkopf(f'Leistungen · {html.escape(l["kurz"])}', html.escape(l["titel"]), html.escape(l["intro"]), praefix="../")
        s += f'''
<div class="wrap abschnitt leistung-raster">
  <article class="leistung-text">
    <aside class="kurz-erklaert" aria-label="Kurz erklärt"><p class="klein-titel">Kurz erklärt</p><p>{html.escape(l["kurz_erklaert"])}</p></aside>
    {abschn}
    <section class="text-block"><h2>So läuft die Behandlung ab</h2><ol class="ablauf">{ablauf}</ol></section>
    <section class="text-block"><h2>Für wen ist das sinnvoll?</h2><ul class="haken-liste">{fuer}</ul></section>
    {aerzt_html}
    <section class="text-block faq-liste"><h2>Häufige Fragen</h2>{faq}</section>
    <section class="text-block"><h2>Das könnte Sie auch interessieren</h2><div class="verwandt">{verwandt}</div></section>
  </article>
  <aside class="leistung-seite" aria-label="Kontakt und weitere Leistungen">
    <div class="cta-karte">
      <p class="klein-titel">Haben Sie Fragen?</p>
      <p>Wir beraten Sie gerne persönlich in unserer Praxis in Mainz-Laubenheim.</p>
      <a class="knopf" href="{TEL_LINK}">{icon("telefon","ikon-klein")} {TEL}</a>
      <a class="knopf knopf-rand" href="../kontakt.html#anfrage">Anfrage senden</a>
      <p class="klein">Mo bis Do 8 bis 20 Uhr, Fr 8 bis 16 Uhr</p>
    </div>
    <p class="dachzeile">Weitere Leistungen</p>
    <ul class="leistung-menue">{andere}</ul>
  </aside>
</div>'''
        s += fuss(praefix="../")
        schreibe(pfad, s)

# ---------------------------------------------------------------- Praxis
def praxis():
    s = kopf("Unsere Praxis in Mainz-Laubenheim | Zahnzentrum Messerschmidt",
             "Das Zahnzentrum Messerschmidt: eigens gebautes Niedrigenergiehaus, helle Räume, eigenes Dentallabor und Service, der Wohlfühlen leicht macht.",
             "praxis.html", schema=[brotkrumen_schema([("Startseite", ""), ("Praxis", "praxis.html")])])
    s += brotkrumen_html([("Startseite", ""), ("Praxis", "praxis.html")])
    s += seitenkopf("Praxis", "Ein Haus, gebaut für Ihr Wohlbefinden.",
                    "Weiß gekachelte Wände suchen Sie bei uns vergeblich. Unsere Praxis liegt in einem eigens dafür errichteten, nachhaltigen Haus mit viel Licht und freundlicher Atmosphäre.",
                    "praxis-kopf", "Das Zahnzentrum Messerschmidt von oben mit Solaranlage auf dem Dach")
    s += f'''
<section class="wrap abschnitt zwei">
  <div class="text-spalte">
    <p class="dachzeile">Architektur</p>
    <h2>Modern, nachhaltig und hell.</h2>
    <p>Unsere Praxisräume liegen in einem Niedrigenergiehaus, bei dem von Anfang an auf hochwertige und nachhaltige Baustoffe geachtet wurde. Wir heizen und kühlen klimaneutral, und unsere Solaranlage erzeugt bis zu 50 Prozent der Energie, die wir brauchen.</p>
    <p>Großzügige Räume, große Fensterflächen und eine angenehme Beleuchtung fügen sich zu einem stimmigen Gesamtbild. Vier moderne Behandlungszimmer sind mit aktueller Technik ausgestattet.</p>
  </div>
  <figure class="bild-quer">{bild("praxis-gebaeude", "Das moderne Gebäude des Zahnzentrums", 1200, 800)}</figure>
</section>

<section class="abschnitt flaeche">
  <div class="wrap zwei umgekehrt">
    <div class="text-spalte">
      <p class="dachzeile">Wohlfühlen</p>
      <h2>Eine Atmosphäre, in der man gerne wartet.</h2>
      <p>Unsere Wartelounge ist hell und großzügig. Für die Kleinen gibt es eine Leseecke mit Kinderbüchern, größere Kinder vertreiben sich die Zeit in der TV-Ecke. Gerne reichen wir Ihnen ein Getränk. Lange warten müssen Sie aber nicht: Kurze Wartezeiten gehören für uns zur Qualität.</p>
    </div>
    <figure class="bild-quer">{bild("praxis-hell", "Zwei Mitarbeiterinnen in einem hellen Behandlungszimmer", 1200, 800)}</figure>
  </div>
</section>

<section class="wrap abschnitt">
  <div class="drei-kacheln">
    <div class="kachel">{icon("labor")}<h3>Eigenes Dentallabor</h3><p>Kronen, Brücken und Inlays aus Keramik oder Gold fertigen wir im eigenen Haus, individuell und passgenau. So können wir flexibel reagieren und kurzfristig anpassen. Für besondere Arbeiten kooperieren wir mit deutschen Meisterlaboren.</p></div>
    <div class="kachel">{icon("herz")}<h3>Service und Qualität</h3><p>Ausführliche Beratung vor und nach jeder Behandlung ist für uns selbstverständlich. Unser Team bildet sich laufend fort, damit Sie von aktuellen Methoden profitieren.</p></div>
    <div class="kachel">{icon("kind")}<h3>Patenschaft für Kindergärten</h3><p>Als Patenschaftszahnarzt betreuen wir zwei Kindergärten in Mainz-Laubenheim. Die Kinder erkunden unsere Praxis spielerisch, damit der Zahnarzt ein Freund wird.</p></div>
  </div>
</section>

<section class="wrap abschnitt zwei">
  <figure class="bild-quer">{bild("praxis-empfang", "Mitarbeiterin am Empfang des Zahnzentrums", 1200, 800)}</figure>
  <div class="text-spalte">
    <p class="dachzeile">Empfang</p>
    <h2>Herzlich willkommen.</h2>
    <p>Am Empfang kümmern wir uns um Ihre Termine und alle Fragen rund um Ihren Besuch. Rufen Sie uns an unter <a href="{TEL_LINK}">{TEL}</a> oder schreiben Sie uns an <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </div>
</section>'''
    s += termin_band() + fuss()
    schreibe("praxis.html", s)

# ---------------------------------------------------------------- Team
ZAHNAERZTINNEN = [
  dict(key="messerschmidt", name="Dr. med. Sabine Messerschmidt", rolle="Zahnärztin, Praxisinhaberin", foto="team-sabine",
       schwerpunkte=["Komplexe prothetisch-chirurgische Rekonstruktionen", "Regenerative Parodontaltherapie und Parodontalchirurgie", "Augmentationschirurgie und Implantologie", "Ganzheitliche Zahnheilkunde"],
       vita=["Studium der Zahnheilkunde in Jena und Erfurt", "1991 Approbation, 1993 Promotion", "1995 Gründung der Praxis in Mainz-Laubenheim", "2009 Gründung des Zahnzentrums Messerschmidt",
             "Tätigkeitsschwerpunkte Akupunktur (1996), Implantologie DGI und APW (2002), Parodontologie (2012), Endodontologie und Ästhetische Zahnheilkunde (2014)", "Seit 2012 Referentin für Fortbildungen von Kolleginnen und Kollegen"]),
  dict(key="miller", name="Olga Miller, MSc", rolle="Zahnärztin", foto=None,
       schwerpunkte=["Komplexe endodontische Behandlungen", "Ganzheitliche Zahnheilkunde", "Prothetische Sanierungen"],
       vita=["Studium der Zahnmedizin in Göttingen, 2010 Approbation", "2018 Tätigkeitsschwerpunkt Endodontologie und Qualifikation zur Lachgassedierung", "2020 Fachkunde digitale Volumentomographie", "Seit 2024 Master für Implantologie und Parodontologie, Universität Krems"]),
  dict(key="blatt", name="Dr. med. dent. Lisa Blatt", rolle="Zahnärztin", foto=None,
       schwerpunkte=["Zahnerhaltung, präventiv und restaurativ", "Ästhetische Zahnheilkunde"],
       vita=["Studium der Zahnmedizin an der Universität Mainz, 2015 Approbation", "2017 Promotion", "Seit 2023 Lehrkraft an der Berufsbildenden Schule 3 in Mainz", "Seit 2024 im Zahnzentrum Messerschmidt"]),
  dict(key="guenther", name="Dr. med. dent. Alina Günther", rolle="Zahnärztin", foto=None,
       schwerpunkte=["Komplexe endodontologische Behandlungen", "Konservierend-chirurgische Behandlungen", "Ganzheitliche Zahnheilkunde"],
       vita=["Studium der Zahnheilkunde in Frankfurt am Main, 2019 Approbation", "Promotion an der MKG-Universitätsklinik Frankfurt", "2023 Hilfseinsatz mit Zahnärzte ohne Grenzen", "Seit 2025 im Zahnzentrum Messerschmidt"]),
]
Z_NACH_SCHLUESSEL = {z["key"]: z for z in ZAHNAERZTINNEN}

def team():
    karten = []
    for z in ZAHNAERZTINNEN:
        if z["foto"]:
            f = bild(z["foto"], z["name"], 900, 1125)
        else:
            ini = "".join(w[0] for w in z["name"].replace("Dr. med. dent. ", "").replace("Dr. med. ", "").replace(", MSc", "").split()[:2])
            f = '<div class="platzhalter-foto"><span>Foto wird<br>nachgereicht</span></div>'
        karten.append(f'''
    <article class="person" id="{z["key"]}">
      <div class="person-bild">{f}</div>
      <div class="person-text">
        <h3>{html.escape(z["name"])}</h3>
        <p class="rolle">{html.escape(z["rolle"])}</p>
        <p class="klein-titel">Schwerpunkte</p>
        <ul class="haken-liste">{"".join(f"<li>{html.escape(x)}</li>" for x in z["schwerpunkte"])}</ul>
        <details><summary>Werdegang</summary><ul>{"".join(f"<li>{html.escape(x)}</li>" for x in z["vita"])}</ul></details>
      </div>
    </article>''')
    s = kopf("Zahnärztinnen & Team | Zahnzentrum Messerschmidt",
             "Lernen Sie unsere Zahnärztinnen kennen: Dr. Sabine Messerschmidt, Olga Miller, Dr. Lisa Blatt und Dr. Alina Günther, dazu unser Praxisteam.",
             "team.html", schema=[brotkrumen_schema([("Startseite", ""), ("Team", "team.html")])] + [
                 {"@context": "https://schema.org", "@type": "Person", "@id": f'{DOMAIN}/team.html#{z["key"]}', "name": z["name"], "jobTitle": z["rolle"],
                  "worksFor": {"@id": DOMAIN + "/#praxis"}, "knowsAbout": z["schwerpunkte"]} for z in ZAHNAERZTINNEN])
    s += brotkrumen_html([("Startseite", ""), ("Team", "team.html")])
    s += seitenkopf("Team", "Modern, kompetent und herzlich.",
                    "Vier Zahnärztinnen und ein engagiertes Team in Anmeldung, Prophylaxe und Assistenz geben jeden Tag ihr Bestes für Ihre Zähne.",
                    "team-kopf", "Das Team des Zahnzentrums Messerschmidt im Behandlungszimmer")
    s += f'''
<section class="wrap abschnitt">
  <div class="abschnitt-kopf">
    <p class="dachzeile">Zahnärztinnen</p>
    <h2>Ihre Behandlerinnen.</h2>
  </div>
  <div class="personen">{"".join(karten)}
  </div>
</section>

<section class="wrap abschnitt team-raster-abschnitt">
  <div class="abschnitt-kopf">
    <p class="dachzeile">Praxisteam</p>
    <h2>Die Gesichter hinter Ihrer Behandlung.</h2>
  </div>
  <div class="team-raster">
    {"".join(f'<figure class="team-person">{bild(n, "Mitarbeiterin des Zahnzentrums Messerschmidt", 720, 900)}<figcaption><strong>Name wird nachgereicht</strong><span>Funktion wird nachgereicht</span></figcaption></figure>' for n in ("team-person-1","team-person-2","team-person-3","team-person-4"))}
  </div>
</section>

<section class="abschnitt flaeche">
  <div class="wrap zwei">
    <figure class="bild-quer">{bild("team-duo", "Zwei Kolleginnen des Zahnzentrums", 1200, 800)}</figure>
    <div class="text-spalte">
      <p class="dachzeile">Praxisteam</p>
      <h2>Anmeldung, Prophylaxe und Assistenz.</h2>
      <p>Hinter jeder Behandlung steht ein ganzes Team: Zahnmedizinische Fachangestellte, Fachassistentinnen und Prophylaxeassistentinnen kümmern sich um Ihre Termine, Ihre Vorsorge und begleiten Sie am Behandlungsstuhl. Und wir bilden selbst aus.</p>
      <a class="mehr" href="{KARRIERE}" rel="noopener" target="_blank">Bei uns arbeiten {icon("pfeil","ikon-pfeil")}</a>
    </div>
  </div>
</section>'''
    s += termin_band() + fuss()
    schreibe("team.html", s)

# ---------------------------------------------------------------- Patienteninfos
def patienteninfos():
    s = kopf("Patienteninfos | Zahnzentrum Messerschmidt Mainz",
             "Ihr erster Besuch im Zahnzentrum Messerschmidt: was Sie mitbringen sollten und worauf Sie nach einem chirurgischen Eingriff achten.",
             "patienteninfos.html", schema=[brotkrumen_schema([("Startseite", ""), ("Patienteninfos", "patienteninfos.html")])])
    s += brotkrumen_html([("Startseite", ""), ("Patienteninfos", "patienteninfos.html")])
    s += seitenkopf("Patienteninfos", "Gut vorbereitet zu Ihrem Termin.",
                    "Hier finden Sie die wichtigsten Informationen für Ihren ersten Besuch und für die Zeit nach einem Eingriff.")
    s += f'''
<section class="wrap abschnitt zwei-text">
  <div class="kachel">
    <h2>Ihr erster Besuch</h2>
    <p>Für den ersten Besuch benötigen wir einen ausgefüllten Anamnesebogen mit Angaben zu Ihrer Gesundheit, zu Allergien und Medikamenten. So können wir Befunde besser einschätzen und die passende Behandlung planen.</p>
    <p>Die Bögen können Sie vorab herunterladen, zu Hause ausfüllen und zum ersten Termin mitbringen. Alles zum ersten Besuch finden Sie auf unserer Seite <a href="neu-bei-uns.html">Neu bei uns</a>.</p>
    {downloads_html("")}
    <p class="klein-titel">Bitte bringen Sie mit</p>
    <ul class="haken-liste">
      <li>Ihre Gesundheitskarte</li><li>gegebenenfalls Ihre Medikationsliste</li><li>gegebenenfalls Röntgenpass und Allergiepass</li>
    </ul>
  </div>
  <div class="kachel">
    <h2>Nach einem chirurgischen Eingriff</h2>
    <ul class="haken-liste">
      <li>Verzichten Sie direkt nach dem Eingriff auf Sport und körperliche Anstrengung.</li>
      <li>Essen Sie erst, wenn die Betäubung nachgelassen hat. Meiden Sie heiße oder scharfe Speisen, heiße Getränke, Milchprodukte, Kaffee, Alkohol und Zigaretten.</li>
      <li>Putzen Sie Ihre Zähne weiter, aber sparen Sie die Wunde aus.</li>
      <li>Bei Nachblutungen drücken Sie ein sauberes Tuch oder eine Mullbinde auf die Wunde. Hört die Blutung nach ein bis zwei Stunden nicht auf, rufen Sie uns an.</li>
      <li>Nach einer Narkose fahren Sie 12 bis 24 Stunden nicht selbst Auto.</li>
      <li>Nehmen Sie keine Schmerzmittel mit Acetylsalicylsäure (ASS), sie können Nachblutungen verstärken.</li>
    </ul>
    <p>Treten Schmerzen erst zwei bis drei Tage nach dem Eingriff auf, melden Sie sich bitte bei uns. Außerhalb der Sprechzeiten erreichen Sie den zahnärztlichen Notdienst unter <a href="tel:+4961316246999">06131 6246-999</a>.</p>
  </div>
</section>'''
    s += termin_band() + fuss()
    schreibe("patienteninfos.html", s)

# ---------------------------------------------------------------- Kontakt
def kontakt():
    s = kopf("Kontakt & Anfahrt | Zahnzentrum Messerschmidt Mainz",
             "So erreichen Sie das Zahnzentrum Messerschmidt: Parkstraße 33, 55130 Mainz-Laubenheim, Telefon 06131 86926. Anfahrt mit Auto, Bus und Bahn.",
             "kontakt.html", schema=[brotkrumen_schema([("Startseite", ""), ("Kontakt", "kontakt.html")])])
    s += brotkrumen_html([("Startseite", ""), ("Kontakt", "kontakt.html")])
    s += seitenkopf("Kontakt", "Wir freuen uns auf Sie.",
                    "Rufen Sie uns an, schreiben Sie uns oder kommen Sie vorbei. Parkplätze finden Sie direkt am Haus.",
                    "kontakt-kopf", "Das Gebäude des Zahnzentrums Messerschmidt in Mainz-Laubenheim")
    s += f'''
<section class="wrap abschnitt">
  <h2 class="sr-only">Kontaktdaten und Sprechzeiten</h2>
  <div class="kontakt-kacheln">
    <div class="kachel">{icon("telefon")}<h3>Telefon und E-Mail</h3><p><a class="gross-link" href="{TEL_LINK}">{TEL}</a><br>Fax 06131 86936<br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div class="kachel">{icon("uhr")}<h3>Sprechzeiten</h3><p><span class="offen-anzeige" data-sprechzeit></span></p><p>Montag bis Donnerstag<br>8:00 bis 20:00 Uhr durchgehend</p><p>Freitag<br>8:00 bis 16:00 Uhr</p><p class="klein">Termine nach Vereinbarung</p></div>
    <div class="kachel kachel-akzent">{icon("herz")}<h3>Zahnärztlicher Notdienst</h3><p>Außerhalb unserer Sprechzeiten wenden Sie sich bitte an den zahnärztlichen Notdienst:</p><p><a class="gross-link" href="tel:+4961316246999">06131 6246-999</a></p></div>
  </div>
</section>

<section id="anfrage" class="wrap abschnitt zwei anfrage">
  <div class="text-spalte">
    <p class="dachzeile">Termin anfragen</p>
    <h2>Ihr Wunschtermin.</h2>
    <p>Sie möchten einen Termin oder einen Rückruf? Schicken Sie uns Ihre Anfrage mit Ihren Wunschzeiten. Wir melden uns schnellstmöglich und bestätigen Ihren Termin telefonisch oder per E-Mail.</p>
    <p>Lieber persönlich? Rufen Sie uns an unter <a href="{TEL_LINK}">{TEL}</a>.</p>
    <p class="klein">Bitte schreiben Sie keine ausführlichen Angaben zu Ihrer Gesundheit in das Formular. Das besprechen wir gerne am Telefon oder in der Praxis. Bei akuten Schmerzen rufen Sie uns bitte direkt an.</p>
  </div>
  <form class="formular" action="anfrage-senden.php" method="post" novalidate>
    <input type="hidden" name="zeit" value="">
    <div class="honigtopf" aria-hidden="true"><label>Webseite <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="feld-reihe">
      <div class="feld"><label for="f-name">Vor- und Nachname *</label><input id="f-name" name="name" type="text" required autocomplete="name"></div>
      <div class="feld"><label for="f-telefon">Telefon *</label><input id="f-telefon" name="telefon" type="tel" required autocomplete="tel"></div>
    </div>
    <div class="feld-reihe">
      <div class="feld"><label for="f-email">E-Mail *</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      <div class="feld"><label for="f-anliegen">Anliegen *</label><select id="f-anliegen" name="anliegen" required><option value="">Bitte wählen</option><option>Terminwunsch</option><option>Rückruf</option><option>Frage zu einer Leistung</option><option>Sonstiges</option></select></div>
    </div>
    <div class="feld"><label for="f-wunsch">Wunschtermin oder beste Erreichbarkeit (optional)</label><input id="f-wunsch" name="wunschzeit" type="text" placeholder="zum Beispiel: dienstags ab 17 Uhr"></div>
    <div class="feld"><label for="f-nachricht">Nachricht (optional)</label><textarea id="f-nachricht" name="nachricht" rows="4"></textarea></div>
    <div class="feld feld-zustimmung"><label><input type="checkbox" name="datenschutz" value="ja" required><span>Ich habe die <a href="datenschutz.html" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage verarbeitet werden. *</span></label></div>
    <p class="formular-meldung" role="status" aria-live="polite"></p>
    <button class="knopf" type="submit">Anfrage senden</button>
    <p class="klein">Oder direkt per E-Mail an <a class="mail-rueckfall" href="mailto:{MAIL}?subject=Anfrage%20%C3%BCber%20die%20Webseite">{MAIL}</a></p>
  </form>
</section>

<section id="anfahrt" class="abschnitt flaeche">
  <div class="wrap zwei">
    <div class="text-spalte">
      <p class="dachzeile">Anfahrt</p>
      <h2>So finden Sie zu uns.</h2>
      <p><strong>{ADRESSE[0]}, {ADRESSE[1]}</strong></p>
      <h3>Mit dem Auto</h3>
      <p>Von der A60 oder aus Mainz kommend folgen Sie der Oppenheimer Straße Richtung Laubenheim, die in die Parkstraße übergeht. Am Kreisel nehmen Sie die erste Ausfahrt in die Hans-Zöller-Straße. Die Einfahrt zum Zahnzentrum liegt gleich nach dem Kreisel bei Hausnummer 114. Dort finden Sie ausreichend Parkplätze.</p>
      <h3>Mit dem Bus</h3>
      <p>Die Linien 61, 63 und 64 halten an der Haltestelle „Hans-Zöller-Straße“, von dort sind es wenige Gehminuten.</p>
      <h3>Mit der Regionalbahn</h3>
      <p>Vom Bahnhof Laubenheim sind es rund 900 Meter zu Fuß, oder Sie steigen in eine der Buslinien 61, 63 oder 64 um.</p>
      <a class="knopf" href="{ROUTE}" rel="noopener" target="_blank">Route planen</a>
    </div>
    <figure class="bild-quer">{bild("start-kontakt", "Eingang des Zahnzentrums Messerschmidt", 1600, 1067)}</figure>
  </div>
  <div class="wrap">
    <div class="karte-box" data-karte="Zahnzentrum Messerschmidt, Parkstraße 33, 55130 Mainz">
      <div class="karte-hinweis">
        {icon("ort","ikon-gross")}
        <p><strong>Karte von Google Maps</strong><br>Mit dem Laden der Karte wird Ihre IP-Adresse an Google übertragen. Mehr dazu in der <a href="datenschutz.html#karten">Datenschutzerklärung</a>.</p>
        <button type="button" class="knopf" data-karte-laden>Karte laden</button>
      </div>
    </div>
  </div>
</section>'''
    s += fuss()
    schreibe("kontakt.html", s)

# ---------------------------------------------------------------- Rechtliches
def rechtliches():
    s = kopf("Impressum | Zahnzentrum Messerschmidt", "Impressum des Zahnzentrums Messerschmidt in Mainz-Laubenheim: Anbieter, Kontaktdaten, zuständige Kammer und berufsrechtliche Angaben der Zahnärztin.", "impressum.html")
    s += f'''
<!-- Angaben aus dem Impressum der bisherigen Hauptseite (06.10.2026). Von der Kundin prüfen lassen, besonders die „Umsatzsteueridentifikationsnummer“ (Format einer Steuernummer). -->
<section class="wrap abschnitt rechtstext">
<h1>Impressum</h1>
<p>Angaben gemäß § 5 DDG</p>
<p><strong>{FIRMA}</strong><br>Dr. Sabine Messerschmidt<br>{ADRESSE[0]}<br>{ADRESSE[1]}</p>
<p>Telefon: <a href="{TEL_LINK}">{TEL}</a><br>Telefax: 06131 86936<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Inhaltlich verantwortlich</h2><p>Dr. Sabine Messerschmidt, Anschrift wie oben</p>
<h2>Berufsrechtliche Angaben</h2>
<p>Gesetzliche Berufsbezeichnung: Zahnärztin<br>Staat, in dem die Berufsbezeichnung verliehen worden ist: Deutschland</p>
<p>Umsatzsteueridentifikationsnummer (laut bisheriger Seite): 28/114/5003/0</p>
<p>Zuständige Kammer:<br>Landeszahnärztekammer Rheinland-Pfalz<br>Langenbeckstraße 2, 55131 Mainz<br><a href="https://www.lzk.de" rel="noopener">www.lzk.de</a></p>
<p>Berufsrechtliche Regelungen:</p>
<ul><li>Gesetz über die Ausübung der Zahnheilkunde (ZHG)</li><li>Berufsordnung der Landeszahnärztekammer Rheinland-Pfalz, abrufbar unter <a href="https://www.lzk.de" rel="noopener">www.lzk.de</a></li><li>Gebührenordnung für Zahnärzte (GOZ)</li><li>Heilberufsgesetz Rheinland-Pfalz</li></ul>
<h2>Haftungshinweis</h2><p>Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.</p>
<h2>Bildmaterial</h2><p>Fotos und Video: Iwan Artemjew, AO Consulting GmbH · © Dr. Messerschmidt</p>
<h2>Gestaltung und technische Umsetzung</h2><p><a href="https://ao-consult.de" rel="noopener">AO Consulting GmbH</a>, Zeiloch 13, 76646 Bruchsal</p>
<p class="klein">Stand: Oktober 2026</p>
</section>'''
    s += fuss()
    schreibe("impressum.html", s)

    s = kopf("Datenschutz | Zahnzentrum Messerschmidt", "Datenschutzerklärung des Zahnzentrums Messerschmidt: Hosting, Kontaktformular, Statistik ohne Cookies, Google Maps nach Einwilligung und Ihre Rechte.", "datenschutz.html")
    s += f'''
<!-- Zur Prüfung durch die Kundin. Verantwortliche, Datenschutzbeauftragte und Rechte von der bisherigen Erklärung übernommen;
     Google Analytics und Privacy Shield gibt es nicht mehr; Google Maps nur nach Einwilligung (AO-Einwilligungsbanner). -->
<section class="wrap abschnitt rechtstext">
<h1>Datenschutzerklärung</h1>
<p>Der Schutz Ihrer persönlichen Daten ist uns wichtig. Hier informieren wir Sie über Zweck, Art und Rechtsgrundlagen der Datenverarbeitung auf dieser Webseite.</p>
<h2>Verantwortliche</h2>
<p>Dr. Sabine Messerschmidt, {FIRMA}<br>{ADRESSE[0]}, {ADRESSE[1]}<br>Telefon {TEL} · Fax 06131 86936<br>E-Mail <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Datenschutzbeauftragte</h2>
<p>Frau Walburga Baronin van Hövell, Am Hofgarten 3, 53113 Bonn</p>
<h2>Hosting und Server-Protokolle</h2>
<p>Diese Webseite wird bei ALL-INKL.COM, Neue Medien Münnich, Inhaber René Münnich, Hauptstraße 68, 02742 Friedersdorf, gehostet. Beim Aufruf verarbeitet der Hoster technisch notwendige Daten (IP-Adresse, Zeitpunkt, aufgerufene Seite, Browser, Betriebssystem, zuvor besuchte Seite) in Server-Protokollen, die nach kurzer Zeit gelöscht werden. Rechtsgrundlage ist unser berechtigtes Interesse an einem sicheren und stabilen Betrieb (Art. 6 Abs. 1 lit. f DSGVO). Mit dem Hoster besteht ein Vertrag zur Auftragsverarbeitung.</p>
<h2>SSL-/TLS-Verschlüsselung</h2>
<p>Diese Seite nutzt eine SSL-/TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie am „https://“ in der Adresszeile.</p>
<h2>Kontakt per Telefon oder E-Mail</h2>
<p>Wenn Sie uns kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung Ihres Anliegens (Art. 6 Abs. 1 lit. b DSGVO bei Terminen und Behandlungen, sonst Art. 6 Abs. 1 lit. f DSGVO). Bitte senden Sie uns per E-Mail keine ausführlichen Gesundheitsangaben, sondern besprechen Sie diese am Telefon oder in der Praxis. E-Mails können auf dem Übertragungsweg unbefugt mitgelesen werden.</p>
<h2>Kontaktformular</h2>
<p>Wenn Sie uns über das Kontaktformular schreiben, verarbeiten wir Ihre Angaben (Name, Telefon, E-Mail, Anliegen, Wunschzeit und Nachricht), um Ihre Anfrage zu beantworten. Die Angaben werden per E-Mail an unsere Praxis übermittelt und nicht auf dem Webserver gespeichert. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bei Terminanfragen, im Übrigen unser berechtigtes Interesse an der Beantwortung (Art. 6 Abs. 1 lit. f DSGVO). Bitte machen Sie im Formular keine ausführlichen Angaben zu Ihrer Gesundheit. Wir löschen die Anfrage, sobald sie erledigt ist und keine Aufbewahrungspflicht besteht.</p>
<h2>Video auf der Startseite</h2>
<p>Das Video auf der Startseite liegt auf unserem eigenen Server. Es wird nichts von YouTube, Vimeo oder anderen Anbietern geladen.</p>
<h2>Besucherstatistik (Matomo)</h2>
<p>Wir nutzen die Statistik-Software Matomo, betrieben auf einem Server der AO Consulting GmbH, Zeiloch 13, 76646 Bruchsal, in Deutschland. Matomo arbeitet hier ohne Cookies und ohne Speicherung auf Ihrem Gerät; Ihre IP-Adresse wird vor der Verarbeitung um zwei Bytes gekürzt. Erfasst werden Mengen und Muster, keine Personen. Rechtsgrundlage ist unser berechtigtes Interesse an der Verbesserung der Seite (Art. 6 Abs. 1 lit. f DSGVO); da nichts auf Ihrem Gerät gespeichert wird, ist keine Einwilligung nach § 25 TDDDG nötig. Sie können widersprechen, indem Sie in Ihrem Browser „Do Not Track“ aktivieren. Die Daten werden nach 13 Monaten gelöscht.</p>
<h2>Einstellungen zur Barrierefreiheit</h2>
<p>Wenn Sie über das Symbol unten rechts Einstellungen zur Barrierefreiheit wählen (zum Beispiel größere Schrift oder hoher Kontrast), speichert Ihr Browser diese Einstellungen lokal auf Ihrem Gerät (Speichereintrag „ao-barrierefreiheit-v1“, kein Cookie), damit sie beim nächsten Seitenaufruf erhalten bleiben. Die Angabe wird nicht an uns übertragen und lässt sich im selben Fenster zurücksetzen oder durch Löschen der Browserdaten entfernen. Rechtsgrundlage ist § 25 Abs. 2 Nr. 2 TDDDG, da die Speicherung für die von Ihnen ausdrücklich gewünschte Funktion erforderlich ist.</p>
<h2>Einwilligung und Cookies</h2>
<p>Diese Webseite setzt keine Cookies. Ihre Entscheidung im Fenster zur Einwilligung („Cookie-Einstellungen“) speichern wir lokal in Ihrem Browser (Speichereintrag „ao-einwilligung-v1“, kein Cookie) für 12 Monate, damit Sie nicht bei jedem Aufruf erneut gefragt werden. Rechtsgrundlage ist § 25 Abs. 2 Nr. 2 TDDDG sowie Art. 6 Abs. 1 lit. c DSGVO (Nachweis der Einwilligung). Ihre Einwilligung können Sie jederzeit über „Cookie-Einstellungen“ unten auf jeder Seite widerrufen oder ändern.</p>
<h2 id="karten">Google Maps (nur nach Einwilligung)</h2>
<p>Auf der Kontaktseite können Sie eine Karte von Google Maps laden. Anbieter ist die Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. Die Karte wird erst geladen, wenn Sie im Einwilligungsfenster „Karten“ zustimmen oder auf „Karte laden“ klicken. Dann werden Ihre IP-Adresse und technische Angaben zu Ihrem Browser an Google übertragen, eine Verarbeitung in den USA ist möglich; Google beruft sich dafür auf das EU-US Data Privacy Framework. Rechtsgrundlage ist Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG), die Sie jederzeit mit Wirkung für die Zukunft widerrufen können. Weitere Informationen: <a href="https://policies.google.com/privacy" rel="noopener">policies.google.com/privacy</a>.</p>
<h2>Keine weiteren Inhalte von Drittanbietern</h2>
<p>Abgesehen von der Karte nach Einwilligung werden keine Schriften, Karten oder Skripte von Drittanbietern geladen. Links zu Instagram, Facebook, Google (Bewertungen, Routenplanung) oder zu unserer Karriereseite führen auf andere Seiten; erst beim Klick gelten deren Datenschutzbestimmungen.</p>
<h2>Weitergabe an Dritte</h2>
<p>Wir geben Ihre Daten nur weiter, wenn Sie eingewilligt haben (Art. 6 Abs. 1 lit. a DSGVO), wenn es zur Geltendmachung oder Verteidigung von Rechtsansprüchen nötig ist (Art. 6 Abs. 1 lit. f DSGVO), wenn eine gesetzliche Pflicht besteht (Art. 6 Abs. 1 lit. c DSGVO) oder wenn es für ein Vertragsverhältnis mit Ihnen erforderlich ist (Art. 6 Abs. 1 lit. b DSGVO).</p>
<h2>Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und auf Widerruf einer Einwilligung (Art. 7 Abs. 3). Verarbeitungen auf Grundlage berechtigter Interessen können Sie widersprechen (Art. 21 DSGVO); dazu genügt eine E-Mail an <a href="mailto:{MAIL}">{MAIL}</a>. Außerdem können Sie sich bei einer Aufsichtsbehörde beschweren (Art. 77 DSGVO), für uns zuständig ist der Landesbeauftragte für den Datenschutz und die Informationsfreiheit Rheinland-Pfalz.</p>
<h2>Datensicherheit</h2>
<p>Wir setzen technische und organisatorische Maßnahmen ein (Art. 32 DSGVO), um Ihre Daten zu schützen, und verbessern sie laufend.</p>
<p class="klein">Stand: Oktober 2026</p>
</section>'''
    s += fuss()
    schreibe("datenschutz.html", s)

def neu_bei_uns():
    brot = [("Startseite", ""), ("Neu bei uns", "neu-bei-uns.html")]
    faq = [("Nehmen Sie neue Patienten auf?", "Sprechen Sie uns gerne an. Am Telefon oder über das Anfrageformular klären wir, wann wir einen Termin für Sie haben."),
           ("Wie lange dauert der erste Termin?", "Für den ersten Termin planen wir ausreichend Zeit für Gespräch und Untersuchung ein. Wie lange es dauert, hängt davon ab, ob schon eine Behandlung nötig ist."),
           ("Kann ich die Bögen auch in der Praxis ausfüllen?", "Ja. Wenn Sie etwas früher kommen, füllen Sie die Bögen einfach bei uns am Empfang aus.")]
    s = kopf("Neu bei uns: Ihr erster Besuch | Zahnzentrum Messerschmidt",
             "Ihr erster Besuch im Zahnzentrum Messerschmidt in Mainz-Laubenheim: Ablauf, Anmeldebogen und Gesundheitsfragebogen zum Herunterladen, Anfahrt und Parken.",
             "neu-bei-uns.html", schema=[brotkrumen_schema(brot), {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}])
    s += brotkrumen_html(brot)
    s += seitenkopf("Neu bei uns", "Herzlich willkommen im Zahnzentrum.", "Schön, dass Sie zu uns kommen möchten. Hier finden Sie alles, was Sie für Ihren ersten Besuch wissen sollten: vom Termin über die Unterlagen bis zum Parkplatz.")
    s += f'''
<section class="wrap abschnitt">
  <div class="abschnitt-kopf"><p class="dachzeile">So einfach geht es</p><h2>Ihr erster Besuch in vier Schritten.</h2></div>
  <ol class="ablauf ablauf-gross">
    <li><strong>Termin anfragen</strong><span>Rufen Sie uns an unter {TEL} oder nutzen Sie unser <a href="{TERMIN}">Anfrageformular</a>. Sagen Sie uns gerne gleich, ob Sie Beschwerden oder Sorgen haben.</span></li>
    <li><strong>Unterlagen vorbereiten</strong><span>Laden Sie Anmeldebogen und Gesundheitsfragebogen herunter und füllen Sie sie zu Hause in Ruhe aus.</span></li>
    <li><strong>Ankommen</strong><span>Parken Sie direkt am Haus, Einfahrt über die Hans-Zöller-Straße 114. Melden Sie sich am Empfang, wir sind für Sie da.</span></li>
    <li><strong>Kennenlernen und Untersuchung</strong><span>Wir sprechen über Ihre Wünsche, untersuchen Zähne und Zahnfleisch und erklären Ihnen, was wir sehen und was als Nächstes sinnvoll ist.</span></li>
  </ol>
</section>

<section class="abschnitt flaeche">
  <div class="wrap zwei-text">
    <div class="kachel">
      <h2>Unterlagen zum Herunterladen</h2>
      <p>Bitte drucken Sie die Bögen aus, füllen Sie sie aus und bringen Sie sie unterschrieben zum ersten Termin mit. Bitte schicken Sie ausgefüllte Gesundheitsbögen nicht per E-Mail.</p>
      {downloads_html("")}
    </div>
    <div class="kachel">
      <h2>Bitte bringen Sie mit</h2>
      <ul class="haken-liste"><li>Ihre Gesundheitskarte</li><li>den ausgefüllten Anmelde- und Gesundheitsbogen</li><li>gegebenenfalls Ihre Medikationsliste</li><li>gegebenenfalls Röntgenpass und Allergiepass</li><li>Ihr Bonusheft, falls vorhanden</li></ul>
      <h2 style="margin-top:28px">Anfahrt und Parken</h2>
      <p>{ADRESSE[0]}, {ADRESSE[1]}. Parkplätze direkt am Haus, Buslinien 61, 63 und 64 (Haltestelle Hans-Zöller-Straße).</p>
      <a class="mehr" href="kontakt.html#anfahrt">Anfahrt ansehen {icon("pfeil","ikon-pfeil")}</a>
    </div>
  </div>
</section>

<section class="wrap abschnitt zwei">
  <div class="text-spalte">
    <p class="dachzeile">Ein mulmiges Gefühl?</p>
    <h2>Sagen Sie es uns einfach.</h2>
    <p>Viele Menschen gehen nicht gerne zum Zahnarzt. Wenn Sie uns das bei der Terminvereinbarung sagen, planen wir mehr Zeit ein und gehen in Ihrem Tempo vor.</p>
    <a class="mehr" href="leistungen/stressfreier-besuch.html">Mehr für Angstpatienten {icon("pfeil","ikon-pfeil")}</a>
  </div>
  <div class="faq-liste">{"".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faq)}</div>
</section>'''
    s += termin_band() + fuss()
    schreibe("neu-bei-uns.html", s)

def ratgeber():
    import datetime as dt
    brot = [("Startseite", ""), ("Ratgeber", "ratgeber.html")]
    s = kopf("Ratgeber Zahngesundheit | Zahnzentrum Messerschmidt",
             "Ratgeber vom Zahnzentrum Messerschmidt in Mainz: verständliche Antworten auf häufige Fragen zu Zahnfleisch, Kinderzähnen, Zahnersatz und Kosten.",
             "ratgeber.html", schema=[brotkrumen_schema(brot)])
    s += brotkrumen_html(brot)
    s += seitenkopf("Ratgeber", "Wissen für gesunde Zähne.", "Verständliche Antworten auf Fragen, die uns Patienten häufig stellen. Ersetzt keine Untersuchung, hilft aber bei der Orientierung.")
    s += f'''
<section class="wrap abschnitt"><h2 class="sr-only">Alle Artikel</h2><div class="ratgeber-raster">{ratgeber_karten("")}</div></section>'''
    s += termin_band() + fuss()
    schreibe("ratgeber.html", s)
    for r in RATGEBER:
        pfad = f'ratgeber/{r["slug"]}.html'
        brot = [("Startseite", ""), ("Ratgeber", "ratgeber.html"), (r["titel"], pfad)]
        l = next(x for x in LEISTUNGEN if x["slug"] == r["leistung"])
        text = "".join(f'<section class="text-block"><h2>{html.escape(t)}</h2>' + "".join(f"<p>{html.escape(a)}</p>" for a in absaetze) + "</section>" for t, absaetze in r["abschnitte"])
        datum = dt.date.fromisoformat(r["datum"]).strftime("%d.%m.%Y")
        schema = [brotkrumen_schema(brot), {"@context": "https://schema.org", "@type": "Article", "headline": r["titel"], "description": r["beschreibung"],
                  "datePublished": r["datum"], "dateModified": r["datum"], "inLanguage": "de-DE", "mainEntityOfPage": f"{DOMAIN}/{pfad}",
                  "image": DOMAIN + "/assets/img/og-bild.jpg", "author": {"@id": DOMAIN + "/#praxis"}, "publisher": {"@id": DOMAIN + "/#praxis"}}]
        s = kopf(f'{r["seo"]} | {FIRMA}', r["beschreibung"], pfad, praefix="../", schema=schema)
        s = s.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
        s += brotkrumen_html(brot, praefix="../")
        s += seitenkopf(f'Ratgeber · {r["lesezeit"]} Min. Lesezeit', html.escape(r["titel"]), f"Veröffentlicht am {datum} vom Zahnzentrum Messerschmidt, Mainz-Laubenheim.", praefix="../")
        s += f'''
<div class="wrap abschnitt leistung-raster">
  <article class="leistung-text">
    <aside class="kurz-erklaert" aria-label="Kurz erklärt"><p class="klein-titel">Kurz erklärt</p><p>{html.escape(r["kurz"])}</p></aside>
    {text}
    <p class="klein">Dieser Artikel dient der allgemeinen Information und ersetzt keine zahnärztliche Untersuchung und Beratung.</p>
  </article>
  <aside class="leistung-seite" aria-label="Kontakt und passende Leistung">
    <div class="cta-karte">
      <p class="klein-titel">Haben Sie Fragen?</p>
      <p>Wir beraten Sie gerne persönlich in unserer Praxis in Mainz-Laubenheim.</p>
      <a class="knopf" href="{TEL_LINK}">{icon("telefon","ikon-klein")} {TEL}</a>
      <a class="knopf knopf-rand" href="../{TERMIN}">Termin anfragen</a>
    </div>
    <p class="dachzeile">Passende Leistung</p>
    <ul class="leistung-menue"><li><a href="../leistungen/{l["slug"]}.html">{icon(l["icon"],"ikon-klein")}<span>{html.escape(l["kurz"])}</span></a></li></ul>
  </aside>
</div>'''
        s += fuss(praefix="../")
        schreibe(pfad, s)

def barrierefreiheit():
    brot = [("Startseite", ""), ("Barrierefreiheit", "barrierefreiheit.html")]
    s = kopf("Barrierefreiheit | Zahnzentrum Messerschmidt", "Barrierefreiheit beim Zahnzentrum Messerschmidt: was wir umgesetzt haben, wie Sie Schrift, Kontrast und Bewegung anpassen und Barrieren melden.",
             "barrierefreiheit.html", schema=[brotkrumen_schema(brot)])
    s += brotkrumen_html(brot)
    s += f'''
<section class="wrap abschnitt rechtstext">
<h1>Barrierefreiheit</h1>
<p>Wir möchten, dass alle Menschen diese Webseite gut nutzen können. Deshalb haben wir sie nach den Grundsätzen der Web Content Accessibility Guidelines (WCAG 2.1) gestaltet.</p>
<h2>Was wir umgesetzt haben</h2>
<ul class="haken-liste">
  <li>Gut lesbare Kontraste zwischen Schrift und Hintergrund</li>
  <li>Bedienung vollständig mit der Tastatur, sichtbare Markierung des ausgewählten Elements</li>
  <li>Ein Link „Zum Inhalt springen“ am Seitenanfang</li>
  <li>Beschreibende Alternativtexte für alle Bilder</li>
  <li>Klare Überschriften-Struktur für Screenreader</li>
  <li>Das Video auf der Startseite lässt sich anhalten und hat keinen Ton</li>
  <li>Bewegungseffekte entfallen, wenn Ihr Gerät „Bewegung reduzieren“ eingestellt hat</li>
  <li>Formularfelder sind beschriftet, Fehlermeldungen werden vorgelesen</li>
</ul>
<h2>Darstellung anpassen</h2>
<p>Über das Symbol mit der Figur unten rechts auf jeder Seite öffnen Sie die Einstellungen zur Barrierefreiheit. Dort können Sie unter anderem:</p>
<ul class="haken-liste">
  <li>die Schrift vergrößern sowie Zeilen- und Buchstabenabstand erhöhen</li>
  <li>einen hohen Kontrast, invertierte Farben oder Graustufen einschalten</li>
  <li>Links und Überschriften hervorheben</li>
  <li>eine besser lesbare Schrift bei Lese- und Rechtschreibschwäche wählen</li>
  <li>einen großen Mauszeiger, eine Leselinie oder eine Lesemaske nutzen</li>
  <li>Animationen und das Video anhalten</li>
</ul>
<p>Ihr Browser merkt sich diese Einstellungen auf Ihrem Gerät. Daneben können Sie die Seite wie gewohnt mit Ihrem Browser vergrößern (Strg und Plus, am Mac Cmd und Plus).</p>
<p><button type="button" class="knopf" data-bf-oeffnen>Einstellungen öffnen</button></p>
<h2>Bekannte Einschränkungen</h2>
<p>Die herunterladbaren Patientenbögen (PDF) sind noch nicht vollständig barrierefrei. Gerne helfen wir Ihnen beim Ausfüllen in der Praxis.</p>
<h2>Barriere melden</h2>
<p>Ist Ihnen eine Barriere aufgefallen? Schreiben Sie uns an <a href="mailto:{MAIL}">{MAIL}</a> oder rufen Sie uns an unter <a href="{TEL_LINK}">{TEL}</a>. Wir kümmern uns darum.</p>
<p class="klein">Stand: Oktober 2026</p>
</section>'''
    s += fuss()
    schreibe("barrierefreiheit.html", s)

def fehlerseite():
    s = kopf("Seite nicht gefunden | Zahnzentrum Messerschmidt", "Diese Seite gibt es nicht mehr. Hier finden Sie unsere Leistungen, Sprechzeiten und den Kontakt zum Zahnzentrum Messerschmidt.", "404.html", praefix="/")
    s = s.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">')
    s += f'''
<section class="seitenkopf"><div class="wrap seitenkopf-text">
  <p class="dachzeile dachzeile-hell">Fehler 404</p>
  <h1>Diese Seite gibt es nicht mehr.</h1>
  <p class="lead">Vielleicht hat sich die Adresse mit unserer neuen Webseite geändert. Hier geht es weiter:</p>
  <div class="knoepfe" style="margin-top:28px"><a class="knopf" href="/">Zur Startseite</a><a class="knopf knopf-rand-hell" href="/leistungen.html">Leistungen</a><a class="knopf knopf-rand-hell" href="/kontakt.html">Kontakt</a></div>
</div></section>'''
    s += fuss(praefix="/")
    schreibe("404.html", s)

def llms():
    z = [f"# {FIRMA}", "", "> Zahnarztpraxis in Mainz-Laubenheim (Parkstraße 33, 55130 Mainz) mit eigenem Dentallabor. Praxisinhaberin: Dr. med. Sabine Messerschmidt.", "",
         "## Fakten", f"- Adresse: Parkstraße 33, 55130 Mainz-Laubenheim (Einfahrt Hans-Zöller-Straße 114, Parkplätze am Haus)",
         f"- Telefon: {TEL}, E-Mail: {MAIL}", "- Sprechzeiten: Montag bis Donnerstag 8 bis 20 Uhr, Freitag 8 bis 16 Uhr",
         "- Zahnärztlicher Notdienst: 06131 6246-999", "- Praxis gegründet 1995, Zahnzentrum seit 2009",
         "- Zahnärztinnen: " + "; ".join(f'{x["name"]} ({", ".join(x["schwerpunkte"][:2])})' for x in ZAHNAERZTINNEN), "",
         "## Leistungen"] + [f'- [{l["titel"]}]({DOMAIN}/leistungen/{l["slug"]}.html): {l["kurz_erklaert"]}' for l in LEISTUNGEN] + ["",
         "## Ratgeber"] + [f'- [{r["titel"]}]({DOMAIN}/ratgeber/{r["slug"]}.html): {r["kurz"]}' for r in RATGEBER] + ["",
         "## Seiten", f"- [Neu bei uns: erster Besuch, Anmeldebögen]({DOMAIN}/neu-bei-uns.html)", f"- [Praxis]({DOMAIN}/praxis.html)", f"- [Team]({DOMAIN}/team.html)", f"- [Patienteninfos]({DOMAIN}/patienteninfos.html)",
         f"- [Kontakt und Anfahrt]({DOMAIN}/kontakt.html)", f"- [Karriere]({KARRIERE})", ""]
    (WEB / "llms.txt").write_text("\n".join(z), encoding="utf-8")

def sitemap():
    seiten = [("", "1.0"), ("leistungen.html", "0.9")] + [(f'leistungen/{l["slug"]}.html', "0.8") for l in LEISTUNGEN] + \
             [("praxis.html", "0.7"), ("team.html", "0.7"), ("neu-bei-uns.html", "0.8"), ("ratgeber.html", "0.6")] + [(f'ratgeber/{r["slug"]}.html', "0.6") for r in RATGEBER] + [("barrierefreiheit.html", "0.2"), ("patienteninfos.html", "0.6"), ("kontakt.html", "0.8"), ("impressum.html", "0.2"), ("datenschutz.html", "0.2")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + \
         [f"  <url><loc>{DOMAIN}/{p}</loc><lastmod>{HEUTE}</lastmod><priority>{pr}</priority></url>" for p, pr in seiten] + ["</urlset>", ""]
    (WEB / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    (WEB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /anfrage-senden.php\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")

def pruefe_seo():
    """Titel- und Beschreibungslängen, doppelte Titel. Gibt Warnungen aus, bricht nicht ab."""
    import re as r
    gesehen = {}
    for f in sorted(WEB.rglob("*.html")):
        t = f.read_text(encoding="utf-8")
        ti = html.unescape(r.search(r"<title>(.*?)</title>", t).group(1)); de = html.unescape(r.search(r'name="description" content="(.*?)"', t).group(1))
        rel = f.relative_to(WEB).as_posix()
        if len(ti) > 62: print(f"WARNUNG Titel zu lang ({len(ti)}): {rel}: {ti}")
        if not 110 <= len(de) <= 165: print(f"WARNUNG Beschreibung {len(de)} Zeichen: {rel}")
        if ti in gesehen: print(f"WARNUNG doppelter Titel: {rel} und {gesehen[ti]}")
        gesehen[ti] = rel

if __name__ == "__main__":
    startseite(); leistungen(); praxis(); team(); patienteninfos(); kontakt(); rechtliches(); neu_bei_uns(); ratgeber(); barrierefreiheit(); fehlerseite(); llms(); sitemap(); pruefe_seo()
    print("Gebaut:", len(list(WEB.rglob("*.html"))), "Seiten")
