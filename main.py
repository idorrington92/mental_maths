from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition


def menu():
    nrounds = 3
    selection = input("Select skill to practice:\n"
                      "1. Multiply by 11\n"
                      "2. Two digit addition\n"
                      "q. Quit\n")

    if selection == "1":
        return MultiplyBy11(nrounds)
    if selection == "2":
        return TwoDigitAddition(nrounds)
    if selection in ('q', 'Q'):
        return False


if __name__ == '__main__':
    while menu():
        pass

    print("Thank you for playing")
