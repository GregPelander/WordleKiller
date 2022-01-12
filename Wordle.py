from collections import defaultdict
import random

# config
number_of_guesses = 6
word_length = 5


# an object representing what we know about the word
class Knowledge:
    def __init__(self, _guess, results):
        self.known = {}
        self.present = set()
        self.absent = set()
        for i in range(0, 5):
            if results[i] == 'Y':
                self.known[i] = _guess[i]
                self.present.add(_guess[i])
            elif results[i] == 'S':
                self.present.add(_guess[i])
            else:
                self.absent.add(_guess[i])


# produce analysis of words
def analyze(word_list):
    pass


# clean up word list from results
def clean_words(unclean_words, _feedback):
    word_list = []
    for word in unclean_words:
        add_word = True
        for place in _feedback.known:
            if word[place] != _feedback.known[place]:
                add_word = False
        for letter in _feedback.present:
            if letter not in word:
                add_word = False
        for letter in _feedback.absent:
            if letter in word:
                add_word = False
        if add_word:
            word_list.append(word)
    return word_list


# turn our information into a guess
def make_guess(unclean_words, _feedback):
    # if we have previous guesses, we should clean up the word list
    if not _feedback:
        word_list = unclean_words
    else:
        word_list = clean_words(unclean_words, _feedback)

    _guess = random.choice(word_list)

    return word_list, _guess


# initial conditions
guess, response, feedback = None, None, None

# get initial word list
words = []
f = open('word-list.txt')
for line in f:
    words.append(line.strip())
f.close()

# main guessing loop
while number_of_guesses > 0:
    if response:
        feedback = Knowledge(guess, response)

    words, guess = make_guess(words, feedback)
    print(f"Guess: {guess}")

    response = input("Enter the results as a string.\n:"
                     "Y = yes; N = no; S = somewhere\n"
                     "E.x., 'YNNSY'")
    number_of_guesses -= 1
