from kivymd.app import MDApp
from kivy.clock import Clock

from Game import GameLogic


class TimeAttack(GameLogic):
    def __init__(self, *args):
        super().__init__(*args)
        self.clock = None
        self.time_limit = 30
        self.timestep = self.time_limit

    def start_round(self, *args):
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.text = self.player_answer = ''
        self.quiz.game_round()
        self.set_prompt(self.quiz.question)

    def play_game(self):
        self.score = 0
        MDApp.get_running_app().root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.timestep = self.time_limit
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)
        self.start_round()

    def update(self, *args):
        if self.timestep > 0:
            self.timestep -= self.timestep_size
            MDApp.get_running_app().root.ids["game_screen"].ids['clock_label'].text = f"{self.timestep:.3f}"
        else:
            self.end_game()

    def end_game(self):
        self.clock.cancel()
        super().end_game()

    def end_game_text(self):
        return f"Score: {self.score}"

    def incorrect_answer_action(self):
        self.timestep -= 10
        super().incorrect_answer_action()
