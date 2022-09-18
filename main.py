from json import dump
from typing import Callable
from collections import deque
from typing import NamedTuple
from enum import Enum

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
from Marathon import Marathon


class GameName(Enum):
    MATHS_DOJO = None
    TIMED_QUIZ = "Timed Quiz"
    MARATHON = "Marathon"


class QuizName(Enum):
    MATHS_DOJO = "Maths Dojo"
    MULTIPLY_BY_11 = "Multiply By 11"
    TWO_DIGIT_ADDITION = "Two Digit Addition"
    THREE_BY_ONE_MULTIPLICATION = "Three By One Digit Multiplication"
    TWO_DIGIT_MULTIPLICATION = "Two Digit Multiplication"


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
        self.quiz_name = QuizName.MATHS_DOJO.value
        self.game_name = ""
        self.game = None
        self.quiz = None
        self.nrounds = 3
        self.data = JsonStore("mental_maths.json", indent=4)
        self.quiz_dict = {QuizName.MATHS_DOJO.value: None,
                          QuizName.MULTIPLY_BY_11.value: MultiplyBy11,
                          QuizName.TWO_DIGIT_ADDITION.value: TwoDigitAddition,
                          QuizName.THREE_BY_ONE_MULTIPLICATION.value: ThreeByOneDigitMultiplication,
                          QuizName.TWO_DIGIT_MULTIPLICATION.value: TwoDigitMultiplication,
                          }
        self.quiz_short_name = {QuizName.MATHS_DOJO.value: "Maths Dojo",
                                QuizName.MULTIPLY_BY_11.value: "Multiplication 1",
                                QuizName.TWO_DIGIT_ADDITION.value: "Addition 1",
                                QuizName.THREE_BY_ONE_MULTIPLICATION.value: "Multiplication 2",
                                QuizName.TWO_DIGIT_MULTIPLICATION.value: "Multiplication 3",
                                }
        self.game_dict = {GameName.MATHS_DOJO.value: None,
                          GameName.MARATHON.value: Marathon,
                          GameName.TIMED_QUIZ.value: TimedQuiz,
                          }
        self.challenges = {
            QuizName.MULTIPLY_BY_11.value: {
                GameName.TIMED_QUIZ.value: Medals(Challenge(f"Finish in 30 seconds", lambda score: score <= 30),
                                     Challenge(f"Finish in  10 seconds", lambda score: score <= 10),
                                     Challenge(f"Finish in 5 seconds", lambda score: score <= 5)),
                GameName.MARATHON.value: Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            },
            QuizName.TWO_DIGIT_ADDITION.value: {
                GameName.TIMED_QUIZ.value: Medals(Challenge(f"Finish in 30 seconds", lambda score: score <= 30),
                                     Challenge(f"Finish in  10 seconds", lambda score: score <= 10),
                                     Challenge(f"Finish in 5 seconds", lambda score: score <= 5)),
                GameName.MARATHON.value: Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            },
            QuizName.THREE_BY_ONE_MULTIPLICATION.value: {
                GameName.TIMED_QUIZ.value: Medals(Challenge(f"Finish in 30 seconds", lambda score: score <= 30),
                                     Challenge(f"Finish in  10 seconds", lambda score: score <= 10),
                                     Challenge(f"Finish in 5 seconds", lambda score: score <= 5)),
                GameName.MARATHON.value: Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            },
            QuizName.TWO_DIGIT_MULTIPLICATION.value: {
                GameName.TIMED_QUIZ.value: Medals(Challenge(f"Finish in 30 seconds", lambda score: score <= 30),
                                     Challenge(f"Finish in  10 seconds", lambda score: score <= 10),
                                     Challenge(f"Finish in 5 seconds", lambda score: score <= 5)),
                GameName.MARATHON.value: Medals(Challenge("Score 5 points", lambda score: score >= 5),
                                      Challenge("Score 7 points", lambda score: score >= 7),
                                      Challenge("Score 10 points", lambda score: score >= 10)),
            }
        }
        self.level_order = {
            QuizName.MULTIPLY_BY_11.value: 1,
            QuizName.TWO_DIGIT_ADDITION.value: 2,
            QuizName.THREE_BY_ONE_MULTIPLICATION.value: 3,
            QuizName.TWO_DIGIT_MULTIPLICATION.value: 4,
        }

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

    def is_level_locked(self, level_name):
        if level_name == QuizName.MULTIPLY_BY_11.value:
            # First level is never locked
            return False
        previous_level = list(self.level_order.keys())[self.level_order[level_name] - 2]
        return not all([self.data[previous_level][game_name]["completed_challenges"]["bronze"]
                       for game_name in self.game_dict.keys() if game_name != GameName.MATHS_DOJO.value])

    def check_and_unlock_level(self):
        level_name = self.quiz_name
        next_level = list(self.level_order.keys())[self.level_order[level_name]]
        # Enable button if it is now unlocked
        self.root.ids["MenuList"].ids[next_level + " button"].disabled = \
            self.is_level_locked(next_level)

    def completed_quiz(self, level_name):
        return all(all(self.data[level_name][game_type]["completed_challenges"].values())
                   for game_type in self.data[level_name])

    def completed_game(self, game_name):
        if self.quiz_name == QuizName.MATHS_DOJO.value:
            return False
        return all(
            self.data[self.quiz_name][game_name]["completed_challenges"].values())

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

    def set_challenge_text(self, quiz_name, game_name):
        for medal, challenge in self.challenges[quiz_name][game_name]._asdict().items():
            self.root.ids[medal + "_challenge_label"].text = challenge.text
            self.root.ids[medal + "_challenge_label"].disabled = \
                not self.data[quiz_name][game_name]["completed_challenges"][medal]

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
            if self.game.end_game_pop_up is None:
                self.game.start_countdown()
        # Don't want count down screen to behave like a regular screen (otherwise can't go back from game screen)
        if previous_screen == "count_down_screen":
            self.previous_screen()
            return
        self.root.ids.screen_manager.current = previous_screen


class BasicScreen(MDScreen):
    pass


class GameLobbyScreen(BasicScreen):
    pass


class RecordScreen(BasicScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.table = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint=(0.7, 0.7),
            column_data=[("Name", dp(30)), ("Score", dp(30))],
            row_data=zip([""] * 5, [""] * 5)
        )
        self.add_widget(self.table)

    def load_table(self):
        records = MDApp.get_running_app().game.records["scores"]
        if MDApp.get_running_app().game_name == GameName.TIMED_QUIZ.value:
            records = [f"{record:.2f}" for record in records]
        names = MDApp.get_running_app().game.records["names"]
        self.update_table(names, records)

    def update_table(self, names, records) -> None:
        self.clear_table()
        row_data = zip(names, records)
        for i, (name, record) in enumerate(row_data):
            self.table.update_row(
                self.table.row_data[i],  # old row data
                [name, record],  # new row data
            )

    def clear_table(self):
        for i in range(5):
            self.table.update_row(self.table.row_data[i], ["", ""])


class GameScreen(BasicScreen):
    def on_enter(self, *args):
        if (popup := MDApp.get_running_app().game.end_game_pop_up) is not None:
            popup.open()
        else:
            MDApp.get_running_app().game.end_game_pop_up = None


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
        self.colour = [0.67, 1.0, 0.2, 1.0] if correct else [1, 0, 0, 1]
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
