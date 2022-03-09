"""SõnaMäng game logic."""
import random

all_letters = 'QWERTYUIOPÜÕASDFGHJKLÖÄZXCVBNMŠŽ'


class SMOrganizer:
    """Class that will create games of SM."""

    def __init__(self):
        self.games = {}
        self.word_lists = {}
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
        with open('../words/index.txt', encoding='utf-8') as file:
            for line in file:
                lists.append(line.strip())
        for word_list in lists:
            file_name, list_name = word_list.split(',')
            words = []
            with open('../words/' + file_name, encoding='utf-8') as file:
                for line in file:
                    words.append(line.strip())
            word_lists[list_name] = words
        self.word_lists = word_lists

    def get_random_word(self, list_name) -> tuple:
        """
        Get a random word from a given word list.
        If no such list exists, fall back to something else.

        :param list_name: word list to look for
        :return: a tuple of list name and a word from that list
        """
        if list_name in self.word_lists:
            return list_name, random.choice(self.word_lists[list_name])
        return 'backup', 'puudu'

    def new_game(self, key, list_name):
        """
        Create a new game with a random word.
        :param key: Key used for accessing the game
        :param list_name: word list to use for game
        """
        list_name, word = self.get_random_word(list_name)
        self.games[key] = SMGame(word)


class SMGame:
    """Class for one game of SM."""

    def __init__(self, password: str):
        self.password = password.upper()
        self.prev_guesses = []
        self.prev_results = []
        self.done = False
        self.grey, self.yellow, self.green = ".", "/", "*"
        self.known_letters = {'unknown': set(all_letters),
                              'grey': set(),
                              'yellow': set(),
                              'green': set()}

    def guess(self, guess: str):
        if len(guess) != len(self.password):
            print('Vale pakkumise pikkus!')
        if not guess.isalpha():
            print('Pakkumine peab koosnema vaid tähtedest!')

        guess = guess.upper()
        letters = list(self.password)
        result = [''] * len(guess)

        for i, letter in enumerate(guess):
            if self.password[i] == letter:  # right letter, right place
                result[i] = self.green
                letters.remove(letter)
                self.known_letters['unknown'].discard(letter)
                self.known_letters['yellow'].discard(letter)
                self.known_letters['green'].add(letter)

        for i, letter in enumerate(guess):
            # mark everything else as wrong place or not in the puzzle
            if result[i]:
                continue
            if letter in letters:  # right letter, wrong place
                result[i] = self.yellow
                letters.remove(letter)
                if letter not in self.known_letters['green']:
                    self.known_letters['unknown'].discard(letter)
                    self.known_letters['yellow'].add(letter)
            else:  # wrong letter
                result[i] = self.grey
                self.known_letters['unknown'].discard(letter)
                self.known_letters['grey'].add(letter)

        result = ''.join(result)
        self.prev_guesses.append(guess)
        self.prev_results.append(result)
        print(guess)
        print(result)
        self.print_known_letters()

        if result == 5 * self.green:
            self.done = True
            self.print_final()

    def print_known_letters(self):
        print(f"Tundmatu - {', '.join(sorted(self.known_letters['unknown']))}")
        print(f"{self.grey} - {', '.join(sorted(self.known_letters['grey']))}")
        print(f"{self.yellow} - {', '.join(sorted(self.known_letters['yellow']))}")
        print(f"{self.green} - {', '.join(sorted(self.known_letters['green']))}")

    def print_final(self):
        print(f'Sõnam {len(self.prev_guesses)}/6')
        for result in self.prev_results:
            print(result)


if __name__ == '__main__':
    game = SMOrganizer()
    game.new_game(0, 'testlist')
    inner_game = game.games[0]
    while not inner_game.done:
        inner_game.guess(input('pakkumine: '))
