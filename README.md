# Hangman_python
In this repository I keep the code for a hangman game in Python. 
Here are the game rules:
1. The computer selects a word at random from the list of available words.
2. The user is given 6 guesses for the whole game and 3 warnings for each attempt at guessing a letter.
3. The game is interactive; the user inputs their guess letter and either:
   
   a. the user looses a warning if the input is not a letter or if it has already been guessed (the user looses a guess after the three warnings).
   
   b. the computer reveals the letter if it exists in the secret word and no guess is subtracted from the total left at this point.
   
   c. the computer penalizes the user (-2 if the wrong guess is a vowel, -1 otherwise) and updates the number of guesses remaining.
   
   d. the guess is '*', in which case the user is shown all the possible words that can be formed with the information so far. The user is not penalised for this option.
   
5. The game ends when the user constructs the secret word or when there are no more guesses left.
6. If the user wins they get a score which is calculated as follows: Total score = guesses_remaining* number unique letters in secret_word.
    
   
