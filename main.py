from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty

from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication


class MentalMathsApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.game = None
        self.nrounds = 3

    def printIDs(self):
        print(self.root.ids)

    def set_game(self, game_name):
        if game_name == "MultiplyBy11":
            self.game = MultiplyBy11
        elif game_name == "TwoDigitAddition":
            self.game = TwoDigitAddition
        elif game_name == "ThreeByOneDigitMultiplication":
            self.game = ThreeByOneDigitMultiplication
        elif game_name == "TwoDigitMultiplication":
            self.game = TwoDigitMultiplication
        else:
            self.game = None

    def launch_game(self):
        self.game(self.nrounds)


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


if __name__ == '__main__':
    MentalMathsApp().run()
