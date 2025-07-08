#import "../../conf.typ": customFigure

== Requirements Engineering <requirements_engineering>
=== Übergeordnetes Ziel & Aufgaben <requirements_engineering_uebergeordnetes_ziel_und_aufgaben>
Das zentrale Ziel des Arbeitspakets „Requirements Engineering“ bestand darin, die funktionalen und nicht-funktionalen Anforderungen für ein System zur dezentralen Identitäts- und Zugriffsverwaltung im Batteriedatenkontext zu erheben, zu strukturieren und für die technische Umsetzung bereitzustellen. Im Fokus standen dabei Anforderungen an den digitalen Batteriepass, an dezentrale Identifikatoren (@DID:pl) und auch an @VC:both:pl. 
Als Grundlage dienten die regulatorischen Vorgaben der EU-Batterieverordnung, die DIN DKE SPEC 99100 sowie die technischen Standards des W3C-Datenmodells für dezentrale Identifikatoren (@DID:pl) und @VC:both:pl. Ziel war es, auf dieser Basis eine verständliche, nachvollziehbare und praxisorientierte Anforderungssystematik zu entwickeln.

=== Teilaufgaben <requirements_engineering_teilaufgaben>
Zu Beginn des Arbeitspakets wurden die zentralen Projektvorgaben und Rahmenbedingungen analysiert. Auf dieser Grundlage konnten erste Anforderungen formuliert und in GitHub in Form von GitHub-Issues als einzelne Requirements integriert werden, um sie dem Entwicklungsteam frühzeitig bereitzustellen.
Im weiteren Verlauf wurden die Anforderungen mit GitHub-Markern in die Kategorien Must, Should und Can eingeteilt. Diese Priorisierung diente dazu, den Fokus gezielt auf die wichtigsten Ziele zu lenken und eine strukturierte Umsetzung zu ermöglichen. 
Diese Vorgehensweise ermöglichte eine transparente Nachverfolgbarkeit der Anforderungen bis hin zur späteren technischen Umsetzung. Die Identifikation neuer, noch nicht konkret definierter Anforderungen erfolgte thematisch aufgeteilt: Eine Person bearbeitete den Bereich der dezentralen Identitäten (@DID:pl) und @VC:both:pl, die andere den Batteriepass.
Im Rahmen dieser Aufteilung entstanden zusätzliche, themenspezifische Aufgaben, die jeweils eigenverantwortlich übernommen wurden:
==== @DID:pl & @VC:long:pl
Im Bereich @DID:pl & @VP:long:pl lag der Fokus auf der detaillierten Analyse der W3C und @VC Data Models.
Im weiteren Projektverlauf wurde eine Einführung zu dezentralen Identitäten (@DID:pl) und verifizierbaren Nachweisen (@VC:pl) gehalten, um das konzeptionelle Verständnis im Gesamtteam zu stärken. Aufbauend darauf erfolgte eine begleitende Unterstützung der Umsetzung durch die regelmäßige Überprüfung technischer Artefakte, darunter beispielsweise @DID\-Dokumente und exemplarische @VP:long:pl.

==== Batteriepass
Batteriepass:
Im Bereich des Batteriepasses lag der Fokus auf der detaillierten Analyse der EU-Batterieverordnung sowie der DIN DKE SPEC 99100. Aus diesen sollten dem Rahmen des Projekts entsprechend Anforderungen, die den Batteriepass betreffen, herausgearbeitet werden.
Eine weitere Teilaufgabe bestand darin, auf Basis der analysierten Quellen ein Rollen- und Rechtesystem abzuleiten, das als Grundlage für die spätere Umsetzung der Zugriffsregelungen gemäß EU-Verordnung dienen sollte.
Ein weiterer Aspekt bestand in der Konzeption einer Attributübersicht zur Unterstützung der Entwicklerteams. Darin sollten alle im Batteriepass vorgesehenen Datenfelder systematisch dokumentiert werden – einschließlich Datentyp, Klassifikation (statisch oder dynamisch) sowie Sichtbarkeit (öffentlich oder eingeschränkt). Die Übersicht war als zentrale Orientierungshilfe für den Umgang mit Beispieldaten vorgesehen.

Sonstiges:
Ein weiterer Bestandteil war die Entwicklung eines Templates zur strukturierten und einheitlichen Erstellung von Anforderungen. 
Darüber hinaus zählte auch die Dokumentation organisatorischer Inhalte zu den Aufgaben.
Zudem stand Richtung Ende der Projektphase auch der Abschlussbericht des Batterieprojekts an, bei dem auch einige allgemeine Inhalte erstellt wurden (siehe Autorentabelle).

=== Ergebnisse <requirements_engineering_ergebnisse>
Resultat war eine gepflegte Anforderungsliste mit klarer Priorisierung. Die Anforderungen wurden in GitHub strukturiert abgelegt und laufend aktualisiert. Besonderer Wert wurde auf die Nachvollziehbarkeit der Quellen gelegt, um Entwicklern bei Bedarf die Möglichkeit zur genaueren Recherche zu ermöglichen. Zudem wurde innerhalb des Requirements-Teams eine Status-Tabelle gepflegt, in der der Fortschritt der einzelnen Anforderungen, die zuständigen Gruppen oder Personen sowie etwaige Abhängigkeiten oder offene Fragen dokumentiert wurden. Diese diente bei Bedarf den Teams als Orientierung. Auch bei der Erstellung der inhaltlichen Struktur der Abschlusspräsentation und des Projektberichts war das Team beteiligt, sowie bei Abschnitten, die nicht konkret einem Arbeitspaket zuzuordnen waren. Außerdem fielen bei den verschiedenen Teilgebieten noch zusätzlich weitere Ergebnisse an:
==== @DID:pl & @VC:long:pl
-	Ableitung und Integration neuer Anforderungen aus den W3C-Spezifikationen zu @DID:both und @VC:both:pl, insbesondere im Hinblick auf PRJ_CSI_REQ_008, PRJ_CSI_REQ_011 und PRJ_CSI_REQ_014AnforderungsbeschreibungDID_Anforderungen_Proje….
-	Einführung in @DID:pl und @VC:pl für das gesamte Projektteam zur Etablierung eines einheitlichen technischen Verständnisses im Kontext von @SSI:pl.
-	Erstellung und Review technischer Artefakte, u. a. Beispiel-@DID\-Dokumente und @VC\-Datenstrukturen gemäß W3C-Modell.
-	Entwicklung einer eigenen  @DID\-Methodenspezifikation, welche im Projekt-Repository unter
main/organizational/requirements/did-method-spec.md dokumentiert ist.
Die Spezifikation definiert den Methodennamen, die ID-Generierung, das Format des @DID\-Dokuments (inkl. Schlüssel, Authentifizierung, Service-Endpunkte) sowie grundlegende Regeln für Erzeugung, Auflösung und Aktualisierung.

==== Batteriepass
-	Ableitung und Integration neuer Anforderungen aus der EU-Verordnung und DIN DKE SPEC 99100
-	Einführung eines einheitlichen Templates zur strukturierten Dokumentation von Anforderungen
Die Nomenklatur sowie das Format der Requirements wurden mit dessen Anleitung einheitlich definiert und projektweit verwendet. Die Anforderungen wurden mit nachfolgendem Schema angelegt, um die Position in der Hierarchieebene kenntlich zu machen:	
Form:   PRJ_CSI_REQ_0XX.XX.XX – Short Description
Beispiel:   PRJ_CSI_REQ_006.01.01 - Create asymmetrical key pair
-	Ausarbeitung eines Rechte- und Rollenkonzepts zur Regelung des Datenzugriffs nach EU-Verordnung und DIN DKE SPEC 99100, insbesondere im Hinblick auf PRJ_CSI_REQ_015 und PRJ_CSI_REQ_016
Es beschreibt, welche Akteure auf welche Datenarten im Batteriepass zugreifen dürfen. 
Folgende Rollen wurden herausgearbeitet (für die Rechte siehe Projekt-Repository: main/organizational/requirements/rights_and_roles.md):

#table(
  columns: (auto, auto),
  align: left,
  table.header(
   [ *Rolle/Zugriffsebene*], [*Beispielhafte Zugriffsberechtigte / Inhalte*],
  ),
  [Publicly Accessible Information],[Allgemeinheit, Hersteller, Entwickler, Händler],
  [Legitimate Interest and Commission],[Fahrzeughersteller (OEMs), Werkstätten, Aufsichtsbehörden],
  [Notified Bodies, Market Surveillance and Commission], [Behörden (Ergebnisse von Prüfberichten zur Einhaltung der Verordnung)],
  [Legitimate Interest],[OEMs, Fahrzeughalter:innen, Recycler – batteriebezogene Informationen]
)

-	Übersichtstabelle mit allen Batteriepass-Attributen, Datentypen, Zugriffsrechten und der Klassifikation, insbesondere im Hinblick auf PRJ_CSI_REQ_018
Zur Unterstützung der Entwicklerteams wurde eine umfassende Attributübersicht erarbeitet, in der alle im Batteriepass vorgesehenen Datenfelder dokumentiert wurden, inklusive ihrer Datentypen, ihrer Klassifikation (statisch/dynamisch) und ihrer Sichtbarkeit (öffentlich oder eingeschränkt). 
Diese Übersicht diente als zentrale Orientierung für die Arbeit mit Beispieldaten. Im Folgenden ein Ausschnitt zur Veranschaulichung (Vollständig siehe Projekt-Repository: main/organizational/requirements/datatypes_attributes.md):

#figure(
  caption: "Datenattribute gemäß DIN DKE SPEC 99100",
  table(
    columns: (auto, auto, auto, auto, auto),
    align: left,
    table.header(
      [*Clause*], [*Data attribute*], [*Data access*], [*Data type [Unit]*], [*Status*],
    ),
    [6.5.2], [Battery chemistry], [Public], [String], [static],
    [6.5.3], [Critical raw materials], [Public], [String], [static],
    [6.5.4], [Materials used in cathode, anode and electrolyte], [People with a legitimate interest and Commission], [String], [static],
    [6.5.5], [Hazardous substances], [Public], [String], [static],
    [6.5.6], [Impact of substances on environment, human health, safety and people], [Public], [String], [static],
  )
)


-	Erstellung und Veröffentlichung von Protokollen zu ersten organisatorischen Sitzungen
Darüber hinaus zählte auch die Dokumentation organisatorischer Inhalte zu den Aufgaben. In der frühen Projektphase wurden hierfür Sitzungsprotokolle erstellt, systematisch aufbereitet und auf GitHub veröffentlicht, um die interne Abstimmung nachvollziehbar festzuhalten.


=== Probleme & Lösungen <requirements_engineering_probleme_und_loesungen>
==== @DID:pl & @VC:long:pl
Ein zentrales Problem stellte die hohe Komplexität einiger Standards dar, insbesondere des W3C @VC Data Models. Eine vollständige Umsetzung hätte den zeitlichen und organisatorischen Rahmen des Projekts gesprengt. Daher wurden gezielt nur die für den Projektkontext relevanten Kernfunktionen übernommen, um einen sinnvollen Kompromiss zwischen Realitätsnähe und Umsetzbarkeit zu finden.
Zudem änderten sich im Verlauf der Umsetzung einzelne Anforderungen. Durch die kontinuierliche Abstimmung mit den Entwicklerteams sowie die aktive Pflege der GitHub-Issues konnte flexibel und koordiniert darauf reagiert werden.
==== Batteriepass
Das detaillierte Durcharbeiten der relevanten Standards erwies sich als sehr arbeits- und zeitintensiv, sodass neue Anforderungen nur schrittweise und mit gewisser Verzögerung in den Entwicklungsprozess einfließen konnten. Eine z.B. architekturrelevante Anforderung wurde zum Beispiel erst zu einem späteren Zeitpunkt erkennbar, konnte jedoch dank klarer Abstimmung und konstruktiver Kommunikation im Team schnell und zielführend berücksichtigt werden. Gute Kommunikation war demnach bei den meisten Schwierigkeiten die beste und entscheidende Lösung.
Eine andere Schwierigkeit bestand darin, einzuordnen, welche Requirements mit integriert werden sollen und welche eventuell für unser Projekt zu vernachlässigen sind. Die Lösung war auch hier Kommunikation in der Sitzung, wenn sich nach persönlichem Ermessen noch zusätzlich versichert werden wollte.

=== Annahmen & Limitierungen <requirements_engineering_annahmen_und_limitierungen>
==== @DID:pl & @VC:long:pl
Einige internationale Standards mussten bewusst reduziert umgesetzt werden, da ihre vollständige Anwendung zu aufwendig gewesen wäre. Stattdessen wurde der Fokus auf die projektrelevanten und technisch umsetzbaren Bestandteile gelegt.
Gleichzeitig wurde eine eigene @DID\-Methodenspezifikation entwickelt. Diese ermöglichte es, dezentrale Identitäten in einem kontrollierten Rahmen praktisch umzusetzen und in die eigens entwickelte Blockchain-Komponente zu integrieren.
==== Batteriepass
Im Hinblick auf den Batteriepass bestand die Einschränkung, dass bestimmte konkrete Anforderungen und Regelungen zum Zeitpunkt der Bearbeitung noch nicht final definiert waren, sondern auf einen späteren Zeitpunkt verschoben wurden (2027). Demnach mussten einige technische Entscheidungen den Entwicklern überlassen werden, da hier noch keine detaillierteren Angaben enthalten waren.
Außerdem hätte es einige Anforderungen gegeben, die den Rahmen unseres Projektes gesprengt hätten, sowohl bezogen auf die Zeit und den Aufwand, die es gekostet hätte, jene umzusetzen. Folglich konnten wir manche Themen nicht ganz berücksichtigen.
