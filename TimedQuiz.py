from kivymd.app import MDApp

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
        self.EndGamePopUpTitle = "Game over"
        super().end_game()

    def challenges_check(self, score=None):
        # The score for timed quiz is actually the time taken to complete the quiz
        if score is None:
            score = self.timestep
        super().challenges_check(score)

    def end_game_text(self):
        return f"Time taken: {self.timestep:.2f}s"

    def correct_answer_action(self):
        super().correct_answer_action()
        if self.score >= self.target:
            self.end_game()

    def incorrect_answer_action(self):
        super().incorrect_answer_action()
        self.timestep += 5

    def records_check(self):
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
