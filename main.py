from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivymd.uix.widget import MDWidget
from kivy.properties import ListProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDRoundFlatIconButton

from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication
from TimedQuiz import TimedQuiz
from TimeAttack import TimeAttack
from Game import Game


class MentalMathsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = "Nothing yet"
        self.game = Game()
        self.quiz_name = ""
        self.game_name = ""
        self.game_type = None
        self.nrounds = 3
        self.data = JsonStore("mental_maths.json")
        self.is_locked_level = self.data.get("is_level_locked")

        self.quiz_dict = {"Maths Dojo": None,
                          "Multiply By 11": MultiplyBy11,
                          "Two Digit Addition": TwoDigitAddition,
                          "Three By One Digit Multiplication": ThreeByOneDigitMultiplication,
                          "Two Digit Multiplication": TwoDigitMultiplication,
                          }
        self.game_dict = {"Maths Dojo": None,
                          "Time Attack": TimeAttack,
                          "Timed Quiz": TimedQuiz
                          }
        self.challenges = {
            "Multiply By 11": {
                "Timed Quiz": {
                    "bronze": {"text": "Get 1 answer correct", "condition": lambda score: score >= 1},
                    "silver": {"text": "Get 2 answers correct", "condition": lambda score: score >= 2},
                    "gold": {"text": "Answer all questions correctly", "condition": lambda score: score > 3}
                },
                "Time Attack": {
                    "bronze": {"text": "Score 5 points", "condition": lambda score: score >=5},
                    "silver": {"text": "Score 7 points", "condition": lambda score: score >= 7},
                    "gold": {"text": "Score 10 points", "condition": lambda score: score >= 10},
                },
            },
            "Two Digit Addition": {
                "Timed Quiz": {
                    "bronze": {"text": "Get 1 answer correct", "condition": lambda score: score >= 1},
                    "silver": {"text": "Get 2 answers correct", "condition": lambda score: score >= 2},
                    "gold": {"text": "Answer all questions correctly", "condition": lambda score: score > 3}
                },
                "Time Attack": {
                    "bronze": {"text": "Score 5 points", "condition": lambda score: score >= 5},
                    "silver": {"text": "Score 7 points", "condition": lambda score: score >= 7},
                    "gold": {"text": "Score 10 points", "condition": lambda score: score >= 10},
                },
            },
            "Three By One Digit Multiplication": {
                "Timed Quiz": {
                    "bronze": {"text": "Get 1 answer correct", "condition": lambda score: score >= 1},
                    "silver": {"text": "Get 2 answers correct", "condition": lambda score: score >= 2},
                    "gold": {"text": "Answer all questions correctly", "condition": lambda score: score > 3}
                },
                "Time Attack": {
                    "bronze": {"text": "Score 5 points", "condition": lambda score: score >= 5},
                    "silver": {"text": "Score 7 points", "condition": lambda score: score >= 7},
                    "gold": {"text": "Score 10 points", "condition": lambda score: score >= 10},
                },
            },
            "Two Digit Multiplication": {
                "Timed Quiz": {
                    "bronze": {"text": "Get 1 answer correct", "condition": lambda score: score >= 1},
                    "silver": {"text": "Get 2 answers correct", "condition": lambda score: score >= 2},
                    "gold": {"text": "Answer all questions correctly", "condition": lambda score: score > 3}
                },
                "Time Attack": {
                    "bronze": {"text": "Score 5 points", "condition": lambda score: score >= 5},
                    "silver": {"text": "Score 7 points", "condition": lambda score: score >= 7},
                    "gold": {"text": "Score 10 points", "condition": lambda score: score >= 10},
                },
            }
        }

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"

    def light_dark_switch(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def printIDs(self):
        print(self.root.ids)

    def set_game(self, quiz_name, game_name):
        self.quiz_name= quiz_name
        self.game_name = game_name
        quiz = self.quiz_dict[quiz_name]
        game = self.game_dict[game_name]
        self.game_type = None

        if quiz and game:
            class Game(quiz, game):
                pass

            self.game_type = Game
            self.set_challenge_text(quiz_name, game_name)

    def set_challenge_text(self, quiz_name, game_name):
        for medal in ("bronze", "silver", "gold"):
            self.root.ids[medal + "_challenge_label"].text = self.challenges[quiz_name][game_name][medal]["text"]
            self.root.ids[medal + "_challenge_label"].disabled = \
                not self.data[quiz_name][game_name]["challenges_completed"][medal]

    def launch_game(self):
        self.game = self.game_type()

    def change_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


class BasicScreen(MDScreen):
    pass


class GameScreen(BasicScreen):
    pass


class CountDownScreen(MDScreen):
    pass


class MenuList(MDBoxLayout):
    pass


class AnswerBoxHighlight(MDWidget):
    colour = ListProperty([0, 0, 0, 0])
    blink_size = ListProperty([1200, 94.5])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 0.5

    def run_correct_answer_animation(self, correct: bool):
        if correct:
            self.colour = [0.67, 1.0, 0.2, 1.0]
        else:
            self.colour = [1, 0, 0, 1]
        anim = Animation(animated_color=self.colour,
                         blink_size=(1200.0, 94.5),
                         opacity=0.75,
                         duration=self.duration)
        anim.bind(on_complete=self.reset)
        anim.start(self)

    def reset(self, *args):
        anim = Animation(animated_color=self.colour,
                         opacity=0.0,
                         duration=self.duration)
        self.blink_size = (0, 0)
        anim.start(self)


class ChallengeLabel(MDRoundFlatIconButton):
    def on_touch_down(self, touch):
        pass


if __name__ == '__main__':
    MentalMathsApp().run()
