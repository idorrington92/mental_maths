from abc import ABC

from kivymd.app import MDApp
from kivy.clock import Clock

from Game import GameLogic


class Marathon(GameLogic, ABC):
    def __init__(self, *args):
        super().__init__(*args)
        self.clock = None
        self.initial_time_limit = 5
        self.time_limit = self.initial_time_limit
        self.clock_paused = False
        # TODO Add lives on game screen
        self.lives = 3
        self.timestep = self.time_limit
        self.combo = 0
        self.question_number = 0

    def start_round(self, *args):
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.text = self.player_answer = ''
        self.question_number += 1

        # Time limit per question should slowly decrease
        if not self.question_number % 5:
            self.time_limit *= 0.7
        self.quiz.game_round()
        self.set_prompt(self.quiz.question)
        self.timestep = self.time_limit
        self.clock_paused = False

    def play_game(self):
        MDApp.get_running_app().root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.timestep = self.time_limit
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)
        self.start_round()

    def reset(self):
        self.time_limit = self.initial_time_limit
        self.timestep = self.time_limit
        self.lives = 3
        super().reset()

    def update(self, *args):
        self.timestep -= self.timestep_size
        if self.timestep > 0:
            MDApp.get_running_app().root.ids["game_screen"].ids['clock_label'].text = f"{self.timestep:.3f}"
        else:
            # Player runs out of time
            # Clock only displays zero rather than a negative time
            MDApp.get_running_app().root.ids["game_screen"].ids['clock_label'].text = f"{0:.3f}"
            if not self.clock_paused:
                # When the clock reaches zero, it is paused
                # NOTE, this is only the display, the actual clock keeps going
                self.clock_paused = True
                # The player input should be handled only once (so they don't lose a life with every timestep)
                self.player_input()

    def end_game_text(self):
        return f"Score: {self.score}"

    def incorrect_answer_action(self):
        super().incorrect_answer_action()
        self.combo = 0
        self.lives -= 1
        # Game ends when player gets an incorrect answer while out of lives
        print(f"{self.lives=}")
        if self.lives < 0:
            self.end_game()

    def correct_answer_action(self):
        super().correct_answer_action()
        self.combo += 1
        if not self.combo % 3 and self.lives < 3:
            self.add_life()
        self.score += self.calculate_score()

    def add_life(self):
        # TODO Add some kind of animation for this
        self.lives += 1
        print(f"New life {self.combo=} {self.lives=}")

    def calculate_score(self):
        return int((self.initial_time_limit - self.timestep) * (1 + self.question_number / 2))
