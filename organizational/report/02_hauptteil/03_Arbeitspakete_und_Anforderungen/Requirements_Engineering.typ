== Requirements Engineering
=== Übergeordnetes Ziel & Aufgaben
Das Ziel des Arbeitspakets „Requirements Engineering“ war es, die zentralen funktionalen und nicht-funktionalen Anforderungen für ein System zur dezentralen Identitäts- und Zugriffsverwaltung im Batteriedatenkontext zu erheben, zu strukturieren und für die technische Umsetzung bereitzustellen. Im Fokus standen dabei sowohl Anforderungen für dezentrale Identifikatoren (DIDs) und verifizierbare Nachweise (VCs) als auch für den digitalen Batteriepass.
Die Grundlage bildeten regulatorische Vorgaben (z. B. EU-Batterieverordnung) sowie technische Standards wie das W3C DID- und VC-Datenmodell. Ziel war es, daraus eine verständliche, nachvollziehbare und umsetzungsorientierte Anforderungsbasis zu schaffen.

=== Teilaufgaben
Zu Beginn wurden die relevanten Standards und Projektvorgaben analysiert und anschließend in einzelne Anforderungen überführt. Die Arbeit erfolgte arbeitsteilig: Ein Teil des Teams fokussierte sich auf DIDs und VCs, der andere auf den Batteriepass.
Die Anforderungen wurden priorisiert, dokumentiert und in GitHub-Issues überführt. So konnte eine transparente Verknüpfung zwischen Anforderung und Umsetzung sichergestellt werden. Zusätzlich wurde eine Einführung zu DIDs und VCs für das Gesamtteam gehalten, um das konzeptionelle Verständnis zu fördern. Im weiteren Verlauf unterstützten wir die Umsetzung durch Reviews technischer Artefakte wie DID-Dokumente oder VC-Beispiele.

=== Ergebnisse
Als Ergebnis entstand eine gepflegte Anforderungsliste mit klarer Priorisierung und Rückverfolgbarkeit. Die Anforderungen wurden in GitHub strukturiert abgelegt und laufend aktualisiert.
Besonderer Wert wurde auf Traceability gelegt – also die Nachvollziehbarkeit von der Quelle über den Status bis zur Umsetzung. Die enge Abstimmung mit den Entwicklungsteams sorgte dafür, dass neue Anforderungen schnell berücksichtigt und offene Punkte geklärt wurden.
Auch bei der Erstellung der Abschlusspräsentation und des Projektberichts war das Team inhaltlich beteiligt, insbesondere bei den übergreifenden Abschnitten.

=== Probleme & Lösungen
Ein zentrales Problem war die hohe Komplexität einiger Standards, insbesondere des W3C VC Data Models. Eine vollständige Umsetzung hätte den Rahmen des Projekts gesprengt. Daher wurden nur die relevanten Kernfunktionen übernommen, um einen sinnvollen Kompromiss zwischen Realismus und Machbarkeit zu finden.
Darüber hinaus veränderten sich einige Anforderungen im Laufe der Umsetzung. Durch die laufende Abstimmung mit den Entwicklerteams und die kontinuierliche Pflege der GitHub-Issues konnte jedoch flexibel darauf reagiert werden.

=== Annahmen & Limitierungen
Einige internationale Standards mussten bewusst reduziert umgesetzt werden, da ihre vollständige Anwendung zu aufwendig gewesen wäre. Stattdessen wurde der Fokus auf die projektrelevanten und technisch umsetzbaren Bestandteile gelegt.
Gleichzeitig wurde eine eigene DID-Methodenspezifikation entwickelt. Diese ermöglichte es, dezentrale Identitäten in einem kontrollierten Rahmen praktisch umzusetzen und in die eigens entwickelte Blockchain-Komponente zu integrieren.
