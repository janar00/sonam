"""Connection to Discord."""
import disnake as discord
from disnake.ext import commands
from os.path import exists
import pickle
from SM import SMOrganizer, GREEN2, YELLOW2, GREY2

# This class name is way too long
Inter = discord.ApplicationCommandInteraction  # any slash command
GInter = discord.GuildCommandInteraction  # only in guilds

permission_error = "Sul pole õigus siin seda käsku kasutada!"

help_message = f"""**Sõnam põhiliste käskude näited:**
`/uus` - Alusta uut mängu tavalise pakiga
`/uus eesti-11` - Alusta uut mängu pakiga eesti-11 (ehk eesti keeles ja 11 tähega sõna)
`/paku temperatuur` - Tee praeguses mängus pakkumine "temperatuur"

**Sõnam reeglid:**
Robot valib ühe sõna, mille sina pead ära arvama.
Paku õige sõna võimalikult väheste käikudega.

Iga pakkumine peab olema sõnastikus esinev sõna.
Iga pakkumise kohta annab mäng infot läbi tähemärkide.
{GREEN2} - täht on õiges kohas
{YELLOW2} - täht esineb sõnas, aga kuskil mujal
{GREY2} - täht ei esine sõnas

Mänge saab mängida vaid määratud kanalites.
Igas kanalis saab korraga toimuda üks mäng, see on kõigi vahel jagatud.
Mängida on võimalik vaid siis, kui SM-Bot on sisselogitud, üldiselt ta öösel tudub. 

**Sõnam käskude kirjeldus:**
Arvesta, et Discord proovib sind aidata käskudega.
Näiteks kui trükid sisse, `/p` ja vajutad Enter, peaks automaatselt minema kirja `/paku`
Eriti kasulik on see uue mängu puhul, kus ainult tähtede arvu kirjutamisel pakutakse õige nimi.

Järgnevates käskudes täida sulgude sees olev osa vastava sisuga. Ära kirjuta sulge välja!
Kui selle ümber on <noolsulud>, siis on see kohustuslik.
Kui selle ümber on [nurksulud], siis ei ole see kohustuslik.

`/uus [paki nimi]` - Alusta uut mängu valitud pakiga
(Pakk on sõnastik, millest valitakse vastus) 
(Kui ei kirjuta midagi, siis tuleb tavaline pakk)
(Kui kirjutad osa nimest, siis valitakse suvaline nende vahelt, milles see sisaldub)
(Kui kirjutad vale nime, siis tuleb suvaline pakk)

`/paku <pakkumine>` - Tee pakkumine praeguses mängus
`/mis_sa_arvad` - Robot vastab sulle ühe sõnaga, mis sobiks pakkumiseks
`/ajalugu` - Kuva pakkumiste ajalugu
`/rohelised` - Kuva kõik tähed, mille asukoht on kindlalt teada
`/annan_alla <kinnitus>` - Annab ette vastuse kui sa oled juba piisavalt pakkumisi teinud, kinnitus on "ma ei suuda enam, palun lõpetame selle tralli ära"

`/abi` - Kuva see abisõnum
`/abi2` - Kuva muude käskude abisõnum
`/kuvapakid` - loetle saadaval olevad pakid
"""

help2_message = """**Muud käsud:**
`/muuda raskus <True/False>` - Kas mäng on Raskes režiimis (ehk sa pead iga pakkumine kasutama teadaolevaid kollaseid/rohelisi tähti)
`/muuda kontroll <True/False>` - Kas mäng kontrollib sõnastikust sinu pakkumist
`/muuda uus_pakk <paku nimi>` - Milline pakk valitakse kui ei anna /uus käsuga midagi kaasa
`/muuda emoji_kasutus [True/False]` - Kas mäng näitab tulemust emojidega või tähtedega `./*`
`/muuda <emoji_hall / emoji_kollane / emoji_roheline> [Emoji]` - Muuda tulemustes näidatavat vastavat emojit, tühjaks jättes taastatakse tavaline

`/vaata <raskus / kontroll / uus_pakk / emoji_kasutus / emoji_list>` - Kuva vastava sätte seisu

Käsud `Manage Channels` õigusega kasutajatele:
`/abi` ja `/abi2` on kuvatavad igas kanalis nende poolt
`/kanal_lisa [kanali id]` - Määra kanal mängukanaliks
`/kanal_eemalda [kanali id]` - Ebamäära kanal mängukanaliks
"""

game_channels_path = '../discord_data/game_channels.bin'
token_path = '../discord_data/token.txt'

# Load in list of channels where games can be played
if exists(game_channels_path):
    with open(game_channels_path, 'rb') as file:
        game_channels: set = pickle.load(file)
else:
    print('Mängukanalite fail puudub, alustan tühja nimekirjaga.')
    game_channels = set()

# Load in secret token for logging in
if exists(token_path):
    with open(token_path) as file:
        token = file.read()
else:
    raise FileNotFoundError('discord_data/token.txt puudub, lisa see fail ja pane selle sisuks Discordi bot token')

game = SMOrganizer()
bot = commands.InteractionBot(test_guilds=[928303868176138290, 958043104441675846])
# If test guilds are given, then commands only work there
# If not test guilds, then updating commands globally takes like an hour according to some documentation


async def autocomplete_packs(inter: Inter, user_input: str):
    return [pack for pack in game.word_lists.keys() if user_input.lower() in pack]


def check_channel(inter: GInter, channel: discord.TextChannel):
    """Check if channel exists in server."""
    if not channel:
        return inter.channel
    if not inter.guild == channel.guild:
        # This may be always false, it seems discord only allows correct channels through
        return None
    return channel


@bot.event
async def on_ready():
    """Will activate when logged in and ready to read messages."""
    print('Sõnam Server 2.0.1')
    print('Sain sisse logitud')
    print('Kasutajanimi:', bot.user, '\n')


@bot.slash_command(
    name='abi',
    description='Kuva abisõnum'
)
async def abi(inter: GInter):
    if inter.channel_id in game_channels or inter.permissions.manage_channels:
        await inter.send(help_message)
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    description='Kuva muude käskude abisõnum'
)
async def abi2(inter: GInter):
    if inter.channel_id in game_channels or inter.permissions.manage_channels:
        await inter.send(help2_message)
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    name='kuvapakid',
    description='Näita olemasolevaid pakke'
)
async def kuvapakid(inter: GInter):
    if inter.channel_id in game_channels:
        await inter.send(game.get_word_lists())
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    name='uus',
    description='Alusta uut mängu'
)
async def uus(
        inter: GInter,
        paki_nimi: str = commands.Param(autocomplete=autocomplete_packs, default='')
):
    if inter.channel_id in game_channels:
        print('Uus mäng:', inter.author.name)
        await inter.send(game.new_game(inter.channel_id, paki_nimi))
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    name='paku',
    description='Tee pakkumine praeguses mängus'
)
async def paku(inter: GInter, pakkumine: str):
    if inter.channel_id in game_channels:
        print('Pakkumine:', inter.author.name)
        await inter.send(game.guess(inter.channel_id, pakkumine))
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    name='mis_sa_arvad',
    description='Mäng annab soovituse, mida pakkuda'
)
async def mis_sa_arvad(inter: GInter):
    if inter.channel_id in game_channels:
        await inter.send(game.get_guess(inter.channel_id))
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    name='ajalugu',
    description='Kuva pakkumiste ajalugu'
)
async def ajalugu(inter: GInter):
    if inter.channel_id in game_channels:
        await inter.send(game.history(inter.channel_id))
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command(
    name='rohelised',
    description='Kuva kõik tähed, mis asuvad juba õiges kohas'
)
async def rohelised(inter: GInter):
    if inter.channel_id in game_channels:
        await inter.send(game.greens(inter.channel_id))
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command()
async def annan_alla(inter: GInter, *, kinnitus: str):
    """Anna alla ja lõpeta ära praegune mäng.

    Parameters
    ----------
    kinnitus: kinnitus peab olema "ma ei suuda enam, palun lõpetame selle tralli ära"
    """
    if inter.channel_id in game_channels:
        await inter.send(game.give_up(inter.channel_id, kinnitus))
    else:
        await inter.send(permission_error, delete_after=10)


@bot.slash_command()
async def muuda(inter: GInter): pass


@muuda.sub_command(
    name='raskus',
    description='Määra, kas mängida raskel režiimil või mitte'
)
async def raskus(inter: GInter, raske: bool):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'hard_mode', raske))


@muuda.sub_command(
    name='kontroll',
    description='Määra, kas sõnu kontrollitakse sõnastikust'
)
async def kontroll(inter: GInter, kontroll: bool):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'dict_check', kontroll))


@muuda.sub_command(
    name='uus_pakk',
    description='Määra, millise pakiga alustatakse tavaliselt uut mängu'
)
async def uus_pakk(inter: GInter, paki_nimi: str):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'default_word_list', paki_nimi))


@muuda.sub_command(
    name='emoji_kasutus',
    description='Määra, kas mängus kasutatakse emojisid (või märke ./*)'
)
async def emoji_kasutus(inter: GInter, emoji: bool = True):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'pretty_format', emoji))


@muuda.sub_command(
    name='emoji_hall',
    description='Määra, millise emojiga märgitakse valed tähed'
)
async def emoji_hall(inter: GInter, emoji: str = GREY2):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'grey2', emoji))


@muuda.sub_command(
    name='emoji_kollane',
    description='Määra, millise emojiga märgitakse vales kohas tähed'
)
async def emoji_kollane(inter: GInter, emoji: str = YELLOW2):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'yellow2', emoji))


@muuda.sub_command(
    name='emoji_roheline',
    description='Määra, millise emojiga märgitakse õiged tähed'
)
async def emoji_roheline(inter: GInter, emoji: str = GREEN2):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'green2', emoji))


@bot.slash_command()
async def vaata(inter: GInter): pass


@vaata.sub_command(
    description='Vaata praegust mängu raskusastet'
)
async def raskus(inter: GInter):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'hard_mode'))


@vaata.sub_command(
    description='Vaata praegust sõnastikukontrolli seisu'
)
async def kontroll(inter: GInter):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'dict_check'))


@vaata.sub_command(
    description='Vaata praegust tavalist uue mängu sõnastikku'
)
async def uus_pakk(inter: GInter):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'default_word_list'))


@vaata.sub_command(
    description='Vaata, kas mäng kasutab emojisid (või märke ./*'
)
async def emoji_kasutus(inter: GInter):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'pretty_format'))


@vaata.sub_command(
    description='Vaata mängu märgiseid'
)
async def emoji_list(inter: GInter):
    if inter.channel_id not in game_channels:
        await inter.send(permission_error, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'emoji_list'))


@bot.slash_command(
    name='kanal_lisa',
    description='Määra kanal mängukanaliks'
)
async def kanal_lisa(inter: GInter, kanal: discord.TextChannel = None):
    if not inter.permissions.manage_channels:
        await inter.send(permission_error, delete_after=10)
        return
    channel = check_channel(inter, kanal)
    if not channel:
        await inter.send('Sellist kanalit ei leitud!')
        return
    await inter.send(f'Kanal lisatud: {channel.name}')
    print(f'Kanal lisatud: {channel.name}')
    game_channels.add(channel.id)
    with open(game_channels_path, 'wb') as file:
        pickle.dump(game_channels, file)


@bot.slash_command(
    name='kanal_eemalda',
    description='Ebamäära kanal mängukanaliks'
)
async def kanal_eemalda(inter: GInter, kanal: discord.TextChannel = None):
    if not inter.permissions.manage_channels:
        await inter.send(permission_error, delete_after=10)
        return
    channel = check_channel(inter, kanal)
    if not channel:
        await inter.send('Sellist kanalit ei leitud!')
        return
    await inter.send(f'Kanal eemaldatud: {channel.name}')
    print(f'Kanal eemaldatud: {channel.name}')
    game_channels.discard(channel.id)
    with open(game_channels_path, 'wb') as file:
        pickle.dump(game_channels, file)


bot.run(token)
