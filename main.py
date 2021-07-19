from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication


def menu():
    nrounds = 3
    selection = input("Select skill to practice:\n"
                      "1. Multiply by 11\n"
                      "2. Two digit addition\n"
                      "3. Three by one digit multiplication\n"
                      "4. Two digit multiplication\n"
                      "q. Quit\n")

    if selection == "1":
        return MultiplyBy11(nrounds)
    if selection == "2":
        return TwoDigitAddition(nrounds)
    if selection == "3":
        return ThreeByOneDigitMultiplication(nrounds)
    if selection == "4":
        return TwoDigitMultiplication(nrounds)
    if selection in ('q', 'Q'):
        return False

    print("Invalid entry\n")
    return True


if __name__ == '__main__':
    while menu():
        pass

    print("Thank you for playing")
