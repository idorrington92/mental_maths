from kivymd.app import MDApp

from Game import GameLogic


class Accuracy(GameLogic):
    short_description = "No time limit, but make one mistake and it's game over"

    def play_game(self):
        self.app.root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.app.root.ids["game_screen"].ids['clock_label'].text = f""
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
        if self.score < 5:
            self.EndGamePopUpTitle = "Accuracy makes perfect"
        else:
            self.EndGamePopUpTitle = "Congratulations"
        super().end_game()

    def end_game_text(self):
        return f"\nScore: {self.score}"

    def correct_answer_action(self):
        self.score += 1
        return super().correct_answer_action()

    def incorrect_answer_action(self):
        super().incorrect_answer_action()
        self.end_game()
