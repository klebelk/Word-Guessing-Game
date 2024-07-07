import random
from collections import Counter

number_of_try = 0
max_try = 5
guess_check = []
max_word_length = 5
min_word_length = 3
wordlist = []

colors = {
    "RED" : "\033[91m",
    "GREEN" : "\033[92m",
    "YELLOW" : "\033[93m",
    "RESET" : "\033[0m"
}

def text_to_list(text_path):
    result = []
    with open(text_path, 'r') as f:
        for line in f:
            word = line.strip('\n').upper()
            result.append(word)
    return result

def print_game(word, guess, guess_check, number_of_try):
    # print(guess_check)
    for i,  letter in enumerate(guess):
        if number_of_try == 0:
            if i != len(word) - 1:
                print('_', end=' | ')
            else: 
                print('_')
        elif 0 < number_of_try < max_try:
            if i != len(word) - 1:
                if guess_check[i] == True:
                    print(colors["GREEN"], letter, colors["RESET"], end=' | ')
                elif guess_check[i] == "Tralse":\
                    print(colors["YELLOW"], letter, colors["RESET"], end=' | ')
                else:
                    print(colors["RED"], letter, colors["RESET"], end=' | ')
            else:
                if guess_check[i] == True:
                    print(colors["GREEN"], letter, colors["RESET"], end='\n')
                elif guess_check[i] == "Tralse":
                    print(colors["YELLOW"], letter, colors["RESET"], end='\n')
                else:
                    print(colors["RED"], letter, colors["RESET"], end='\n')
        
def word_random(wordlist):
    while True:
        word = random.choice(wordlist).upper()
        if min_word_length <len(word) <= max_word_length:
            break
    return word

def check_common_letters(word, guess):
    guess_check = []
    common_letter = {}
    letters_word = Counter(word)
    letters_guess = Counter(guess)

    common_counter = letters_guess & letters_word

    for letter, count in common_counter.items():
        common_letter.update({letter: count})

    for i, letter in enumerate(guess):
        if letter ==  word[i]:
            guess_check.append(True)
            common_letter[letter] -= 1
        else:
            guess_check.append(False)


    for i, letter in enumerate(guess):
        if guess_check[i] == False and letter in word and common_letter[letter] >= 1:
            guess_check[i] = "Tralse"
            common_letter[letter] -= 1

    return guess_check

def main():
    text_path = "wordlist\english_words.txt"
    wordlist = text_to_list(text_path)
    guess_check = []
    number_of_try = 0
    guess = ""
    chances = 5
    while True:
        if len(set(guess_check)) == 0:
            print("Check")
            word = word_random(wordlist)
            guess = word
            print_game(word, guess, guess_check, number_of_try)
        elif len(set(guess_check)) == 1 and guess_check[0] == True :
            print(f"{colors["GREEN"]}You win!{colors["RESET"]}")
            try_again = input("Press Enter to Try again (q to quit).")
            if try_again != "" and "q":
                break
            word = word_random(wordlist)    
            print_game(word, word, guess_check, 0)
        elif number_of_try == max_try:
            guess_check = [True]
            guess_check *= len(word)
            print(f"{colors['RED']}You lose!{colors['RESET']}")
            print("The Correct Word")
            print_game(word, word, guess_check, 1)
            try_again = input("Press Enter to Try again (q to quit).")
            if try_again != "" and "q":
                break
            print_game(word, word, guess_check, 0)
        else:   
            print_game(word, guess, guess_check, number_of_try)
        guess_check = []
        while True:
            guess = input(f"Guess the word({len(word)}):").upper()
            if len(guess) != len(word):
              print(f"{colors["RED"]}The word have {len(word)} letters.Try Again.{colors["RESET"]}")
            elif guess not in wordlist:
                print(f"{colors['RED']}The word is not in the word list. Try Again.{colors['RESET']}")
            else:
                break
        guess_check = check_common_letters(word, guess)
        number_of_try += 1
        print(f"Chances left: {chances - number_of_try}")

main()