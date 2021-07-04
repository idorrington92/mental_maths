import numpy.random as rand
import time


class TwoDigitAddition:
    def __init__(self, number_of_rounds):
        self.number1 = 0
        self.number2 = 0
        self.player_answer = 0
        self.score = 0
        self.startTime = 0
        self.number_of_rounds = number_of_rounds
        self.help = "..."

        self.play_game()

    def play_game(self):
        self.startTime = time.time()
        for g_round in range(1, self.number_of_rounds + 1):
            print(f"Round {g_round}")
            if not self.game_round():  # game_round returns false when player quits
                break
        else:
            self.end_game()  # Player reaches end of game without quiting

    def game_round(self):
        self.number1 = rand.randint(10, 999)
        self.number2 = rand.randint(10, 99)

        # Keep looping until player enters a valid (i.e. numeric or 'q') answer
        while not self.handle_player_input(f"{self.number1} + {self.number2} = "):
            if self.player_answer in ('q', 'Q'):  # Player quits
                return False
        return True

    def end_game(self):
        print(f"Score: {100 * self.score / self.number_of_rounds:.2f}%")
        print(f"Time taken: {time.time() - self.startTime:.2f}s")

    def handle_player_input(self, prompt):
        self.player_answer = input(prompt)

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
            self.score += 1
            print("Correct!")
            return True

        print(f"Unlucky. The correct answer is {self.correct_answer()}")
        return True

    def correct_answer(self):
        return self.number1 + self.number2

    def is_player_correct(self):
        return self.player_answer == str(self.correct_answer())

    def is_valid_input(self):
        return self.player_answer in ("q", "Q", "h", "H") or self.player_answer.isnumeric()
