import numpy.random as rand

from Game import QuizLogic
from TimedQuiz import TimedQuiz


class TwoDigitAddition(QuizLogic, TimedQuiz):
    def __init__(self):
        # NOTE Short description must go before super
        self.short_description = "Add the two digit numbers together. Solve as many as you can"
        super().__init__()
        self.game_id = "TwoDigitAddition"
        self.number1 = 0
        self.number2 = 0
        self.help = "..."

    def game_round(self):
        self.number1 = rand.randint(10, 100)
        self.number2 = rand.randint(10, 100)
        self.prompt = f"{self.number1} + {self.number2} = "

    def correct_answer(self):
        return self.number1 + self.number2
