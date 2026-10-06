# Hauptseite Zahnzentrum Messerschmidt – Entscheidungen und offene Punkte

Stand 06.10.2026, Awan Tofik mit Claude. Kein eigenes Onboarding für die Hauptseite; Grundlage sind das Zoom-Protokoll
(Ovidiu mit Dr. Messerschmidt), die bisherige Seite zahnzentrum-messerschmidt.de und das Shooting von Iwan Artemjew.

## Vorgaben

- Modern und frisch, bewegtes Bild im Hero (Vorbild BMW/Mercedes, Wunsch der Kundin laut Protokoll), große Bilder statt viel Text.
- Sie-Ansprache für Patienten. Keine Gedankenstriche. Nur Querformat-Fotos, kein Motiv doppelt auf einer Seite.
- Farben aus dem Logo (Blau #006eb7, Hellblau #84d0f5), dazu Nachtblau #0b1f33. Schrift Manrope (lokal, SIL OFL).

## Hero-Video

- `website/assets/video/hero.webm` (VP9, ca. 2 MB, wird zuerst geladen) und `hero.mp4` (H.264 für Safari, 1600×900, 25 s, ohne Ton, ca. 3 MB) ist **aus Shooting-Fotos erzeugt** (langsamer Zoom und Überblendung,
  ffmpeg, Skript `film.sh` im Mac-Arbeitsordner): Bilder 29, 24, 9, 44, 36, 17. Sobald Iwan echte Bewegtaufnahmen liefert, Datei austauschen
  (gleicher Name, H.264, ohne Ton, möglichst unter 5 MB, `-movflags +faststart`). Poster `hero-poster.jpg` = erstes Bild.
- Bei „Bewegung reduzieren“ im Betriebssystem läuft das Video nicht automatisch. Anhalten-Knopf unten rechts.

## Bilder

| Datei | Nr. | Seite |
|---|---|---|
| start-sabine | 62 | Start, Willkommen |
| start-haus | 8 | Start, Praxis-Band |
| start-angst | 33 | Start, Angstpatienten |
| start-karriere | 112 | Start, Karriere |
| start-kontakt | 1 | Kontakt, Anfahrt |
| praxis-kopf / -gebaeude / -hell / -empfang | 13 / 4 / 21 / 31 | Praxis |
| team-kopf / team-sabine / team-duo | 28 / 57 / 105 | Team |
| kontakt-kopf | 2 | Kontakt |
| og-bild | 29 | Vorschaubild für Links |

## Offen / bitte bestätigen

- [ ] **Fotos der Zahnärztinnen:** Olga Miller, Dr. Lisa Blatt und Dr. Alina Günther haben vorerst den Platzhalter „Foto wird nachgereicht“ (Vorgabe Awan).
- [ ] **Praxisteam-Raster (Team-Seite):** Portraits Nr. 71, 79, 91, 101 mit „Name wird nachgereicht / Funktion wird nachgereicht“. Falls darunter Zahnärztinnen sind, nach oben zu den Behandlerinnen verschieben.
- [ ] **Team-Liste:** Die bisherige Seite nennt 14 Mitarbeiterinnen namentlich (Stand unklar). Mit Namen aufnehmen? Dann Liste bestätigen lassen.
- [ ] **Hanh Geyrhofer** wird auf der alten Seite als Kinderzahnärztin/Endodontie genannt, steht aber nicht mehr bei den Zahnärztinnen. Bewusst weggelassen.
- [ ] **Homöopathie** von der alten Seite nicht übernommen (Heilmittelwerberecht); Akupunktur bleibt als begleitendes Angebot.
- [ ] **Anamnesebogen/Anmeldebogen** (PDF-Downloads der alten Seite): Dateien von der Kundin holen und auf Patienteninfos verlinken.
- [x] **Kontaktformular** wieder eingebaut (alte Seite hatte eins, Vorgabe Awan): Kontakt-Seite, `anfrage-senden.php` an info@zahnzentrum-messerschmidt.de, Hinweis „keine Gesundheitsangaben“, Datenschutz ergänzt. Vor dem Livegang Testanfrage.
- [ ] Impressum: „Umsatzsteueridentifikationsnummer 28/114/5003/0“ ist das Format einer Steuernummer.
- [ ] Karriere-Link zeigt in der Vorschau auf messerschmidt-karriere.vorschau.ao-consult.de, vor dem Livegang in `quelltexte/bauen.py` (KARRIERE) auf die Karriere-Domain umstellen.
- [ ] Alte Adressen weiterleiten (Livegang): /uber-uns/ → /team.html, /praxis/… → /praxis.html, /service/patienteninfos/ → /patienteninfos.html, /anfahrt/ und /kontakt/ → /kontakt.html; /leistungen/<name>/ → /leistungen/<name>.html (gleiche Namen).
- [ ] Matomo-Eintrag anlegen, Kennung in `website/assets/js/statistik.js` (seite) eintragen.

## Effekte (Runde 2, Wunsch Awan: „was Heftiges“)

Hero-Zeilen gleiten herein, Video zoomt langsam; Zähler in der Faktenleiste; Leitsatz füllt sich Wort für Wort beim Scrollen;
Laufband mit Leistungen (Outline-Schrift); Parallax auf großen Bildflächen; Bilder werden beim Scrollen enthüllt; Lichtkegel folgt der Maus
auf Karten; Knöpfe mit leichtem Magnet-Effekt; Kopf verschwindet beim Runterscrollen. Alles ohne fremde Bibliothek und abgeschaltet,
wenn im Betriebssystem „Bewegung reduzieren“ an ist.

## SEO und GEO (Runde 3, 06.10.2026)

- Inhaltsbreite überall 1500 px (vorher 1320 px).
- Leistungsseiten ausgebaut (rund 450 bis 650 Wörter statt rund 200): Antwortbox „Kurz erklärt“, ausführliche Abschnitte,
  Ablauf in Schritten, „Für wen sinnvoll“, Ansprechpartnerinnen mit Link zum Team, FAQ, verwandte Leistungen.
  „Haben Sie Fragen?“ steht in der rechten Spalte über „Weitere Leistungen“.
- **Texte von der Kundin freigeben lassen.** Neu und allgemein formuliert (nicht von der alten Seite): Kostenhinweise (Kasse/Privat),
  Häufigkeiten, Dauer eines Prophylaxetermins (etwa eine Stunde), Handzeichen für Pausen, Begleitperson willkommen, Fluoridlack auf Wunsch,
  Zuordnung der Ansprechpartnerinnen zu Leistungen (aus den Arbeitsschwerpunkten der Lebensläufe).
- Strukturierte Daten auf jeder Seite: Dentist/MedicalClinic mit Adresse, Geo-Koordinaten (OpenStreetMap), Sprechzeiten, Fax, sameAs;
  Startseite zusätzlich WebSite und FAQPage; Leistungsseiten MedicalWebPage, Service, FAQPage, BreadcrumbList; Team: Person je Zahnärztin.
- Sichtbare Brotkrumen auf allen Unterseiten, FAQ-Bereich auf der Startseite.
- Titel bis 60 Zeichen und Beschreibungen 110 bis 165 Zeichen, eindeutig je Seite (bauen.py prüft das bei jedem Lauf und warnt).
- `llms.txt` (Kurzprofil der Praxis für KI-Suchen), Sitemap mit lastmod und Priorität, robots.txt, eigene 404-Seite.
- `.htaccess`: 301-Weiterleitungen aller alten WordPress-Adressen, Fehlerseite 404, Zwischenspeicher für Video und Schriften.
  https/ohne-www-Umleitung ist vorbereitet und wird am Livegang-Tag freigeschaltet (alte Seite lief ohne www).
- Nach dem Livegang: Search Console, Sitemap einreichen, Google-Unternehmensprofil prüfen (gleiche Adresse, Telefon, Sprechzeiten, Webseite).

## Runde 4 (06.10.2026)

- „Jetzt geöffnet“ im Kopf, bei Sprechzeiten und im Fuß (Zeit in Mainz, Mo bis Do 8 bis 20, Fr 8 bis 16). Gesetzliche Feiertage Rheinland-Pfalz
  2026 und 2027 sind in `website/assets/js/app.js` (FEIERTAGE) hinterlegt, **Ende 2027 ergänzen**. Urlaub/Brückentage der Praxis kennt die Anzeige nicht.
- Schnellleiste am Handy unten: Anrufen, Route, Termin. Kein WhatsApp auf der Hauptseite (Vorgabe Awan).
- Terminanfrage über das Kontaktformular (wie auf der alten Seite), Knöpfe „Termin anfragen“ auf allen Seiten.
- Neue Seite „Neu bei uns“ mit Ablauf, Mitbringliste, Anfahrt und den drei PDF-Bögen (`website/downloads/`, Dateien von der Kundin).
- Bewertungen: Abschnitt auf der Startseite mit Link zu Google Maps. Bewusst keine eingebetteten Google-Bewertungen
  (würde Daten an Google senden und eine Einwilligung erfordern) und keine erfundenen Sternezahlen oder Zitate.
- Ratgeber mit drei ersten Artikeln (`quelltexte/inhalt_ratgeber.py`), Artikel-Daten für Google. Weitere Artikel einfach anhängen.
  Kundin bitte Artikel freigeben lassen.
- Barrierefreiheit: Erklärungsseite, Knöpfe „Schrift größer“ und „Bewegung aus“ (Einstellung lokal im Browser, im Datenschutz erwähnt),
  sichtbare Tastatur-Markierung.

## Runde 5 (06.10.2026)

- Leitsatz auf der Startseite mit Hintergrundbild (Foto 19, Hände im Team, `start-haende`), Text weiß auf dunklem Verlauf.
- Zweites Laufband unter dem Praxis-Bild, andere Reihenfolge, läuft in Gegenrichtung.
- Bewertungen mit Luftbild Laubenheim (Foto 11, `start-luftbild`) statt Google-Maps-Einbettung: lädt schnell, braucht keine Einwilligung,
  eine Karte hinter der Karte wäre unruhig und würde beim Scrollen Mausrad und Finger abfangen.
- Google Maps auf der Kontaktseite unter „Anfahrt“, erst nach Einwilligung (Kategorie „karten“).
- AO-Standard eingebunden: Einwilligungsbanner (`assets/js/einwilligung.js` + `ao-konfiguration.js`, Stand Kiefer) und
  Barrierefreiheits-Widget (`assets/js/barrierefreiheit.js`, Stand ao-karriere). Pro Kunde nur `ao-konfiguration.js` anpassen.
  Eigene Knöpfe „Schrift größer / Bewegung aus“ entfernt. Am Handy sitzt der Widget-Knopf über der Schnellleiste.
- Achtung Namenskonflikt: Das Banner nutzt `data-offen`. Die Öffnungsanzeige heißt deshalb `data-sprechzeit`.
