from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication
from TimedQuiz import TimedQuiz
from TimeAttack import TimeAttack


class MentalMathsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = "close"
        self.prompt = "Nothing yet"
        self.game = None
        self.game_type = None
        self.nrounds = 3
        self.game_name = None
        self.quiz_dict = {"Maths Dojo": None,
                          "Multiply By 11": MultiplyBy11,
                          "Two Digit Addition": TwoDigitAddition,
                          "Three By One Digit Multiplication": ThreeByOneDigitMultiplication,
                          "Two Digit Multiplication": TwoDigitMultiplication,
                          }
        self.game_dict = {"Time Attack": TimeAttack,
                          "Timed Quiz": TimedQuiz}

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"

    def light_dark_switch(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def printIDs(self):
        print(self.root.ids)

    def set_game(self, game_name):
        print(self.quiz_dict[game_name])
        quiz = self.quiz_dict[game_name]
        self.game_name = game_name
        self.game_type = None

        if quiz is not None:
            class Game(quiz, TimeAttack):
                pass

            self.game_type = Game


    def launch_game(self):
        self.game = self.game_type()
        # TODO not all game modes will have rounds now
        # self.game = self.game_type(self.nrounds)

    def open_close_toolbar(self):
        self.toolbar = "open" if self.toolbar == "close" else "close"
        return self.toolbar



class GameScreen(MDScreen):
    pass


class MenuList(MDBoxLayout):
    pass


if __name__ == '__main__':
    MentalMathsApp().run()
