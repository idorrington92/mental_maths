import numpy.random as rand

from Game import Game


class TwoDigitMultiplication(Game):
    def __init__(self, number_of_rounds):
        # NOTE Short description must go before super
        self.short_description = "Multiply the two digit numbers together"
        super().__init__(number_of_rounds)
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
