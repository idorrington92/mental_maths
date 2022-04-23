from abc import ABC, abstractmethod

from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class QuizLogic:
    """This abstract class is for the logic of the questions that get asked,
    i.e. calculating the correct answer and generating the question prompt"""

    @abstractmethod
    def game_round(self):
        pass

    @abstractmethod
    def correct_answer(self):
        pass


class GameLogic:
    """This class is for all the game logic apart from the questions.
    e.g. how to set up a new round, how the game starts and ends, etc."""

    def __init__(self):
        self.player_answer = None
        self.timestep = 0
        self.timestep_size = 0.1
        self.score = 0
        self.goal = 0
        self.startTime = 0
        self.help = ""
        self.prompt = ""
        self.EndGamePopUpTitle = ""
        self.PopUp = None
        self.HelpPopUp = None

    def generate_end_game_pop_up(self):
        self.PopUp = MDDialog(title=self.EndGamePopUpTitle,
                              text=self.end_game_text(),
                              buttons=[
                                  PlayAgainButton(),
                                  PopUpMenuButton(),
                                  ],
                              auto_dismiss=False,
                              )

    def generate_help_pop_up(self):
        self.HelpPopUp = MDDialog(title="Help",
                                  text=self.help,
                                  buttons=[
                                      CloseButton(),
                                  ],
                                  md_bg_color=MDApp.get_running_app().theme_cls.bg_dark,
                                  auto_dismiss=False,
                                  )

    def display_help(self):
        self.generate_help_pop_up()
        self.HelpPopUp.open()

    @abstractmethod
    def play_game(self):
        self.timestep = 0
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)

    def update(self, *args):
        self.timestep += self.timestep_size
        MDApp.get_running_app().root.ids[self.game_id].ids['clock_label'].text = f"{self.timestep:.3f}"

    @abstractmethod
    def start_round(self, *args):
        pass

    @abstractmethod
    def game_round(self):
        """
        Set up game prerequisites. For example, generating random numbers and assigning the prompt for the player
        :return: None:
        """

    @abstractmethod
    def end_game(self):
        """
        End game display
        :return:
        """
        self.clock.cancel()
        self.set_end_game_text()
        self.generate_end_game_pop_up()
        self.PopUp.open()

    @abstractmethod
    def set_end_game_text(self):
        pass

    def end_game_text(self):
        return "End game"

    def player_input(self):
        """
        Checks player input is valid, then checks if player wants help, quit, or has entered the correct answer.
        Otherwise they must have entered an incorrect answer.
        :return: Boolean
            False indicates that the game should not move on (either because the input was invalid, the player asked for
            help to be displayed, or the player quit. True indicates the game player entered a valid answer and the game
            should move on to the next round.
        """
        self.player_answer = MDApp.get_running_app().root.ids[self.game_id].ids.PlayerInput.text
        if not self.is_player_correct():
            self.incorrect_answer_action()
        else:
            self.correct_answer_action()
        Clock.schedule_once(self.start_round, 0.5 if self.is_player_correct() else 1)

    def incorrect_answer_action(self):
        MDApp.get_running_app().root.ids[self.game_id].ids.highlight.run_correct_answer_animation(correct=False)
        self.prompt = f"Unlucky. The correct answer is {self.correct_answer()}"
        MDApp.get_running_app().root.ids[self.game_id].ids.prompt.text = self.prompt

    def correct_answer_action(self):
        """
        Actions to be carried out when player is correct (e.g. increment score)
        :return:
        """
        self.score += 1
        MDApp.get_running_app().root.ids[self.game_id].ids.highlight.run_correct_answer_animation(correct=True)
        self.prompt = "Correct!"
        MDApp.get_running_app().root.ids[self.game_id].ids.prompt.text = self.prompt

    @abstractmethod
    def correct_answer(self):
        """
        Returns the correct answer
        """
        pass

    def is_player_correct(self):
        return self.player_answer == str(self.correct_answer())


class Game(ABC, QuizLogic, GameLogic):
    pass


class MenuButton(MDFlatButton):
    pass


class PopUpMenuButton(MDFlatButton):
    pass


class PlayAgainButton(MDFlatButton):
    pass


class StartGameButton(MDFlatButton):
    pass


class HelpButton(MDFlatButton):
    pass


class CloseButton(MDFlatButton):
    pass


class ClockLabel(MDLabel):
    pass
