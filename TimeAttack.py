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
        MDApp.get_running_app().root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.timestep = self.time_limit
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)
        self.start_round()

    def reset(self):
        self.timestep = self.time_limit
        super().reset()

    def update(self, *args):
        self.timestep -= self.timestep_size
        if self.timestep > 0:
            MDApp.get_running_app().root.ids["game_screen"].ids['clock_label'].text = f"{self.timestep:.3f}"
        else:
            self.timestep = 0
            MDApp.get_running_app().root.ids["game_screen"].ids['clock_label'].text = f"{self.timestep:.3f}"
            self.end_game()

    def end_game_text(self):
        return f"Score: {self.score}"

    def incorrect_answer_action(self):
        self.timestep -= 10
        return super().incorrect_answer_action()

    def correct_answer_action(self):
        self.score += 1
        return super().correct_answer_action()
