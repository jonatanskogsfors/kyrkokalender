# kyrkokalender

Skapa kalenderfiler i iCalendar-format (.ics) för hela kyrkoår med information om helgdagarnas namn, tema, 
textläsningar etc. Datat hämtas från
svenskakyrkan.se och är samma datamängd som visas på deras sida [Kyrkoårets bibeltexter](https://www.svenskakyrkan.se/kyrkoaret/bibeltexter).

Exempel på information för en helgdag:
```text
-------
DTSTART
-------
2025-11-30

-------
SUMMARY
-------
Första söndagen i advent

-----------
DESCRIPTION
-----------
Tema: Ett nådens år

Den första söndagen i advent berättar om hur Jesus som vuxen rider in i Jerusalem
för att fira den judiska påsken, den händelse som skedde alldeles innan det vi
firar under påsken. Han kommer ridande på en åsna och vill frid och fred istället
för död och blod.

Årgång 3:
Sak 9:9-10
Upp 5:1-5
Matt 21:1-9
Ps 24:1-10

Den liturgiska färgen är vit - byte till violett/blå efter kl 18. På altaret står
sex ljus samt vita blommor.

Advent
Ordet advent betyder ankomst, Jesu ankomst. Under advent minns och tänker vi på
Jesu födelse, Jesu återkomst och Jesus som finns hos oss idag.

---
URL
---
https://www.svenskakyrkan.se/kyrkoaret/bibeltexter?id=12&year=2025
```

För användare av Google Kalender kan filerna lätt importeras till en befintlig kalender.

## Användning
### Installation
Det enda systemkravet är [uv](https://docs.astral.sh/uv/). Det går såklart att installera utan uv men varför? Klona 
eller ladda ner repot så är det redo att köras direkt.

### Skapa kalender
```bash
uv run create-calendar 2025
```

#### API-nyckel
För att använda skriptet behöver du en API-nyckel. Detta kan skapas kostnadsfritt på [api.svenskakyrkan.se](https://api.svenskakyrkan.se).

Den fiffige kan även kika på [Kyrkoårets bibeltexter](https://www.svenskakyrkan.se/kyrkoaret/bibeltexter)
med Developer tools i sin webbläsare och kika på hur `webapi/api-v2/churchcalendar/` anropas...

#### Cachning
För att inte anropa Svenska kyrkans servrar i onödan cachas resultatet i datorns temp-mapp. Använd flaggan 
`--reload` för att ignorera cachad data.

### Granska kalender
Granska kalenderfilerna för att se att det blev rätt:
```bash
uv run review-calendar kyrkoåret_2025.ics
```

## Kör utan att installera
Så länge du har [uv](https://docs.astral.sh/uv/) och en API-nyckel kan du köra:
```
uvx kyrkokalender 2025
```

