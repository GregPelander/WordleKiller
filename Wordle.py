from collections import defaultdict
import random

# config
number_of_guesses = 6
word_length = 5


# i/o
def export_guess(_guess):
    print(f"Guess: {_guess}")


def import_response():
    _response = input("Enter the results as a string.\n:"
                      "Y = yes; N = no; S = somewhere;\n"
                      "E.x., 'YNNSY'\n"
                      "Results: ")
    return _response


# get initial word list
def get_all_words():
    _words = []
    f = open('word-list.txt')
    for line in f:
        _words.append(line.strip())
    f.close()
    return _words


# an object representing what we know about the word
class Knowledge:
    def __init__(self):
        # initial knowledge
        self.all_words = get_all_words()
        self.all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # acquired knowledge
        self.known = {}
        self.present = set()
        self.absent = set()

        # external

        # derived knowledge
        self.clean_words = self.all_words.copy()
        self.letter_frequency = defaultdict(int)

    def add_knowledge(self, _guess, _results):
        for i in range(0, 5):
            if _results[i] == 'Y':
                self.known[i] = _guess[i]
                self.present.add(_guess[i])
            elif _results[i] == 'S':
                self.present.add(_guess[i])
            else:
                self.absent.add(_guess[i])
        self.cleanse()

    def cleanse(self):
        word_list = []
        for word in self.clean_words:
            add_word = True
            for place in self.known:
                if word[place] != self.known[place]:
                    add_word = False
                    break
            if not add_word:
                continue
            for letter in word:
                if letter in self.absent:
                    add_word = False
                    break
            if add_word:
                word_list.append(word)
        self.clean_words = word_list.copy()

    def get_letter_frequency(self):
        for word in self.clean_words:
            for letter in self.all_letters:
                if letter in word:
                    self.letter_frequency[letter] += 1

    def make_guess_naive(self):
        self.get_letter_frequency()
        print(self.letter_frequency)
        return random.choice(self.clean_words)


# initial conditions
guess, response = None, None
knowledge = Knowledge()

# main guessing loop
while number_of_guesses > 0:
    guess = knowledge.make_guess_naive()
    export_guess(guess)
    response = import_response()
    knowledge.add_knowledge(guess, response)
    number_of_guesses -= 1
