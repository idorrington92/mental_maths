import time

from kivymd.app import MDApp

from Game import GameLogic


class TimedQuiz(GameLogic):
    def __init__(self):
        super().__init__()
        self.startTime = 0
        self.number_of_rounds = 3
        self.g_round = 0

    def play_game(self):
        self.startTime = time.time()
        self.g_round = 0
        self.score = 0
        self.start_round()

    def start_round(self):
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.focus = True
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.text = self.player_answer = ''
        self.g_round += 1
        if self.g_round <= self.number_of_rounds:
            print(f"Round {self.g_round}")
            self.game_round()
            MDApp.get_running_app().root.ids[self.game_id].ids.prompt.text = self.prompt
        else:
            self.end_game()  # Player reaches end of game without quiting

    def game_round(self):
        """
        Set up game prerequisites. For example, generating random numbers and assigning the prompt for the player
        :return: None:
        """

    def end_game(self):
        """
        End game display
        :return:
        """
        MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.focus = False
        if self.score / self.number_of_rounds < 0.7:
            self.EndGamePopUpTitle = "Practice makes perfect"
        else:
            self.EndGamePopUpTitle = "Congratulations"
        super().end_game()

    def end_game_text(self):
        return f"\nScore: {self.score / self.number_of_rounds * 100:.2f}%\n" \
               f"Time taken: {time.time() - self.startTime:.2f}s"

