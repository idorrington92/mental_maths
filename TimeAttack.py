from kivymd.app import MDApp
from kivy.clock import Clock

from Game import GameLogic


class TimeAttack(GameLogic):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.timestep_size = 0.01
        self.time_limit = 3
        self.timestep = self.time_limit

    def start_round(self):
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.text = self.player_answer = ''
        self.game_round()
        MDApp.get_running_app().root.ids[self.game_id].ids.prompt.text = self.prompt

    def play_game(self):
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)
        self.timestep = self.time_limit
        self.start_round()

    def update(self, *args):
        print(self.timestep)
        if self.timestep > 0:
            self.timestep -= self.timestep_size
        else:
            self.end_game()

    def end_game(self):
        self.clock.cancel()
        super().end_game()

    def end_game_text(self):
        return f"Score: {self.score}"
