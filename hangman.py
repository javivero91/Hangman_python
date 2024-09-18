# Name: José Vivero
# Hangman Game
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
    

# Load the list of words into the variable wordlist so that it can be accessed from anywhere in the program
wordlist = load_words()

# -----------------------------------

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for letter in secret_word:
        if letter in letters_guessed:
            guessed_word = guessed_word + letter
        else:
            guessed_word = guessed_word + '_ '
    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    available_letters = ''.join([letter for letter in alphabet if letter not in letters_guessed])
    return available_letters

def valid_letter(new_letter, letters_guessed):
    '''
    Parameters
    ----------
    new_letter : Input from the user.
    letters_guessed : List of letters guessed so far
        This function takes a user input and tells you if it is valid,
        which means if it is a single letter in the alphabet.

    Returns
    -------
    List [True] or [False, explanation].
    '''
    alphabet = string.ascii_lowercase
    if len(new_letter)>1:
        explanation = 'Enter a single character.'
        return [False, explanation]
    elif new_letter not in alphabet:
        explanation = 'Enter a letter.'
        return [False, explanation]
    elif new_letter in letters_guessed:
        explanation = 'Enter a new letter.'
        return [False, explanation]
    else:
        explanation = 'Valid input'
        return [True, explanation]


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    alphabet = string.ascii_lowercase
    num_guesses = 0
    letters_guessed = []
    print('')
    print('Welcome to the game Hangman!')
    while num_guesses < 6:
        print('I am thinking of a word that has', len(secret_word), 'letters.')
        print(get_guessed_word(secret_word, letters_guessed))
        print('')
        print('Available letters:', get_available_letters(letters_guessed))
        print('Guesses left:', 6-num_guesses)
        print('Warnings left:', 3)
        #The user enters an input
        new_letter = input('Please guess a new letter: ').lower()
        entry = 1
        while entry <= 3:
            #We check the user's input is a letter and that it has not been guessed
            if not valid_letter(new_letter, letters_guessed)[0]:
                print('Warnings left: ' + str(3-entry)+'. ' + valid_letter(new_letter, letters_guessed)[1])
                new_letter = input('Please guess a new letter: ').lower()
                entry = entry + 1
            #In case the input is a letter we store it and check if it is in the secret word 
            else:
                letters_guessed.append(new_letter)
                if new_letter in secret_word:
                    print("That's Correct!:", get_guessed_word(secret_word, letters_guessed))
                elif new_letter in ['a', 'e', 'i', 'o', 'u']:
                    print('The vowel '+new_letter+' is not in the word:', get_guessed_word(secret_word, letters_guessed))
                    num_guesses = num_guesses + 2
                else:
                    print('The consonant '+new_letter+' is not in the word:', get_guessed_word(secret_word, letters_guessed))
                    num_guesses = num_guesses + 1
                break
            #After 3 incorrect entries the user loses a guess
            if entry == 3 and not valid_letter(new_letter, letters_guessed)[0]:
                num_guesses = num_guesses + 1
                print('You lost one guess. Guesses left:', 6-num_guesses)
                break
    
        print('-'*15)
        #Anounce the winner/looser
        if is_word_guessed(secret_word, letters_guessed):
            score = (6-num_guesses)*len(set(secret_word))
            print('Congratulations! Your score is:', score)
            break
        if not is_word_guessed(secret_word, letters_guessed) and num_guesses==6:
            print('Sorry, that was your last guess. The word was', secret_word)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(' ', '')
    alphabet = string.ascii_lowercase
    if len(my_word) != len(other_word):
        return False
    for l1, l2 in zip(my_word, other_word):
        if l1 in alphabet and l1 != l2:
            return False
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    print('Possible word matches are:')
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word, end=' ')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    alphabet = string.ascii_lowercase
    num_guesses = 0
    letters_guessed = []
    print('')
    print('Welcome to the game Hangman!')
    while num_guesses < 6:
        print('I am thinking of a word that has', len(secret_word), 'letters.')
        print(get_guessed_word(secret_word, letters_guessed))
        print('')
        print('Available letters:', get_available_letters(letters_guessed))
        print('Guesses left:', 6-num_guesses)
        print('Warnings left:', 3)
        #The user enters an input
        new_letter = input('Please guess a new letter: ').lower()
        entry = 1
        while entry <= 3:
            #We check the user's input is a letter and that it has not been guessed
            if not valid_letter(new_letter, letters_guessed)[0]:
                if new_letter == '*':
                    show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                    print('')
                    new_letter = input('Please guess a new letter: ').lower()
                else:
                    print('Warnings left: ' + str(3-entry)+'. ' + valid_letter(new_letter, letters_guessed)[1])
                    new_letter = input('Please guess a new letter: ').lower()
                    entry = entry + 1
        
            #In case the input is a letter we store it and check if it is in the secret word 
            else:
                letters_guessed.append(new_letter)
                if new_letter in secret_word:
                    print("That's Correct!:", get_guessed_word(secret_word, letters_guessed))
                elif new_letter in ['a', 'e', 'i', 'o', 'u']:
                    print('The vowel '+new_letter+' is not in the word:', get_guessed_word(secret_word, letters_guessed))
                    num_guesses = num_guesses + 2
                else:
                    print('The consonant '+new_letter+' is not in the word:', get_guessed_word(secret_word, letters_guessed))
                    num_guesses = num_guesses + 1
                break
            #After 3 incorrect entries the user loses a guess
            if entry == 3 and not valid_letter(new_letter, letters_guessed)[0]:
                num_guesses = num_guesses + 1
                print('You lost one guess. Guesses left:', 6-num_guesses)
                break
    
        print('-'*15)
        #Anounce the winner/looser
        if is_word_guessed(secret_word, letters_guessed):
            score = (6-num_guesses)*len(set(secret_word))
            print('Congratulations! Your score is:', score)
            break
        if not is_word_guessed(secret_word, letters_guessed) and num_guesses==6:
            print('Sorry, that was your last guess. The word was', secret_word)
            


# if __name__ == "__main__":
    
#     secret_word = choose_word(wordlist)
#     hangman_with_hints(secret_word)


