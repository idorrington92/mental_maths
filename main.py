from json import dump
from typing import Callable
from collections import deque
from typing import NamedTuple

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivymd.uix.widget import MDWidget
from kivy.properties import ListProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication
from TimedQuiz import TimedQuiz
from TimeAttack import TimeAttack


class Challenge(NamedTuple):
    text: str
    condition: Callable


class Medals(NamedTuple):
    bronze: Challenge
    silver: Challenge
    gold: Challenge


class MentalMathsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = "Nothing yet"
        self.previous_screens = deque(["home"])
        self.game = None
        self.quiz_name = ""
        self.game_name = ""
        self.game = None
        self.quiz = None
        self.nrounds = 3
        self.data = JsonStore("mental_maths.json", indent=4)
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
                "Timed Quiz": Medals(Challenge("Get 1 answer correct", lambda score: score >= 1),
                                     Challenge("Get 2 answers correct", lambda score: score >= 2),
                                     Challenge("Answer all questions correctly", lambda score: score >= 3)),
                "Time Attack": Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            },
            "Two Digit Addition": {
                "Timed Quiz": Medals(Challenge("Get 1 answer correct", lambda score: score >= 1),
                                     Challenge("Get 2 answers correct", lambda score: score >= 2),
                                     Challenge("Answer all questions correctly", lambda score: score >= 3)),
                "Time Attack": Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            },
            "Three By One Digit Multiplication": {
                "Timed Quiz": Medals(Challenge("Get 1 answer correct", lambda score: score >= 1),
                                     Challenge("Get 2 answers correct", lambda score: score >= 2),
                                     Challenge("Answer all questions correctly", lambda score: score >= 3)),
                "Time Attack": Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            },
            "Two Digit Multiplication": {
                "Timed Quiz": Medals(Challenge("Get 1 answer correct", lambda score: score >= 1),
                                     Challenge("Get 2 answers correct", lambda score: score >= 2),
                                     Challenge("Answer all questions correctly", lambda score: score >= 3)),
                "Time Attack": Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            }
        }
        self.records = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root.ids["dark_mode_switch"].active = not self.data["theme"]["dark_mode"]
        self.theme_cls.primary_palette = "Cyan"

    def save(self):
        self.data["theme"]["dark_mode"] = True if self.theme_cls.theme_style == "Dark" else False
        with open(self.data.filename, 'w') as fd:
            dump(
                self.data._data, fd,
                indent=self.data.indent,
                sort_keys=self.data.sort_keys
            )

    def light_dark_switch(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.save()

    def completed(self, level_name):
        return all(all(self.data[level_name][game_type]["challenges_completed"].values())
                   for game_type in self.data[level_name])
    
    def printIDs(self):
        print(self.root.ids)

    def set_quiz(self, quiz_name):
        self.quiz_name = quiz_name

    def set_game(self, game_name):
        self.game_name = game_name
        self.quiz = self.quiz_dict[self.quiz_name]
        self.game = self.game_dict[self.game_name]

        if self.quiz and self.game:
            self.set_challenge_text(self.quiz_name, self.game_name)
            self.records = self.data[self.quiz_name][self.game_name]["records"]

    def set_challenge_text(self, quiz_name, game_name):
        for medal, challenge in self.challenges[quiz_name][game_name]._asdict().items():
            self.root.ids[medal + "_challenge_label"].text = challenge.text
            self.root.ids[medal + "_challenge_label"].disabled = \
                not self.data[quiz_name][game_name]["challenges_completed"][medal]

    def launch_game(self):
        self.game = self.game(self.quiz())

    def change_screen(self, screen_name):
        self.previous_screens.append(self.root.ids.screen_manager.current)
        self.root.ids.screen_manager.current = screen_name

    def previous_screen(self):
        if len(self.previous_screens) == 1:
            self.root.ids.screen_manager.current = "home"
            return
        if (previous_screen := self.previous_screens.pop()) == "game_screen":
            self.game.start_game()
            return
        # Don't want count down screen to behave like a regular screen (otherwise can't go back from game screen)
        if previous_screen == "count_down_screen":
            self.previous_screen()
            return
        self.root.ids.screen_manager.current = previous_screen


class BasicScreen(MDScreen):
    pass


class RecordScreen(BasicScreen):
    def on_enter(self):
        records = MDApp.get_running_app().records["scores"]
        names = MDApp.get_running_app().records["names"]
        table = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint=(0.7, 0.7),
            column_data=[("Name", dp(30)), ("Score", dp(30))],
            row_data=[[n, r] for n, r in zip(names, records)]
        )
        self.add_widget(table)


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


class MenuCard(MDCard):
    text = StringProperty("")
    description = StringProperty("")

if __name__ == '__main__':
    MentalMathsApp().run()
