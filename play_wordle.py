from wordle_game import Wordle

game = Wordle('data/possible_answers.txt', 'data/valid_guesses.txt', debug=True)
game.play()