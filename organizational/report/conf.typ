#import "@preview/glossy:0.4.0": *
#import "@preview/linguify:0.4.0": *

#show: init-glossary.with(yaml("./glossary.yaml"))
#let longline() = line(length: 100%, stroke: 1pt)

#let customFigure(..args) = figure(..args, supplement: "Abb.")

#let custom-gls-theme = (
  section: (title, body) => {
    if (body != none) {
      pagebreak()
      [
        *#title* \
        Das Glossar enthält eine List aller Abkürzungen und ihrer Bedeutungen.
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
        table.header([*Abkürzung*], [*Bedeutung*]),
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

  pagebreak()
  set page(numbering: "1")
  counter(page).update(1)
  set align(left)
  set par(justify: true)
  
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
}
