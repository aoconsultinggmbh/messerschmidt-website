# messerschmidt-website – Hauptseite Zahnzentrum Messerschmidt (Mainz-Laubenheim)

Neue Hauptseite, gebaut von der AO Consulting GmbH. Ersetzt die bisherige WordPress/Divi-Seite unter
https://zahnzentrum-messerschmidt.de/.

- **Vorschau:** https://messerschmidt.vorschau.ao-consult.de (Zweig `main`, Google ausgesperrt)
- **Live:** https://zahnzentrum-messerschmidt.de (Zweig `live`, nur auf das Wort „live“ eines Mitarbeiters)
- **Karriereseite:** eigenes Projekt `messerschmidt-karriere`, wird nach dieser Seite gestalterisch angeglichen.

## Aufbau

| Ordner | wofür |
|---|---|
| `quelltexte/bauen.py` | baut alle HTML-Seiten (Kopf, Fuß, Texte). Leistungstexte in `quelltexte/inhalt_leistungen.py` |
| `website/` | die Seite, nur was hier liegt, geht online. HTML wird von `bauen.py` erzeugt, **nicht von Hand ändern** |
| `website/assets/` | CSS, JavaScript, Schrift Manrope (lokal), Bilder (jpg + webp), Hero-Video |
| `doku/` | Entscheidungen, offene Punkte, Bildzuordnung, Checkliste Livegang |

Ändern: Text in `quelltexte/` anpassen, dann `python3 quelltexte/bauen.py`, dann hochladen.
Regeln: Sie-Ansprache, keine Gedankenstriche (das Skript bricht sonst ab), keine Heilversprechen.

## Vor dem Livegang

Siehe `doku/entscheidungen.md` (offene Punkte) und `doku/checkliste-livegang.md`.
