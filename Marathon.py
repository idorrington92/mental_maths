from abc import ABC

from kivymd.app import MDApp
from kivy.clock import Clock

from Game import GameLogic


class Marathon(GameLogic, ABC):
    def __init__(self, *args):
        super().__init__(*args)
        self.combo = 10
        self.clock = None
        self.initial_time_limit = 20
        self.time_limit = self.initial_time_limit
        self.clock_paused = False
        self.app.root.ids["game_screen"].ids['life1'].text_color = (100, 0, 0, 1)
        self.app.root.ids["game_screen"].ids['life2'].text_color = (100, 0, 0, 1)
        self.app.root.ids["game_screen"].ids['life3'].text_color = (100, 0, 0, 1)
        self.lives = 3
        self.timestep = self.time_limit
        self.current_combo = 0
        self.question_number = 0

    def start_round(self, *args):
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)
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

    def player_input(self):
        self.clock.cancel()
        super().player_input()

    def play_game(self):
        MDApp.get_running_app().root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.timestep = self.time_limit
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
            # Enter player answer as it is
            self.player_input()

    def end_game_text(self):
        return f"Score: {self.score}"

    def incorrect_answer_action(self):
        super().incorrect_answer_action()
        self.current_combo = 0
        self.lives -= 1
        self.change_lives_display()
        # Returning a delay of None indicates the game is over. See Game.player_input
        if self.lives < 1:
            return None
        # Return the number of seconds to delay the clock restarting
        return 1

    def correct_answer_action(self):
        self.current_combo += 1
        self.score += self.calculate_score()
        prompt = "Correct!"
        extra_delay_factor = 1
        if not self.current_combo % self.combo:
            prompt = f"{self.current_combo} correct answers in a row!"
            extra_delay_factor = 3
            if self.lives < 3:
                self.add_life()
                prompt = "".join([prompt, "One life restored!"])
        delay = super().correct_answer_action(prompt)
        # Return the number of seconds to delay the clock restarting
        return delay * extra_delay_factor

    def add_life(self):
        self.lives += 1
        self.change_lives_display()

    def change_lives_display(self):
        self.app.root.ids["game_screen"].ids['life3'].disabled = True if self.lives < 3 else False
        self.app.root.ids["game_screen"].ids['life2'].disabled = True if self.lives < 2 else False
        self.app.root.ids["game_screen"].ids['life1'].disabled = True if self.lives < 1 else False

    def calculate_score(self):
        return int((self.initial_time_limit - self.timestep) * (1 + self.question_number / 2))
