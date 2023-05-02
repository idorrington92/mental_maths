from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import numpy.random as rand

from Game import GameLogic


class TutorialCloseButton(MDFlatButton):
    pass


class TutorialNextButton(MDFlatButton):
    pass


class Tutorial(GameLogic):
    short_description = "Learn how to solve the problem"

    def __init__(self, quiz_logic):
        super(Tutorial, self).__init__(quiz_logic)
        self.tutorial_pop_up = None
        self.tutorial_idx = 0
        self.tutorial_phase = -1

    def start_countdown(self):
        # No Countdown for tutorial
        self.reset()
        self.app.change_screen("game_screen")
        self.display_tutorial()

    def get_records(self):
        return

    def update_tutorial(self):
        self.tutorial_idx += 1
        # None indicates end of this part of the tutorial
        if self.tutorial_idx >= len(self.quiz.tutorial):
            self.end_game()
        elif self.quiz.tutorial[self.tutorial_idx] is None:
            self.score = 0
            self.tutorial_idx += 1
            self.tutorial_phase += 1
            self.tutorial_pop_up.dismiss()
            self.play_game()
        else:
            self.tutorial_pop_up.text = self.quiz.tutorial[self.tutorial_idx]

    def generate_tutorial_pop_up(self):
        self.tutorial_pop_up = MDDialog(title=self.app.quiz_name,
                                        text=self.quiz.tutorial[self.tutorial_idx],
                                        buttons=[TutorialNextButton()],
                                        md_bg_color=self.app.theme_cls.bg_dark,
                                        auto_dismiss=False,
                                        )

    def display_tutorial(self):
        self.generate_tutorial_pop_up()
        self.tutorial_pop_up.open()

    def play_game(self):
        self.app.root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.app.root.ids["game_screen"].ids['clock_label'].text = f""
        self.start_round()

    def start_round(self, *args):
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.text = self.player_answer = ''
        self.quiz.tutorial_game_round(self.tutorial_phase)
        self.set_prompt(self.quiz.question)

    def end_game(self):
        """
        End game display
        :return:
        """
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.focus = False
        self.EndGamePopUpTitle = "Congratulations, you finished the tutorial"
        super().end_game()

    def end_game_text(self):
        return f"\nScore: {self.score}"

    def correct_answer_action(self):
        self.score += 1
        if self.score >= 3:
            print(self.tutorial_idx, len(self.quiz.tutorial))
            if self.tutorial_idx < len(self.quiz.tutorial):
                self.display_tutorial()
            else:
                self.end_game()
        return super().correct_answer_action()
