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

- [ ] **Fotos der Zahnärztinnen:** Olga Miller, Dr. Lisa Blatt und Dr. Alina Günther haben vorerst ein Monogramm statt Foto. Welche Portraits aus dem Shooting (Nr. 66–104) sind wer?
- [ ] **Team-Liste:** Die bisherige Seite nennt 14 Mitarbeiterinnen namentlich (Stand unklar). Mit Namen aufnehmen? Dann Liste bestätigen lassen.
- [ ] **Hanh Geyrhofer** wird auf der alten Seite als Kinderzahnärztin/Endodontie genannt, steht aber nicht mehr bei den Zahnärztinnen. Bewusst weggelassen.
- [ ] **Homöopathie** von der alten Seite nicht übernommen (Heilmittelwerberecht); Akupunktur bleibt als begleitendes Angebot.
- [ ] **Anamnesebogen/Anmeldebogen** (PDF-Downloads der alten Seite): Dateien von der Kundin holen und auf Patienteninfos verlinken.
- [ ] **Kontaktformular** bewusst nicht eingebaut (Gesundheitsdaten im Freitext); Kontakt per Telefon/E-Mail. Mit Kundin klären.
- [ ] Impressum: „Umsatzsteueridentifikationsnummer 28/114/5003/0“ ist das Format einer Steuernummer.
- [ ] Karriere-Link zeigt in der Vorschau auf messerschmidt-karriere.vorschau.ao-consult.de, vor dem Livegang in `quelltexte/bauen.py` (KARRIERE) auf die Karriere-Domain umstellen.
- [ ] Alte Adressen weiterleiten (Livegang): /uber-uns/ → /team.html, /praxis/… → /praxis.html, /service/patienteninfos/ → /patienteninfos.html, /anfahrt/ und /kontakt/ → /kontakt.html; /leistungen/<name>/ → /leistungen/<name>.html (gleiche Namen).
- [ ] Matomo-Eintrag anlegen, Kennung in `website/assets/js/statistik.js` (seite) eintragen.
