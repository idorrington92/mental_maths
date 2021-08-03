import numpy.random as rand

from Game import Game


class ThreeByOneDigitMultiplication(Game):
    def __init__(self, number_of_rounds, inst):
        super().__init__(number_of_rounds)
        self.number1 = 0
        self.number2 = 0
        self.help = "..."

        self.play_game()

    def game_round(self):
        self.number1 = rand.randint(11, 1000)
        self.number2 = rand.randint(2, 10)
        self.prompt = f"{self.number1} x {self.number2} = "
        return self.player_input()

    def correct_answer(self):
        return self.number1 * self.number2
