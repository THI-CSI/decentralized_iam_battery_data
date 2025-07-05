== Cloud

=== Übergeordnetes Ziel & Aufgaben

In der Cloud sollen Batteriepassdaten in einer verschlüsselten Form gespeichert werden. 
Die Zugriffskontrolle auf die Daten erfordert die Verwendung von DID-Dokumenten und Verifiable Credentials bzw. Verifiable Presentations. 
Dafür wurde entschieden, dass der Zugriff über eine API erfolgt, welche in Python geschrieben ist. 
Zu den Hauptaufgaben gehören also die Entwicklung der Schnittstelle und die Konzeption einer Datenbank für die Batteriepassdaten. 
Dazu gehören auch kryptografische Überlegungen sowie eine Dokumentation für die Anwendung. 
Zuletzt sollte auch eine visuelle Oberfläche für das Darstellen der Batteriepassdaten erstellt werden. #h(1fr) _Deniz_

=== Teilaufgaben

==== Batteriepass-Datenbank <clouddb>

Für die Datenbank benutzen wir TinyDB, ein Dokumenten-Datenbanksystem -- eine Art "MongoDB Lite". 
Dafür haben wir uns entschieden, da wir dadurch das BatteryPassDataModel für die Datenstruktur verwenden können. 
Das BatteryPassDataModel ist ein Datenmodell, das für die Implementierung des Batteriepasses von der Firma Circulor GmbH im Auftrag des Battery Pass Consortiums entwickelt wurde. 
In der Datenbank selbst werden die Daten der Batterie-Management-Systeme gespeichert. Die Daten sind verschlüsselt in einer JSON-Datei verfügbar. #h(1fr) _Ensar_

==== Batteriepass-Schnittstelle

Es wurde vom Cloud-Team entschieden, dass die Implementierung der API in Python mit FastAPI erfolgen soll. 
Grund dafür ist die Flexibilität der Sprache sowie bereits bestehende Sprachkenntnisse der Teammitglieder. 
Der initiale Gedanke war die Umsetzung über vier Methoden `PUT`, `POST`, `GET` und `DELETE`, 
mit welchen respektive die Funktionalitäten Erzeugen, Aktualisieren, Abrufen und Löschen des Batteriepasses dargestellt werden. 
Da die Übermittlung der Daten an die Cloud jedoch vertraulich sein muss, wird `POST` als Methode aller Endpunkte verwendet, 
die einen spezifischen Batteriepass ansteuern. Der initiale Wrapper-Payload wird genauer in #ref(<cloudcrypto>) beschrieben. 
Der entschlüsselte eigentliche Inhalt unterscheidet sich je nach Endpunkt. Genaueres dazu ist auf GitHub dokumentiert: 
#underline[#link("https://github.com/THI-CSI/decentralized_iam_battery_data/blob/main/cloud/docs/api.md", "Link")]. 
Die konkreten Endpunkte lauten wie folgt: #h(1fr) _Valentin_

#table(
  columns: 2,
  inset: 8pt,
  [*Endpunkt*], [*Beschreibung*],
  [`GET /`], [Allgemeiner Health-Check],
  [`GET /batterypass/`], [Abfrage aller DIDs, für die ein Batteriepass existiert],
  [`POST /batterypass/create/{did}`], [Erzeugen eines neuen Batteriepasses],
  [`POST /batterypass/update/{did}`], [Aktualisieren von bestimmten Batteriepassdaten],
  [`POST /batterypass/read/{did}`], [Abfragen von Batteriepassdaten je nach Zugriffsrecht],
  [`POST /batterypass/delete/{did}`], [Löschen eines Batteriepasses]
)

Die Batteriepassdaten orientieren sich an dem in #ref(<clouddb>) beschriebenen BatteryPassDataModel. 
Um sicherzustellen, dass die Daten die korrekte Form und Attributtypen besitzen, werden sie mithilfe eine JSON-Schema-Validators überprüft. 
Dieser kann für die Überprüfung eines kompletten BatteryPass-JSON-Dokuments oder einzelner Felder des Dokuments verwendet werden. 
Die Zugriffsrechte für die jeweiligen Attribute ist nach der DIN DKE SPEC 99100 implementiert. #h(1fr) _Deniz_

==== Batteriepass-UI

Die Oberfläche wurde mit Streamlit, einer Python-Bibliothek für einfache Datenvisualisierung, erstellt. 
In der Oberfläche lassen sich öffentliche Batteriepassdaten zu einer bestimmten DID und eine Liste aller verfügbaren DIDs anzeigen. 
Die öffentlichen Batteriepassdaten werden über die API abgefragt und in einer tabellarischen Ansicht dargestellt. 
Außerdem wird ein QR-Code erzeugt, welcher einen Link zu der Batteriepass-UI-Seite einer bestimmten DID enthält. 
Es lassen sich bisher keine nicht-öffentlichen Daten anzeigen. #h(1fr) _Ensar_

==== Kryptografische Überlegungen <cloudcrypto>

Die Datenübertragung vom BMS an die Cloud muss in ihrer Vertraulichkeit und Integrität geschützt sein. 
Initial sollte dafür das "Hybrid Public Key Encryption (HPKE)"-Verfahren genutzt werden. 
Dies war jedoch wegen Hardwarelimitationen seitens des BMS nicht möglich. Deshalb wird für den tatsächlichen Austausch eine JSON-Payload verwendet, 
die aus `ciphertext`, `eph_pub`, `aad`, `salt`, `did` und `signature` besteht. 
Mithilfe des öffentlichen Ephemeralschlüssels kann in Kombination mit dem privaten Schlüssel der Cloud die Nachricht entschlüsselt werden. 
Der öffentliche Cloud-Schlüssel würde in einem realen Kontext durch einen OEM oder die EU signiert und an die IAM-Blockchain veröffentlicht werden. 
Die im Payload enthaltene `did` ist die DID des Senders und wird verwendet, um den öffentlichen Schlüssel des Senders von der IAM-Blockchain abzufragen. 
Mit diesem kann die Signatur überprüft und sichergestellt werden, dass der Absender im Besitz des privaten Schlüssels ist. 
Eine weitere Anforderung war die Verwendung von Verifiable Presentations. Diese werden bei einer Leseabfrage überprüft und mit der IAM-Blockchain abgeglichen. 
Das Projektteam hat sich gemeinsam dazu entschieden NIST-P-256-Schlüssel zu verwenden. Diese werden auch verwendet, um die Batteriepassdaten verschlüsselt zu sichern. #h(1fr) _Valentin_

==== Dokumentation

Eine genaue API-Dokumentation ist unter `decentralized_iam_battery_data/cloud/docs` vorhanden. 
Die Swagger-Dokumentation der API ist innerhalb des Projektcodes mithilfe von Pydantic-Modellen beschrieben 
und kann unter `http://example.instance.cloud/docs` abgerufen werden. #h(1fr) _Ensar_

=== Ergebnisse

In der Cloud-Datenbank können mehrere Batteriepässe für DIDs erstellt und verwaltet werden. Die Löschung funktioniert ebenso
und ermöglicht das vollständige Ausleben einer Batterie.
Das Cloud-System ist über Docker-Compose startbar und funktioniert den Anforderungen entsprechend. #h(1fr) _Deniz_

=== Probleme & Lösungen

Hardwarelimitationen des BMS haben dazu geführt, dass die Implementierung der kryptografischen Funktionen erschwert wurden. HPKE konnte beispielsweise nicht  verwendet werden. 
Als Lösung musste gemeinsam mit dem BMS-Team ein Schema definiert werden.
Zudem gab es Schwierigkeiten im Deployment-Prozess durch die Docker-Netzwerkkonfiguration, welche jedoch gelöst werden konnten. #h(1fr) _Deniz_

=== Annahmen & Limitierungen

Das verwendete Kryptoverfahren ist zum jetzigen Standpunkt nicht gegen Replay-Angriffe geschützt. 
Dies muss in der Zukunft angegangen werden, beispielsweise mit einem Challenge-Response-Verfahren. #h(1fr) _Valentin_ #linebreak() #v(1pt)
Des weiteren ist derzeit nur vorgesehen, dass eine Cloud-Instanz gestartet und gemanagt wird. 
Außerdem existiert kein Mechanismus um sicherzustellen, dass die Batteriedaten erhalten bleiben, 
falls der Cloud-Anbieter die Infrastruktur nicht mehr erhalten kann, zum Beispiel in einem Insolvenzfall. 
Die Cloud ist zudem abhängig vom BatteryPassDataModel, inklusive der enthaltenen Rechtschreibfehler innerhalb der Schemadefinition.
Diese müssen in der Zukunft beim öffentlichen GitHub-Repository ausgebessert werden. 
Außerdem sollte TinyDB zukünftig durch eine robuste und skalierbare Datenbanklösung wie beispielsweise MongoDB abgelöst werden. #h(1fr) _Deniz_ #linebreak() #v(1pt)
Eventuell wäre es auch interessant,  sich eine
dezentrale Speicherung der Batteriepassdaten selbst anzuschauen. Bei dieser muss jedoch überlegt werden, wie private Daten gespeichert werden sollen.
Ein weiterer Aspekt, welcher ausgebaut werden sollte, ist die visuelle Oberfläche. In ihr lassen sich zum jetzigen Standpunkt nur öffentliche Daten anzeigen.
Eine Unterstützung für das Hochladen von VPs und der Betrachtung von nicht-öffentlichen Daten wäre denkbar und nicht zu komplex. #h(1fr) _Valentin_
