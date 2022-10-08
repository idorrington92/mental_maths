import numpy.random as rand

from Game import QuizLogic


class TwoByOneDigitMultiplication(QuizLogic):
    def __init__(self):
        # NOTE Short description must go before super
        self.short_description = "Multiply a three digit number by a single digit number"
        super().__init__()
        self.number1 = 0
        self.number2 = 0
        self.help = "..."

    def game_round(self):
        self.number1 = rand.randint(11, 100)
        self.number2 = rand.randint(2, 10)
        self.question = f"{self.number1} x {self.number2} = "

    def correct_answer(self):
        return self.number1 * self.number2
