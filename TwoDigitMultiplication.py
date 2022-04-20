import numpy.random as rand

from Game import QuizLogic
from TimedQuiz import TimedQuiz

class TwoDigitMultiplication(QuizLogic):
    def __init__(self):
        # NOTE Short description must go before super
        self.short_description = "Multiply the two digit numbers together"
        super().__init__()
        self.game_id = "TwoDigitMultiplication"
        self.number1 = 0
        self.number2 = 0
        self.help = "..."


    def game_round(self):
        self.number1 = rand.randint(11, 100)
        self.number2 = rand.randint(11, 100)
        self.prompt = f"{self.number1} x {self.number2} = "

    def correct_answer(self):
        return self.number1 * self.number2
