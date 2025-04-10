
# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:
import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split() 
    # print(" ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    """
    return random.choice(wordlist)



# -----------------------------------
# END OF HELPER CODE
# -----------------------------------


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far
    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    """
    if not secret_word:
        return True
    elif not letters_guessed:
        return False
    for char in secret_word:
        if char not in letters_guessed:
            return False
    return True
    
def get_word_progress(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
    guessed so far
    returns: string, comprised of letters and asterisks (*) that represents
    which letters in secret_word have not been guessed so far
    """
    progress = []
    for char in secret_word:
        if char in letters_guessed:
            progress.append(char)
        else:
            progress.append("*")
    progress = ''.join(progress)
    return progress

def get_available_letters(letters_guessed: list):
    """
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    for item in letters_guessed:
      if item in letters:
          letters = letters.replace(item, '')
    return letters

def score(guess, letters_guessed, secret_word):
    unique_letters = [char for char in letters_guessed if char in secret_word]
    score = (guess + 4*len(unique_letters)) + (3*len(secret_word))                          
    return score



def hangman(secret_word , with_help, item = []):
    """
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.
    Starts up an interactive game of Hangman.
    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses they start with.
    * The user should start with 10 guesses.
    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)
    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.
    * After each guess, you should display to the user the
      partially guessed word so far.
    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.
    Follows the other limitations detailed in the problem write-up.
    """
    letters_guessed = []
    def reveal_letters(secret_word):
      progress = get_word_progress(secret_word, letters_guessed)
      progress = list(progress)
      secret_word = list(secret_word)
      y = len(secret_word)
      y = y - 1
      while True:
          x = random.randint(0, y)
          if progress[x] == "*":
              if secret_word[x] not in item:
                progress[x] = secret_word[x]
                item.append(progress[x])
                break
              else:
                 continue
          else:
              continue
      return progress[x]


    vowels = "aeiou"
    guess = 10


    print("Welcome to Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("------------------------")
    if with_help:
      while guess > 0:
        print(f"You have {guess} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        try:
            letter = input("Please guess a letter: ").lower()
            if len(letter) == 1 and letter in string.ascii_lowercase:
                if letter not in letters_guessed:
                    letters_guessed.append(letter)
                    if letter in secret_word:
                      progress = get_word_progress(secret_word, letters_guessed)
                      print(f"Good guess: {progress}")
                      print("------------------------")
                      if has_player_won(secret_word, letters_guessed):
                          print("Congratulations, you won!")
                          print(f"Your total score for this game is: {score(guess, letters_guessed, secret_word)}")
                          break
                      else:
                          continue
                    else:
                      if letter in vowels:
                        print(f"Oops! That letter is not in my word: {get_word_progress(secret_word, letters_guessed)}")
                        guess -= 2
                      else:  
                        print(f"Oops! That letter is not in my word: {get_word_progress(secret_word, letters_guessed)}")
                        guess -= 1
                else:
                    print(f"Oops! You've already guessed that letter: {get_word_progress(secret_word, letters_guessed)}")
            elif letter == "!" and guess >=3:
                spec = reveal_letters(secret_word)
                guess -= 3
                letters_guessed.append(spec)
                print(f"Letter revealed: {spec}")
                print(f"{get_word_progress(secret_word, letters_guessed)}")
                print("------------------------")
                if has_player_won(secret_word, letters_guessed):
                    print("Congratulations, you won!")
                    print(f"Your total score for this game is: {score(guess, letters_guessed, secret_word)}")
                    break
                else:
                    continue
            elif letter == "!" and guess < 3:
                print(f"Oops! Not enough guesses left: {get_word_progress(secret_word, letters_guessed)}")                
            else:
                raise ValueError
        except ValueError:
            print(f"Oops! That is not a valid letter. Please input a letter from the alphabet: {get_word_progress(secret_word, letters_guessed)}")
        print("------------------------")
      if guess == 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")  
    else:  
      while guess > 0:
        print(f"You have {guess} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        try:
            letter = input("Please guess a letter: ").lower()
            if len(letter) == 1 and letter in string.ascii_lowercase:
                if letter not in letters_guessed:
                    letters_guessed.append(letter)
                    if letter in secret_word:
                      print(f"Good guess: {get_word_progress(secret_word, letters_guessed)}")
                      print("------------------------")
                      if has_player_won(secret_word, letters_guessed):
                          print("Congratulations, you won!")
                          print(f"Your total score for this game is: {score(guess, letters_guessed, secret_word)}")
                          break
                      else:
                          continue
                    else:
                      if letter in vowels:
                        print(f"Oops! That letter is not in my word: {get_word_progress(secret_word, letters_guessed)}")
                        guess -= 2
                      else:  
                        print(f"Oops! That letter is not in my word: {get_word_progress(secret_word, letters_guessed)}")
                        guess -= 1
                else:
                    print(f"Oops! You've already guessed that letter: {get_word_progress(secret_word, letters_guessed)}")
            else:
                raise ValueError
        except ValueError:
            print(f"Oops! That is not a valid letter. Please input a letter from the alphabet: {get_word_progress(secret_word, letters_guessed)}")
        print("------------------------")
      if guess == 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")           
    

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test

if __name__ == "__main__":
    # To test your game, uncomment the following three lines.

    secret_word = choose_word(wordlist)
    with_help = True
    hangman(secret_word, with_help)

    # After you complete with_help functionality, change with_help to True
    # and try entering "!" as a guess!

    ###############

    # SUBMISSION INSTRUCTIONS
    # -----------------------
    # It doesn't matter if the lines above are commented in or not
    # when you submit your pset. However, please run ps2_student_tester.py
    # one more time before submitting to make sure all the tests pass.
  

 