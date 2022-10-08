import numpy.random as rand

from Game import QuizLogic


class TwoDigitAddition(QuizLogic):
    short_description = "Add the two digit numbers together"

    def __init__(self):
        # NOTE Short description must go before super
        super().__init__()
        self.number1 = 0
        self.number2 = 0
        self.help = "..."

    def game_round(self):
        self.number1 = rand.randint(10, 100)
        self.number2 = rand.randint(10, 100)
        self.question = f"{self.number1} + {self.number2} = "

    def correct_answer(self):
        return self.number1 + self.number2
