import random


class Hangman:

    def __init__(self):
        """Initializes the Hangman class with 8 max guesses and word bank"""
        self.maxGuesses = 8
        self.guessed_letter = ""
        self.word = random.choice(["python", "java", "kotlin", "javascript"])
        self.hidden_word = ("-" * len(self.word))

    def check_guess(self, guess):
        """Take guess as parameter and check if input is valid, reduce max guesses if the guess is wrong"""
        if len(guess) != 1 or guess == "":
            print("You should input a single letter")
        elif not guess.islower() or not guess.isalpha():
            print("Please enter a lowercase English letter")
        elif guess in self.hidden_word or guess in self.guessed_letter:
            print("You've already guessed this letter")
        elif guess in self.word:
            for el, letter in enumerate(self.word):
                if guess == letter:  #if guess is a letter in word, replace the "-" with the correct character
                    self.hidden_word = self.hidden_word[:el] + letter + self.hidden_word[el + 1:]
        else:
            self.maxGuesses -= 1
            self.guessed_letter += guess
            print("That letter doesn't appear in the word")

    def main(self):
        print("H A N G M A N")

        while self.maxGuesses > 0:
            print("")
            print(self.hidden_word)
            guess = input("Input a letter:")
            self.check_guess(guess)
            if self.hidden_word == self.word:
                print("You guessed the word {}!\nYou survived!".format(self.word))
                exit()
        if "-" in self.hidden_word:
            print("You lost!")


if __name__ == '__main__':
    hangman = Hangman()
    start_game = input("Type \"play\" to lay the game, \"exit\" to quit: ")
    if start_game.lower() == "play":
        hangman.main()
    elif start_game.lower() == "exit":
        exit()
