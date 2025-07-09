#pagebreak()
= Allgemeine Projektbeschreibung <projektbeschreibung>

#include "01_Allgemeine_Projektbeschreibung/Projektkontext.typ"
#include "01_Allgemeine_Projektbeschreibung/Problembeschreibung.typ"
#include "01_Allgemeine_Projektbeschreibung/Projektziel.typ"

#pagebreak()
= Projektorganisation 
#include "02_Projekt_Organisation/Genutzte_Tools_und_Plattformen.typ"
#include "02_Projekt_Organisation/Systemarchitektur.typ"
#include "02_Projekt_Organisation/Ueberblick_und_Zusammenhang_der_Arbeitspakete.typ"

#pagebreak()
= Arbeitspakete & Anforderungen im Detail 
#include "03_Arbeitspakete_und_Anforderungen/Uebersicht_der_arbeitspakete_und_zugeordneter_requirements.typ"
#include "03_Arbeitspakete_und_Anforderungen/Projekt_Management.typ"
#let subsections = (
  "03_Arbeitspakete_und_Anforderungen/Requirements_Engineering.typ",
  "03_Arbeitspakete_und_Anforderungen/Infrastructure.typ",
  "03_Arbeitspakete_und_Anforderungen/IAM-Blockchain.typ",
  "03_Arbeitspakete_und_Anforderungen/BMS.typ",
  "03_Arbeitspakete_und_Anforderungen/Cloud.typ"
)

#for subsection in subsections {
  pagebreak()
  include subsection
}