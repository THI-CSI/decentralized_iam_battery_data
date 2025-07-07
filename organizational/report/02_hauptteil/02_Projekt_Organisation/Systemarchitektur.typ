#import "../../conf.typ": customFigure

== Systemarchitektur <systemarchitektur>

#customFigure(
  image("../../assets/systemarchitektur.png", width: 95%),
  caption: "Diagramm der Systemarchitektur des Projekts",
) <systemarchitektur_diagramm>

Wir schlagen eine Architektur aus drei Zentralen Komponenten vor, die über standardisierte Schnittstellen miteinander kommunizieren:
+ *@BMS* (@arbeitspaket_bms): @BMS:long, das Sensordaten erfasst, diese verschlüsselt und über eine gesicherte Schnittstelle an eine oder mehrere Cloud-Datenbanken überträgt.

+ *Cloud* (@arbeitspaket_cloud): Dient als Backend, das die Daten des @BMS empfängt, entschlüsselt, validiert und speichert. Es stellt die Schnittstelle zum digitalen Batteriepass dar und verwaltet Zugriffsrecht.

+ *Blockchain* (@arbeitspaket_iam_blockchain): Verwaltet die @DID:pl, Zugriffsrechte und Transaktionen. Sie ermöglicht eine transparente und unveränderliche Aufzeichnung aller Vorgänge.

+ *@OEM:short\-Service* (@infrastructure_oem_service): Simuliert die Rolle des @OEM, der den digitalen Batteriepass erstellt und für die @DID:pl des @BMS signiert.

