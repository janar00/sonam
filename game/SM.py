"""SõnaMäng game logic."""
from copy import deepcopy
from os.path import exists
import pickle
import random

INDEX_PATH = '../words/index.txt'
GAME_DATA_PATH = '../discord_data/SMData.bin'
ALL_LETTERS = 'QWERTYUIOPÜÕASDFGHJKLÖÄZXCVBNMŠŽ'

# console markings
GREY, YELLOW, GREEN = ".", "/", "*"
# emoji markings (hearts)(because the squares don't work on some phones)
GREY2, YELLOW2, GREEN2 = "\U0001F90D", "\U0001F49B", "\U0001F49A"


def check_emoji(emoji: str) -> bool:

    return emoji not in './*_~>' and len(emoji) < 10


class SMOrganizer:
    """Class that will create games of SM."""

    def __init__(self):
        self.games: dict[int, SMGame] = {}
        self.datas: dict[int, SMData] = {}
        self.word_lists: dict = {}
        self.unused_letters: dict = {}
        self.read_datas()
        self.read_word_lists()

    def read_datas(self):
        if exists(GAME_DATA_PATH):
            with open(GAME_DATA_PATH, 'rb') as file:
                self.datas = pickle.load(file)
        else:
            print('Mängu sätete fail puudub, alustan tavasätetega.')

    def read_word_lists(self):
        """
        Read in word lists from files.

        It first reads index.txt for a list of word lists.
        In index.txt each line is formatted like: filename,list_name
        Each list contains valid words, separated by newlines.
        """
        lists = []
        word_lists = {}
        unused_letters_dict = {}
        with open(INDEX_PATH, encoding='utf-8') as file:
            if file.readline() != 'file_name,unused_letters,list_name\n':
                raise AssertionError('vale faili index.txt esimene rida, see peaks olema file_name,unused_letters,list_name')
            for line in file:
                lists.append(line.strip())
        for word_list in lists:
            file_name, unused_letters, list_name = word_list.split(',')
            words = []
            with open('../words/' + file_name, encoding='utf-8') as file:
                for line in file:
                    words.append(line.strip())
            word_lists[list_name] = words
            unused_letters_dict[list_name] = set(unused_letters.upper())
        self.word_lists = word_lists
        self.unused_letters = unused_letters_dict

    def get_word_lists(self) -> str:
        """Create a formatted string of all word lists."""
        printable = 'Praegused pakid: '
        printable += ', '.join(sorted(self.word_lists.keys()))
        return printable

    def get_random_word(self, list_name) -> tuple:
        """
        Get a random word from a given word list.
        If no such list exists, fall back to something else.

        :param list_name: word list to look for
        :return: a tuple of list name and a word from that list
        """
        word_lists = [name for name in self.word_lists.keys() if list_name in name]
        if word_lists:
            list_name = random.choice(word_lists)
        else:
            list_name = random.choice(list(self.word_lists.keys()))
        return list_name, random.choice(self.word_lists[list_name])

    def new_game(self, key: int, list_name: str):
        """
        Create a new game with a random word.
        :param key: Key used for accessing the game
        :param list_name: word list to use for game
        """
        game = self.games.get(key, None)
        if game and not game.done:
            return 'Hetkel juba käib mäng. Palun lõpeta see enne ära.'
        data = self.datas.get(key, SMData())
        if not list_name:
            list_name = data.default_word_list
        list_name, word = self.get_random_word(list_name)
        self.games[key] = SMGame(word,
                                 list_name,
                                 self.word_lists[list_name],
                                 self.unused_letters[list_name],
                                 data)
        return 'Uus mäng on alanud. Sõnastik: ' + list_name

    def guess(self, key: int, guess: str) -> str:
        """
        Play a move in the game.
        :param key: Key used for accessing the game
        :param guess: word guessed in the game
        :return: move result as a string
        """
        if key not in self.games:
            return 'Mängu ei leitud.'
        return self.games[key].guess(guess)

    def get_guess(self, key: int):
        """Get a random word, that works in a given game."""
        if key not in self.games:
            return 'Mängu ei leitud.'
        if self.datas.get(key, SMData()).hard_mode:
            return 'Raskes režiimis ei saa isegi mina sind aidata enam.'
        word = self.get_random_word(self.games[key].lang)[1]
        return 'Mulle meeldib ' + word

    def history(self, key: int) -> str:
        """Show guess history in given game."""
        if key not in self.games:
            return 'Mängu ei leitud.'
        return self.games[key].print_history()

    def greens(self, key: int) -> str:
        if key not in self.games:
            return 'Mängu ei leitud.'
        return self.games[key].print_greens()

    def give_up(self, key: int, msg: str) -> str:
        if key not in self.games:
            return 'Mängu ei leitud.'
        if msg == "ma ei suuda enam, palun lõpetame selle tralli ära":
            return self.games[key].give_up()
        else:
            return 'Vale kinnitus'

    def set_data(self, key_channel: int, key_data: str, value_data) -> str:
        data = self.datas.setdefault(key_channel, SMData())
        printable = ''
        if key_data == 'hard_mode':
            data.hard_mode = value_data
            printable = 'Raskusaste: ' + ('Raske' if value_data else 'Normaalne')
        elif key_data == 'dict_check':
            data.dict_check = value_data
            printable = 'Sõnastiku kontroll: ' + ('Sees' if value_data else 'Väljas')
        elif key_data == 'default_word_list':
            data.default_word_list = value_data
            printable = 'Tavaline sõnastik on ' + value_data
        elif key_data == 'pretty_format':
            data.pretty_format = value_data
            printable = 'Emoji kasutus on ' + ('Sees' if value_data else 'Väljas')
        elif key_data == 'grey2':
            if check_emoji(value_data):
                data.grey2 = value_data
                printable = 'Uus hall märgis on ' + value_data
            else:
                printable = 'Märgis peab olema < 10 tähte pikk ning ei tohi olla `./*_~>` märkide hulgas'
        elif key_data == 'yellow2':
            if check_emoji(value_data):
                data.yellow2 = value_data
                printable = 'Uus kollane märgis on ' + value_data
            else:
                printable = 'Märgis peab olema < 10 tähte pikk ning ei tohi olla `./*_~>` märkide hulgas'
        elif key_data == 'green2':
            if check_emoji(value_data):
                data.green2 = value_data
                printable = 'Uus roheline märgis on ' + value_data
            else:
                printable = 'Märgis peab olema < 10 tähte pikk ning ei tohi olla `./*_~>` märkide hulgas'

        if printable:
            with open(GAME_DATA_PATH, 'wb') as file:
                pickle.dump(self.datas, file)
            return printable
        return 'Sätteid ei leitud.'

    def get_data(self, key_channel: int, key_data: str) -> str:
        data = self.datas.get(key_channel, None)
        if data:
            if key_data == 'hard_mode':
                return 'Raskusaste: ' + ('Raske' if data.hard_mode else 'Normaalne')
            if key_data == 'dict_check':
                return 'Sõnastikukontroll: ' + ('Sees' if data.dict_check else 'Väljas')
            if key_data == 'default_word_list':
                return 'Tavaline sõnastik on ' + data.default_word_list
            if key_data == 'pretty_format':
                return 'Emoji kasutus on ' + ('Sees' if data.pretty_format else 'Väljas')
            if key_data == 'emoji_list':
                if data.pretty_format:
                    return f'Hall: {data.grey2}\nKollane: {data.yellow2}\nRoheline: {data.green2}'
                return f'Hall: `{GREY}`\nKollane: `{YELLOW}`\nRoheline: `{GREEN}`'
        return 'Sätteid ei leitud.'


class SMData:
    """Class for storing settings for each channel."""

    def __init__(self):
        self.dict_check = True
        self.hard_mode = False
        self.default_word_list = 'eesti'
        self.pretty_format = True
        self.grey2 = GREY2
        self.yellow2 = YELLOW2
        self.green2 = GREEN2


class SMGame:
    """Class for one game of SM."""

    def __init__(self, password: str, lang: str, dictionary: set, unused_letters: set, data: SMData):
        self.password = password.upper()
        self.greens = list('.' * len(password))  # used for storing already known letters
        self.lang = lang
        self.dictionary = dictionary
        self.known_letters = {'unknown': set(ALL_LETTERS).difference(unused_letters),
                              'grey': set(),
                              'yellow': set(),
                              'green': set()}
        self.data = data
        self.prev_guesses = []
        self.prev_results = []
        self.done = False

    def guess(self, guess: str) -> str:
        guess = guess.upper()

        if self.done:
            return 'Mäng on juba läbi!'
        if len(guess) < len(self.password):
            return f'{guess} on liiga lühike pakkumine!'
        if len(guess) > len(self.password):
            return f'{guess} on liiga pikk pakkumine!'
        if not guess.isalpha():
            return 'Pakkumine peab koosnema vaid tähtedest!'

        if self.data.dict_check and guess not in self.dictionary:
            return f'{guess} ei esine sõnastikus!'

        printable = ''
        letters = list(self.password)
        result = [''] * len(guess)

        prev_known = None
        if self.data.hard_mode:
            prev_known = deepcopy(self.known_letters)

        for i, letter in enumerate(guess):
            if self.password[i] == letter:  # right letter, right place
                result[i] = GREEN
                letters.remove(letter)
                self.known_letters['unknown'].discard(letter)
                self.known_letters['grey'].discard(letter)
                self.known_letters['yellow'].discard(letter)
                self.known_letters['green'].add(letter)

        for i, letter in enumerate(guess):
            # mark everything else as wrong place or not in the puzzle
            if result[i]:
                continue
            if letter in letters:  # right letter, wrong place
                result[i] = YELLOW
                letters.remove(letter)
                if letter not in self.known_letters['green']:
                    self.known_letters['unknown'].discard(letter)
                    self.known_letters['grey'].discard(letter)
                    self.known_letters['yellow'].add(letter)
            else:  # wrong letter
                result[i] = GREY
                if letter not in self.known_letters['green'] and letter not in self.known_letters['yellow']:
                    self.known_letters['unknown'].discard(letter)
                    self.known_letters['grey'].add(letter)

        result = ''.join(result)

        if self.data.hard_mode and prev_known:
            green = self.known_letters['green'].copy()
            yellow = self.known_letters['yellow'].copy()
            for i in range(len(guess)):
                if result[i] == GREEN:
                    green.discard(guess[i])
                elif result[i] == YELLOW:
                    yellow.discard(guess[i])
            if green or yellow:
                self.known_letters = prev_known
                return f'Sinu pakkumises {guess} ei esine {", ".join(green.union(yellow))} korrektselt!'

        for i, letter in enumerate(result):
            if letter == GREEN:
                self.greens[i] = self.password[i]
        self.prev_guesses.append(guess)
        self.prev_results.append(result)
        printable += self.prettify_result(guess) + '\n' + self.prettify_result(result)
        printable += '\n' + self.print_known_letters()

        if result == len(self.password) * GREEN:
            self.done = True
            printable += '\n\n' + self.print_final()
        return printable

    def give_up(self):
        if len(self.prev_results) < 6:
            return 'Sa pole veel piisavalt pakkumisi teinud, proovin ikka natuke rohkem.'
        self.done = True
        return self.prettify_result(self.password) + '\n' + self.print_final()

    def print_known_letters(self) -> str:
        printable = f"Tundmatu - {', '.join(sorted(self.known_letters['unknown']))}"
        printable += '\n' + f"{self.prettify_result(GREY)} - {', '.join(sorted(self.known_letters['grey']))}"
        printable += '\n' + f"{self.prettify_result(YELLOW)} - {', '.join(sorted(self.known_letters['yellow']))}"
        printable += '\n' + f"{self.prettify_result(GREEN)} - {', '.join(sorted(self.known_letters['green']))}"
        return printable

    def print_greens(self) -> str:
        return '`' + ''.join(self.greens) + '`\n' + self.print_known_letters()

    def print_history(self) -> str:
        printable = ""
        for i in range(len(self.prev_guesses)):
            printable += self.prettify_result(self.prev_guesses[i]) + '\n'
            printable += self.prettify_result(self.prev_results[i]) + '\n'
        if not printable:
            return 'Pole ajalugu, mdia kuvada.'
        return printable.strip()

    def print_final(self) -> str:
        printable = f'Sõnam {len(self.prev_guesses)} pakkumisega'
        for result in self.prev_results:
            printable += '\n' + self.prettify_result(result)
        if 'eesti' in self.lang:
            printable += f'\nhttps://www.eki.ee/dict/ekss/index.cgi?Q={self.password.lower()}&F=M'
        return printable

    def prettify_result(self, string: str) -> str:
        if self.data.pretty_format:
            return string.replace(GREY, self.data.grey2).replace(YELLOW, self.data.yellow2).replace(GREEN, self.data.green2)
        return '`' + string + '`'  # monospace in Discord


if __name__ == '__main__':
    game = SMOrganizer()
    print('Testmäng:')
    game.datas[0] = SMData()
    game.datas[0].pretty_format = False
    # game.datas[0].hard_mode = True
    print(game.new_game(0, 'eesti-5'))
    inner_game = game.games[0]
    while not inner_game.done:
        print(inner_game.guess(input('pakkumine: ')))
