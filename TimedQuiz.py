from kivymd.app import MDApp

from Game import GameLogic


class TimedQuiz(GameLogic):
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

    def end_game_text(self):
        return f"\nScore: {self.score}\n" \
               f"Time taken: {self.timestep:.2f}s"

    def correct_answer_action(self):
        super().correct_answer_action()
        if self.score >= 3:
            self.end_game()

    def incorrect_answer_action(self):
        super().incorrect_answer_action()
        self.timestep += 5
