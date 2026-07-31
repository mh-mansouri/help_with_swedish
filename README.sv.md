# Hjälp med svenska — en Claude Skill

[Svenska](README.sv.md) · [English](README.md) · [فارسی](README.fa.md)

En Claude Skill som hjälper människor att hitta YouTube-klipp som passar deras nivå och mål när de lär sig svenska.

Många får svårt att välja rätt material när de lär sig ett nytt språk. Den här skillen gör det enklare genom att ge korta, konkreta förslag istället för slumpmässiga videor.

## Använd den på 30 sekunder

1. Ladda ner [hjälp_om_svenska.skill](hjälp_om_svenska.skill).
2. Öppna den i Claude.
3. Fråga till exempel: “Jag är på A2-nivå och vill bli bättre på att prata inför en resa till Sverige.”

## Demo

En användare skriver: “Jag är på A2-nivå och vill bli bättre på att prata inför en resa till Sverige.” Skillen svarar med en kort plan, några relevanta klipp och ett tydligt nästa steg.

![Demo förhandsvisning](https://via.placeholder.com/800x320.png?text=Hj%C3%A4lp+med+svenska+Demo)

## Vad den gör

- Väljer en lärväg utifrån nivå, mål och färdighet.
- Föreslår videor för lyssning, läsning, skrivning och tal.
- Prioriterar praktiska kanaler som Peter SFI, Lätt Svenska med Oskar, UR Play och Swedish Shadowing.
- Håller rekommendationerna korta, uppmuntrande och lätt att följa.

## Varför den finns

Många läser eller tittar på material som är antingen för svårt eller för enkelt. Den här skillen hjälper till att undvika det och ger ett mer realistiskt sätt att lära sig steg för steg.

## Installera

Alternativ A — en fil: ladda ner [hjälp_om_svenska.skill](hjälp_om_svenska.skill) och öppna den i Claude.

Alternativ B — paketera den lokalt:

```bash
python package_skill.py
python package_skill.py --check
python package_skill.py --install --skills-dir <sökväg-till-skills-mapp>
```

Kommandot `--check` kontrollerar att alla nödvändiga filer finns innan du använder paketet.

## Hur du använder den

Testa frågor som:

- “Jag vill bli bättre på att förstå vardagligt svenska.”
- “Jag är nybörjare och vill ha en enkel plan för att prata.”
- “Ge mig bra svenska videor för läsning på nivå B1.”
- “Jag vill ha en plan på två veckor för att lära mig svenska inför jobbet.”
- “Jag är på A2-nivå och vill förbättra mitt ordförråd inför en flytt till Sverige.”
- “Jag tror att jag är intermediate i svenska, men jag är inte säker på var jag egentligen hör hemma.”

En bra respons brukar innehålla:

- en kort nivåbedömning eller förslag,
- 3–5 videor eller spellistor,
- och ett tydligt nästa steg för användaren.

Ett starkt exempel ser ut så här:

> “Du verkar ligga runt A2. Ett bra nästa steg är lyssningsövningar och korta pratövningar. Jag rekommenderar tre korta klipp och en enkel daglig rutin.”

## Vad den hjälper till med

- Att välja ett bra nästa steg i svenskstudier
- Att matcha användaren till en nivåanpassad väg
- Att föreslå praktiska YouTube-resurser utan att överväldiga användaren

## Vad den inte ersätter

- En formell språktestning
- En lärarledd nivåplacering
- En garanterad CEFR-betyg

## Struktur

- hjälp_om_svenska/SKILL.md — instruktionerna för skillen
- hjälp_om_svenska/references/ — referensfiler med exempel och tips
- hjälp_om_svenska.skill — den paketerade skillfilen
- package_skill.py — bygger paketet

## Bygg

Kör:

```bash
python package_skill.py
```

## Bidra

Bidrag är välkomna. Om du har bättre kanaler, tydligare exempel eller starkare vägledning är du välkommen att bidra.

## Licens

Detta projekt är licensierat under MIT-licensen.

## Om projektet

Det här repo:t paketerar en Claude Skill för personer som vill lära sig svenska på ett enkelt och praktiskt sätt.
