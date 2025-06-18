= IAM-Blockchain

== Übergeordnetes Ziel & Aufgaben
Wir mussten ein dezentrales Identity Access Management System nach dem W3C Did, VC und
VP Standards entwickeln.

- Für Identities haben wir DIDs verwendet
- Für Access Management haben wir VCs und VPs verwendet.
- Für den dezentrales Ansatz haben wir auf Blockchain-Architektur gesetzt

== Teilaufgaben
Wir haben unsere Implementierung der Blockchain in mehrere Module unterteilt:

- Blockchain Core Module

    - Das Blockchain Core Module ist wie der Name bereits sagt, dass zentrale Module, dass die
      Funktionalität der Blockchain bereitstellt.

    - Das Module ist dafür zuständig Transaktionen, bestehend aus DIDs und VCs zu erstellen und
      an einen neuen Block anzuhängen.

    - Außerdem erstellt das Modul aus einem oder mehreren Transaktionen Blöcke, welche dann
      eine Kette aus Blöcken, der Blockchain angehängt werden

    - Die Transaktionen werden hierbei in einem sogenannten Merkle-Tree gehasht, welcher
      zusammen mit dem Timestamp, den Hash des letzten Blocks und dem Index genutzt wird,
      um den Block Hash zu berechnen.

    - Außerdem bietet der Blockchain core die Möglichkeit, automatisch neue Blöcke
      hinzuzufügen, wenn die Bedingung der Consensus Algorithmus erfüllt ist.

    - Der Konsens Algorithmus, der ebenfalls im Blockchain Core ist, umfasst derzeit eine
      Bedingung, die bei einem TransactionThreshold von 1, also beim hinzufügen einer neuen
      Transaktion, einen neuen Block generiert und der Blockchain hinzufügt.

- Storage Module

    - Das Storage Module unser kleinstes Modul, welches lediglich zum laden und speichern der
      Blockchain zuständig ist. Für das Projekt haben wir uns dazu entschieden, die Blockchain
      lediglich in einer Datei zu speichern

- API Module: besteht bei uns aus mehreren Untermodulen

    - Cli: Das Untermodul bietet uns die Möglichkeit, die verschiedenen Funktionen der
      Blockchain mit Kommandozeilenbefehlen zu testen. Dies war sehr hilfreich während der
      Entwicklung.

    - Web Interface:

        - Für die Kommunikation mit anderen Komponenten aus dem Projekt, damit z.B. das BMS
          oder die Cloud auf Daten der Blockchain zugreifen können oder um DIDs und VCs
          anzulegen oder zu revoken.

        - GET Endpunkte sind öffentlich

        - POST Endpunkte erfordern eine valides jws (Signatur)

    - Web UI

        - Wir haben eine einfache Web Oberfläche implementiert, dass man schön sieht was in der
          Blockchain steht. Diese Oberfläche zeigt alle Blocks, Dids und Schemadocs die für die
          Blockchain verwenden. Die Web GUI war keine Anforderungen, deswegen gibt es kein gutes
          Error Handling und alle Errors werden einfach in die Konsole geschrieben.

- Infrastruktur

    - Wir haben ein docker bundle für unser Projekt aufgesetzt, dass wir ein einfachen weg sowohl
      andere das Projekt einfach zu starten.

    - pyhton script

        - Stellt utilities bereit, welche die Entwicklung vereinfachen

        - U.a. werden Kommands wie cleanup, install und docs bereitgestellt sowie einen wrapper
          um obiges docker bundle zu steuern.

== Ergebnisse
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

== Probleme & Lösungen
- JWS Signature, die passende Key Generierung und w3c konforme Formate waren schwierig
  umzusetzen

- Generell bietet JWS wenig tooling. Einige web tools schaffen Abhilfe aber für effizientes
  testen waren immer python scripts notwendig

- Die Agile Arbeitsweise hatte zur folge, dass wir gezwungenermaßen immer wieder Änderungen
  an grundlegenden Datenstrukturen und Designentscheidungen vornehmen mussten. Dies
  haben wir mittels dem im Ergebnis beschriebenen JSON-first approach und code Generierung
  gelöst.

== Annahmen & Limitierungen
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
