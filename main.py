from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication


class MentalMathsApp(MDApp):
    def __init__(self):
        super().__init__()
        self.prompt = "Nothing yet"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.game = None
        self.game_type = None
        self.nrounds = 3
        self.game_name = None
        self.game_dict = {"Maths Dojo": None,
                          "Multiply By 11": MultiplyBy11,
                          "Two Digit Addition": TwoDigitAddition,
                          "Three By One Digit Multiplication": ThreeByOneDigitMultiplication,
                          "Two Digit Multiplication": TwoDigitMultiplication,
                          }

    def printIDs(self):
        print(self.root.ids)

    def set_game(self, game_name):
        self.game_name = game_name
        self.game_type = self.game_dict[game_name]


    def launch_game(self):
        self.game = self.game_type(self.nrounds)


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class GameScreen(MDScreen):
    pass

class SM(ScreenManager):
    pass


class HomePage(MDScreen):
    pass

class ToolBar(MDToolbar):
    pass


if __name__ == '__main__':
    MentalMathsApp().run()
