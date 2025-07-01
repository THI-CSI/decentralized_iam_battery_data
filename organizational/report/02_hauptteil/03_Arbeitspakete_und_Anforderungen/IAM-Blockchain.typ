== IAM-Blockchain

=== Übergeordnetes Ziel & Aufgaben
Wir mussten ein dezentrales Identity Access Management System nach dem W3C Did, VC und
VP Standards entwickeln.

- Für Identities haben wir DIDs verwendet
- Für Access Management haben wir VCs und VPs verwendet.
- Für den dezentrales Ansatz haben wir auf Blockchain-Architektur gesetzt

=== Teilaufgaben
Wir haben uns dazu entschieden die Blockchain in Go zu entwickeln und haben deshalb bei der Implementierung die Komponente in mehrere eigenständige Module unterteilt, um eine klare Struktur und Funktionalität zu gewährleisten.

==== Core Module
Das Core Module ist das Herzstück der IAM-Blockchain und stellt die zentrale Funktionalität der Blockchain bereit. Es ist primär dafür verantwortlich, Transaktionen, die aus Decentralized Identities (DIDs) und Verifiable Credentials (VCs) bestehen, zu erstellen und an neue Blöcke anzuhängen. 
Das Modul aggregiert eine oder mehrere dieser Transaktionen zu Blöcken, die anschließend einer Kette aus Blöcken, der eigentlichen Blockchain, hinzugefügt werden.

Um die Integrität der Transaktionen zu gewährleisten, werden diese in einem Merkle-Tree gehasht. 
Dieser Merkle-Tree-Hash wird zusammen mit einem Timestamp, dem Hash des vorherigen Blocks und dem Block-Index verwendet, um den eindeutigen Block-Hash zu berechnen.

Ein weiterer wichtiger Bestandteil des Blockchain Cores ist die Fähigkeit, automatisch neue Blöcke der Chain hinzuzufügen, sobald die Bedingungen des Konsens-Algorithmus erfüllt wird. Aktuell ist dieser Algorithmus ledeglich darauf ausgelegt, einen neuen Block zu generieren und der Blockchain hinzuzufügen, sobald ein Transaktionsschwellenwert erreicht wird. Wir haben für die Demo den Schwellenwert auf eins gesetzt, um bei jeder neuen Transaktion einen neuen Block anzulegen.

==== Storage Module
Das Storage Module ist das kleinste Modul unserer Implementierung und hat die alleinige Aufgabe, die Blockchain zu laden und zu speichern. Für dieses Projekt haben wir uns entschieden, die gesamte Blockchain in einer einzigen Datei zu persistieren. 


==== API Module
Das API Module bietet verschiedene Schnittstellen zur Interaktion mit der Blockchain bereitstellen. Hierbei haben wir diese in weitere Untermodule kategorisiert.


Das CLI Modul, kurz für Command Line Interface oder Kommandozeilenschnittstelle, ermöglicht es, die verschiedenen Funktionen der Blockchain über Kommandozeilenbefehle auszuführen und zu testen. Dies erwies sich als äußerst nützlich während der Entwicklungsphase. 
Es gibt zum beispielsweise ein Argument, um eine neue Blockchain JSON Datei mit dem Genesis Block zu generieren, welcher die EU DID als Transaktion beinhaltet.

Außerdem bieten wir nach außen hin eine Web API bereit, welche dazu genutzt wird, damit andere Komponenten innerhalb des Projekts mit der Blockchain kommunizieren können. Es ermöglicht beispielsweise dem Battery Management System (BMS) oder der Cloud, DIDs und VCs anzulegen oder zu revoken, aber auch mit einer DID ein DID Dokument abzufragen. Außerdem bietet die API Endpunkte an um einzelne Blöcke oder Transaktionen aus der Blockchain abzufragen, welche für eine Frontends genutzt werden können. 
In der API sind alle GET-Endpunkte öffentlich zugänglich. Jedoch müssen alle POST-Endpunkte, die zum erstellen, verändern oder wiederrufen von DIDs und VCs genutzt werden, eine gültige JSON Web Signature (JWS) zur Authentifizierung mitliefern, um sich damit bei der Blockchain zu authentifizieren.

==== Web UI
 
Wir haben eine einfache Web-Oberfläche entwickelt, die eine klare Visualisierung der Blockchain-Inhalte ermöglicht. Diese Oberfläche zeigt alle relevanten Blocks, DIDs (Dezentrale Identifikatoren) und Schema-Dokumente, die in der Blockchain verwendet werden. Da diese Web-GUI nicht Teil der ursprünglichen Anforderungen war, wurde auf ein umfassendes Error Handling verzichtet; Fehler werden derzeit direkt in die Konsole geschrieben.

==== Infrastruktur

Für die Infrastruktur unseres Projekts haben wir ein Docker-Bundle erstellt. Dies ermöglicht einen unkomplizierten Start und einfache Tests unserer Anwendung.

Zusätzlich haben wir ein Utility-Skript implementiert, das die Entwicklung erheblich vereinfacht hat. Dieses Skript ist auch für andere Teams nützlich, da es einen einfachen Weg bietet, die Blockchain zu starten, Dokumentationen zu generieren oder die Anbindung ihrer Komponenten an die Blockchain zu testen. Dadurch werden komplexe und potenziell missverständliche Anleitungen in README-Dateien vermieden. Wir haben uns bewusst gegen die Verwendung eines Makefiles entschieden, da die Komplexität der benötigten Utilities zu hoch war. Das Skript stellt unter anderem Befehle wie `cleanup`, `install` und `docs` bereit und fungiert zudem als Wrapper zur Steuerung des erwähnten Docker-Bundles.

=== Ergebnisse
Bei der implementierung des blockchain cores war das finale Design der VC Records und DIDs,
welche auf der blockchain gespeichert werden, nicht klar. Daher haben wir hier auf einen JSON-
first approach gesetzt. JSONschemas definieren die Datenstruktur, welche die basis für die
Generierung von Datentypen bildet.

Die API hatten wir zunächst primitiv auf unseren core gesetzt und mussten viele Datentypen und
Services selbst definieren. Als es in Richtung integration ging, ergaben sich viele Änderungen am
konkrete Aufbau von DIDs, VCs, VC Records und VPs, sowie von den konkreten Requests. Das
hat uns veranlasst auch hier wieder auf Flexibilität zu setzen und den kompletten Webserver neu
zu schreiben. Der Schema-Ansatz erlaubt es uns außerdem mit Bibliotheksfunktionen rigoros
inputs/outputs der API zu validieren.

Nun werden alle Datenstrukturen, sowie POST Request bodies & Response bodies durch
JSONschemas definiert. Die API wird in einer großen openapi.yaml definiert, welche genannte
Schemas referenziert. Aus dieser yaml Datei werden wiederum Datentypen und handler interfaces
für das backend, sowie große Teile des frontends generiert.

Außerdem wird aus der openapi definition docs generiert.

Die Sourcecode-Dokumentation wurde sowohl für das Backend in golang als auch für das
frontend in typescript aus inline Kommentaren generiert.

=== Probleme & Lösungen
- JWS Signature, die passende Key Generierung und w3c konforme Formate waren schwierig
  umzusetzen

- Generell bietet JWS wenig tooling. Einige web tools schaffen Abhilfe aber für effizientes
  testen waren immer python scripts notwendig

- Die Agile Arbeitsweise hatte zur folge, dass wir gezwungenermaßen immer wieder Änderungen
  an grundlegenden Datenstrukturen und Designentscheidungen vornehmen mussten. Dies
  haben wir mittels dem im Ergebnis beschriebenen JSON-first approach und code Generierung
  gelöst.

=== Annahmen & Limitierungen
- Aktuell können nicht mehrere Instanzen der Blockchain laufen. Es fehlt ein peer2peer module,
  sowie ein ausgereifter Konsens Mechanismus.

- Die Suche nach einzelnen Transactions ist ineffizient, da schlichtweg die Chain vom neuesten
  Block ab durchsucht wird. Eine art Smart-Contract Schicht, welche zu jeder zeit alle aktiven
  VCs und DIDs zum Abruf bereit hält währe sinnvoll.

- Wird eine DID revoked, sollten auch alle DIDs revoked werden, die von ihr erzeugt wurden. Das
  passiert derzeit noch nicht.

- Es wird beim Anlegen einer neuen did nicht geprüft ob das publicKeyMultibase format korrekt
  ist. Sondern nur ob der Request korrekt signiert wurde und ob die controller did vom richtigen
  typ ist. Wenn im Folgenden dann versucht wird eine Signatur mit diesem key zu prüfen wird ein
  Fehler geworfen

- Werden zu schnell nacheinander Requests gestellt kann dies aktuell zu bugs führen bei denen
  der Transaction Threshold pro block überschritten wird. Die Transaktionen werden korrekt
  geprüft, und auch zuverlässig angelegt landen allerdings im falschen Block.

- Das JSONschema für den VC welcher den access von services steuert hat doppelte issuance & expiration dates.
