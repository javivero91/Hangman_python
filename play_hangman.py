# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:34:08 2024

@author: javiv
"""

from hangman import *
import streamlit as st
import string
import random

wordlist = load_words()

# Version 1

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

# Get the secret word
secret_word = st.session_state.secret_word

st.title('Hangman Game')

if st.session_state.game_over:
    st.write("Game Over! The word was:", secret_word)
    if st.button("Play Again"):
        # Reset session state to start a new game
        st.session_state.secret_word = random.choice(wordlist)
        st.session_state.letters_guessed = []
        st.session_state.num_guesses = 0
        st.session_state.warnings_left = 3
        st.session_state.game_over = False
else:
    # Show game status
    st.write(f'I am thinking of a word that has {len(secret_word)} letters.')
    st.write('Guessed so far:', get_guessed_word(secret_word, st.session_state.letters_guessed))
    st.write('Available letters:', get_available_letters(st.session_state.letters_guessed))
    st.write('Guesses left:', 6 - st.session_state.num_guesses)
    st.write('Warnings left:', st.session_state.warnings_left)

    # Input for the user to guess a new letter
    new_letter = st.text_input('Please guess a new letter:').lower()

    if new_letter:
        valid, message = valid_letter(new_letter, st.session_state.letters_guessed)

        if not valid:
            if new_letter == '*':
                show_possible_matches(get_guessed_word(secret_word, st.session_state.letters_guessed))
            else:
                st.session_state.warnings_left -= 1
                st.write(f"Warning: {message}. Warnings left: {st.session_state.warnings_left}")

            if st.session_state.warnings_left == 0:
                st.session_state.num_guesses += 1
                st.write('You lost one guess due to warnings. Guesses left:', 6 - st.session_state.num_guesses)
        else:
            st.session_state.letters_guessed.append(new_letter)

            if new_letter in secret_word:
                st.write("Correct guess!")
            else:
                if new_letter in 'aeiou':
                    st.session_state.num_guesses += 2
                else:
                    st.session_state.num_guesses += 1
                st.write(f"Incorrect guess. The letter '{new_letter}' is not in the word.")

        # Check if the user has won or lost
        if is_word_guessed(secret_word, st.session_state.letters_guessed):
            st.session_state.game_over = True
            score = (6 - st.session_state.num_guesses) * len(set(secret_word))
            st.write('Congratulations! You won! Your score is:', score)
        elif st.session_state.num_guesses >= 6:
            st.session_state.game_over = True
            st.write(f"Sorry, you're out of guesses. The word was '{secret_word}'.")

    # Reset functionality at any point
    if st.button("Reset Game"):
        st.session_state.secret_word = random.choice(['apple', 'banana', 'grape', 'orange', 'peach'])
        st.session_state.letters_guessed = []
        st.session_state.num_guesses = 0
        st.session_state.warnings_left = 3
        st.session_state.game_over = False
