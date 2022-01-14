from collections import defaultdict
import random
import wordle_utils

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

# utility function to get max


# an object representing what we know about the word
class Knowledge:
    def __init__(self):
        # initial knowledge
        self.all_words = get_all_words()
        self.all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # acquired knowledge
        self.known_positions = {}
        self.present = set()
        self.absent = set()
        self.known_non_positions = defaultdict(set)

        # derived knowledge
        self.clean_words = self.cleanse(self.all_words)
        self.clean_letter_frequency = defaultdict(int)

    def add_knowledge(self, _guess, _results):
        for i in range(0, 5):
            if _results[i] == 'Y':
                self.known_positions[i] = _guess[i]
                self.present.add(_guess[i])
            elif _results[i] == 'S':
                self.present.add(_guess[i])
                self.known_non_positions[_guess[i]].add(i)
            else:
                self.absent.add(_guess[i])
                self.known_non_positions[_guess[i]].add(i)
        print(self.known_non_positions)
        self.clean_words = self.cleanse(self.clean_words, self.present)

    def cleanse(self, dirty_words, must_include=None):
        cleaned_words = []
        for word in dirty_words:
            add_word = True
            for place in self.known_positions:
                if word[place] != self.known_positions[place]:
                    add_word = False
                    break
            if not add_word:
                continue
            for place, letter in enumerate(word):
                if letter in self.absent:
                    add_word = False
                    break
                if place in self.known_non_positions[letter]:
                    add_word = False
                    break
            if must_include:
                for letter in must_include:
                    if letter not in word:
                        add_word = False
                        break
            if add_word:
                cleaned_words.append(word)
        return cleaned_words

    def get_letter_frequency(self, word_list):
        freq = defaultdict(int)
        for word in word_list:
            for letter in self.all_letters:
                if letter in word:
                    freq[letter] += 1
        return freq

    def make_guess_naive(self):
        return random.choice(self.clean_words)

    # we'll make guesses based on the most frequent available letters
    def make_guess_freq(self):
        test_letters = set()
        test_words = self.clean_words.copy()

        while len(test_words) > 0:
            last_words = test_words.copy()
            letter_freq = self.get_letter_frequency(test_words)
            test_letter = wordle_utils.find_max_freq(letter_freq, test_letters)
            if not test_letter:
                break
            test_letters.add(test_letter)
            test_words = self.cleanse(test_words, test_letters)
            print(test_words)

        return random.choice(last_words)


# initial conditions
guess, response = None, None
knowledge = Knowledge()

# main guessing loop
while number_of_guesses > 0:
    guess = knowledge.make_guess_freq()
    export_guess(guess)
    response = import_response()
    knowledge.add_knowledge(guess, response)
    number_of_guesses -= 1
