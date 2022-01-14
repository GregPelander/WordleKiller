import random
from knowledge import Knowledge
import wordle_utils


# i/o
def export_guess(guess):
    print(f'Guess: {guess}')


def import_response():
    response = input('Enter the results as a string.\n:'
                     'Y = yes; N = no; S = somewhere;\n'
                     'E.x., "YNNSY"\n'
                     'Results: ')
    return response


class Harness:
    def __init__(self):
        self.number_of_runs = 10000
        self.test_models = ['naive', 'freq', 'halving']
        self.words = wordle_utils.get_all_words()
        self.averages = {}
        self.word = random.choice(self.words)
        for model in self.test_models:
            self.averages[model] = 0.0

    def guess(self, guess):
        response = ''
        for place, letter in enumerate(guess):
            if self.word[place] == letter:
                response += 'Y'
            elif letter in self.word:
                response += 'S'
            else:
                response += 'N'
        return response

    def run_tests(self):
        run_number = 1
        while run_number <= self.number_of_runs:
            print(f'Run {run_number} out of {self.number_of_runs}')
            for model in self.test_models:
                guesses = self.run_guesses(model, True)
                avg = (self.averages[model] * (run_number - 1) + guesses) / run_number
                self.averages[model] = avg
            run_number += 1
            self.word = random.choice(self.words)

        print('Results:\n')
        for model in self.test_models:
            print(f'{model}: {self.averages[model]}')

    def run_guesses(self, model_type, is_test=False):
        # naive, freq, halving
        # initial conditions
        guess, response = None, None
        knowledge = Knowledge()
        guess_num = 1

        # main guessing loop
        while response != 'YYYYY':
            guess = knowledge.run_model(model_type)
            if is_test:
                response = self.guess(guess)
            else:
                export_guess(guess)
                response = import_response()
            if response == 'YYYYY':
                break
            knowledge.add_knowledge(guess, response)
            guess_num += 1
        return guess_num


harness = Harness()
harness.run_tests()
