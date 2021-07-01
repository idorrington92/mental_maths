import numpy.random as rand

class multiplyBy11:
    def __init__(self, number_of_rounds):
        self.number = 0
        self.player_answer = 0
        self.number_of_rounds = number_of_rounds

        self.playGame()

    def playGame(self):
        for round in range(self.number_of_rounds):
            print(f"Round {round}")
            if not self.gameRound():
                break

    def gameRound(self):
        self.number = rand.randint(10, 99)
        self.player_answer = input(f"{self.number} x 11 = ")

        while not self.validInput():
            print("Invalid input. Please enter numeric value to play or Q to quit\n")
            self.player_answer = input(f"{self.number} x 11 = ")

        if self.player_answer in ("q", "Q"):
            print("Exiting program")
            return False

        if self.playerCorrect():
            print("Correct!")
            return True

        print(f"Unlucky. The correct answer is {self.correctAnswer()}")
        return True

    def correctAnswer(self):
        return self.number * 11

    def playerCorrect(self):
        return self.player_answer == str(self.correctAnswer())

    def validInput(self):
        return self.player_answer in ("q", "Q") or self.player_answer.isnumeric()

if __name__ == '__main__':
    multiplyBy11(3)
