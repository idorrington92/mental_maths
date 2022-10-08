import numpy.random as rand

from Game import QuizLogic


class MultiplyBy11(QuizLogic):
    short_description = "Each problem involves multiplying by 11"

    def __init__(self):
        # NOTE Short description must go before super
        super().__init__()
        self.number = 0
        self.help = "To multiply a two digit number by 11, add the two digits together and put the result between \n" \
                    "the two digits. e.g. 42 x 11 = 462, as 4 + 2 = 6. If the two digits sum to more than 10, then \n" \
                    "add one to the first digit and put the second digit in the middle. e.g. 58 x 11 = 638 as 5 + 8\n" \
                    " = 13, so we add one to the 5 and put 3 in the middle."

    def game_round(self):
        self.number = rand.randint(10, 100)
        self.question = f"{self.number} x 11 = "

    def correct_answer(self):
        return self.number * 11
