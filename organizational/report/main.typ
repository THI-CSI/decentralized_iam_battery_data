#import "conf.typ": conf, customFigure, longline
#import "@preview/glossy:0.4.0": *


#show: init-glossary.with(yaml("./glossary.yaml"))

#show: doc => conf(
  type: [Abschlussbericht],
  title: [Decentralized Identity and Access Management für Batteriedaten],
  major: [Cybersicherheit B. Sc.],
  sem_type: [Sommersemester],
  sem_year: [2025],
  university: (
    name: [Technische Hochschule Ingolstadt], 
    logo_path: "THILogo.svg",
  ),
  doc,
)


#include "02_hauptteil/wrapper.typ"

#include "03_schluss/main.typ"
