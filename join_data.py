import pandas as pd

answers = pd.read_csv('data/possible_answers.txt').squeeze("columns")
valid_guesses = pd.read_csv('data/orig_valid_gusses.txt').squeeze("columns")

concatenated = pd.concat([answers, valid_guesses], axis=0).sort_values()
concatenated = concatenated.drop_duplicates()
concatenated.to_csv('data/valid_guesses.txt', sep=';', index=False)