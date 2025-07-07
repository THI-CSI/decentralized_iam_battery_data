== Genutzte Tools & Plattformen <genutzte_tools_und_plattformen>

Zur Umsetzung des Projekts wurden verschiedene Werkzeuge und Plattformen eingesetzt, die sowohl die technische Implementierung als auch die organisatorische Zusammenarbeit ermöglichten und unterstützten.
Die zentrale Plattform für Projektmanagement und Quellcodeverwaltung war GitHub. Hier wurden sämtliche Anforderungen in Form von Issues dokumentiert, strukturierte Pull-Requests erstellt und ein gemeinsames Kanban-Board gepflegt. Für eine einheitliche Vorgehensweise kamen standardisierte Templates für Issues und Pull Requests zum Einsatz.
Für spontane Teamabsprachen, Protokolle und Ideensammlungen wurde HedgeDoc verwendet. Die dortige Startseite verlinkt auf alle relevanten Teildokumente und diente als zentrales internes Wissensmanagementsystem.
Eine Besonderheit war die Entwicklung eines Mock-@BMS:short, das ein reales Battery Management System simuliert. Dieses generiert Sensordaten, verschlüsselt diese und überträgt sie über eine gesicherte Schnittstelle an die Cloud. Die Simulation diente als realitätsnahe Testumgebung für das Gesamtsystem.
Das Cloud-Backend wurde in Form einer REST-API implementiert, die die Entgegennahme und Entschlüsselung von Daten ermöglicht. Die Daten werden anschließend in einer selbst entwickelten Datenbankstruktur gespeichert und über eine Weboberfläche im Rahmen des digitalen Batteriepasses dargestellt.
Für das dezentrale Identitätsmanagement wurde eine eigene Blockchain-Komponente mit REST-Schnittstelle entwickelt. Diese verwaltet @DID:short:pl, Zugriffsrechte und Transaktionen. Ein zusätzlicher Block Explorer dient der Visualisierung und Überprüfung von Transaktionsverläufen und Beziehungsstrukturen.
BatteryPass-Schemas aus dem offiziellen GitHub-Repository wurden verwendet, um einheitliche Datenstrukturen gemäß den regulatorischen Anforderungen zu gewährleisten. Diese stehen unter einer Creative-Commons-Lizenz und wurden als JSON-Schemas eingebunden.
Die Kommunikation zwischen den Komponenten (@BMS, Cloud, Blockchain) erfolgt standardisiert über HTTP, unter Berücksichtigung von Authentifizierungsmechanismen, Fehlerbehandlung und JSON-Datenformaten.
Abschließend kamen containerisierte Lösungen zum Einsatz, um eine saubere Trennung der Umgebungen sowie eine einfache Reproduzierbarkeit des Setups sicherzustellen.

