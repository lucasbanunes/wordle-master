from colorama import init, Back, Style

class Wordle(object):

    def __init__(self):
        pass
        WRONG = 0
        PRESENT = 1
        PERFECT = 2
        board = list()
        valid_gusses = list()   
    
    def _load_valid_guesses(self):
        """Loads a list with all possible answers"""
        pass

    def _generate_answer(self):
        """Chooses a new answer to be guessed"""
        pass

    def _print_guess(self):
        """Builds a colored string based on the information of each letter"""
    
    def _print_menu(self):
        """Print start menu"""
        pass

    def _is_valid_word(self):
        """Checks if the word is valid"""
        pass

    def new_game(self):
        """Starts a new game"""
        pass

    def guess(self):
        """Recieves a word and returns the result"""
        pass

    def play(self):
        """Starts the game"""
        print('Welcome to Wordle, try me')
        pass