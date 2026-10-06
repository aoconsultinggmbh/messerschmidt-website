<?php
/* ============================================================================
   Kontaktformular Zahnzentrum Messerschmidt.
   Nimmt die Anfrage entgegen und schickt sie als E-Mail an die Praxis. Speichert nichts.

   $an   Empfänger der Anfragen (vor dem Livegang mit der Praxis abgestimmt)
   $von  Absender: echtes Postfach auf derselben Domain, sonst landet die Mail im Spam.
         Zum Antworten zählt das Reply-To mit der Adresse des Patienten.

   Schutz: Honigtopf-Feld "website", Zeitsperre 3 Sekunden, Kopfzeilen ohne Zeilenumbrüche,
   Pflichtfelder auch hier geprüft (dritte Stelle nach Browser und app.js).
   ============================================================================ */

$an  = 'info@zahnzentrum-messerschmidt.de';
$von = 'info@zahnzentrum-messerschmidt.de';

header('Content-Type: application/json; charset=utf-8');

function ende($ok, $text = '') { echo json_encode(array('ok' => $ok, 'text' => $text), JSON_UNESCAPED_UNICODE); exit; }
function wert($n) { $w = isset($_POST[$n]) ? trim((string) $_POST[$n]) : ''; return mb_substr($w, 0, 3000); }
function einzeilig($w) { return trim(preg_replace('/[\r\n]+/', ' ', $w)); }
function betreff($s) { return '=?UTF-8?B?' . base64_encode($s) . '?='; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); ende(false, 'Nur POST.'); }

if (wert('website') !== '') { ende(true, 'Danke!'); }
$start = (int) wert('zeit');
if ($start > 0 && (time() - (int) ($start / 1000)) < 3) { ende(true, 'Danke!'); }

$name      = einzeilig(wert('name'));
$telefon   = einzeilig(wert('telefon'));
$email     = einzeilig(wert('email'));
$anliegen  = einzeilig(wert('anliegen'));
$wunsch    = einzeilig(wert('wunschzeit'));
$nachricht = wert('nachricht');

if ($name === '' || $telefon === '' || $anliegen === '') { http_response_code(400); ende(false, 'Bitte füllen Sie alle Pflichtfelder aus.'); }
if (!filter_var($email, FILTER_VALIDATE_EMAIL))         { http_response_code(400); ende(false, 'Bitte prüfen Sie die E-Mail-Adresse.'); }
if (wert('datenschutz') !== 'ja')                       { http_response_code(400); ende(false, 'Bitte stimmen Sie der Datenschutzerklärung zu.'); }

$text = "Neue Anfrage über die Webseite\r\n\r\n"
      . "Anliegen:   $anliegen\r\n"
      . "Name:       $name\r\n"
      . "Telefon:    $telefon\r\n"
      . "E-Mail:     $email\r\n"
      . "Wunschzeit: " . ($wunsch !== '' ? $wunsch : '(keine Angabe)') . "\r\n\r\n"
      . "Nachricht:\r\n" . ($nachricht !== '' ? $nachricht : '(keine)') . "\r\n\r\n"
      . "Eingang: " . date('d.m.Y H:i') . " Uhr. Antworten geht direkt an den Absender.\r\n";

$kopf = "From: " . betreff('Webseite Zahnzentrum Messerschmidt') . " <$von>\r\n"
      . "Reply-To: " . betreff($name) . " <$email>\r\n"
      . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";

$ok = mail($an, betreff("Anfrage: $anliegen, $name"), $text, $kopf, "-f$von");
if (!$ok) { http_response_code(500); ende(false, 'Der Versand hat nicht geklappt. Bitte rufen Sie uns an: 06131 86926.'); }
ende(true, 'Danke! Ihre Anfrage ist angekommen. Wir melden uns schnellstmöglich.');
