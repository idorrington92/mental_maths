import numpy.random as rand

from Game import Game


class ThreeByOneDigitMultiplication(Game):
    def __init__(self, number_of_rounds):
        self.game_id = "ThreeByOneDigitMultiplication"
        self.number1 = 0
        self.number2 = 0
        self.help = "..."
        self.short_description = "Multiply a three digit number by a single digit number"
        super().__init__(number_of_rounds)
        self.PopUp.open()

    def game_round(self):
        self.number1 = rand.randint(101, 1000)
        self.number2 = rand.randint(2, 10)
        self.prompt = f"{self.number1} x {self.number2} = "

    def correct_answer(self):
        return self.number1 * self.number2
