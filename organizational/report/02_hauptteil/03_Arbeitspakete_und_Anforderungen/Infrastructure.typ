== Infrastructure <arbeitspaket_infrastructure>

=== Übergeordnetes Ziel & Aufgaben <infrastructure_uebergeordnetes_ziel_und_aufgaben>
Das Infrastruktur-Team hatte im Projekt „Decentralized IAM for Battery Data“ die Aufgabe, die technische und organisatorische Grundlage für eine funktionierende und strukturierte Zusammenarbeit innerhalb der Entwicklerteams zu schaffen. Ziel war es, eine stabile, übersichtliche und kollaborationsfreundliche Umgebung in GitHub bereitzustellen, die sowohl den Entwicklungsprozess unterstützt als auch eine einheitliche Arbeitsweise sicherstellt.

Ein zentrales Anliegen war es, durch klare Strukturen, standardisierte Abläufe und gezielte Automatisierung eine zuverlässige Grundlage für die Arbeit aller Projektbeteiligten zu schaffen. Dabei standen nicht nur technische Konfigurationen im Vordergrund, sondern auch der Aufbau eines funktionierenden Workflows, die Definition von Richtlinien zur Zusammenarbeit sowie Maßnahmen zur Qualitätssicherung.

=== Teilaufgaben <infrastructure_teilaufgaben>
Zu Beginn wurde das GitHub-Repository als zentrale Plattform für die Zusammenarbeit im Projekt eingerichtet. Dazu gehörte das Anlegen verschiedener Projekt-Teams mit differenzierten Rechten, um eine saubere Rollen- und Rechteverteilung zu ermöglichen. Weiterhin wurde das Repository mit passenden Labels ausgestattet und ein Kanban-Board zur Organisation und Verfolgung von Aufgaben erstellt. Das Infrastruktur-Team definierte außerdem ein Branching-Modell, das eine strukturierte und parallele Entwicklung in verschiedenen Feature-Branches ermöglichte.

Ein weiterer wichtiger Aspekt war die Ausarbeitung der Contribution Guidelines. Diese beinhalten verbindliche Regeln zur Nutzung des Kanban-Boards sowie konkrete Arbeitsanweisungen für das Erstellen und Bearbeiten von Issues, Branches, Pull Requests und Commits. Ziel war es, eine klare und nachvollziehbare Vorgehensweise für alle Teammitglieder zu etablieren und dadurch die Qualität und Konsistenz des Codes sowie der Arbeitsprozesse zu verbessern.

Zur weiteren Standardisierung der Zusammenarbeit wurden Templates für Issues und Pull Requests erstellt. Diese Vorlagen helfen dabei, wichtige Informationen strukturiert zu erfassen und unterstützen die Kommunikation im Team, indem sie klare Erwartungen an die Inhalte und den Ablauf von Änderungen formulieren.

Ein wesentlicher technischer Beitrag des Infrastruktur-Teams war zudem die Entwicklung und Integration einer GitHub Action, die sich aus zwei Teilen zusammensetzt und über die Datei `.github/workflows/build-d2-and-typst.yaml` eingebunden ist. Ziel dieser Action war es, bestimmte Aufgaben wie die Erstellung von Diagrammen und die Generierung der Dokumentation zu automatisieren und dadurch den Arbeitsprozess zu vereinfachen und zu standardisieren.

Die Action besteht aus zwei Hauptschritten: Zunächst werden `.d2`-Dateien automatisch gerendert, um die Diagramme für das Projekt in einheitlicher Form zu erzeugen. Anschließend wird aus dem Typst-Quelltext die Projektdokumentation gebaut. Anstatt diese Artefakte manuell zu erzeugen oder als statische Dateien zu pflegen, stellt die GitHub Action sicher, dass stets eine aktuelle und konsistente Version auf Basis des tatsächlichen Repository-Inhalts verfügbar ist.

Zusätzlich wurde vom Infrastruktur-Team ein zentrales Dokumentationstemplate in Typst entwickelt und bereitgestellt. Dieses diente als gemeinsame Grundlage für alle Teams im Projekt und sorgte dafür, dass die Dokumentationen einheitlich aufgebaut und strukturiert waren. Dadurch wurde nicht nur die Lesbarkeit verbessert, sondern auch die spätere Zusammenführung der Inhalte erleichtert.

=== Ergebnisse <infrastructure_ergebnisse>

Wesentliche Ergebnisse waren:

==== Erfolgreiche Einrichtung und Konfiguration des zentralen GitHub-Repositories

Das Infrastruktur-Team richtete das GitHub-Repository so ein, dass es eine klare Struktur für die Zusammenarbeit bot. Dazu gehörten:
- Anlegen von Projekt-Teams mit differenzierten Rechten (#emph("Maintainers") und einzelne #emph("Developer ") Teams)
  - Festlegung von Repository Schreibrechten (Nur #emph("Maintainers") können auf den `main`-Branch pushen)
- Ausstattung des Repositories mit passenden Labels zur einfacheren Organisation von Issues und Pull Requests
- Entwicklung eines @ADP, um die Arbeitsweise zu standardisieren und die Qualität der Issues, Commits und Pull Requests zu verbessern (siehe #emph("Github Contribution Guidelines"))
  - Branching-Modell, das parallele Entwicklungen in verschiedenen Feature-Branches ermöglicht
- Erstellung eines Kanban-Boards zur Organisation und Verfolgung von Aufgaben
- Entwicklung und Integration einer GitHub Action

==== Erfolgreiche Bereitstellung eines einheitlichen Typst-Dokumentationstemplates
Wir haben uns für die Nutzung von Typst als Textsatzprogram entschieden, da wir von der einfachen Nutzbarkeit und den schnellen Kompilierzeiten überzeugt waren. 

Als Ergebnis zeigen wir den vorliegenden Projektabschlussbericht vor.

=== Probleme & Lösungen <infrastructure_probleme_und_loesungen>
In Bezug auf die Teamkoordination verlief die Zusammenarbeit im Infrastruktur-Team insgesamt sehr gut. Da wir bereits in früheren Projekten zusammengearbeitet hatten, bestand von Anfang an eine gute Kommunikationsbasis und ein gemeinsames Verständnis für Arbeitsweisen und Verantwortlichkeiten. Wir standen während des gesamten Projektzeitraums in regelmäßigem Kontakt, wodurch wir sehr individuell und spontan Absprachen treffen konnten. Aufgabenverteilungen oder kurzfristige Änderungen konnten so unkompliziert abgestimmt werden.

Bei der Umsetzung der GitHub Action zur automatisierten Verarbeitung von Dokumentation und Diagrammen trafen wir dafür auf eine Herausforderung, aus der wir auch gelernt haben. Es ging dabei um den Umgang mit den Branch-Protection-Regeln des `main`-Branches.

Ursprünglich war geplant, die GitHub Action so einfach wie möglich zu halten. Dazu wurde zunächst die Branch Protection auf `main` vorübergehend deaktiviert, damit der Action-Bot die generierten Dateien – insbesondere die gerenderten Diagramme und die Typst-Dokumentation – direkt in den Hauptbranch pushen konnte. Diese Entscheidung basierte auf der Annahme, dass das gesamte Projektteam den vereinbarten Workflow einhält und nicht direkt auf `main` pusht.

Kurz nach der Deaktivierung der Branch-Protection zeigte sich jedoch, dass diese Annahme zu optimistisch war, da mehrere Teammitglieder versehentlich direkt auf den `main`-Branch gepusht haben, was Inkosistenzen innerhalb des `main`-Branches herbeiführen könnte. Daraufhin wurde die Branch Protection umgehend wieder aktiviert, um unbeabsichtigte Änderungen am Hauptbranch zuverlässig zu verhindern.

Die Herausforderung bestand nun darin, einen alternativen Weg zu finden, wie die GitHub Action trotzdem automatisiert auf den `main`-Branch schreiben konnte, ohne gegen die Schutzregeln zu verstoßen. Die Lösung bestand darin, zwei unterschiedliche Mechanismen zu kombinieren: Die generierte Projektdokumentation (der Typst-Bericht) wird nun im Rahmen eines Releases hochgeladen, was unabhängig von der Branch Protection erfolgt. Die gerenderten Diagramme hingegen werden weiterhin direkt in den `main`-Branch geschrieben – allerdings durch den Action-Bot, der mit entsprechenden Deploy Keys ausgestattet wurde. Diese Deploy Keys besitzen gezielt eingeräumte Schreibrechte für genau diesen Zweck, sodass die Action trotz aktiver Branch Protection gezielt und kontrolliert Änderungen an definierten Dateien vornehmen kann.

Diese Lösung stellte sicher, dass die Vorteile der Branch Protection erhalten blieben, ohne auf die notwendige Automatisierung und Aktualisierung der generierten Dateien verzichten zu müssen.

=== OEM-Service <infrastructure_oem_service>

@DID:pl müssen vor der Registrierung auf der Blockchain kryptographisch durch den verantwortlichen signiert werden. Die @EU (als primärer-) etabliert jeden @OEM als sekundären Vertrauensanker (Trust Anchor) für die von ihm hergestellten Geräte. Die Signatur des @OEM\s fungiert als digitale Geburtsurkunde, die bezeugt, dass die @DID legitim ist und zu einem spezifischen, im Rahmen des regulären Herstellungsprozesses entstandenen @BMS gehört.

Dies bedeutet für den Batteriepass:

+ *Schutz vor Identitätsdiebstahl und Spoofing*: Unbefugte Dritte können keine gültigen @BMS\-Identitäten erstellen, da ihnen die kryptographische Signatur eines autorisierten @OEM\s fehlt.
+ *Etablierung einer nachvollziehbaren Vertrauenskette*: Es entsteht eine ununterbrochene, kryptographisch gesicherte Verbindung von einer realen, juristischen Entität (dem @OEM) zur digitalen Identität eines physischen Geräts (dem @BMS).
+ *Grundlage für den Batteriepass*: Diese initiale Vertrauensbildung ist die Voraussetzung für alle nachfolgenden Interaktionen und Dateneinträge im Lebenszyklus der Batterie. Nur mit einer authentifizierten Identität können Daten wie Produktionsdatum, chemische Zusammensetzung oder erste Leistungstests verlässlich dem korrekten @BMS zugeordnet werden.

Um diese Signatur zu generieren, ohne den privaten Schlüssel des @OEM\s offenzulegen, wird ein spezieller Dienst implementiert, welcher drei Funktionen erfüllt: 

+ *Signatur einer  @DID*: 
  Der @OEM signiert die @DID des @BMS, um dessen Authentizität zu bestätigen.
+ *Signatur einer  @VC*: 
  Der @OEM signiert eine @VC, die den Zusammenhang zwischen dem @BMS und mehreren Cloud-Instanzen herstellt (CloudInstance @VC:pl). 
+ *Registrierung des @BMS bei der Blockchain*: Der @OEM registriert das @BMS mit den ersten Batteriepass-Daten bei der Blockchain.
