from abc import ABC, abstractmethod

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class QuizLogic:
    """This abstract class is for the logic of the questions that get asked,
    i.e. calculating the correct answer and generating the question prompt"""
    def __init__(self):
        self.question = ""

    @abstractmethod
    def game_round(self):
        pass

    @abstractmethod
    def correct_answer(self):
        pass


class GameLogic:
    """This class is for all the game logic apart from the questions.
    e.g. how to set up a new round, how the game starts and ends, etc."""

    def __init__(self, quiz_logic):
        self.quiz = quiz_logic
        self.player_answer = None
        self.player_name = ""
        self.timestep = 0
        self.timestep_size = 0.1
        self.score = 0
        self.goal = 0
        self.start_time = 0
        self.clock = None
        self.help = ""
        self.prompt = ""
        self.end_game_pop_up_title = ""
        self.end_game_pop_up = None
        self.record_pop_up = None
        self.challenge_pop_up = None
        self.help_pop_up = None
        self.count_down = 3
        self.app = MDApp.get_running_app()

    def generate_end_game_pop_up(self):
        self.end_game_pop_up = MDDialog(title=self.end_game_pop_up_title,
                                        text=self.end_game_text(),
                                        buttons=[
                                  PlayAgainButton(),
                                  PopUpMenuButton(),
                                  RecordButton(),
                                  ],
                                        auto_dismiss=False,
                                        )

    def generate_record_pop_up(self):
        self.record_pop_up = MDDialog(title="New Record!",
                                      text="Congratulations",
                                      type="custom",
                                      content_cls=RecordDialog(),
                                      auto_dismiss=False,
                                      )

    def generate_challenge_pop_up(self, challenges_completed):
        medal = challenges_completed.pop()
        print(f"{medal} pop up")
        self.challenge_pop_up = MDDialog(title="Challenge Completed!",
                                      text=f"Congratulations, you completed the {medal} medal challenge",
                                      buttons=[
                                          ChallengeCloseButton(challenges_completed)
                                      ],
                                      auto_dismiss=False,
                                      )

    def generate_help_pop_up(self):
        self.help_pop_up = MDDialog(title="Help",
                                    text=self.help,
                                    buttons=[
                                      CloseButton(),
                                  ],
                                    md_bg_color=self.app.theme_cls.bg_dark,
                                    auto_dismiss=False,
                                    )

    def display_help(self):
        self.generate_help_pop_up()
        self.help_pop_up.open()

    def reset_countdown(self):
        self.count_down = 3
        self.app.root.ids["count_down_screen"].ids["count_down"].text = f"{self.count_down}"

    def start_countdown(self):
        self.reset()
        self.app.change_screen("count_down_screen")
        Clock.schedule_interval(self.update_count_down, 1)

    def reset(self):
        self.score = 0
        self.timestep = 0
        self.end_game_pop_up = None
        self.record_pop_up = None
        self.challenge_pop_up = None

    def update_count_down(self, *args):
        self.count_down -= 1
        self.app.root.ids["count_down_screen"].ids["count_down"].text = f"{self.count_down}"
        if self.count_down == 0:
            self.app.change_screen("game_screen")
            self.play_game()
        elif self.count_down < 0:
            Clock.unschedule(self.update_count_down)
            self.reset_countdown()

    @abstractmethod
    def play_game(self):
        self.app.root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.clock = Clock.schedule_interval(self.update, self.timestep_size)

    def update(self, *args):
        self.timestep += self.timestep_size
        self.app.root.ids["game_screen"].ids['clock_label'].text = f"{self.timestep:.3f}"

    @abstractmethod
    def start_round(self, *args):
        pass

    @abstractmethod
    def end_game(self, score=None):
        """
        Stop game clock, clear prompt, and open pop ups
        """
        if score is None:
            score = self.score
        self.clock.cancel()
        self.set_prompt("")
        self.open_pop_ups(score)

    def open_pop_ups(self, score=None):
        """
        Open the end game pop ups. This involves chaining together pop ups so that
        when one is closed the next appropriate one opens.

        e.g. If a challenge is completed and a record is broken, then the challenge
        pop up will open, followed by the record one once the challenge pop up is
        dismissed, and then finally the end game pop up.

        If no challenge is completed, but a record is broken, then it will first open
        the record pop up followed by the end game pop up.

        The implementation is that only the first pop up is called in the main code,
        with following pop ups opened by the first one being dismissed
        """
        if completed_challenges := self.newly_completed_challenges(score):
            # Save to the json file that any challenge has been completed, then
            # generate and open the pop ups
            self.challenges_update_and_open_pop_up(completed_challenges)
        else:
            # check if a record has been broken and act accordingly, otherwise open
            # the end game pop up
            self.records_check_and_open()

    def records_check_and_open(self):
        if self.any_records_broken():
            self.generate_record_pop_up()
            self.record_pop_up.open()
        else:
            self.generate_end_game_pop_up()
            self.end_game_pop_up.open()

    def any_records_broken(self):
        scores = self.app.records["scores"]
        if len(scores) < 5 or self.score > min(scores):
            return True
        return False

    def records_update(self):
        scores = self.app.records["scores"]

        if len(scores) < 5:
            # If there are less than 5 records, then always add player score
            self.app.records["names"].append(self.player_name)
            self.app.records["scores"].append(self.score)

        elif self.score > min(scores):
            # If there are more than 5 records, then add score if it's bigger than the
            # smallest existing score
            for i, score in enumerate(scores):
                if score == min(scores):
                    self.app.records["names"][i] = self.player_name
                    self.app.records["scores"][i] = self.score
        else:
            # No new record
            return

        # Sort records by score
        self.app.records["scores"], self.app.records["names"] = \
            zip(*sorted(zip(self.app.records["scores"], self.app.records["names"]),
                        reverse=True))

        # Convert to lists as these must be mutable next time we want to write
        self.app.records["scores"], self.app.records["names"] = \
            list(self.app.records["scores"]), list(self.app.records["names"])

        # Save to the Json file
        self.app.data[self.app.quiz_name][self.app.game_name]["records"] = self.app.records
        self.app.save()

    def set_player_name(self, text):
        self.player_name = text

    def newly_completed_challenges(self, score):
        medals = ["gold", "silver", "bronze"]
        return [medal for medal in medals if self.challenge_is_completed(score, medal)]

    def challenge_is_completed(self, score, medal: str):
        medal_num = {"bronze": 0, "silver": 1, "gold": 2}[medal]
        return self.app.challenges[self.app.quiz_name][self.app.game_name][medal_num].condition(score) and \
                not self.app.data[self.app.quiz_name][self.app.game_name]["completed_challenges"][medal]

    def challenge_update_and_open_pop_up(self, completed_challenges):
        medal = completed_challenges[-1]
        self.app.data[self.app.quiz_name][self.app.game_name]["completed_challenges"][medal] = True
        self.generate_challenge_pop_up(completed_challenges)
        self.challenge_pop_up.open()

    def challenges_update_and_open_pop_up(self, completed_challenges):
        self.challenge_update_and_open_pop_up(completed_challenges)
        self.app.check_and_unlock_level()

        # TODO This only shows a pop up for the hardest challenge completed. This probably requires chaining
        # the pop ups together in an analgous way to how challenges chains to records chains to the end game
        # pop up
        self.challenge_pop_up.open()
        self.app.save()
        self.app.root.ids["MenuList"].ids[self.app.quiz_name + " button"].completed_quiz = \
            self.app.completed_quiz(self.app.quiz_name)

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
        self.player_answer = self.app.root.ids["game_screen"].ids.PlayerInput.text
        if not self.is_player_correct():
            self.incorrect_answer_action()
        else:
            self.correct_answer_action()
        Clock.schedule_once(self.start_round, 0.5 if self.is_player_correct() else 1)

    def set_prompt(self, text):
        self.prompt = text
        self.app.root.ids["game_screen"].ids.prompt.text = self.prompt

    def incorrect_answer_action(self):
        self.app.root.ids["game_screen"].ids.highlight.run_correct_answer_animation(correct=False)
        self.set_prompt(f"Unlucky. The correct answer is {self.quiz.correct_answer()}")

    def correct_answer_action(self):
        """
        Actions to be carried out when player is correct (e.g. increment score)
        :return:
        """
        self.score += 1
        self.app.root.ids["game_screen"].ids.highlight.run_correct_answer_animation(correct=True)
        self.app.root.ids["game_screen"].ids.score.text = f"Score: {self.score}"
        self.set_prompt("Correct!")

    def is_player_correct(self):
        return self.player_answer == str(self.quiz.correct_answer())


class RecordButton(MDFlatButton):
    pass


class PopUpMenuButton(MDFlatButton):
    pass


class PlayAgainButton(MDFlatButton):
    pass


class StartGameButton(MDFlatButton):
    pass


class HelpButton(MDFlatButton):
    pass


class ChallengeCloseButton(MDFlatButton):
    def __init__(self, challenges_completed):
        super().__init__()
        self.challenges_completed = challenges_completed


class CloseButton(MDFlatButton):
    pass


class ClockLabel(MDLabel):
    pass


class RecordDialog(BoxLayout):
    pass
