"""SõnaMäng game logic."""
import random

ALL_LETTERS = 'QWERTYUIOPÜÕASDFGHJKLÖÄZXCVBNMŠŽ'

# console markings
GREY, YELLOW, GREEN = ".", "/", "*"
# emoji markings
GREY2, YELLOW2, GREEN2 = "\U00002B1B", "\U0001F7E8", "\U0001F7E9"


class SMOrganizer:
    """Class that will create games of SM."""

    def __init__(self):
        self.games: dict[int, SMGame] = {}
        self.word_lists: dict = {}
        self.unused_letters: dict = {}
        self.read_word_lists()

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
        with open('../words/index.txt', encoding='utf-8') as file:
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
        if list_name in self.word_lists:
            return list_name, random.choice(self.word_lists[list_name])
        return 'eesti-5', random.choice(self.word_lists['eesti-5'])

    def new_game(self, key, list_name, pretty_format=True):
        """
        Create a new game with a random word.
        :param key: Key used for accessing the game
        :param list_name: word list to use for game
        :param pretty_format: use pretty characters for the game (may not work with all fonts)
        """
        list_name, word = self.get_random_word(list_name)
        self.games[key] = SMGame(word,
                                 self.word_lists[list_name],
                                 self.unused_letters[list_name],
                                 pretty_format)
        return 'Uus mäng on alanud. Sõnastik: ' + list_name


class SMGame:
    """Class for one game of SM."""

    def __init__(self, password: str, dictionary: set, unused_letters: set, pretty_format=True):
        self.password = password.upper()
        self.dictionary = dictionary
        self.known_letters = {'unknown': set(ALL_LETTERS).difference(unused_letters),
                              'grey': set(),
                              'yellow': set(),
                              'green': set()}
        self.pretty = pretty_format
        self.prev_guesses = []
        self.prev_results = []
        self.done = False

    def guess(self, guess: str) -> str:
        if self.done:
            return 'Mäng on juba läbi!'
        if len(guess) != len(self.password):
            return 'Vale pakkumise pikkus!'
        if not guess.isalpha():
            return 'Pakkumine peab koosnema vaid tähtedest!'

        guess = guess.upper()
        if guess not in self.dictionary:
            return 'Pakkumine ei esine sõnastikus!'

        printable = ''
        letters = list(self.password)
        result = [''] * len(guess)

        for i, letter in enumerate(guess):
            if self.password[i] == letter:  # right letter, right place
                result[i] = GREEN
                letters.remove(letter)
                self.known_letters['unknown'].discard(letter)
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
                    self.known_letters['yellow'].add(letter)
            else:  # wrong letter
                result[i] = GREY
                self.known_letters['unknown'].discard(letter)
                self.known_letters['grey'].add(letter)

        result = ''.join(result)
        self.prev_guesses.append(guess)
        self.prev_results.append(result)
        printable += guess + '\n' + self.prettify_result(result)
        printable += '\n' + self.prettify_result(self.print_known_letters())

        if result == 5 * GREEN:
            self.done = True
            printable += '\n\n' + self.print_final()
        return printable

    def print_known_letters(self) -> str:
        printable = f"Tundmatu - {', '.join(sorted(self.known_letters['unknown']))}"
        printable += '\n' + f"{GREY} - {', '.join(sorted(self.known_letters['grey']))}"
        printable += '\n' + f"{YELLOW} - {', '.join(sorted(self.known_letters['yellow']))}"
        printable += '\n' + f"{GREEN} - {', '.join(sorted(self.known_letters['green']))}"
        return printable

    def print_final(self) -> str:
        printable = f'Sõnam {len(self.prev_guesses)} pakkumisega'
        for result in self.prev_results:
            printable += '\n' + self.prettify_result(result)
        return printable

    def prettify_result(self, string: str) -> str:
        if self.pretty:
            return string.replace(GREY, GREY2).replace(YELLOW, YELLOW2).replace(GREEN, GREEN2)
        return string


if __name__ == '__main__':
    game = SMOrganizer()
    print('Testmäng:')
    print(game.new_game(0, 'eesti-5', pretty_format=False))
    inner_game = game.games[0]
    while not inner_game.done:
        print(inner_game.guess(input('pakkumine: ')))
