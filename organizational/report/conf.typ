#import "@preview/glossy:0.8.0": *
#import "@preview/linguify:0.4.2": *

#show: init-glossary.with(yaml("./glossary.yaml"))
#let longline() = line(length: 100%, stroke: 1pt)

#let customFigure(..args) = figure(..args, supplement: "Abb.")

#let custom-gls-theme = (
  section: (title, body) => {
    if (body != none) {
      pagebreak()
      [
        *#title* \
        Das Glossar enthält eine Liste aller Abkürzungen und ihrer Beschreibungen.
        \
        \
        #body
      ]
    }
  },
  group: (name, index, total, body) => {
    block(
      width: 100%,
      table(
        columns: (0.5fr, 1fr), stroke: 0.5pt,
        table.header([*Abkürzung*], [*Beschreibung*]),
        ..body
      ),
    )
  },
  entry: (entry, index, total) => {
    if entry.long == none {
      ([#entry.short], [#entry.description])
    } else {
      ([#entry.long (#entry.short)], [#entry.description])
    }
  },
)

#let conf(
  type: [Abschlussbericht],
  title: [],
  major: [],
  sem_type: none,
  sem_year: none,
  university: (),
  doc,
) = {
  set text(font: "Liberation Sans", lang: "de", size: 11pt)
  set align(center)
  show "TODO": text(stroke: red + 1pt, [TODO])
  text(24pt, [ #type ])
  v(3cm)
  text(18pt, [ #title ], style: "oblique")
  linebreak()
  box(height: 75pt)
  linebreak()
  image(university.logo_path, width: 230pt)
  v(1cm)
  text(18pt, [ #major\ #sem_type #sem_year ])
  pagebreak()
  show heading.where(level: 1): set text(18pt)
  show heading.where(level: 2): set text(14pt)
  show heading.where(level: 3): set text(12pt)
  show heading.where(level: 4): set text(10pt)
  show heading.where(level: 5): set text(8pt)

  set heading(numbering: "1.")
  show outline.entry.where(level: 1): it => {
    v(12pt, weak: true)
    strong(it)
  }

  outline(indent: auto, depth: 2)

  glossary(
    title: "Glossar",
    theme: custom-gls-theme,
  )

  set page(numbering: "1")
  counter(page).update(1)
  set align(left)
  set par(justify: true)


  show ref: it => {
    
    let el = it.element
    if el != none and el.func() == heading {
      let counter = counter(heading).at(el.location())
      let loc = numbering(el.numbering,..counter)
      if el.supplement == [Appendix] {
        link(el.location(), [Anhang #loc])
      } else {
        link(el.location(), [Abschnitt #loc (#el.body)])
      }
    } else {
      it
    }
  }
  doc
  pagebreak()
  [= Abbildungsverzeichnis]
  outline(
    title: [],
    target: figure.where(kind: image),
  )
  let bibliography_file = read("ref.bib")

  if bibliography_file.len() > 0 {
    pagebreak()
    [= Literaturverzeichnis]
    bibliography("ref.bib", title: none, style: "ieee")
  }
  pagebreak()
  include "appendix.typ"
}
