
#let appendix(body) = {
  set heading(numbering: "AA ", supplement: [Appendix])
  counter(heading).update(0)
  [= Anhang]
  body
}
#show: appendix

#include "04_Anhang/authorentabelle.typ"
#pagebreak()
#include "04_Anhang/bms_creation.typ"