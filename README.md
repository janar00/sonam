# Sõnam

Mitme inimesega koos lahendatav eestikeelne Wordle.

Sõnam ehk rohkem sõna või sõnamäng (ise tead kumb rohkem meeldib)
on Discordi serveris töötav programm,
mille abil on võimalik koos sõpradega sõnu ära arvata.

## Sõnam reeglid
Robot valib ühe sõna, mille sina pead ära arvama.\
Paku õige sõna võimalikult väheste käikudega.

- Iga pakkumine peab olema sõnastikus esinev sõna
- Iga pakkumise kohta annab mäng infot läbi tähemärkide:
  - Roheline - täht on õiges kohas
  - Kollane - täht esineb sõnas, aga kuskil mujal
  - Hall - täht ei esine sõnas
- Mänge saab mängida vaid määratud kanalites.
- Igas kanalis saab korraga toimuda üks mäng, see on kõigi vahel jagatud.
- Mängida on võimalik vaid siis, kui bot kasutaja on sisse logitud. 


## Jooksutamine

- Mäng vajab käivitamiseks Python versiooni 3.9+
- Ühenduseks Discordiga on vaja [installida disnake lisand](https://docs.disnake.dev/en/latest/intro.html)
- Samuti on Discordiga ühenduseks vajalik [luua bot ja ühendada see oma serveriga](https://docs.disnake.dev/en/latest/discord.html)
  - Boti võti paiguta kausta `discord_data`, faili `token.txt` 
  - See programm vajab jooksmiseks `bot` ja `application.commands` õigusi serveris
- Käskude uuendamisel võib minna kaua aega, et need käsud oleks globaalselt uuendatud
  - Selle vältimiseks on võimalik lisada üksikute serverite id'd boti deklareerivasse koodi
  - Näiteks saab siin `bot` muutuja deklaratsiooni serveri failis lisada parameetri `test_guilds` nii: `bot = commands.InteractionBot(test_guilds=[928303868176138290, 958043104441675846])`

- Kui soovid mängu katsetada üksinda, siis jookusta faili `SM.py`
- Kui soovid mängida Discordis, siis käivita fail `server.py`
- Käskude nägemiseks saab kanalite muutmise õigusega kasutaja saata sõnumi `/abi`

## Sõnade pakid

Selle mänguga on kaasas eestikeelsete sõnade pakid 4-18 täheliste sõnade jaoks.
Need põhinevad EKI `lemmad.txt` failil.

### Uue paki lisamine

- Hangi sõnade nimekiri
- Teisalda see kujule, kus sõnad on tekstifailis, igal real eraldi sõna, faili formaat utf-8
- Võta lahti `wordlist_tools.py`, selle main osas on välja toodud üks võimalus selle funktsioone kasutada
  - `read_in_wordlist` abil on võimalik sisse lugeda oma sõnade nimekiri
  - `find_letter_counts` aitab leida, milliseid tähti esineb sõnades ning milliseid võiks välja filtreerida
  - `filter_wordlist_by_character` filtreerib välja kõik etteantud tähtedega sõnad
  - `find_word_lengths` leiab üles, mitu tükki iga pikkusega sõna esineb
    - Lemmade pakkide puhul jäeti alles näiteks kõik pikkused, kus oli 1000+ sõna
  - `filter_wordlist_by_length` eraldab listi alamlistideks etteantud pikkuste järgi
  - `find_unused_letters` leiab millised tähed kõikidest tavatähtedest ei esine listis ja peab kirjutama indeksi faili
  - `write_wordlist_to_file` kirjutab listi faili, soovitavalt võiks see asuda `words` kataloogis
- Uuenda faili `index.txt`
  - Iga uue faili kohta lisa uus rida, kus on komadega eraldatult:
    - Faili asukoht index.txt suhtes
    - Puuduvad tähed `ALL_LETTERS` suhtes
    - Nimi, mille järgi on võimalik pakk valida

## Käsud

Seda programmi on üldiselt võimalik käsutada vaid serveri kanalites, kus ta on aktiveeritud.
Teatud käske saavad käivitada `Manage Channels` õigustega kasutajad kõikjal.

Arvesta, et Discord proovib sind aidata käskudega.
Näiteks kui trükid sisse, `/p` ja vajutad Enter, peaks automaatselt minema kirja `/paku`
Eriti kasulik on see uue mängu puhul, kus ainult tähtede arvu kirjutamisel pakutakse õige nimi.

Järgnevates käskudes täida sulgude sees olev osa vastava sisuga. Ära kirjuta sulge välja!\
Kui selle ümber on `<noolsulud>`, siis on see kohustuslik.\
Kui selle ümber on `[nurksulud]`, siis ei ole see kohustuslik.

- Põhiliste käskude näited:
  - `/uus` - Uus mäng tavalise pakiga
  - `/uus eesti-11` - Uus mäng pakiga eesti-11 ehk 11-täheline sõna
  - `/paku temperatuur` - Tee mängus pakkumine "temperatuur"

- Tavalisemad käsud:
  - `/uus [paki nimi]` - Alusta uut mängu valitud pakiga
    - Pakk on sõnastik, millest valitakse vastus
    - Kui ei kirjuta midagi, siis tuleb tavaline pakk
    - Kui kirjutad osa nimest, siis valitakse suvaline nende vahelt, milles see sisaldub
    - Kui kirjutad vale nime, siis tuleb suvaline pakk
  - `/paku <pakkumine>` - Tee pakkumine praeguses mängus
  - `/mis_sa_arvad` - Robot vastab sulle ühe sõnaga, mis sobiks pakkumiseks
  - `/ajalugu` - Kuva pakkumiste ajalugu
  - `/rohelised` - Kuva kõik tähed, mille asukoht on kindlalt teada
  - `/annan_alla <kinnitus>` - Annab ette vastuse kui sa oled juba piisavalt pakkumisi teinud, kinnitus on "ma ei suuda enam, palun lõpetame selle tralli ära"
  - `/abi` - Kuva abisõnum
  - `/abi2` - Kuva muude käskude abisõnum
  - `/kuvapakid` - loetle saadaval olevad pakid

- Muud käsud:
  - `/muuda raskus <True/False>` - Kas mäng on Raskes režiimis (ehk sa pead iga pakkumine kasutama teadaolevaid kollaseid/rohelisi tähti)
  - `/muuda kontroll <True/False>` - Kas mäng kontrollib sõnastikust sinu pakkumist
  - `/muuda uus_pakk <paku nimi>` - Milline pakk valitakse kui ei anna /uus käsuga midagi kaasa
  - `/muuda emoji_kasutus [True/False]` - Kas mäng näitab tulemust emojidega või tähtedega `./*`
  - `/muuda <emoji_hall / emoji_kollane / emoji_roheline> [Emoji]` - Muuda tulemustes näidatavat vastavat emojit, tühjaks jättes taastatakse tavaline
  - `/vaata <raskus / kontroll / uus_pakk / emoji_kasutus / emoji_list>` - Kuva vastava sätte seisu

- Käsud `Manage Channels` õigusega kasutajatele:
  - `/abi` ja `/abi2` on kuvatavad igas kanalis nende poolt
  - `/kanal_lisa [kanali id]` - Määra kanal mängukanaliks
  - `/kanal_eemalda [kanali id]` - Ebamäära kanal mängukanaliks
