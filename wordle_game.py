from collections import OrderedDict

import numpy as np
import pandas as pd
from colorama import init, Back, Style, Fore
from termcolor import colored

WORD_SIZE = 5

class Wordle(object):

    def __init__(self, answers_filename: str, valid_filename: str, debug: bool):
        init()
        self.WRONG = 0
        self.PRESENT = 1
        self.PERFECT = 2
        self.COLOR_MAP = np.array([Back.BLACK, Back.YELLOW, Back.GREEN])
        self.N_TRIES = 6
        self.GAME_RUNNING = 0
        self.GAME_WIN = 1
        self.GAME_LOSS = 2
        self.board = list()
        self.valid_guesses = pd.read_csv(valid_filename).squeeze("columns")
        self.answers_filename = answers_filename
        self.debug = debug

    def _generate_answer(self):
        """Chooses a new answer to be guessed"""
        possible_answers = pd.read_csv(self.answers_filename).squeeze("columns")
        ans_idx = np.random.choice(len(possible_answers), 1)[0]
        self.ans = np.array(list(possible_answers[ans_idx]))
        self.ans_counts = np.array(self._get_char_count(self.ans))
        self.ans_sort = np.argsort(self.ans)
        return self.ans, self.ans_counts

    def _get_char_count(self, word):
        word = list(word)
        counts = [word.count(char) for char in word]
        return counts

    def _print_guess(self, guess, guess_eval):
        """Builds a colored string based on the information of each letter"""
        guess_print = list()
        for char, eval in zip(guess, guess_eval):
            if eval == self.WRONG:
                guess_print.append(self.COLOR_MAP[eval] + char + Style.RESET_ALL)
            else:
                guess_print.append(self.COLOR_MAP[eval] + Fore.BLACK + char + Style.RESET_ALL)
        guess_print = ' '.join(guess_print)
        return guess_print
    
    def _print_board(self):
        """Prints the board"""
        print('----------------------------------------')
        for board_word  in self.board:
            print(board_word)
        print('----------------------------------------')

    def _is_valid_guess(self, guess: str):
        """Checks if the guess is valid"""
        if len(guess) != WORD_SIZE:
            print('The word must have 5 letters.')
            return 1
        elif not (self.valid_guesses == guess).any():
            print(f'{guess.capitalize()} is not a valid guess.')
            return 2
        else:
            return 0
    
    def _evaluate_guess(self, guess):
        """Evaluates each letter of a guess and inserts it to the board"""
        guess = np.array(list(guess))
        guess_counts = np.array(self._get_char_count(guess))
        guess_eval = np.full(len(guess), -1, dtype=np.int8)
        
        perfect_match = (guess == self.ans)
        guess_eval[perfect_match] = self.PERFECT
        guess_counts -= perfect_match.astype(int)

        are_in = np.isin(guess, self.ans)
        guess_eval[np.logical_not(are_in)] = self.WRONG
        
        is_present = np.logical_and(guess_eval == -1, guess_counts > 0)
        guess_eval[is_present] = self.PRESENT

        guess_eval[guess_eval == -1] = self.WRONG

        return guess, guess_eval
    
    def _update_game(self, guess):

        if self._is_valid_guess(guess) == 0:
            guess, guess_eval = self._evaluate_guess(guess)
            guess_print = self._print_guess(guess, guess_eval)
            self.board.append(guess_print)
            if len(self.board) >= self.N_TRIES:
                return self.GAME_LOSS
            elif np.all(guess_eval == self.PERFECT):
                return self.GAME_WIN
        
        return self.GAME_RUNNING
        

    def play(self):
        """Starts the game"""
        status = self.GAME_RUNNING
        print('Welcome to Wordle, try me')
        self._generate_answer()
        if self.debug:
            print(f'The answer is {self.ans}')
        while status == self.GAME_RUNNING:
            self._print_board()
            print('Type a 5 letter word')
            guess = input('Type a word: ')
            status = self._update_game(guess)
        
        self._print_board()
        if status == self.GAME_WIN:
            print('You won congrats')
        elif status == self.GAME_LOSS:
            print(f'You lost. The answer was {"".join(self.ans).capitalize()}. Try again')
        else:
            raise RuntimeError(f'_update_game returned {status}')
        