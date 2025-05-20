// Import customFigures and longline
#import "../conf.typ": customFigure, longline

= Einleitung
Nachdem die custom Funktionen importiert wurden (`#import "../conf.typ": customFigure, longline`), können sie in der Konfiguration verwendet werden.
Ein Bild kann mit `#customFigure()` eingebunden werden. Die Funktion wird in der Konfiguration definiert.
#customFigure(
  image("../THILogo.png", width: 50%),
  caption: "Logo der Technischen Hochschule Ingolstadt",
) <THILogo>

Beispiel für einen Verweis: @THILogo

Beispiel für einen Glossar-Eintrag: @test

Eine Longline kann erstellt werden mit `#longline()`. Diese wird in der Konfiguration definiert.
#longline()
