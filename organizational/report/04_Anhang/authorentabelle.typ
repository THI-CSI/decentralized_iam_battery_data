== Authorentabelle <authorentabelle>

#show ref.where(form: "normal"): it => {
  [#it (#it.element.body) #linebreak()]
}

#align(center, table(
  align: left, 
  columns: (
    auto, auto
  ),
  table.header(
    [*Autor*], [*Kapitel*]
  ),
  [Paulina Mair], [ @projektbeschreibung],
  [Fatma Aladağ], [ @genutzte_tools_und_plattformen
                    @ueberblick_und_zusammenhang_der_arbeitspakete 
                    @requirements_engineering],
  [Berkan Erkasap], [ @systemarchitektur],
  [Timo Weese], [ @arbeitspaket_project_management],
  [Pascal Esser], [ @arbeitspaket_infrastructure],
  [Felix Wallner], [ @arbeitspaket_iam_blockchain],
  [Jonas Ampferl], [ @arbeitspaket_iam_blockchain],
  [Till Hoffmann], [ @arbeitspaket_iam_blockchain],
  [Florian Mülken], [],
  [Matthias Maier], [],
  [pal1222 (at) thi (punkt) de], [],
  [Deniz Volkan], [],
  [Valentin Härter], [],
  [Ensar Özen], []
))
#align(center, [Wenn lediglich das Oberkapitel angegeben ist, so hat der Author an jedem Unterkapitel mitgewirkt.#linebreak()Wenn statt einem Klarnamen ein Nutzername angegeben ist, so hat der Author der Veröffentlichung nicht zugestimmt.])