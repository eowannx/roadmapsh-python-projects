import random
import time

# dictionary: key = user input, value = (difficulty name, number of chances)
DIFFICULTIES = {
    "1": ("Easy", 10),
    "2": ("Medium", 5),
    "3": ("Hard", 3),
}


def get_difficulty():
    print("\nPlease select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")

    while True:
        choice = input("Enter your choice: ").strip()
        if choice in DIFFICULTIES:
            # tuple unpacking - assigns both values from the tuple at once
            name, chances = DIFFICULTIES[choice]
            print(f"\nGreat! You have selected the {name} difficulty level.")
            print("Let's start the game!\n")
            return chances
        print("Invalid choice. Please enter 1, 2 or 3.")


def play_round():
    number = random.randint(1, 100) # Random integer between a and b inclusive (see notes: random)
    chances = get_difficulty()
    attempts = 0
    start_time = time.time() # Current time in seconds since 1970 (see notes: time)

    # main game loop - runs until attempts run out
    while attempts < chances:
        remaining = chances - attempts
        print(f"Chances remaining: {remaining}")

        try:
            guess = int(input("Enter your guess: ").strip())
        except ValueError: # catches non-numeric input (e.g. "abc")
            print("Invalid input. Please enter a number.")
            continue # skips the remainder of the current iteration and moves on to the next one

        if guess < 1 or guess > 100:
            print("Please enter a number between 1 and 100.")
            continue # skips the remainder of the current iteration and moves on to the next one

        attempts += 1

        if guess == number:
            elapsed = round(time.time() - start_time, 2)
            print(f"\nCongratulations! You guessed the correct number in {attempts} attempts.")
            print(f"Time taken: {elapsed} seconds.")
            return attempts
        elif guess < number:
            print("Incorrect! The number is greater than your guess.")
        else:
            print("Incorrect! The number is less than your guess.")

    print(f"\nGame over! You ran out of chances. The number was {number}.")
    return None # player lost - no score to return


def main():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess it within the allowed number of attempts.")

    while True:
        play_round()

        again = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing. Goodbye!")
            break # exits the loop completely

# This block executes only if file executed directly
# (and not imported as a module in another file)
if __name__ == "__main__":
    main()