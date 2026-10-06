#!/usr/bin/env python3
"""
bauen.py – baut alle Seiten der Hauptseite Zahnzentrum Messerschmidt nach website/.

Aufruf im Projektordner:  python3 quelltexte/bauen.py
Nur Python-Standardbibliothek. Texte stehen hier und in inhalt_leistungen.py.
Regeln: Sie-Ansprache, keine Gedankenstriche, keine Heilversprechen, keine externen Dateien.
"""
import html, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from inhalt_leistungen import LEISTUNGEN

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
}
def icon(n, cls="ikon"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>'

def bild(name, alt, w, h, cls="", lazy=True, praefix=""):
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    k = ' class="' + cls + '"' if cls else ""
    return (f'<picture{k}><source srcset="{praefix}assets/img/{name}.webp" type="image/webp">'
            f'<img src="{praefix}assets/img/{name}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}"{l}></picture>')

NAVI = [("leistungen.html", "Leistungen"), ("praxis.html", "Praxis"), ("team.html", "Team"),
        ("patienteninfos.html", "Patienteninfos"), ("kontakt.html", "Kontakt")]

def kopf(titel, beschr, pfad, praefix="", hell_start=False, body_klasse=""):
    canon = f"{DOMAIN}/{pfad}" if pfad else f"{DOMAIN}/"
    akt = ' aria-current="page"'
    navi = "".join(f'<a href="{praefix}{h}"{akt if h == pfad else ""}>{t}</a>' for h, t in NAVI)
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
<meta property="og:image" content="{DOMAIN}/assets/img/og-bild.jpg">
<meta name="theme-color" content="#0b1f33">
<link rel="icon" href="{praefix}assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{praefix}assets/img/apple-touch-icon.png">
<link rel="preload" href="{praefix}assets/fonts/manrope-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{praefix}assets/css/stil.css">
</head>
<body class="{body_klasse}">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="{klasse}">
  <div class="wrap kopf-zeile">
    <a class="logo" href="{praefix}index.html" aria-label="{FIRMA}, zur Startseite">
      <img class="logo-farbe" src="{praefix}assets/img/logo.png" alt="{FIRMA}" width="246" height="135">
      <img class="logo-weiss" src="{praefix}assets/img/logo-weiss.png" alt="" width="246" height="135">
    </a>
    <nav class="hauptnavi" id="navi" aria-label="Hauptnavigation">
      {navi}
      <a href="{KARRIERE}" rel="noopener">Karriere</a>
    </nav>
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
      <img src="{praefix}assets/img/logo-weiss.png" alt="{FIRMA}" width="246" height="135">
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
      <p>Montag bis Donnerstag<br>8:00 bis 20:00 Uhr</p>
      <p>Freitag<br>8:00 bis 16:00 Uhr</p>
      <p class="fuss-notdienst">Zahnärztlicher Notdienst<br><a href="tel:+4961316246999">06131 6246-999</a></p>
    </div>
    <div>
      <p class="fuss-titel">Leistungen</p>
      <ul class="fuss-liste">{leist}</ul>
    </div>
  </div>
  <div class="wrap fuss-unten">
    <p>© <span data-jahr>2026</span> {FIRMA} · <a href="{praefix}impressum.html">Impressum</a> · <a href="{praefix}datenschutz.html">Datenschutz</a> · <a href="{KARRIERE}" rel="noopener">Karriere</a></p>
    <p><a href="https://www.instagram.com/zahnzentrum_messerschmidt/" rel="noopener" target="_blank">Instagram</a> · <a href="https://www.facebook.com/zahnzentrummesserschmidt/" rel="noopener" target="_blank">Facebook</a> · made by <a href="https://ao-consult.de" rel="noopener">AO Consulting</a></p>
  </div>
</footer>
<script src="{praefix}assets/js/app.js" defer></script>
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
      <a class="knopf knopf-rand-hell" href="mailto:{MAIL}">E-Mail schreiben</a>
    </div>
  </div>
</section>'''

def seitenkopf(dach, titel, text, bildname=None, alt="", praefix=""):
    b = (f'<div class="seitenkopf-bild">{bild(bildname, alt, 2000, 1000, lazy=False, praefix=praefix)}</div>' if bildname else "")
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

# ---------------------------------------------------------------- Startseite
def startseite():
    karten = "".join(f'''
      <a class="leistung-karte" href="leistungen/{l["slug"]}.html">
        {icon(l["icon"])}
        <h3>{html.escape(l["kurz"])}</h3>
        <p>{html.escape(l["teaser"])}</p>
        <span class="mehr">Mehr erfahren {icon("pfeil","ikon-pfeil")}</span>
      </a>''' for l in LEISTUNGEN)
    jsonld = {
        "@context": "https://schema.org", "@type": "Dentist", "name": FIRMA, "url": DOMAIN + "/",
        "image": DOMAIN + "/assets/img/og-bild.jpg", "logo": DOMAIN + "/assets/img/logo.png",
        "telephone": "+49 6131 86926", "email": MAIL, "faxNumber": "+49 6131 86936",
        "address": {"@type": "PostalAddress", "streetAddress": "Parkstraße 33", "postalCode": "55130",
                    "addressLocality": "Mainz", "addressRegion": "Rheinland-Pfalz", "addressCountry": "DE"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "16:00"}],
        "sameAs": ["https://www.instagram.com/zahnzentrum_messerschmidt/", "https://www.facebook.com/zahnzentrummesserschmidt/"],
    }
    s = kopf("Zahnarzt Mainz-Laubenheim | Zahnzentrum Messerschmidt",
             "Zahnzentrum Messerschmidt in Mainz-Laubenheim: Prophylaxe, Implantate, Parodontologie, Ästhetik, Kinderzahnheilkunde und eigenes Dentallabor. Mo bis Do bis 20 Uhr.",
             "", hell_start=True, body_klasse="startseite")
    s = s.replace("</head>", f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n</head>')
    s += f'''
<section class="hero" aria-labelledby="hero-titel">
  <video class="hero-video" autoplay muted loop playsinline preload="metadata" poster="assets/video/hero-poster.jpg" aria-hidden="true">
    <source src="assets/video/hero.mp4" type="video/mp4">
  </video>
  <div class="hero-schleier"></div>
  <div class="wrap hero-inhalt">
    <p class="dachzeile dachzeile-hell">Zahnzentrum Messerschmidt · Mainz-Laubenheim</p>
    <h1 id="hero-titel">Kompetenz<br>im Detail.</h1>
    <p class="hero-unterzeile">Moderne Zahnmedizin in einem hellen, eigens gebauten Haus. Für Ihr Lächeln, ein Leben lang.</p>
    <div class="knoepfe">
      <a class="knopf" href="{TEL_LINK}">Termin vereinbaren</a>
      <a class="knopf knopf-rand-hell" href="leistungen.html">Leistungen entdecken</a>
    </div>
  </div>
  <button class="video-schalter" type="button" aria-label="Video anhalten" aria-pressed="false"><span></span></button>
  <a class="hero-runter" href="#willkommen" aria-label="Weiter nach unten"></a>
</section>

<section class="fakten-leiste" aria-label="Auf einen Blick">
  <div class="wrap fakten-raster">
    <div><strong>Seit 1995</strong><span>in Mainz-Laubenheim</span></div>
    <div><strong>4</strong><span>moderne Behandlungszimmer</span></div>
    <div><strong>Eigenes Labor</strong><span>Zahnersatz aus dem Haus</span></div>
    <div><strong>Bis 20 Uhr</strong><span>Montag bis Donnerstag</span></div>
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

<section class="abschnitt bild-band">
  {bild("start-haus", "Das Zahnzentrum Messerschmidt in der Parkstraße in Mainz-Laubenheim", 1600, 1067, cls="bild-band-bild")}
  <div class="wrap bild-band-text">
    <div class="karte-glas">
      <p class="dachzeile">Unsere Praxis</p>
      <h2>Ein Haus, gebaut für Ihr Wohlbefinden.</h2>
      <p>Unsere Praxis liegt in einem eigens dafür errichteten Niedrigenergiehaus. Große Fenster, helle Räume und eine eigene Solaranlage: Nachhaltigkeit ist uns wichtig, bei den Räumen genauso wie bei der Behandlung.</p>
      <a class="mehr" href="praxis.html">Die Praxis entdecken {icon("pfeil","ikon-pfeil")}</a>
    </div>
  </div>
</section>

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
      <a class="knopf knopf-hell" href="{KARRIERE}" rel="noopener">Zu den offenen Stellen</a>
    </div>
  </div>
</section>

<section class="wrap abschnitt kontakt-kurz">
  <div class="kontakt-kacheln">
    <div class="kachel">{icon("ort")}<h3>Anfahrt</h3><p>{ADRESSE[0]}<br>{ADRESSE[1]}<br>Einfahrt über die Hans-Zöller-Straße 114, Parkplätze direkt am Haus.</p><a class="mehr" href="kontakt.html#anfahrt">Anfahrt ansehen {icon("pfeil","ikon-pfeil")}</a></div>
    <div class="kachel">{icon("uhr")}<h3>Sprechzeiten</h3><p>Montag bis Donnerstag<br>8:00 bis 20:00 Uhr durchgehend<br>Freitag 8:00 bis 16:00 Uhr</p><p class="klein">Termine nach Vereinbarung</p></div>
    <div class="kachel">{icon("telefon")}<h3>Kontakt</h3><p><a href="{TEL_LINK}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p><p class="klein">Notdienst außerhalb der Sprechzeiten:<br><a href="tel:+4961316246999">06131 6246-999</a></p></div>
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
    s = kopf("Leistungen | Zahnzentrum Messerschmidt Mainz-Laubenheim",
             "Unsere Leistungen: Prophylaxe, Ästhetik, Parodontologie, Zahnersatz und Implantate, Endodontie, Kinderzahnheilkunde, Funktionsdiagnostik, Oralchirurgie.",
             "leistungen.html")
    s += seitenkopf("Leistungen", "Ihre Zahngesundheit hat oberste Priorität.",
                    "Wir verbinden Qualifikation mit moderner Technik. Unsere Zahnärztinnen haben Zusatzqualifikationen in Implantologie, Parodontologie, Endodontie, ästhetischer Zahnheilkunde und Akupunktur. Zahnersatz fertigen wir im eigenen Dentallabor.")
    s += f'''
<section class="wrap abschnitt">
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
        abschn = "".join(f'<section class="text-block"><h2>{html.escape(t)}</h2><p>{html.escape(p)}</p></section>' for t, p in l["abschnitte"])
        andere = "".join(f'<li><a href="{x["slug"]}.html">{icon(x["icon"],"ikon-klein")}<span>{html.escape(x["kurz"])}</span></a></li>' for x in LEISTUNGEN if x is not l)
        s = kopf(f'{l["titel"]} in Mainz-Laubenheim | {FIRMA}', f'{l["titel"]} im Zahnzentrum Messerschmidt in Mainz-Laubenheim. {l["teaser"]}',
                 f'leistungen/{l["slug"]}.html', praefix="../")
        s += seitenkopf(f'Leistungen · {html.escape(l["kurz"])}', html.escape(l["titel"]), html.escape(l["intro"]), praefix="../")
        s += f'''
<div class="wrap abschnitt leistung-raster">
  <article class="leistung-text">{abschn}
    <div class="cta-karte">
      <h2>Haben Sie Fragen?</h2>
      <p>Wir beraten Sie gerne persönlich in unserer Praxis.</p>
      <div class="knoepfe"><a class="knopf" href="{TEL_LINK}">{icon("telefon","ikon-klein")} {TEL}</a><a class="knopf knopf-rand" href="mailto:{MAIL}">E-Mail schreiben</a></div>
    </div>
  </article>
  <aside class="leistung-seite" aria-label="Weitere Leistungen">
    <p class="dachzeile">Weitere Leistungen</p>
    <ul class="leistung-menue">{andere}</ul>
  </aside>
</div>'''
        s += fuss(praefix="../")
        schreibe(f'leistungen/{l["slug"]}.html', s)

# ---------------------------------------------------------------- Praxis
def praxis():
    s = kopf("Unsere Praxis | Zahnzentrum Messerschmidt Mainz-Laubenheim",
             "Das Zahnzentrum Messerschmidt: eigens gebautes Niedrigenergiehaus, helle Räume, eigenes Dentallabor und Service, der Wohlfühlen leicht macht.",
             "praxis.html")
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
  dict(name="Dr. med. Sabine Messerschmidt", rolle="Zahnärztin, Praxisinhaberin", foto="team-sabine",
       schwerpunkte=["Komplexe prothetisch-chirurgische Rekonstruktionen", "Regenerative Parodontaltherapie und Parodontalchirurgie", "Augmentationschirurgie und Implantologie", "Ganzheitliche Zahnheilkunde"],
       vita=["Studium der Zahnheilkunde in Jena und Erfurt", "1991 Approbation, 1993 Promotion", "1995 Gründung der Praxis in Mainz-Laubenheim", "2009 Gründung des Zahnzentrums Messerschmidt",
             "Tätigkeitsschwerpunkte Akupunktur (1996), Implantologie DGI und APW (2002), Parodontologie (2012), Endodontologie und Ästhetische Zahnheilkunde (2014)", "Seit 2012 Referentin für Fortbildungen von Kolleginnen und Kollegen"]),
  dict(name="Olga Miller, MSc", rolle="Zahnärztin", foto=None,
       schwerpunkte=["Komplexe endodontische Behandlungen", "Ganzheitliche Zahnheilkunde", "Prothetische Sanierungen"],
       vita=["Studium der Zahnmedizin in Göttingen, 2010 Approbation", "2018 Tätigkeitsschwerpunkt Endodontologie und Qualifikation zur Lachgassedierung", "2020 Fachkunde digitale Volumentomographie", "Seit 2024 Master für Implantologie und Parodontologie, Universität Krems"]),
  dict(name="Dr. med. dent. Lisa Blatt", rolle="Zahnärztin", foto=None,
       schwerpunkte=["Zahnerhaltung, präventiv und restaurativ", "Ästhetische Zahnheilkunde"],
       vita=["Studium der Zahnmedizin an der Universität Mainz, 2015 Approbation", "2017 Promotion", "Seit 2023 Lehrkraft an der Berufsbildenden Schule 3 in Mainz", "Seit 2024 im Zahnzentrum Messerschmidt"]),
  dict(name="Dr. med. dent. Alina Günther", rolle="Zahnärztin", foto=None,
       schwerpunkte=["Komplexe endodontologische Behandlungen", "Konservierend-chirurgische Behandlungen", "Ganzheitliche Zahnheilkunde"],
       vita=["Studium der Zahnheilkunde in Frankfurt am Main, 2019 Approbation", "Promotion an der MKG-Universitätsklinik Frankfurt", "2023 Hilfseinsatz mit Zahnärzte ohne Grenzen", "Seit 2025 im Zahnzentrum Messerschmidt"]),
]
def team():
    karten = []
    for z in ZAHNAERZTINNEN:
        if z["foto"]:
            f = bild(z["foto"], z["name"], 900, 1125)
        else:
            ini = "".join(w[0] for w in z["name"].replace("Dr. med. dent. ", "").replace("Dr. med. ", "").replace(", MSc", "").split()[:2])
            f = f'<div class="monogramm" aria-hidden="true">{ini}</div>'
        karten.append(f'''
    <article class="person">
      <div class="person-bild">{f}</div>
      <div class="person-text">
        <h3>{html.escape(z["name"])}</h3>
        <p class="rolle">{html.escape(z["rolle"])}</p>
        <p class="klein-titel">Schwerpunkte</p>
        <ul class="haken-liste">{"".join(f"<li>{html.escape(x)}</li>" for x in z["schwerpunkte"])}</ul>
        <details><summary>Werdegang</summary><ul>{"".join(f"<li>{html.escape(x)}</li>" for x in z["vita"])}</ul></details>
      </div>
    </article>''')
    s = kopf("Unser Team | Zahnzentrum Messerschmidt Mainz-Laubenheim",
             "Lernen Sie unsere Zahnärztinnen kennen: Dr. Sabine Messerschmidt, Olga Miller, Dr. Lisa Blatt und Dr. Alina Günther, dazu unser Praxisteam.",
             "team.html")
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

<section class="abschnitt flaeche">
  <div class="wrap zwei">
    <figure class="bild-quer">{bild("team-duo", "Zwei Kolleginnen des Zahnzentrums", 1200, 800)}</figure>
    <div class="text-spalte">
      <p class="dachzeile">Praxisteam</p>
      <h2>Anmeldung, Prophylaxe und Assistenz.</h2>
      <p>Hinter jeder Behandlung steht ein ganzes Team: Zahnmedizinische Fachangestellte, Fachassistentinnen und Prophylaxeassistentinnen kümmern sich um Ihre Termine, Ihre Vorsorge und begleiten Sie am Behandlungsstuhl. Und wir bilden selbst aus.</p>
      <a class="mehr" href="{KARRIERE}" rel="noopener">Bei uns arbeiten {icon("pfeil","ikon-pfeil")}</a>
    </div>
  </div>
</section>'''
    s += termin_band() + fuss()
    schreibe("team.html", s)

# ---------------------------------------------------------------- Patienteninfos
def patienteninfos():
    s = kopf("Patienteninfos | Zahnzentrum Messerschmidt Mainz-Laubenheim",
             "Ihr erster Besuch im Zahnzentrum Messerschmidt: was Sie mitbringen sollten und worauf Sie nach einem chirurgischen Eingriff achten.",
             "patienteninfos.html")
    s += seitenkopf("Patienteninfos", "Gut vorbereitet zu Ihrem Termin.",
                    "Hier finden Sie die wichtigsten Informationen für Ihren ersten Besuch und für die Zeit nach einem Eingriff.")
    s += f'''
<section class="wrap abschnitt zwei-text">
  <div class="kachel">
    <h2>Ihr erster Besuch</h2>
    <p>Für den ersten Besuch benötigen wir einen ausgefüllten Anamnesebogen mit Angaben zu Ihrer Gesundheit, zu Allergien und Medikamenten. So können wir Befunde besser einschätzen und die passende Behandlung planen.</p>
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
    s = kopf("Kontakt und Anfahrt | Zahnzentrum Messerschmidt Mainz-Laubenheim",
             "So erreichen Sie das Zahnzentrum Messerschmidt: Parkstraße 33, 55130 Mainz-Laubenheim, Telefon 06131 86926. Anfahrt mit Auto, Bus und Bahn.",
             "kontakt.html")
    s += seitenkopf("Kontakt", "Wir freuen uns auf Sie.",
                    "Rufen Sie uns an, schreiben Sie uns oder kommen Sie vorbei. Parkplätze finden Sie direkt am Haus.",
                    "kontakt-kopf", "Das Gebäude des Zahnzentrums Messerschmidt in Mainz-Laubenheim")
    s += f'''
<section class="wrap abschnitt">
  <div class="kontakt-kacheln">
    <div class="kachel">{icon("telefon")}<h3>Telefon und E-Mail</h3><p><a class="gross-link" href="{TEL_LINK}">{TEL}</a><br>Fax 06131 86936<br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div class="kachel">{icon("uhr")}<h3>Sprechzeiten</h3><p>Montag bis Donnerstag<br>8:00 bis 20:00 Uhr durchgehend</p><p>Freitag<br>8:00 bis 16:00 Uhr</p><p class="klein">Termine nach Vereinbarung</p></div>
    <div class="kachel kachel-akzent">{icon("herz")}<h3>Zahnärztlicher Notdienst</h3><p>Außerhalb unserer Sprechzeiten wenden Sie sich bitte an den zahnärztlichen Notdienst:</p><p><a class="gross-link" href="tel:+4961316246999">06131 6246-999</a></p></div>
  </div>
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
</section>'''
    s += fuss()
    schreibe("kontakt.html", s)

# ---------------------------------------------------------------- Rechtliches
def rechtliches():
    s = kopf("Impressum | Zahnzentrum Messerschmidt", "Impressum des Zahnzentrums Messerschmidt in Mainz-Laubenheim: Anbieter, Kontakt, berufsrechtliche Angaben.", "impressum.html")
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

    s = kopf("Datenschutz | Zahnzentrum Messerschmidt", "Datenschutzerklärung des Zahnzentrums Messerschmidt: Hosting, Kontakt, Besucherstatistik ohne Cookies, Ihre Rechte.", "datenschutz.html")
    s += f'''
<!-- Zur Prüfung durch die Kundin. Verantwortliche, Datenschutzbeauftragte und Rechte von der bisherigen Erklärung übernommen;
     Google Analytics, Google Maps, Cookies und Privacy Shield gibt es auf dieser Seite nicht mehr. -->
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
<h2>Kontakt per Telefon, E-Mail oder WhatsApp</h2>
<p>Wenn Sie uns kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung Ihres Anliegens (Art. 6 Abs. 1 lit. b DSGVO bei Terminen und Behandlungen, sonst Art. 6 Abs. 1 lit. f DSGVO). Bitte senden Sie uns per E-Mail keine ausführlichen Gesundheitsangaben, sondern besprechen Sie diese am Telefon oder in der Praxis. E-Mails können auf dem Übertragungsweg unbefugt mitgelesen werden.</p>
<h2>Video auf der Startseite</h2>
<p>Das Video auf der Startseite liegt auf unserem eigenen Server. Es wird nichts von YouTube, Vimeo oder anderen Anbietern geladen.</p>
<h2>Besucherstatistik (Matomo)</h2>
<p>Wir nutzen die Statistik-Software Matomo, betrieben auf einem Server der AO Consulting GmbH, Zeiloch 13, 76646 Bruchsal, in Deutschland. Matomo arbeitet hier ohne Cookies und ohne Speicherung auf Ihrem Gerät; Ihre IP-Adresse wird vor der Verarbeitung um zwei Bytes gekürzt. Erfasst werden Mengen und Muster, keine Personen. Rechtsgrundlage ist unser berechtigtes Interesse an der Verbesserung der Seite (Art. 6 Abs. 1 lit. f DSGVO); da nichts auf Ihrem Gerät gespeichert wird, ist keine Einwilligung nach § 25 TDDDG nötig. Sie können widersprechen, indem Sie in Ihrem Browser „Do Not Track“ aktivieren. Die Daten werden nach 13 Monaten gelöscht.</p>
<h2>Keine Cookies, keine eingebetteten Inhalte</h2>
<p>Diese Webseite setzt keine Cookies. Es werden keine Schriften, Karten oder Skripte von Drittanbietern geladen. Links zu Instagram, Facebook, WhatsApp, Google Maps (Routenplanung) oder zu unserer Karriereseite führen auf andere Seiten; erst beim Klick gelten deren Datenschutzbestimmungen.</p>
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

def sitemap():
    seiten = ["", "leistungen.html", "praxis.html", "team.html", "patienteninfos.html", "kontakt.html", "impressum.html", "datenschutz.html"] + [f'leistungen/{l["slug"]}.html' for l in LEISTUNGEN]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f"  <url><loc>{DOMAIN}/{p}</loc></url>" for p in seiten] + ["</urlset>", ""]
    (WEB / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    (WEB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")

if __name__ == "__main__":
    startseite(); leistungen(); praxis(); team(); patienteninfos(); kontakt(); rechtliches(); sitemap()
    print("Gebaut:", len(list(WEB.rglob("*.html"))), "Seiten")
