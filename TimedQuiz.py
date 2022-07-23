from kivymd.app import MDApp
from kivy.clock import Clock

from Game import GameLogic


class TimedQuiz(GameLogic):
    target = 3

    def play_game(self):
        super().play_game()
        self.start_round()

    def start_round(self, *args):
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.text = self.player_answer = ''
        self.quiz.game_round()
        self.set_prompt(self.quiz.question)

    def end_game(self):
        """
        End game display
        :return:
        """
        MDApp.get_running_app().root.ids["game_screen"].ids.PlayerInput.focus = False
        self.end_game_pop_up_title = "Game over"
        super().end_game(score=self.timestep)

    def end_game_text(self):
        return f"Time taken: {self.timestep:.2f}s"

    def correct_answer_action(self):
        delay = super().correct_answer_action()
        self.score += 1
        if self.score >= self.target:
            self.end_game()
        return delay

    def incorrect_answer_action(self):
        self.timestep += 5
        delay = super().incorrect_answer_action()
        self.change_clock_colour(duration=delay)
        return delay

    def change_clock_colour(self, duration=1):
        self.app.root.ids["game_screen"].ids.clock_label.change_colour(duration)

    def any_records_broken(self):
        timesteps = self.app.records["scores"]
        if len(timesteps) < 5 or self.timestep < max(timesteps):
            return True
        return False

    def records_update(self):
        timesteps = self.app.records["scores"]

        if len(timesteps) < 5:
            # If there are less than 5 records, then always add player score
            self.app.records["names"].append(self.player_name)
            self.app.records["scores"].append(self.timestep)

        elif self.timestep < max(timesteps):
            # If there are more than 5 records, then add score if it's smaller than the
            # largest existing score
            for i, timestep in enumerate(timesteps):
                if timestep == max(timesteps):
                    self.app.records["names"][i] = self.player_name
                    self.app.records["scores"][i] = self.timestep
        else:
            # No new record
            return

        # Sort records by score
        self.app.records["scores"], self.app.records["names"] = \
            zip(*sorted(zip(self.app.records["scores"], self.app.records["names"]),
                        reverse=False))

        # Convert to lists as these must be mutable next time we want to write
        self.app.records["scores"], self.app.records["names"] = \
            list(self.app.records["scores"]), list(self.app.records["names"])

        # Save to the Json file
        self.app.data[self.app.quiz_name][self.app.game_name]["records"] = self.app.records
        self.app.save()
