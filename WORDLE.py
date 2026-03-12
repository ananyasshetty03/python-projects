import random


class Wordle:
    def __init__(self, word_list):
        self.words = [word.lower() for word in word_list if len(word) == 5 and word.isalpha()]
        assert self.words, "No valid 5-letter words found in the file!"
        self.secret = random.choice(self.words)
        self.attempts = 0
        self.max_attempts = 6
        self.history = []

    def guess_word(self, word):
        self.attempts += 1
        assert len(word) == 5, "Word must be 5 letters!"
        result = self.evaluate(word)
        self.history.append((word, result))
        return result

    def evaluate(self, guess):
        result = []
        for i in range(5):
            if guess[i] == self.secret[i]:
                result.append("🟩")
            elif guess[i] in self.secret:
                result.append("🟨")
            else:
                result.append("⬜")
        return result

    def correct_word(self, word):
        return word == self.secret

    def show_history(self):
        for guess, result in self.history:
            print(f"{guess.upper()} -> {''.join(result)}")

def word_file(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("File not found!")
        return []

def get_guess():
    while True:
        word = input("Enter your 5 letter guess: ").lower()
        try:
            assert len(word) == 5 and word.isalpha(), "Guess must be a 5 letter word!"
            return word
        except AssertionError as e:
            print(e)

def save_result(player, attempts, won):
    try:
        with open("wordle_scores.txt", "a") as file:
            file.write(f"{player}: {'Win' if won else 'Loss'} in {attempts} tries\n")
    except Exception as e:
        print("Error saving result:", e)

def main():
    print("Welcome to Custom Wordle!")
    wordfile = input("Enter the filename containing your word list: ")
    words = word_file(wordfile)

    if not words:
        return

    try:
        game = Wordle(words)
    except AssertionError as e:
        print(f"❌{e}")
        return

    player = input("Enter your name: ")

    while game.attempts < game.max_attempts:
        guess = get_guess()
        result = game.guess_word(guess)
        print("Result:", ''.join(result))
        if game.correct_word(guess):
            print(f"Congrats 🎉{player}! You guessed it in {game.attempts} tries.")
            save_result(player, game.attempts, True)
            break
    else:
        print(f"Oops 😢 Out of tries! The word was: {game.secret}")
        save_result(player, game.attempts, False)

    print("\nYour guesses:")
    game.show_history()

main()
