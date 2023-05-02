import numpy.random as rand

from Game import QuizLogic


class MultiplyBy11(QuizLogic):
    short_description = "Each problem involves multiplying by 11"

    def __init__(self):
        super().__init__()
        self.number = 0
        self.help = "To multiply a two digit number by 11, add the two digits together and put the result between \n" \
                    "the two digits. e.g. 42 x 11 = 462, as 4 + 2 = 6. If the two digits sum to more than 10, then \n" \
                    "add one to the first digit and put the second digit in the middle. e.g. 58 x 11 = 638 as 5 + 8\n" \
                    " = 13, so we add one to the 5 and put 3 in the middle."
        self.tutorial = ["We are going to learn a quick and easy way to multiply a two digit number by 11",
                         "The trick is to add the two digits together, and sandwich the result between them,"
                         "so 42x11 become 462, as 4+2=6 and we put this between the 4 and 2",
                         "Now you try. Get three correct answers to move to the next section",
                         None,
                         "Well done! You got three correct answers!",
                         "You may be wondering what to do when the two digits add up to more than 10, such as in 67x11.",
                         "In this case you add the two digits together, and sandwich the"
                         " second digit of the answer between the two digits, and add one to the first digit.\n"
                         " So 67x11=737, as we sandwich the second digit of 6+7=13 and add one to the first digit.",
                         "Now you have a go! Get three correct answers to move on!",
                         None,
                         "Well done! You completed the tutorial!"
                        ]

    def game_round(self):
        self.number = rand.randint(10, 100)
        self.question = f"{self.number} x 11 = "

    def tutorial_game_round(self, tutorial_phase):
        if tutorial_phase == 0:
            numbers = [i for i in range(10, 100) if int(str(i)[0]) + int(str(i)[1]) < 10]
            self.number = rand.choice(numbers)
        else:
            numbers = [i for i in range(10, 100) if int(str(i)[0]) + int(str(i)[1]) >= 10]
            self.number = rand.choice(numbers)
        self.question = f"{self.number} x 11 = "


    def correct_answer(self):
        return self.number * 11
