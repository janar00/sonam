"""Tools for analyzing/generating word lists."""

"""
eki lehelt leitud sõnaloendid:

https://www.eki.ee/tarkvara/wordlist/

lemmad
    kokkukuuluvate sõnavormide hulk?
    koostatud sõnastike alusel,
    sisse juhtunud kaheldavad algvormid + fraasid jms
    104 000 rida
lemmad2013
    uuem versioon eelmisest
    178 000 rida
    esinevad tähed:
        - 012358 ABCDEFGHIJKLMNOPQRSTUVWXYZ ÀÄÈÉÊÕÖÜŠŽ ̀ ́α
    eemaldasin:
        - (enamus neist sõnadest näis esinevat ka ilma sidekriipsuta)
        numbrid, CQWXYZ, ÀÈÉÊŠŽ ̀ ́α (iga üks neist esines väga vähe)
    pikkustest jätsin alles:
        4-18 (sest seal on üle tuhande sõna)
soned2013
    eri vormis sõnad
    üsna üksikasjalik
    taga kirjas mitu korda see esineb vist kuskil?
    2 000 000 rida
soned2013_top1000
    eelmisest ainult popimad 1000
    1 000 rida
vormid
    korpuse alusel
    mõned eri vormid
    liitsõna piirid "|" märgiga
    198 000 rida
"""

all_letters = 'QWERTYUIOPÜÕASDFGHJKLÖÄZXCVBNMŠŽ'


def read_in_wordlist(path: str) -> set:
    """Read in a wordlist from a file into a set."""
    words = set()
    with open(path, encoding='utf-8') as file:
        for line in file:
            words.add(line.strip().upper())
    words.discard('')  # an empty string seems to make it into the set
    return words


def find_unique_letters(words: set):
    """Find every unique character in wordlist."""
    letters = set()
    for word in words:
        letters.update(set(word))
    print(sorted(letters))


def find_all_unused_letters():
    """Use index.txt to find unused letters for every wordlist."""
    with open('index.txt', encoding='utf-8') as file:
        if file.readline() != 'file_name,unused_letters,list_name\n':
            raise AssertionError('vale faili index.txt esimene rida')
        for line in file:
            path, _, name = line.split(',')
            print('\n' + name.strip())
            find_unused_letters(read_in_wordlist(path))


def find_unused_letters(words: set):
    """Find which letters are unused compared to all_letters."""
    letters = set(all_letters)
    for word in words:
        letters = letters.difference(set(word))
    print(''.join(sorted(letters)))


def find_letter_counts(words: set):
    """For every unique character find how many words it appears in."""
    letters = {}
    for word in words:
        for letter in set(word):
            letters[letter] = letters.get(letter, 0) + 1
    for key in sorted(letters.keys()):
        print(key, letters[key])


def find_word_lengths(words: set):
    """Find how many times each length of word appears in the list."""
    lengths = {}
    for word in words:
        length = len(word)
        lengths[length] = lengths.get(length, 0) + 1
    for key in sorted(lengths.keys()):
        print(key, lengths[key])


def filter_wordlist_by_character(words: set, characters_to_remove: set) -> set:
    """Remove words with unwanted characters."""
    found = set()
    for word in words:
        if set(word).intersection(characters_to_remove):
            found.add(word)
    return words.difference(found)


def filter_wordlist_by_length(words: set, lengths: set) -> dict:
    """Filter wordlist into smaller lists by word length, keeping only allowed lengths."""
    lists = {}
    for word in words:
        length = len(word)
        if length in lengths:
            lists.setdefault(length, set()).add(word)
    return lists


def write_wordlist_to_file(words: set, path: str):
    """Take a given wordlist and write it to a file."""
    with open(path, 'w', encoding='utf-8') as file:
        for line in words:
            file.write(line + '\n')


if __name__ == '__main__':
    wordlist = read_in_wordlist('lemmad2013.txt')
    # print('Letter counts:')
    # find_letter_counts(wordlist)
    wordlist = filter_wordlist_by_character(wordlist, set('-012358CQWXYZÀÈÉỀ́Α'))
    # print('\nWord lengths:')
    # find_word_lengths(wordlist)
    for key, value in filter_wordlist_by_length(wordlist, set(range(4, 19))).items():
        write_wordlist_to_file(value, 'lemmad-' + str(key) + '.txt')

