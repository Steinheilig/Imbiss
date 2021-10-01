# Imbiss

Dieses Programm ist eine 1:1 Implementation (der Spielmechanik) von <br>
"Imbiss-Bude" von F. Brall 1983 für Apple II, Homecomputer 8/1983, S. 37-41<br>
"Imbiss" von O. Schwald 1984 für Commodore C64, Homecomputer 10/1984, S. 55-58 <br>

Darüber hinaus reproduziert das Programm die Spielmechanik von <br>
"Imbiss" v. 5.4 von T. Bauer für IBM PC, Public Domain<br>

ToDo:<br>
* Prüfen Eingabe 
* Überspringen, wenn keine Eingabe
* Code refaktorisieren

## Spielgeschichte: 
F. Brall    1983,   Apple II,   "Imbiss-Bude"<br>
O. Schwald  1984,   C64,        "Imbiss"<br>
T. Bauer    1984,   VZ200,      "Imbiss"        *nicht veröffentlicht*<br>
T. Bauer    1986,   CPC664,     "Imbiss"        *nicht veröffentlicht*<br>
O. Schwald  1987,   Amiga,      "Imbiss III"<br>
T. Bauer    1991,   PC,         "Imbiss"<br>
A. Kern     1994,   Amiga,      "Tom's Imbiss"<br>
A. Kern     2009,   PC,         "Tom's Imbiss"<br>
A. Kern     2011,   Crossplat*  "Tom's Imbiss"<br>
L. Brämer   2019,   Amiga,      "Tom's Imbiss"<br>
T. Bauer    2021,   Android,    "Imbiss Classic"<br>
Steinheilig 2021,   PC,         "Imbiss"<br>
  
*Crossplatform:  AmigaOS 3 (m68k) AmigaOS 4 (ppc) Android (arm) AROS (x86)
iOS (arm) Linux (x86) Linux (x64)
Linux (arm) Linux (ppc) macOS (x86) macOS (x64) macOS (ppc)
MorphOS (ppc) WarpOS (m68k/ppc) Windows (x86) Windows (x64)

## Exploits
Exploits der Spielmechanik für die Spielversionen von 1983/1984:<br>
1) 10% der Fälle, keine Prüfung von Eispreis => Ein Eis super billig -> EK  (nur abhängig von kleinstem Eispreis (1440))  // Anderen Eissorten Max preis wird bezahllt<br>
2) 10% der Fälle, keine Prüfung von Bratwurst-/Pommespreis=> Eins super billig -> BK  (nur abhängig von kleinstem Preis (1440))  // Andere Max preis wird bezahllt<br>
3) Kein Einfluss des Cola Preises auf Kunden (Cola Kunden sind zufällige Eiskunden) / keine Prüfung von Colapreis => Jeder Cola Preis wird bezahlt in ca. für EK/4 % Der Fälle<br>

## Bugs
"Bratwurst Anomalie" in der Spielversion von 1991:
Wird der Verkaufspreis einer Ware aus einer Warengruppe zu hoch angesetzt (z.B. die Cola oder die Bratwurst), 
werden die anderen Eltemente der Warengruppe nicht mehr nachgefragt (da es keine Kunden gibt). 
Also können z.B. alle Eissorten beliebig billig angeboten werden, sobald die Cola mehr als X kostet, wird kein Eis mehr verkauft. 
Das Gleiche gilt auch für die Bratwurst, wenn diese zu teuer angeboten wird, werden keine Pommes mehr verkauft.     

## Optimale Verkausstrategie

## Analyse der Spielmechanik "Imbiss" für PC von 1991

## Danksagung: 
Vielen Dank an **Oliver Schwald**, der mit die Listings von F. Brall "Imbiss-Bude" aus dem Homecomputer 8/1983 sowie seiner C64 Implementation aus dem Homecomputer 10/1984 eingescannt und geschickt hat! Vielen Dank an **Thomas Bauer**, für die vielen interessante Information und Anekdoten zu seiner PC Version von 1991 und dessen Entstehung. 
