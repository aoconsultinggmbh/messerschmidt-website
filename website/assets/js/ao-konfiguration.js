/* ============================================================================
   KONFIGURATION für das Einwilligungsbanner (AO-Standard).
   DIESE DATEI IST DIE EINZIGE, DIE PRO KUNDE ANGEPASST WIRD.
   Kategorie „karten“: Google Maps auf der Kontaktseite, lädt erst nach Zustimmung.
   Kommt später etwas hinzu (z. B. Statistik mit Cookies), hier eintragen UND die
   Datenschutzerklärung anpassen.
   ============================================================================ */
window.AO_EINWILLIGUNG = {
  datenschutz: '/datenschutz.html',
  impressum: '/impressum.html',
  kategorien: [
    {
      id: 'notwendig',
      name: 'Notwendig',
      kurz: 'Hält die Webseite funktionsfähig und speichert Ihre Entscheidung aus diesem Fenster. Ohne diese Funktionen lässt sich die Seite nicht sinnvoll anzeigen.',
      pflicht: true,
      dienste: [{
        name: 'Einwilligungsspeicher',
        anbieter: 'Zahnzentrum Messerschmidt, Dr. Sabine Messerschmidt, Parkstraße 33, 55130 Mainz-Laubenheim',
        zweck: 'Speichert, welchen Diensten Sie zugestimmt haben, damit Sie nicht bei jedem Aufruf erneut gefragt werden.',
        art: 'Lokaler Speicher im Browser, kein Cookie',
        dauer: '12 Monate'
      }]
    },
    {
      id: 'karten',
      name: 'Karten',
      kurz: 'Lädt die Anfahrtskarte von Google Maps auf der Kontaktseite. Erst dann wird Ihre IP-Adresse an Google übertragen.',
      dienste: [{
        name: 'Google Maps',
        anbieter: 'Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland',
        zweck: 'Zeigt die Anfahrt zum Zahnzentrum auf einer interaktiven Karte.',
        art: 'Einbettung über iframe, Übertragung der IP-Adresse, Verarbeitung auch in den USA möglich',
        dauer: 'Siehe Datenschutzerklärung von Google'
      }]
    }
  ]
};
