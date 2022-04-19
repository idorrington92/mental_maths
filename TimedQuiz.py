from abc import ABC, abstractmethod
import time

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from Game import Game


class TimedQuiz(Game):
    def __init__(self):
        self.player_answer = None
        self.score = 0
        self.startTime = 0
        self.number_of_rounds = 3
        self.g_round = 0
        self.help = ""
        self.prompt = ""
        self.EndGamePopUpTitle = ""
        self.PopUp = None
        self.HelpPopUp = None
        self.generate_start_game_pop_up()
        self.PopUp.open()

    def generate_start_game_pop_up(self):
        self.PopUp = MDDialog(title=MDApp.get_running_app().game_name,
                              text=self.short_description,
                              size_hint=[.8, .8],
                              # background_color=MDApp.get_running_app().theme_cls.bg_darkest,
                              md_bg_color=MDApp.get_running_app().theme_cls.bg_dark,
                              buttons=[
                                  StartGameButton(),
                                  MenuButton(),
                                  HelpButton(),
                              ],
                              auto_dismiss=False,
                              )

    def generate_end_game_pop_up(self):
        self.PopUp = MDDialog(title=self.EndGamePopUpTitle,
                              text=f"\nScore: {100 * self.score / self.number_of_rounds:.2f}%\n"
                                   f"Time taken: {time.time() - self.startTime:.2f}s",
                              size_hint=[.8, .8],
                              #background_color=MDApp.get_running_app().theme_cls.bg_darkest,
                              md_bg_color=MDApp.get_running_app().theme_cls.bg_dark,
                              buttons=[
                                  PlayAgainButton(),
                                  MenuButton(),
                                  ],
                              auto_dismiss=False,
                              )

    def generate_help_pop_up(self):
        self.HelpPopUp = MDDialog(title="Help",
                                  text=self.help,
                                  size_hint=[.8, .8],
                                  #background_color=MDApp.get_running_app().theme_cls.bg_darkest,
                                  buttons=[
                                      CloseButton(),
                                  ],
                                  md_bg_color=MDApp.get_running_app().theme_cls.bg_dark,
                                  auto_dismiss=False,
                                  )

    def display_help(self):
        self.generate_help_pop_up()
        self.HelpPopUp.open()

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

    def player_input(self):
        """
        Keep looping until player enters a valid (i.e. numeric or 'q') answer.
        :return: Boolean
            Returns False if player quits, True otherwise.
        """
        self.player_answer = MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.text
        self.handle_player_input()
        if self.player_answer in ('q', 'Q'):  # Player quits
            return False

        # Start next round
        self.start_round()
        return True

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
        self.generate_end_game_pop_up()
        self.PopUp.open()

    def end_game_score(self):
        return f"\nScore: {self.score:.2f}%\n" \
               f"Time taken: {time.time() - self.startTime:.2f}s"

    def handle_player_input(self):
        """
        Checks player input is valid, then checks if player wants help, quit, or has entered the correct answer.
        Otherwise they must have entered an incorrect answer.
        :return: Boolean
            False indicates that the game should not move on (either because the input was invalid, the player asked for
            help to be displayed, or the player quit. True indicates the game player entered a valid answer and the game
            should move on to the next round.
        """
        if not self.is_valid_input():
            print("Invalid input. Please enter numeric value to play or Q to quit\n")
            return False

        if self.player_answer in ("h", "H"):
            print(self.help)
            return False

        if self.player_answer in ("q", "Q"):
            print("Exiting program")
            return False

        if not self.is_player_correct():
            print(f"Unlucky. The correct answer is {self.correct_answer()}")
            return True

        self.player_is_correct()
        return True

    def player_is_correct(self):
        """
        Actions to be carried out when player is correct (e.g. increment score)
        :return:
        """
        self.score += 1
        print("Correct!")

    @abstractmethod
    def correct_answer(self):
        """
        Returns the correct answer
        """
        pass

    def is_player_correct(self):
        return self.player_answer == str(self.correct_answer())

    def is_valid_input(self):
        return self.player_answer in ("q", "Q", "h", "H") or self.player_answer.isnumeric()

class MenuButton(MDFlatButton):
    pass

class PlayAgainButton(MDFlatButton):
    pass

class StartGameButton(MDFlatButton):
    pass

class HelpButton(MDFlatButton):
    pass

class CloseButton(MDFlatButton):
    pass
