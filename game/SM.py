"""SõnaMäng game logic."""
all_letters = 'QWERTYUIOPÜÕASDFGHJKLÖÄZXCVBNMŠŽ'


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
    game = SMGame('kruus')
    while not game.done:
        game.guess(input('pakkumine: '))
