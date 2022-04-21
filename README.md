# Sõnam

Mitme inimesega koos lahendatav eestikeelne Wordle.

Sõnam ehk rohkem sõna või sõnamäng (ise tead kumb rohkem meeldib)
on Discordi serveris töötav programm, mille abil on võimalik koos sõpradega sõnu ära arvata.

## Jooksutamine

- Mäng vajab käivitamiseks Python versiooni 3.9+
- Ühenduseks Discordiga on vaja [installida disnake lisand](https://docs.disnake.dev/en/latest/intro.html)
- Samuti on Discordiga ühenduseks vajalik [luua bot ja ühendada see oma serveriga](https://docs.disnake.dev/en/latest/discord.html)
  - Boti võti paiguta kausta `discord_data`, faili `token.txt` 

- Kui soovid mängu katsetada üksinda, siis jookusta faili `SM.py`
- Kui soovid mängida Discordis, siis käivita fail `server.py`
- Käskude nägemiseks saab kanalite muutmise õigusega kasutaja saata sõnumi `/abi`
