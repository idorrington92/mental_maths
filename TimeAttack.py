from kivymd.app import MDApp
from kivy.clock import Clock

from Game import GameLogic


class TimeAttack(GameLogic):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.time_limit = 30
        self.timestep = self.time_limit

    def start_round(self, *args):
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.text = self.player_answer = ''
        self.game_round()
        MDApp.get_running_app().root.ids[self.game_id].ids.prompt.text = self.prompt

    def play_game(self):
        self.timestep = self.time_limit
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)
        self.start_round()

    def update(self, *args):
        print(self.timestep)
        if self.timestep > 0:
            self.timestep -= self.timestep_size
            MDApp.get_running_app().root.ids[self.game_id].ids['clock_label'].text = f"{self.timestep:.3f}"
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
