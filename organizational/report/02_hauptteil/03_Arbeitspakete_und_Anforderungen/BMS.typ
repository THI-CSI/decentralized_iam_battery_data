// Import customFigures and longline
#import "../../conf.typ": customFigure, longline

== @BMS:short <arbeitspaket_bms>
=== Übergeordnetes Ziel & Aufgaben <bms_uebergeordnetes_ziel_und_aufgaben>
Ziel dieses Arbeitspakets war die Entwicklung einer Firmware für ein @BMS:both.

=== Aufgabenverteilung <bms_aufgabenverteilung>
Während Matthias und Florian die Firmware auf realer Hardware mit einem Renesas-Mikrocontroller entwickelten und testeten, erstellte Patrick ein ergänzendes Mock-@BMS in Python, das als Simulationsumgebung für das System diente.
Die Firmware-Entwicklung erfolgte arbeitsteilig: Matthias und Florian übernahmen jeweils unterschiedliche technische Schwerpunkte. Florian war insbesondere für die interne Architektur der Firmware verantwortlich. Er konzipierte und implementierte ein Verfahren zur Erstellung von Nachrichten. Dieses Verfahren ermöglicht die sichere Übertragung dynamischer Batteriedaten über einen unverschlüsselten, verbindungslosen Kanal – wie er im Projektsetup zwischen dem @BMS und den Cloud-Endpunkten verwendet wird – unter Gewährleistung von Vertraulichkeit, Integrität und Authentizität. Darüber hinaus war er maßgeblich an der Gestaltung und Strukturierung des Programmablaufs sowie der Programmlogik beteiligt, beispielsweise im Bereich der Inter-Task-Kommunikation.
Matthias war hauptsächlich für die Netzwerkanbindung des Systems verantwortlich, sodass das @BMS nach außen kommunizieren und so unter anderem die zuvor generierten Nachrichten mit den Battriedaten an die Cloud-Endpunkte senden kann.

#pagebreak()
=== Programmablauf und -logik <bms_programmablauf_und_logik>

Nach dem Flashen der Firmware wird in der main-Funktion zunächst das RTOS initialisiert. Dazu zählen unter anderem das Einrichten der Tasks, die Konfiguration des Schedulers sowie das Anlegen der benötigten Objekte der @ITC. Das folgende Sequenzdiagramm veranschaulicht vereinfacht die Programmlogik und den grundlegenden Ablauf der Firmware – beispielsweise unter Verwendung von Mechanismen wie dem Deferred Interrupt Handling.
#customFigure(
  image("../../assets/program_flow.png", width: 100%),
  caption: [Program flow @BMS],
) <ProgramFlowBMS>
Mit Ausnahme der Funktionalität zur Signierung von Service-@VC:pl und deren Schreiben auf die Blockchain ist der übrige Ablauf bereits vollständig auf der Hardware implementiert.
#pagebreak()

=== Nachrichtengenerierung <bms_nachrichtengenerierung>
Wie bereits in Abschnitt 3.5.2 beschrieben, war ich zudem für die Konzeption und Entwicklung eines Verfahrens zur Nachrichtenerstellung verantwortlich. Dieses Verfahren kommt im dargestellten Programmablauf an der mit ① markierten Stelle zum Einsatz: Nachdem im Rahmen einer Simulation einmalig die dynamischen Batteriedaten abgefragt wurden, wird für jedes empfangene DID_doc (Cloud-Endpunkt) eine individuelle Nachricht mit den dynamischen Batteriedaten erzeugt und anschließend versendet.

Der Prozess zur Erstellung einer solchen Nachricht umfasst folgende Schritte:

1. Es wird ein temporäres ECC-Schlüsselpaar auf Basis der Kurve secp256r1 erzeugt. Mithilfe des privaten Schlüssels dieses Paares sowie des öffentlichen Schlüssels des Empfängers (extrahiert aus dem jeweiligen DID_doc) wird per ECDH ein gemeinsames Geheimnis berechnet.

2. Aus dem gemeinsamen Geheimnis wird unter Verwendung eines Salt-Werts und eines Info-Blocks (bestehend aus „cloud_pub_key“ und „bms_signing_pub_key“) mittels HKDF (basierend auf SHA-256) ein symmetrischer Schlüssel abgeleitet.

3. Die zuvor abgefragten Batteriedaten werden mit dem symmetrischen Schlüssel durch das AES-GCM-256-Verfahren verschlüsselt und authentifiziert.

4. Die verschlüsselten Batteriedaten sowie weitere für den jeweiligen Cloud-Endpunkt relevante Informationen werden in ein JSON-Dokument eingebettet (@MessageLayout) und mit dem privaten Schlüssel des @BMS digital signiert. Dies ermöglicht dem Empfänger sowohl die Entschlüsselung als auch die Überprüfung von Integrität und Authentizität der Nachricht.

5. Die so erzeugte Nachricht wird zusammen mit dem zugehörigen Service-Endpoint (ebenfalls aus dem DID_doc extrahiert) an den Network Task übergeben.

Die generierten Nachrichten (siehe Struktur @MessageLayout) können anschließend über einen ungesicherten, verbindungslosen Kanal an die Cloud-Endpunkte übertragen werden, ohne dass dabei die Vertraulichkeit, Integrität oder Authentizität der Batteriedaten gefährdet wird.
#customFigure(
  image("../../assets/message_layout.png", width: 100%),
  caption: "Message Layout",
) <MessageLayout>
Der Timestamp wird im aktuellen Projekt-Setup noch nicht berücksichtigt, könnte aber zukünftig als Replay-Schutz eingesetzt werden.

Die kryptografischen Funktionen wurden mit mbedTLS implementiert, das die PSA-Crypto-API unterstützt. Über das FSP-Package und den HAL-Treiber rm_psa_crypto kann die @SCE der MCU direkt angesprochen werden. Dadurch lassen sich die meisten kryptografischen Operationen hardwarebeschleunigt und sicher im isolierten Speicher der @SCE ausführen.

=== Networking <bms_networking>

Die Netzwerkkommunikation des Renesas-Mikrocontrollers erfolgt über eine physische Ethernet-Verbindung zu einem Laptop, welcher die Infrastruktur der Cloud- und Blockchain-Endpunkte simuliert. Nach der Initialisierung des IP-Stacks wird der Mikrocontroller befähigt, Netzwerkkommunikation über das statisch konfigurierte IPv4-Netzwerk durchzuführen. Die Netzwerkkonfiguration umfasst die IP-Adresse 192.168.0.52, ein Gateway unter 192.168.0.3 sowie die Verwendung eines lokalen DNS-Servers (dnsmasq) auf 192.168.0.2, welcher für die Namensauflösung der Cloud-Endpunkte verantwortlich ist. Alle IP-Adressen sind statisch vergeben.

Jeden Monat beginnt der Mikrocontroller mit dem Sammeln der @DID:pl der Cloud-Endpunkte aus der Blockchain. Jede Batteriedaten-Nachricht wird vor dem Versand mit den entsprechenden kryptografischen Schlüsseln verschlüsselt. Die Verschlüsselung und der Nachrichtenversand werden über zwei getrennte FreeRTOS-Tasks koordiniert:
- net_task: Verantwortlich für das Netzwerkhandling und die Kommunikation mit der IP-Schicht.
- message_creation_task: Zuständig für die Verschlüsselung und Erstellung der Nachrichten unter Verwendung der jeweils zugeordneten Schlüssel.

Zwischen diesen beiden Tasks erfolgt der Datenaustausch über einen MessageBuffer, welcher verschlüsselte Nachrichten vom message_creation_task entgegennimmt und sie an den net_task weiterleitet. Der Versand an die Endpunkte erfolgt über eine FreeRTOS-Queue, wodurch eine deterministische und task-sichere Weitergabe der verschlüsselten Nachrichten gewährleistet wird.

Zur Simulation der Endpunkte wurde bewusst auf ein Podman-Netzwerk statt Docker zurückgegriffen. Dies erlaubt eine feinere Steuerung der Firewall-Einstellungen, insbesondere in Kombination mit iptables und aktiviertem IPv4-Forwarding. Durch diese Konfiguration ist es möglich, eingehende Pakete vom Mikrocontroller über das Ethernet-Interface in das Podman-Netzwerk weiterzuleiten. Die Firewall-Regeln wurden so definiert, dass:

- der Mikrocontroller ausgehende Verbindungen in das Podman-Netzwerk initiieren darf,
- jedoch nur bestehende Verbindungen aus dem Podman-Netzwerk Antworten an den Mikrocontroller senden dürfen.

=== Werkzeuge und Methoden zur Firmwareentwicklung <bms_werkzeuge_und_methoden_zur_firmwareentwicklung>

Als Betriebssystem für den Mikrocontroller kommt FreeRTOS zum Einsatz, da alternative RTOS-Optionen wie Zephyr für das verwendete Renesas-Modell keine Unterstützung für Ethernet-Kommunikation bieten. Die gesamte Firmware ist dokumentiert mittels Doxygen, um eine nachvollziehbare und wartbare Codebasis zu gewährleisten.

Für die Entwicklung der Firmware kommt eine bewährte und plattformübergreifend einsetzbare Toolchain zum Einsatz. Der Compiler ist arm-none-eabi-gcc, ein etablierter Cross-Compiler für ARM-Architekturen. Dieser wurde gewählt, da er eine breite Unterstützung für verschiedene ARM-basierten Mikrocontroller bietet und die Portabilität zwischen unterschiedlichen Zielsystemen erleichtert.

Das Buildsystem basiert auf klassischen Makefile-Strukturen. Diese wurden manuell konfiguriert, da sie für die Anforderungen des Projekts eine einfache, transparente und gleichzeitig performante Möglichkeit zur Verwaltung des Kompilierungsprozesses darstellen. Komplexere Buildsysteme wie CMake wurden bewusst vermieden, um volle Kontrolle über den Buildprozess zu behalten und zusätzliche Abhängigkeiten zu vermeiden.

Für das Debugging kommt der plattformübergreifende SEGGER J-Link Debug-Probe zum Einsatz, welcher eine zuverlässige JTAG/SWD-Kommunikation mit dem Mikrocontroller ermöglicht. Durch die breite Unterstützung in IDEs wie SEGGER Embedded Studio sowie über GDB ist ein effizienter und stabiler Debug-Workflow gewährleistet.

Das Flashing der Firmware erfolgt über den Renesas Flash Programmer, das offizielle Tool von Renesas. Es bietet eine robuste und zuverlässige Möglichkeit zur Programmierung des Mikrocontrollers über serielle oder JTAG-Schnittstellen und lässt sich gut in bestehende Entwicklungsumgebungen integrieren.


=== Herausforderungen & Lösungsansätze <bms_herausforderungen_und_loesungsansaetze>

- Die Umsetzung eines hardware-nahen Setups stellte anfangs eine Herausforderung dar, konnte letztlich jedoch erfolgreich realisiert werden.

- Der Projektumfang erwies sich als sehr groß, insbesondere unter Berücksichtigung bewährter Sicherheitsprinzipien wie z. B. der Einsatz von Secure Zones.

- Für eine funktionierende Integration wären zahlreiche zusätzliche Services erforderlich gewesen (z. B. ein dedizierter Service-Client zur Verarbeitung von OEM-Signaturen).

- Bei der USB-Verbindung traten vereinzelt technische Probleme auf.

=== Annahmen & Einschränkungen <bms_annahmen_und_einschraenkungen>

- Aktuell ist ausschließlich eine Netzwerkverbindung über Ethernet vorgesehen, um die Entwicklung zu vereinfachen.

- Die Batteriedaten auf dem Board werden derzeit zufällig generiert.

- Der Mikrocontroller erhält die DIDs über Ethernet aus der Blockchain (bereitgestellt als Podman-Container), verschlüsselt die zufälligen Batteriedaten mithilfe des Schlüssels und sendet diese ebenfalls über Ethernet in die Cloud.

- Aufgrund des begrenzten Zeitrahmens konnten nicht alle Komponenten vollständig umgesetzt werden, etwa der vollständige Workflow zwischen Service und BMS.

=== Mock-BMS <mockbms>

==== Mock-@BMS Teilaufgaben <mockbms_teilaufgaben>
Das Mock-@BMS dient als simuliertes Battery Management System (BMS), welches innerhalb eines Gesamtsystems für die Generierung, Signatur und verschlüsselte Bereitstellung der Batteriedaten verantwortlich ist. Diese simulierte Alternative entstand aus der Notwendigkeit einer hardwareunabhängigen Lösung. Vorteile sind die vereinfachte Entwicklung, da hier auf hardwarenahe Programmierung verzichtet werden kann, und das flexiblere Testen & Ausführen, da keine weitere Hardware benötigt wird. Die Kernaufgaben vom @BMS und dem Mock-@BMS unterscheiden sich jedoch nicht, sodass letztlich beide Systeme aus Sicht der anderen Systeme jeweils als unterschiedliche @BMS Systeme erkannt werden.
Die Programmierung des Mock-@BMS wurde mittels Python und entsprechenden Bibliotheken umgesetzt.

Das Mock-@BMS bildet einen vollständigen technischen Ablauf ab: von der Identitätserstellung über die Interaktion mit einem externen OEM-Signaturdienst bis hin zur zyklischen Übertragung verschlüsselter Zustandsdaten an autorisierte Cloud-Dienste.

===== Initialisierung & Identitätserzeugung <mockbms_identitaet>
Beim Start erzeugt das Mock-@BMS ein ECC-Schlüsselpaar (mittels NIST-P-256) und speichert dieses lokal. Der öffentliche Schlüssel wird in einem multibase-codierten String umgewandelt und in ein W3C-konformes DID-Dokument eingebettet. Dieses Dokument wird nicht lokal signiert, sondern an einen externen OEM-Signaturservice übergeben, der eine JWS-Signatur erstellt. Nach Erhalt der Signatur registriert das Mock-@BMS die DID über die IAM-Blockchain mittels eines API-Endpunkts.

===== CloudInstance Credentials & Zugriffsauthorisierung <mockbms_vc>
Im Anschluss erzeugt das Mock-@BMS für jede konfigurierte Cloud-DID ein CloudInstance-Verifiable Credential. Diese werden durch den OEM-Signaturdienst signiert – ebenfalls via API. Die signierten VCs werden dann über die Blockchain-API registriert. Die Credentials dienen der Zugriffsauthorisierung auf die jeweiligen Cloud-Services. Sie bestätigen, dass durch den OEM das @BMS zur Kommunikation mit einer genannten Cloud berechtigt ist.

#customFigure(
  image("../../assets/batterydata.png", width: 50%),
  caption: "Beispielausschnitt der generierten BatterieDaten",
) <mockbmsBatteryData>

===== Erzeugung, Verschlüsselung und Signatur der Batterie-Daten <mockbms_datengenerierung>
Das Mock-@BMS nutzt zur Generierung von Batteriepassdaten ein strukturiertes Datenmodell (siehe @mockbmsBatteryData). Diese umfassen Zustandswerte (z. B. Restkapazität, Ladezyklen), technische Eigenschaften (z.B. maximale Spannung) sowie Umweltkennzahlen (CO₂ Fußabdruck). Der initiale Datensatz wird serialisiert und für jede Cloud mit deren öffentlichem Schlüssel verschlüsselt. Für den initialen Batteriepass erfolgt die Verschlüsselung mit dem OEM-Key. Für darauffolgende Updates wird jeweils der Public Key der Cloud verwendet. Die resultierende Payload enthält zusätzlich eine Signatur, welche mit dem privaten @BMS\-Schlüssel erzeugt wird. (Datenstruktur siehe @MessageLayout)

===== Kommunikation mit externen Systemen <mockbms_kommunikation>
Die Interaktion mit anderen Systemen erfolgt über klar definierte REST-Endpunkte. Für die Erstellung eines BatteryPass-Dokuments wird geprüft, ob bereits ein Eintrag in der jeweiligen Cloud existiert. Falls nicht, erfolgt die Erstellung über den SignaturService des OEMs. Wenn bereits ein BatteryPass vorliegt, werden neue Daten direkt an den entsprechenden Cloud-Endpunkt gesendet. Die jeweiligen Service-Endpunkte und Schlüssel werden zuvor über die IAM-Blockchain ausgelesen.

===== Automatisierte Datenaktualisierung <mockbms_update>
Das Mock-@BMS wechselt nach der Initialisierung in einen kontinuierlichen Update-Modus. In einem einstellbaren Intervall werden neue Zustandsdaten erzeugt, verschlüsselt und verschickt. Dabei bleibt der Ablauf identisch zur initialen Übertragung, jedoch erfolgt die Kommunikation ausschließlich mit dem Cloud-Service – nicht mehr über den OEM. Die Payload wird für jede Cloud-Instanz erneut individuell verschlüsselt und signiert.

==== Mock-@BMS Ergebnisse <mockbms_ergebnisse>
Das Mock-@BMS implementiert einen vollständigen, realitätsnahen Datenfluss eines Battery Management Systems. Es erzeugt, verschlüsselt und überträgt strukturierte Daten und nutzt dabei eine vollständig dezentrale Identitätsinfrastruktur. Die Interaktion mit OEM-Signaturdiensten, der IAM-Blockchain sowie Cloud-Instanzen wurde erfolgreich integriert. Das System ermöglicht umfassende Integrationstests auch ohne echte Hardware und ist flexibel anpassbar durch Umgebungsvariablen.

==== Mock-@BMS Probleme & Lösungen <mockbms_probleme_und_loesungen>
Ein zentrales Thema war gegen Ende des Projekts der OEM-Service, welcher in der vorherigen Planung des Gesamtsystems (zu dem Zeitpunkt: bestehend aus Cloud, @BMS und Blockchain) noch gar nicht enthalten war. Es stellte sich erst recht spät heraus, dass zusätzlich eine Vertrauensinstanz exisitieren muss, welche die DIDs und VCs vom @BMS verifiziert. Denn das @BMS hat nicht die Berechtigung sich als vertrauenswürdige Entität auszugeben.

=== Mock-@BMS Annahmen & Limitierungen <mockbms_annahmen_und_limitierungen>
Alle Konfigurationen (z. B. Intervallzeit, Cloud-DIDs, Endpunkte) erfolgen ausschließlich über Umgebungsvariablen. Eine dynamische Neuregistrierung zur Laufzeit ist nicht vorgesehen.
Der private Schlüssel des Mock-@BMS wird nicht verschlüsselt abgespeichert.
Es wird angenommen, dass alle genutzten Public Keys und DIDs valide sind und korrekt in der IAM-Blockchain registriert wurden. Prüfungen der Gültigkeit von DIDs oder VCs vor jedem Upload erfolgen derzeit nicht.
Dazu kommt, dass hier ein gutes und vollständiges Error-Handling fehlt. Bei einem Fehler wird das System stattdessen terminiert.