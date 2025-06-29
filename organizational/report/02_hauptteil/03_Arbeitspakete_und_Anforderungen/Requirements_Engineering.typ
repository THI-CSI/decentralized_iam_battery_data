== Requirements Engineering
=== Übergeordnetes Ziel & Aufgaben
Das zentrale Ziel des Arbeitspakets „Requirements Engineering“ bestand darin, die funktionalen und nicht-funktionalen Anforderungen für ein System zur dezentralen Identitäts- und Zugriffsverwaltung im Batteriedatenkontext zu erheben, zu strukturieren und für die technische Umsetzung bereitzustellen. Im Fokus standen dabei Anforderungen an den digitalen Batteriepass, an dezentrale Identifikatoren (DIDs) und auch an verifizierbare Nachweise (VCs). 
Als Grundlage dienten die regulatorischen Vorgaben der EU-Batterieverordnung, die DIN DKE SPEC 99100 sowie die technischen Standards des W3C-Datenmodells für dezentrale Identifikatoren (DIDs) und verifizierbare Nachweise (VCs). Ziel war es, auf dieser Basis eine verständliche, nachvollziehbare und praxisorientierte Anforderungssystematik zu entwickeln.
=== Teilaufgaben
Zu Beginn wurden die relevanten Standards und Projektvorgaben analysiert und anschließend in einzelne Anforderungen überführt. Die Anforderungen wurden priorisiert, dokumentiert und in GitHub-Issues überführt. So konnte eine transparente Verknüpfung zwischen Anforderung und späterer Umsetzung sichergestellt werden. Die Arbeit erfolgte arbeitsteilig: Ein Teil des Teams fokussierte sich auf DIDs und VCs, der andere auf den Batteriepass. Dabei fielen zusätzlich unterschiedliche Aufgaben an:
== DIDs & Verifiable Credentials (Fatma)
Im Bereich DIDs & Verifiable Credentials lag der Fokus auf der detaillierten Analyse der W3C und VC Data Models.
Im weiteren Projektverlauf wurde eine Einführung zu dezentralen Identitäten (DIDs) und verifizierbaren Nachweisen (VCs) gehalten, um das konzeptionelle Verständnis im Gesamtteam zu stärken. Aufbauend darauf erfolgte eine begleitende Unterstützung der Umsetzung durch die regelmäßige Überprüfung technischer Artefakte, darunter beispielsweise DID-Dokumente und exemplarische Verifiable Credentials.
== Batteriepass (Paulina)
Im Bereich des Batteriepasses lag der Fokus auf der detaillierten Analyse der EU-Batterieverordnung sowie der DIN DKE SPEC 99100. 
Darüber hinaus wurde ein neues Template zur strukturierten Erstellung neuer Anforderungen entwickelt, das die Nomenklatur sowie das Format einheitlich definiert und projektweit verwendet wurde.
Ein weiterer wesentlicher Bestandteil war die Erstellung eines Rechte- und Rollenkonzepts auf Basis der EU-Verordnung und der DIN DKE SPEC 99100. Es beschreibt, welche Akteure auf welche Datenarten im Batteriepass zugreifen dürfen.
Zur Unterstützung der Entwicklerteams wurde eine umfassende Attributübersicht erarbeitet, in der alle im Batteriepass vorgesehenen Datenfelder dokumentiert wurden, inklusive ihrer Datentypen, ihrer Klassifikation (statisch/dynamisch) und ihrer Sichtbarkeit (öffentlich oder eingeschränkt). Diese Übersicht diente als zentrale Orientierung für die Arbeit mit Beispieldaten.
Auch organisatorische Inhalte wurden dokumentiert: In der frühen Projektphase wurden Sitzungsprotokolle erstellt, strukturiert und auf GitHub veröffentlicht. 
=== Ergebnisse
Das Resultat war eine gepflegte Anforderungsliste mit klarer Priorisierung. Die Anforderungen wurden in GitHub strukturiert abgelegt und laufend aktualisiert. Besonderer Wert wurde auf die Nachvollziehbarkeit der Quellen gelegt, um Entwicklern bei Bedarf die Möglichkeit zur genaueren Recherche zu ermöglichen. Zudem wurde innerhalb des Requirements-Teams eine Status-Tabelle gepflegt, in der der Fortschritt der einzelnen Anforderungen, die zuständigen Gruppen oder Personen sowie etwaige Abhängigkeiten oder offene Fragen dokumentiert wurden. Diese diente bei Bedarf den Teams als Orientierung. Auch bei der Erstellung der inhaltlichen Struktur der Abschlusspräsentation und des Projektberichts war das Team beteiligt, sowie bei Abschnitten, die nicht konkret einem Arbeitspaket zuzuordnen waren. Außerdem fielen bei den verschiedenen Teilgebieten noch zusätzlich folgende Ergebnisse an:
== DIDs & Verifiable Credentials (Fatma)
•	Ableitung und Integration neuer Anforderungen aus den W3C und VC Data Models
•	Einführung zu DIDs und VCs für das gesamte Projektteam
•	Erstellung und Review technischer Artefakte (z. B. Beispiel-DID-Dokumente, VC-Datenstrukturen)
•	Entwicklung einer eigenen DID-Methodenspezifikation zur praktischen Umsetzung
== Batteriepass (Paulina)
•	Ableitung und Integration neuer Anforderungen aus der EU-Verordnung und DIN DKE SPEC 99100
•	Einheitliches Template zur strukturierten Dokumentation von Anforderungen eingeführt
•	Ausarbeitung eines Rechte- und Rollenkonzepts zur Regelung des Datenzugriffs nach EU-Verordnung und DIN DKE SPEC 99100
•	Übersichtstabelle mit allen Batteriepass-Attributen, Datentypen, Zugriffsrechten und ob die Daten Statisch/Dynamisch sind
•	Erstellung und Veröffentlichung von Protokollen zu ersten organisatorischen Sitzungen
=== Probleme & Lösungen
== DIDs & Verifiable Credentials (Fatma)
Ein zentrales Problem war die hohe Komplexität einiger Standards, insbesondere des W3C VC Data Models. Eine vollständige Umsetzung hätte den Rahmen des Projekts gesprengt. Daher wurden nur die relevanten Kernfunktionen übernommen, um einen sinnvollen Kompromiss zwischen Realismus und Machbarkeit zu finden. Darüber hinaus veränderten sich einige Anforderungen im Laufe der Umsetzung. Durch die laufende Abstimmung mit den Entwicklerteams und die kontinuierliche Pflege der GitHub-Issues konnte jedoch flexibel darauf reagiert werden.
== Batteriepass (Paulina)
Das detaillierte Durcharbeiten der relevanten Standards erwies sich als sehr arbeits- und zeitintensiv, sodass neue Anforderungen nur schrittweise und mit gewisser Verzögerung in den Entwicklungsprozess einfließen konnten. Eine z.B. architekturrelevante Anforderung wurde erst zu einem späteren Zeitpunkt erkennbar, konnte jedoch dank klarer Abstimmung und konstruktiver Kommunikation im Team schnell und zielführend berücksichtigt werden. Gute Kommunikation war demnach bei vielen Schwierigkeiten die entscheidende Lösung.
=== Annahmen & Limitierungen
== DIDs & Verifiable Credentials (Fatma)
Einige internationale Standards mussten bewusst reduziert umgesetzt werden, da ihre vollständige Anwendung zu aufwendig gewesen wäre. Stattdessen wurde der Fokus auf die projektrelevanten und technisch umsetzbaren Bestandteile gelegt. Gleichzeitig wurde eine eigene DID-Methodenspezifikation entwickelt. Diese ermöglichte es, dezentrale Identitäten in einem kontrollierten Rahmen praktisch umzusetzen und in die eigens entwickelte Blockchain-Komponente zu integrieren.
== Batteriepass (Paulina)
Im Hinblick auf den Batteriepass bestand die Einschränkung, dass bestimmte konkrete Anforderungen und Regelungen zum Zeitpunkt der Bearbeitung noch nicht final definiert waren, sondern auf einen späteren Zeitpunkt verschoben wurden (2027). Demnach mussten einige technische Entscheidungen den Entwicklern überlassen werden, da hier noch keine detaillierteren Angaben enthalten waren.
