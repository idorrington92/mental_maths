from abc import ABC, abstractmethod
import time


class Game(ABC):
    def __init__(self, number_of_rounds):
        self.player_answer = 0
        self.score = 0
        self.startTime = 0
        self.number_of_rounds = number_of_rounds
        self.help = ""
        self.prompt = ""

        # self.play_game()

    def play_game(self):
        self.startTime = time.time()
        for g_round in range(1, self.number_of_rounds + 1):
            print(f"Round {g_round}")
            if not self.game_round():  # game_round returns false when player quits
                break
        else:
            self.end_game()  # Player reaches end of game without quiting

    def game_round(self):
        """
        Set up game prerequisites. For example, generating random numbers and assigning the prompt for the player
        :return: Boolean:
            False if player has quit, True otherwise.
        """
        return self.player_input()

    def player_input(self):
        """
        Keep looping until player enters a valid (i.e. numeric or 'q') answer.
        :return: Boolean
            Returns False if player quits, True otherwise.
        """
        while not self.handle_player_input():
            if self.player_answer in ('q', 'Q'):  # Player quits
                return False
        return True

    def end_game(self):
        """
        End game display
        :return:
        """
        print(f"\nScore: {100 * self.score / self.number_of_rounds:.2f}%")
        print(f"Time taken: {time.time() - self.startTime:.2f}s")

    def handle_player_input(self):
        """
        Checks player input is valid, then checks if player wants help, quit, or has entered the correct answer.
        Otherwise they must have entered an incorrect answer.
        :return: Boolean
            False indicates that the game should not move on (either because the input was invalid, the player asked for
            help to be displayed, or the player quit. True indicates the game player entered a valid answer and the game
            should move on to the next round.
        """
        self.player_answer = input(self.prompt)

        if not self.is_valid_input():
            print("Invalid input. Please enter numeric value to play or Q to quit\n")
            return False

        if self.player_answer in ("h", "H"):
            print(self.help)
            return False

        if self.player_answer in ("q", "Q"):
            print("Exiting program")
            return False

        if self.is_player_correct():
            self.player_is_correct()
            return True

        print(f"Unlucky. The correct answer is {self.correct_answer()}")
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
