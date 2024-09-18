# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:34:08 2024

@author: javiv
"""

from hangman import *

if __name__ == "__main__":
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)