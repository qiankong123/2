import random
# 2猜数字
# generate a random number between 1 and 100
number = random.randint(1, 100)

# initialize the guess count
guess_count = 0

# loop until the user guesses the correct number
while True:
    # ask the user for their guess
    guess = int(input("Guess a number between 1 and 100: "))

    # increment the guess count
    guess_count += 1

    # check if the guess is correct
    if guess == number:
        print("Congratulations! You guessed the number in", guess_count, "tries.")
        break
    # provide feedback based on the guess
    elif guess < number:
        print("Your guess is too low. Try again.")
    else:
        print("Your guess is too high. Try again.")