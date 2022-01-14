from collections import defaultdict
import random
import wordle_utils


# an object representing what we know about the word
class Knowledge:
    def __init__(self):
        # initial knowledge
        self.all_words = wordle_utils.get_all_words()
        self.all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # acquired knowledge
        self.known_positions = {}
        self.present = set()
        self.absent = set()
        self.known_non_positions = defaultdict(set)

        # derived knowledge
        self.clean_words = self.cleanse(self.all_words)
        self.clean_letter_frequency = defaultdict(int)

    def guessed_letters(self):
        letters = set()
        letters.add(self.present)
        letters.add(self.absent)
        return letters

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

    def run_model(self, model_name):
        match model_name:
            case 'naive':
                return self.make_guess_naive()
            case 'freq':
                return self.make_guess_freq()
            case 'halving':
                return self.make_guess_halving()
        return

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

        return random.choice(last_words)

    # trying to cut the problem area in half
    def make_guess_halving(self):
        test_letters = set()
        test_words = self.clean_words.copy()

        while len(test_words) > 0:
            test_count = len(test_words)
            last_words = test_words.copy()
            letter_freq = self.get_letter_frequency(test_words)
            test_letter = wordle_utils.find_best_divisor(letter_freq, test_letters, test_count)
            if not test_letter:
                break
            test_letters.add(test_letter)
            test_words = self.cleanse(test_words, test_letters)

        return random.choice(last_words)
