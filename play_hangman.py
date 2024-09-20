import streamlit as st
import random
from hangman import *

# List of all possible words
wordlist = load_words()

# Initialize session state variables
if 'secret_word' not in st.session_state:
    st.session_state.secret_word = random.choice(wordlist)

if 'letters_guessed' not in st.session_state:
    st.session_state.letters_guessed = []

if 'num_guesses' not in st.session_state:
    st.session_state.num_guesses = 0

if 'warnings_left' not in st.session_state:
    st.session_state.warnings_left = 3

if 'game_over' not in st.session_state:
    st.session_state.game_over = False

if 'game_won' not in st.session_state:
    st.session_state.game_won = False

if 'display' not in st.session_state:
    st.session_state.display = ''


# Get the secret word
secret_word = st.session_state.secret_word

#Title of game
st.title('Hangman Game')

if st.session_state.game_over:
    if st.session_state.game_won:
        score = (6 - st.session_state.num_guesses) * len(set(secret_word))
        st.write('Congratulations! You won! The word is', secret_word + '.','Your score is:', score)
    else:
        st.write("Game Over! The word was:", secret_word)

    if st.button("Play Again"):
        # Reset session state to start a new game
        st.session_state.secret_word = random.choice(wordlist)
        st.session_state.letters_guessed = []
        st.session_state.num_guesses = 0
        st.session_state.warnings_left = 3
        st.session_state.game_over = False
        st.session_state.game_won = False
        st.session_state.display = ''
else:
    # Show game status
    st.write(f'I am thinking of a word that has {len(secret_word)} letters.')
    st.write('Guessed so far:', get_guessed_word(secret_word, st.session_state.letters_guessed))
    st.write('Available letters:', ' '.join(get_available_letters(st.session_state.letters_guessed)))
    st.write('Guesses left:', 6 - st.session_state.num_guesses)
    st.write('Warnings left:', st.session_state.warnings_left)


    #Callback function: Used to update the game status using the user input down below 
    def handle_enter():
        new_letter = st.session_state.input_letter # Use the key to get the value for text input
        new_letter = new_letter.lower()
        if new_letter:
            valid, message = valid_letter(new_letter, st.session_state.letters_guessed)

            if not valid:
                if new_letter == '*':
                    st.session_state.display = "Click the 'Hint' button on the left side."
                    #show_possible_matches(get_guessed_word(secret_word, st.session_state.letters_guessed))
                else:
                    st.session_state.warnings_left -= 1
                    st.session_state.display = f"Warning: {message}. Warnings left: {st.session_state.warnings_left}"

                if st.session_state.warnings_left == 0:
                    st.session_state.num_guesses += 1
                    st.session_state.display = 'You lost one guess due to warnings. Guesses left:', 6 - st.session_state.num_guesses
            else:
                st.session_state.letters_guessed.append(new_letter)
                st.session_state.warnings_left = 3
                st.session_state.display = ''

                if new_letter in secret_word:
                    st.session_state.display = "Correct guess!"
                else:
                    if new_letter in 'aeiou':
                        st.session_state.num_guesses += 2
                        st.session_state.display = f"Incorrect guess. The letter '{new_letter}' is not in the word."
                    else:
                        st.session_state.num_guesses += 1
                        st.session_state.display = f"Incorrect guess. The letter '{new_letter}' is not in the word."

            # Check if the user has won or lost
            if is_word_guessed(secret_word, st.session_state.letters_guessed):
                st.session_state.game_over = True
                st.session_state.game_won = True
                
            elif st.session_state.num_guesses >= 6:
                st.session_state.game_over = True

    # User input that will be passed to the callback function
    new_letter = st.text_input('Write a letter', on_change = handle_enter, key='input_letter')
    
    st.write(st.session_state.display)

    # Side bar:
    st.sidebar.header('Options:')

    rules = st.sidebar.button('Game rules')
    # Option to show rules
    if rules:
        hide_rules = st.sidebar.button('Hide rules')
        st.sidebar.write('''These are the game rules:\n
1. The computer selects a word at random from the list of available words.
2. The user is given 6 guesses for the whole game and 3 warnings for each attempt at guessing a letter.
3. The game is interactive; the user inputs their guess letter and either:\n
    a. the user looses a warning if the input is not a letter or if it has already been guessed (the user looses a guess after three warnings).\n
    b. the computer reveals the letter if it exists in the secret word and no guess is subtracted from the total left at this point.\n
    c. the computer penalizes the user (-2 if the wrong guess is a vowel, -1 otherwise) and updates the number of guesses remaining.\n
    d. the user click the 'Show hint' button to see all the possible words that can be formed with the information so far. The user is not penalised for this option.
4. The game ends when the user constructs the secret word or when there are no more guesses left.
5. If the user wins they get a score which is calculated as follows: Total score = (guesses_remaining) x (number unique letters in secret_word).                   ''', 
                         key = 'rules')
        
        # Option to hide rules
        if hide_rules:
            st.session_state.rules = ''

    hint = st.sidebar.button('Show hint')
    # Option to show hints
    if hint:
        hide_hint = st.sidebar.button('Hide hint')
        st.sidebar.write('These are all the words that can be formed so far:', key = 'message')
        st.sidebar.write(', '.join(show_possible_matches(get_guessed_word(secret_word, st.session_state.letters_guessed))), key = 'hints')
        # Option to hide hints
        if hide_hint:
            st.session_state.message = ''
            st.session_state.hints = ''


    if st.button('Reset'):
        st.session_state.secret_word = random.choice(wordlist)
        st.session_state.letters_guessed = []
        st.session_state.num_guesses = 0
        st.session_state.warnings_left = 3
        st.session_state.game_over = False
        st.session_state.game_won = False
        st.session_state.display = ''
