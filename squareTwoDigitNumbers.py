import numpy.random as rand

from Game import QuizLogic


class SquareTwoDigitNumbers(QuizLogic):
    short_description = "Square two digit numbers."

    def __init__(self):
        # NOTE Short description must go before super
        super().__init__()
        self.number = 0
        self.help = ""

    def game_round(self):
        self.number = rand.randint(10, 100)
        self.question = f"{self.number} x {self.number} = "

    def correct_answer(self):
        return self.number ** 2
