#import "../../conf.typ": customFigure
#pagebreak(weak: true)
== Systemarchitektur <systemarchitektur>

Wir schlagen eine Architektur aus drei Zentralen Komponenten (siehe @systemarchitektur_diagramm) vor, die über standardisierte und gesicherte Schnittstellen miteinander kommunizieren, um eine dezentrale Verwaltung von Batteriedaten und Zugriffsrechten zu ermöglichen. 

#customFigure(
  image("../../assets/systemarchitektur.png", width: 95%),
  caption: "Diagramm der Systemarchitektur des Projekts",
) <systemarchitektur_diagramm>

Diese Architektur besteht aus:

+ *@arbeitspaket_iam_blockchain*: Verwaltet die @DID:pl, Zugriffsrechte und Transaktionen. Sie ermöglicht eine transparente und unveränderliche Aufzeichnung aller Vorgänge.

+ *@arbeitspaket_bms*: @BMS:long, das Sensordaten erfasst, diese verschlüsselt und über eine gesicherte Schnittstelle an eine oder mehrere Cloud-Datenbanken überträgt.

+ *@arbeitspaket_cloud*: Dient als Backend, das die Daten des @BMS empfängt, entschlüsselt, validiert und speichert. Es stellt die Schnittstelle zum digitalen Batteriepass dar und verwaltet Zugriffsrecht.

Zusätzlich:

- *@infrastructure_oem_service*: Simuliert die Rolle des Batterieherstellers (@OEM), der den digitalen Batteriepass erstellt und für die @DID:pl des @BMS signiert.

#parbreak()
Die Interaktion zwischen den Komponenten ist klar strukturiert, um Sicherheit und Nachvollziehbarkeit zu gewährleisten:

- *Schnittstellen und Protokolle*: Die gesamte Kommunikation erfolgt über HTTP-basierte REST-APIs, was eine flexible und standardisierte Anbindung ermöglicht.

- *Datenformate*: Als primäres Datenformat für den Austausch wird JSON verwendet. Die Struktur der Identitätsdokumente und Berechtigungsnachweise folgt den W3C-Standards für @DID:pl, VCs und VPs.

- *Sicherheit und Authentifizierung*: Die Kommunikation ist mehrstufig abgesichert.

  - Die Datenübertragung vom @BMS zur Cloud wird durch ein hybrides Verschlüsselungsverfahren geschützt, das Vertraulichkeit und Integrität der Batteriedaten sicherstellt.

  - Schreibende Zugriffe auf die Blockchain-API, wie das Registrieren einer @DID oder das Ausstellen eines VCs, erfordern eine Authentifizierung mittels @JWS. Dadurch wird sichergestellt, dass nur autorisierte Entitäten Änderungen am Vertrauensregister vornehmen können.

Durch diese Architektur konzentriert sich das @BMS auf die reine Datenerfassung, die Cloud auf die Datenverarbeitung und -darstellung und die Blockchain auf die dezentrale und manipulationssichere Verwaltung von Identitäten und Rechten.

Ein neues @BMS wird wie in @bms_creation_appendix abgebildet in das System integriert. Zunächst registriert es sich bei der Blockchain, anschließend sendet es periodisch die Updates an predefinierte Cloud-Endpunkte. Diese Endpunkte sind in der Blockchain hinterlegt und können über die @DID:pl des @BMS:pl abgefragt werden. Der Batteriepass wird durch den @OEM signiert und in der Blockchain hinterlegt.