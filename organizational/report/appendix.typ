
#let appendix(body) = {
  set heading(numbering: "A", supplement: [Appendix])
  counter(heading).update(0)
  [= Anhang]
  body
}
#show: appendix

#include "04_Anhang/authorentabelle.typ"