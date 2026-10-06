# Ratgeber-Artikel. Allgemeine Patienteninformation, keine Heilversprechen, keine Gedankenstriche.
# Neue Artikel einfach unten anhängen; neueste zuerst wird automatisch sortiert (datum).
# Felder: slug, titel (H1), seo (Titel vor „| Zahnzentrum Messerschmidt“), beschreibung (Meta 140–160),
#   datum (ISO), lesezeit (Min.), kurz (Antwortbox), abschnitte [(H2, [Absatz, ...])], leistung (slug für den Querverweis)

RATGEBER = [
  dict(slug="zahnfleischbluten-was-tun", datum="2026-10-06", lesezeit=4,
       titel="Zahnfleischbluten: Was steckt dahinter und was hilft?",
       seo="Zahnfleischbluten: was tun?",
       beschreibung="Zahnfleischbluten beim Putzen? Häufige Ursachen, was Sie selbst tun können und wann Sie in die Zahnarztpraxis kommen sollten. Ratgeber vom Zahnzentrum Messerschmidt.",
       kurz="Zahnfleischbluten ist meist ein Zeichen für eine Entzündung des Zahnfleisches durch Beläge. Gründliche, aber sanfte Pflege mit Reinigung der Zwischenräume hilft oft schon nach wenigen Tagen. Hält das Bluten länger als etwa eine Woche an, sollten Sie es in der Zahnarztpraxis abklären lassen, denn dahinter kann eine Parodontitis stecken.",
       abschnitte=[
         ("Warum blutet das Zahnfleisch?", ["Gesundes Zahnfleisch blutet beim Putzen normalerweise nicht. Häufigste Ursache für Zahnfleischbluten sind bakterielle Beläge am Zahnfleischrand. Das Zahnfleisch reagiert darauf mit einer Entzündung, Fachleute sprechen von Gingivitis. Es wird rot, schwillt an und blutet leicht.",
                                           "Weitere mögliche Gründe sind eine zu harte Zahnbürste oder zu starker Druck beim Putzen, hormonelle Veränderungen etwa in der Schwangerschaft, bestimmte Medikamente wie Blutverdünner oder Allgemeinerkrankungen wie Diabetes."]),
         ("Gingivitis oder schon Parodontitis?", ["Eine Gingivitis betrifft nur das Zahnfleisch und kann bei guter Pflege vollständig abheilen. Bleibt die Entzündung über längere Zeit bestehen, kann sie in die Tiefe gehen und den Zahnhalteapparat angreifen. Dann spricht man von Parodontitis. Typisch sind zusätzlich Mundgeruch, zurückgehendes Zahnfleisch, empfindliche Zahnhälse und im späteren Verlauf lockere Zähne.",
                                                   "Weil eine Parodontitis oft keine Schmerzen macht, wird sie häufig spät bemerkt. Ob es sich um eine Gingivitis oder eine Parodontitis handelt, lässt sich nur in der Zahnarztpraxis sicher feststellen, zum Beispiel durch das Messen der Zahnfleischtaschen."]),
         ("Was Sie selbst tun können", ["Putzen Sie weiter, auch wenn es blutet. Gerade dann ist es wichtig, die Beläge zu entfernen. Verwenden Sie eine weiche Zahnbürste und putzen Sie mit wenig Druck.",
                                        "Reinigen Sie täglich die Zahnzwischenräume mit Zahnseide oder passenden Zwischenraumbürsten. Dort beginnen die meisten Entzündungen.",
                                        "Achten Sie auf zuckerarme Ernährung und verzichten Sie möglichst aufs Rauchen. Rauchen kann Zahnfleischbluten sogar verdecken, weil es die Durchblutung verringert."]),
         ("Wann Sie zu uns kommen sollten", ["Wenn das Zahnfleisch trotz guter Pflege länger als etwa eine Woche blutet, wenn Mundgeruch, Schwellungen oder Schmerzen dazukommen oder wenn sich Zähne locker anfühlen, sollten Sie einen Termin vereinbaren. Wir untersuchen Ihr Zahnfleisch, entfernen Beläge und Zahnstein in einer professionellen Zahnreinigung und behandeln bei Bedarf eine Parodontitis.",
                                             "Im Zahnzentrum Messerschmidt hat Dr. Sabine Messerschmidt den Tätigkeitsschwerpunkt Parodontologie."]),
       ], leistung="feste-zaehne"),

  dict(slug="kind-erster-zahnarztbesuch", datum="2026-10-06", lesezeit=4,
       titel="Der erste Zahnarztbesuch mit Kind: wann und wie?",
       seo="Erster Zahnarztbesuch mit Kind",
       beschreibung="Ab wann sollte Ihr Kind zum Zahnarzt, wie bereiten Sie es vor und was passiert beim ersten Termin? Tipps für Eltern vom Zahnzentrum Messerschmidt in Mainz.",
       kurz="Der erste Zahnarztbesuch ist sinnvoll, sobald die ersten Milchzähne da sind, meist zwischen dem sechsten und zwölften Lebensmonat. Am besten kommt Ihr Kind ohne Beschwerden, einfach zum Kennenlernen. Bis sechs Jahre empfehlen wir einen, danach zwei Kontrolltermine im Jahr.",
       abschnitte=[
         ("Ab wann zum Zahnarzt?", ["Der erste Termin ist sinnvoll, sobald der erste Milchzahn durchgebrochen ist. Für Kinder ab dem sechsten Lebensmonat gibt es zahnärztliche Früherkennungsuntersuchungen, die die gesetzlichen Krankenkassen übernehmen. So können wir früh beraten und mögliche Probleme erkennen, bevor sie entstehen."]),
         ("Warum Milchzähne so wichtig sind", ["Milchzähne fallen zwar später aus, sie haben aber wichtige Aufgaben. Sie helfen beim Kauen und Sprechenlernen und halten den Platz für die bleibenden Zähne frei. Karies an Milchzähnen kann Schmerzen verursachen und sich auf die nachfolgenden Zähne auswirken."]),
         ("So bereiten Sie Ihr Kind vor", ["Sprechen Sie positiv und entspannt über den Besuch. Vermeiden Sie Sätze wie „Du brauchst keine Angst zu haben“ oder „Es tut nicht weh“, denn sie bringen das Kind erst auf den Gedanken, dass es Grund zur Angst geben könnte.",
                                           "Bilderbücher über den Zahnarztbesuch oder ein Rollenspiel zu Hause, bei dem das Kuscheltier untersucht wird, helfen beim Vorbereiten. Planen Sie den Termin zu einer Tageszeit, zu der Ihr Kind ausgeruht ist."]),
         ("Was beim ersten Termin passiert", ["Beim ersten Besuch geht es vor allem ums Kennenlernen. Ihr Kind darf sich in Ruhe umsehen, auf dem Behandlungsstuhl hoch und runter fahren und die Lampe ausprobieren. Wenn es mitmacht, schauen wir uns die Zähne an. Sie erhalten Tipps zur Pflege, zur passenden Zahnpasta mit Fluorid und zur Ernährung.",
                                              "Je öfter Kinder ohne Beschwerden kommen, desto vertrauter wird die Praxis. Das hilft, wenn doch einmal eine Behandlung nötig ist."]),
         ("Zähneputzen bei Kleinkindern", ["Mit dem ersten Zahn beginnt das Putzen, zweimal täglich mit einer weichen Kinderzahnbürste und einer Kinderzahnpasta mit Fluorid in der empfohlenen Menge. Bis ins Grundschulalter sollten Eltern nachputzen, weil Kinder die nötige Geschicklichkeit erst nach und nach entwickeln."]),
       ], leistung="junge-zaehne"),

  dict(slug="zahnersatz-was-zahlt-die-kasse", datum="2026-10-06", lesezeit=5,
       titel="Zahnersatz: Was zahlt die gesetzliche Krankenkasse?",
       seo="Zahnersatz: Was zahlt die Kasse?",
       beschreibung="Festzuschuss, Bonusheft und Härtefall einfach erklärt: So beteiligt sich die gesetzliche Krankenkasse an Kronen, Brücken, Prothesen und Implantaten.",
       kurz="Bei Zahnersatz zahlt die gesetzliche Krankenkasse einen befundbezogenen Festzuschuss. Er beträgt 60 Prozent der Kosten der sogenannten Regelversorgung und steigt mit lückenlos geführtem Bonusheft auf 70 Prozent (fünf Jahre) oder 75 Prozent (zehn Jahre). Vor jeder Behandlung erhalten Sie einen Heil- und Kostenplan, den die Kasse genehmigt.",
       abschnitte=[
         ("Der Festzuschuss", ["Für Zahnersatz wie Kronen, Brücken und Prothesen zahlt die gesetzliche Krankenkasse einen Festzuschuss. Er richtet sich nicht nach der gewählten Versorgung, sondern nach dem Befund, also danach, was im Mund fehlt oder geschädigt ist. Für jeden Befund gibt es eine sogenannte Regelversorgung: eine medizinisch notwendige, bewährte Standardlösung.",
                               "Der Festzuschuss beträgt 60 Prozent der durchschnittlichen Kosten dieser Regelversorgung. Wählen Sie eine aufwendigere Lösung, bleibt der Zuschuss gleich, und Sie tragen die Differenz selbst."]),
         ("Mehr Zuschuss mit dem Bonusheft", ["Wer regelmäßig zur Kontrolle geht und das im Bonusheft dokumentieren lässt, erhält einen höheren Festzuschuss: 70 Prozent bei lückenlosen Einträgen über fünf Jahre, 75 Prozent bei zehn Jahren. Bringen Sie Ihr Bonusheft deshalb zu jeder jährlichen Kontrolle mit."]),
         ("Härtefallregelung", ["Bei geringem Einkommen kann ein Anspruch auf den doppelten Festzuschuss bestehen. Dann übernimmt die Kasse die Kosten der Regelversorgung vollständig. Ob Sie dazu berechtigt sind, klären Sie mit Ihrer Krankenkasse."]),
         ("Und Implantate?", ["Implantate gehören in der Regel nicht zur Regelversorgung. Die Krankenkasse zahlt aber auch hier den Festzuschuss, der für den jeweiligen Befund vorgesehen ist, zum Beispiel für die Krone auf dem Implantat. Die übrigen Kosten sind privat. Eine Zahnzusatzversicherung kann einen Teil übernehmen, je nach Vertrag."]),
         ("Der Heil- und Kostenplan", ["Vor der Behandlung erstellen wir einen Heil- und Kostenplan. Darin stehen der Befund, die geplante Versorgung und die voraussichtlichen Kosten. Sie reichen den Plan bei Ihrer Krankenkasse ein, die den Festzuschuss genehmigt. Erst dann beginnt die Behandlung. So wissen Sie vorher, mit welchem Eigenanteil Sie rechnen müssen.",
                                       "Kronen, Brücken und Inlays fertigt das Zahnzentrum Messerschmidt im eigenen Dentallabor. Bei Fragen zu Ihrem Heil- und Kostenplan beraten wir Sie gerne."]),
       ], leistung="neue-zaehne"),
]
