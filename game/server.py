"""Connection to Discord."""
import disnake as discord
from disnake.ext import commands
from os.path import exists
import pickle
from SM import SMOrganizer, GREEN2, YELLOW2, GREY2

print('Sõnam Server 2.0.2')

# This class name is way too long
Inter = discord.ApplicationCommandInteraction  # any slash command
GInter = discord.GuildCommandInteraction  # only in guilds

MSG_PERMISSION_ERROR = "Sul pole õigus siin seda käsku kasutada!"

MSG_HELP = f"""**Sõnam põhiliste käskude näited:**
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
Mängida on võimalik vaid siis, kui SM-Bot on sisse logitud, üldiselt ta öösel tudub. 

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

MSG_HELP2 = """**Muud käsud:**
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

GAME_CHANNELS_PATH = '../discord_data/game_channels.bin'
TOKEN_PATH = '../discord_data/token.txt'

# Load in secret token for logging in
if exists(TOKEN_PATH):
    with open(TOKEN_PATH) as file:
        token = file.read()
else:
    raise FileNotFoundError(TOKEN_PATH + ' puudub, lisa see fail ja pane selle sisuks Discordi bot token')

# Load in list of channels where games can be played
if exists(GAME_CHANNELS_PATH):
    with open(GAME_CHANNELS_PATH, 'rb') as file:
        game_channels: set = pickle.load(file)
else:
    print('Mängukanalite fail puudub, alustan tühja nimekirjaga.')
    game_channels = set()

game = SMOrganizer()
bot = commands.InteractionBot()
# If test guilds are given, then commands only work there
# If not test guilds, then updating commands globally takes like an hour according to some documentation


async def autocomplete_packs(inter: Inter, user_input: str):
    """Offer pack names for starting a new game."""
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
    print('Sain sisse logitud')
    print('Kasutajanimi:', bot.user, '\n')


# discord command name and description can be given
# via slash command decorator parameters: @bot.slash_command(name=..., description=...)
# or via function name and docstring: async def name(): """desc."""
@bot.slash_command()
async def abi(inter: GInter):
    """Kuva abisõnum"""
    if inter.channel_id in game_channels or inter.permissions.manage_channels:
        await inter.send(MSG_HELP)
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def abi2(inter: GInter):
    """Kuva muude käskude abisõnum"""
    if inter.channel_id in game_channels or inter.permissions.manage_channels:
        await inter.send(MSG_HELP2)
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def kuvapakid(inter: GInter):
    """Näita olemasolevaid pakke"""
    if inter.channel_id in game_channels:
        await inter.send(game.get_word_lists())
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def uus(
        inter: GInter,
        paki_nimi: str = commands.Param(autocomplete=autocomplete_packs, default='')
):
    """Alusta uut mängu"""
    if inter.channel_id in game_channels:
        print('Uus mäng:', inter.author.name)
        await inter.send(game.new_game(inter.channel_id, paki_nimi))
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def paku(inter: GInter, pakkumine: str):
    """Tee pakkumine praeguses mängus"""
    if inter.channel_id in game_channels:
        print('Pakkumine:', inter.author.name)
        await inter.send(game.guess(inter.channel_id, pakkumine))
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def mis_sa_arvad(inter: GInter):
    """Mäng annab soovituse, mida pakkuda"""
    if inter.channel_id in game_channels:
        await inter.send(game.get_guess(inter.channel_id))
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def ajalugu(inter: GInter):
    """Kuva pakkumiste ajalugu"""
    if inter.channel_id in game_channels:
        await inter.send(game.history(inter.channel_id))
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def rohelised(inter: GInter):
    """Kuva kõik tähed, mis asuvad juba õiges kohas"""
    if inter.channel_id in game_channels:
        await inter.send(game.greens(inter.channel_id))
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def annan_alla(inter: GInter, *, kinnitus: str):
    """Anna alla ja lõpeta ära praegune mäng

    Parameters
    ----------
    kinnitus: kinnitus peab olema "ma ei suuda enam, palun lõpetame selle tralli ära"
    """
    if inter.channel_id in game_channels:
        await inter.send(game.give_up(inter.channel_id, kinnitus))
    else:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)


@bot.slash_command()
async def muuda(inter: GInter): pass


@muuda.sub_command()
async def raskus(inter: GInter, raske: bool):
    """Määra, kas mängida raskel režiimil või mitte"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'hard_mode', raske))


@muuda.sub_command()
async def kontroll(inter: GInter, kontroll: bool):
    """Määra, kas sõnu kontrollitakse sõnastikust"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'dict_check', kontroll))


@muuda.sub_command()
async def uus_pakk(inter: GInter, paki_nimi: str):
    """Määra, millise pakiga alustatakse tavaliselt uut mängu"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'default_word_list', paki_nimi))


@muuda.sub_command()
async def emoji_kasutus(inter: GInter, emoji: bool = True):
    """Määra, kas mängus kasutatakse emojisid (või märke ./*)"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'pretty_format', emoji))


@muuda.sub_command()
async def emoji_hall(inter: GInter, emoji: str = GREY2):
    """Määra, millise emojiga märgitakse valed tähed"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'grey2', emoji))


@muuda.sub_command()
async def emoji_kollane(inter: GInter, emoji: str = YELLOW2):
    """Määra, millise emojiga märgitakse vales kohas tähed"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'yellow2', emoji))


@muuda.sub_command()
async def emoji_roheline(inter: GInter, emoji: str = GREEN2):
    """Määra, millise emojiga märgitakse õiged tähed"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    await inter.send(game.set_data(inter.channel_id, 'green2', emoji))


@bot.slash_command()
async def vaata(inter: GInter): pass


@vaata.sub_command()
async def raskus(inter: GInter):
    """Vaata praegust mängu raskusastet"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'hard_mode'))


@vaata.sub_command()
async def kontroll(inter: GInter):
    """Vaata praegust sõnastikukontrolli seisu"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'dict_check'))


@vaata.sub_command()
async def uus_pakk(inter: GInter):
    """Vaata praegust tavalist uue mängu sõnastikku"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'default_word_list'))


@vaata.sub_command()
async def emoji_kasutus(inter: GInter):
    """Vaata, kas mäng kasutab emojisid (või märke ./*)"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'pretty_format'))


@vaata.sub_command()
async def emoji_list(inter: GInter):
    """Vaata mängu märgiseid"""
    if inter.channel_id not in game_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
    await inter.send(game.get_data(inter.channel_id, 'emoji_list'))


@bot.slash_command()
async def kanal_lisa(inter: GInter, kanal: discord.TextChannel = None):
    """Määra kanal mängukanaliks"""
    if not inter.permissions.manage_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    channel = check_channel(inter, kanal)
    if not channel:
        await inter.send('Sellist kanalit ei leitud!')
        return
    await inter.send(f'Kanal lisatud: {channel.name}')
    print(f'Kanal lisatud: {channel.name}')
    game_channels.add(channel.id)
    with open(GAME_CHANNELS_PATH, 'wb') as file:
        pickle.dump(game_channels, file)


@bot.slash_command()
async def kanal_eemalda(inter: GInter, kanal: discord.TextChannel = None):
    """Ebamäära kanal mängukanaliks"""
    if not inter.permissions.manage_channels:
        await inter.send(MSG_PERMISSION_ERROR, delete_after=10)
        return
    channel = check_channel(inter, kanal)
    if not channel:
        await inter.send('Sellist kanalit ei leitud!')
        return
    await inter.send(f'Kanal eemaldatud: {channel.name}')
    print(f'Kanal eemaldatud: {channel.name}')
    game_channels.discard(channel.id)
    with open(GAME_CHANNELS_PATH, 'wb') as file:
        pickle.dump(game_channels, file)


bot.run(token)
