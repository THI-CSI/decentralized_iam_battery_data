// Import customFigures and longline
#import "../../conf.typ": customFigure, longline

#pagebreak()
== BMS <arbeitspaket_bms>
=== Übergeordnetes Ziel & Aufgaben <bms_uebergeordnetes_ziel_und_aufgaben>
Ziel dieses Arbeitspakets war die Entwicklung einer Firmware für ein Batterie-Management-System (BMS).

=== Aufgabenverteilung <bms_aufgabenverteilung>
Während Matthias und Florian die Firmware auf realer Hardware mit einem Renesas-Mikrocontroller entwickelten und testeten, erstellte Patrick ein ergänzendes Mock-BMS in Python, das als Simulationsumgebung für das System diente. 
Die Firmware-Entwicklung erfolgte arbeitsteilig: Matthias und Florian übernahmen jeweils unterschiedliche technische Schwerpunkte. Florian war insbesondere für die interne Architektur der Firmware verantwortlich. Er konzipierte und implementierte ein Verfahren zur Erstellung von Nachrichten. Dieses Verfahren ermöglicht die sichere Übertragung dynamischer Batteriedaten über einen unverschlüsselten, verbindungslosen Kanal – wie er im Projektsetup zwischen dem BMS und den Cloud-Endpunkten verwendet wird – unter Gewährleistung von Vertraulichkeit, Integrität und Authentizität. Darüber hinaus war er maßgeblich an der Gestaltung und Strukturierung des Programmablaufs sowie der Programmlogik beteiligt, beispielsweise im Bereich der Inter-Task-Kommunikation.
Matthias war hauptsächlich für die Netzwerkanbindung des Systems verantwortlich, sodass das BMS nach außen kommunizieren und so unter anderem die zuvor generierten Nachrichten mit den Battriedaten an die Cloud-Endpunkte senden kann.

#pagebreak()
=== Ergebnisse <bms_ergebnisse>

Nach dem Flashen der Firmware wird in der main-Funktion zunächst das RTOS initialisiert. Dazu zählen unter anderem das Einrichten der Tasks, die Konfiguration des Schedulers sowie das Anlegen der benötigten Inter-Task-Kommunikationsobjekte (ITC). Das folgende Sequenzdiagramm veranschaulicht vereinfacht die Programmlogik und den grundlegenden Ablauf der Firmware – beispielsweise unter Verwendung von Mechanismen wie dem Deferred Interrupt Handling.
#customFigure(
  image("../../assets/program_flow.png", width: 100%),
  caption: "Program flow BMS",
) <ProgramFlowBMS>
Mit Ausnahme der Funktionalität zur Signierung von Service-VCs und deren Schreiben auf die Blockchain ist der übrige Ablauf bereits vollständig auf der Hardware implementiert.
#pagebreak()
Wie bereits in Abschnitt 3.5.2 beschrieben, war ich zudem für die Konzeption und Entwicklung eines Verfahrens zur Nachrichtenerstellung verantwortlich. Dieses Verfahren kommt im dargestellten Programmablauf an der mit ① markierten Stelle zum Einsatz: Nachdem im Rahmen einer Simulation einmalig die dynamischen Batteriedaten abgefragt wurden, wird für jedes empfangene DID_doc (Cloud-Endpunkt) eine individuelle Nachricht mit den dynamischen Batteriedaten erzeugt und anschließend versendet.

Der Prozess zur Erstellung einer solchen Nachricht umfasst folgende Schritte:

1. Es wird ein temporäres ECC-Schlüsselpaar auf Basis der Kurve secp256r1 erzeugt. Mithilfe des privaten Schlüssels dieses Paares sowie des öffentlichen Schlüssels des Empfängers (extrahiert aus dem jeweiligen DID_doc) wird per ECDH ein gemeinsames Geheimnis berechnet.

2. Aus dem gemeinsamen Geheimnis wird unter Verwendung eines Salt-Werts und eines Info-Blocks (bestehend aus „cloud_pub_key“ und „bms_signing_pub_key“) mittels HKDF (basierend auf SHA-256) ein symmetrischer Schlüssel abgeleitet.

3. Die zuvor abgefragten Batteriedaten werden mit dem symmetrischen Schlüssel durch das AES-GCM-256-Verfahren verschlüsselt und authentifiziert.

4. Die verschlüsselten Batteriedaten sowie weitere für den jeweiligen Cloud-Endpunkt relevante Informationen werden in ein JSON-Dokument eingebettet (@MessageLayout) und mit dem privaten Schlüssel des BMS digital signiert. Dies ermöglicht dem Empfänger sowohl die Entschlüsselung als auch die Überprüfung von Integrität und Authentizität der Nachricht.

5. Die so erzeugte Nachricht wird zusammen mit dem zugehörigen Service-Endpoint (ebenfalls aus dem DID_doc extrahiert) an den Network Task übergeben.

Die generierten Nachrichten (siehe Struktur @MessageLayout) können anschließend über einen ungesicherten, verbindungslosen Kanal an die Cloud-Endpunkte übertragen werden, ohne dass dabei die Vertraulichkeit, Integrität oder Authentizität der Batteriedaten gefährdet wird.
#customFigure(
  image("../../assets/message_layout.png", width: 100%),
  caption: "Message Layout",
) <MessageLayout>
Der Timestamp wird im aktuellen Projekt-Setup noch nicht berücksichtigt, könnte aber zukünftig als Replay-Schutz eingesetzt werden.

Die kryptografischen Funktionen wurden mit mbedTLS implementiert, das die PSA-Crypto-API unterstützt. Über das FSP-Package und den HAL-Treiber rm_psa_crypto kann die Secure Crypto Engine (SCE) der MCU direkt angesprochen werden. Dadurch lassen sich die meisten kryptografischen Operationen hardwarebeschleunigt und sicher im isolierten Speicher der SCE ausführen.


Die Netzwerkkommunikation des Renesas-Mikrocontrollers erfolgt über eine physische Ethernet-Verbindung zu einem Laptop, welcher die Infrastruktur der Cloud- und Blockchain-Endpunkte simuliert. Nach der Initialisierung des IP-Stacks wird der Mikrocontroller befähigt, Netzwerkkommunikation über das statisch konfigurierte IPv4-Netzwerk durchzuführen. Die Netzwerkkonfiguration umfasst die IP-Adresse 192.168.0.52, ein Gateway unter 192.168.0.3 sowie die Verwendung eines lokalen DNS-Servers (dnsmasq) auf 192.168.0.2, welcher für die Namensauflösung der Cloud-Endpunkte verantwortlich ist. Alle IP-Adressen sind statisch vergeben. 

Jeden Monat beginnt der Mikrocontroller mit dem Sammeln der DIDs der Cloud-Endpunkte aus der Blockchain. Jede Batteriedaten-Nachricht wird vor dem Versand mit den entsprechenden kryptografischen Schlüsseln verschlüsselt. Die Verschlüsselung und der Nachrichtenversand werden über zwei getrennte FreeRTOS-Tasks koordiniert:
- net_task: Verantwortlich für das Netzwerkhandling und die Kommunikation mit der IP-Schicht.
- message_creation_task: Zuständig für die Verschlüsselung und Erstellung der Nachrichten unter Verwendung der jeweils zugeordneten Schlüssel.

Zwischen diesen beiden Tasks erfolgt der Datenaustausch über einen MessageBuffer, welcher verschlüsselte Nachrichten vom message_creation_task entgegennimmt und sie an den net_task weiterleitet. Der Versand an die Endpunkte erfolgt über eine FreeRTOS-Queue, wodurch eine deterministische und task-sichere Weitergabe der verschlüsselten Nachrichten gewährleistet wird.

Zur Simulation der Endpunkte wurde bewusst auf ein Podman-Netzwerk statt Docker zurückgegriffen. Dies erlaubt eine feinere Steuerung der Firewall-Einstellungen, insbesondere in Kombination mit iptables und aktiviertem IPv4-Forwarding. Durch diese Konfiguration ist es möglich, eingehende Pakete vom Mikrocontroller über das Ethernet-Interface in das Podman-Netzwerk weiterzuleiten. Die Firewall-Regeln wurden so definiert, dass:

- der Mikrocontroller ausgehende Verbindungen in das Podman-Netzwerk initiieren darf,
- jedoch nur bestehende Verbindungen aus dem Podman-Netzwerk Antworten an den Mikrocontroller senden dürfen.

Als Betriebssystem für den Mikrocontroller kommt FreeRTOS zum Einsatz, da alternative RTOS-Optionen wie Zephyr für das verwendete Renesas-Modell keine Unterstützung für Ethernet-Kommunikation bieten. Die gesamte Firmware ist dokumentiert mittels Doxygen, um eine nachvollziehbare und wartbare Codebasis zu gewährleisten.

Für die Entwicklung der Firmware kommt eine bewährte und plattformübergreifend einsetzbare Toolchain zum Einsatz. Der Compiler ist arm-none-eabi-gcc, ein etablierter Cross-Compiler für ARM-Architekturen. Dieser wurde gewählt, da er eine breite Unterstützung für verschiedene ARM-basierten Mikrocontroller bietet und die Portabilität zwischen unterschiedlichen Zielsystemen erleichtert.

Das Buildsystem basiert auf klassischen Makefile-Strukturen. Diese wurden manuell konfiguriert, da sie für die Anforderungen des Projekts eine einfache, transparente und gleichzeitig performante Möglichkeit zur Verwaltung des Kompilierungsprozesses darstellen. Komplexere Buildsysteme wie CMake wurden bewusst vermieden, um volle Kontrolle über den Buildprozess zu behalten und zusätzliche Abhängigkeiten zu vermeiden.

Für das Debugging kommt der plattformübergreifende SEGGER J-Link Debug-Probe zum Einsatz, welcher eine zuverlässige JTAG/SWD-Kommunikation mit dem Mikrocontroller ermöglicht. Durch die breite Unterstützung in IDEs wie SEGGER Embedded Studio sowie über GDB ist ein effizienter und stabiler Debug-Workflow gewährleistet.

Das Flashing der Firmware erfolgt über den Renesas Flash Programmer, das offizielle Tool von Renesas. Es bietet eine robuste und zuverlässige Möglichkeit zur Programmierung des Mikrocontrollers über serielle oder JTAG-Schnittstellen und lässt sich gut in bestehende Entwicklungsumgebungen integrieren.

=== Probleme & Lösungen
(z. B. Teamkoordination, Ressourcenplanung)

=== Annahmen & Limitierungen
(z. B. Zeitrahmen, verfügbare Ressourcen)

