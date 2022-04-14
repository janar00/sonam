"""Connection to Discord."""
import discord
from os.path import exists
import pickle
from SM import SMOrganizer, GREEN2, YELLOW2, GREY2

help_message = """Sõnam abi:
`!pakid` - loetle saadaval olevad pakid
`!uus [paki nimi]` - Alusta uut mängu valitud pakiga
`!paku *pakkumine*` - Tee pakkumine praeguses mängus

Mänge saab mängida vaid määratud kanalites.

Serveri omaniku käsud:
`!abi` - Kuva see abisõnum
`!reeglid` - Kuva mängu reeglid
`!lisakanal [kanali_id]` - Määra kanal mängukanaliks
`!eemaldakanal [kanali_id]` - Ebamäära kanal mängukanaliks
"""

rules_message = f"""Sõnam reeglid:
Paku õige sõna võimalikult väheste käikudega.

Iga pakkumine peab olema sõnastikus esinev sõna.
Iga pakkumise kohta annab mäng infot läbi tähemärkide.
{GREEN2} - täht on õiges kohas
{YELLOW2} - täht esineb sõnas, aga kuskil mujal
{GREY2} - täht ei esine sõnas
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
intents = discord.Intents.default()
intents.members = True  # Needed for checking guild owner
client = discord.Client(intents=intents)


def check_channel_id(message: discord.Message) -> tuple:
    """Check if an id given in a second part of a message is correct and in the same guild as the message."""
    channel_id = message.content.split()[1]
    if not channel_id.isdigit():
        return 0, 'kanali id on ebakorrektne!'
    channel_id = int(channel_id)
    if not message.guild.get_channel(channel_id):
        return 0, 'Sellise id-ga kanalit ei leitud siit serverist!'
    return channel_id, ''


@client.event
async def on_ready():
    """Will activate when logged in and ready to read messages."""
    print('Sain sisse logitud')
    print('Kasutajanimi:', client.user)


@client.event
async def on_message(message: discord.Message):
    """Will activate when a message is sent in a server."""
    if message.author == client.user:
        return

    if not message.guild:
        # Direct Message
        return

    if message.channel.id in game_channels:
        # Message was sent in a game channel
        print('game')

        if message.content == '!pakid':
            await message.channel.send(game.get_word_lists())

        elif message.content.startswith('!uus'):
            print('uus mäng:', message.author.name)
            await message.channel.send(game.new_game(message.channel.id, message.content[4:].strip()))

        elif message.content.startswith('!paku '):
            print('pakkumine:', message.author.name)
            guess = message.content.split()[1]
            await message.channel.send(game.games[message.channel.id].guess(guess))

    if message.author == message.guild.owner:
        # Message was sent by the owner of the server
        print('owner')

        change = False

        if message.content == '!abi':
            await message.channel.send(help_message)
        elif message.content == '!reeglid':
            await message.channel.send(rules_message)

        elif message.content.startswith('!lisakanal'):
            if len(message.content.split()) == 2:
                channel_id, msg = check_channel_id(message)
                if msg:
                    await message.channel.send(msg)
                    return
            else:
                channel_id = message.channel.id

            if channel_id:
                print('kanal lisatud:', channel_id)
                await message.channel.send('Kanal lisatud!')
                game_channels.add(channel_id)
                change = True

        elif message.content.startswith('!eemaldakanal'):
            if len(message.content.split()) == 2:
                channel_id, msg = check_channel_id(message)
                if msg:
                    await message.channel.send(msg)
                    return
            else:
                channel_id = message.channel.id

            if channel_id:
                print('kanal eemaldatud:', channel_id)
                await message.channel.send('Kanal eemaldatud!')
                game_channels.discard(channel_id)
                change = True

        if change:
            with open(game_channels_path, 'wb') as file:
                pickle.dump(game_channels, file)


client.run(token)
