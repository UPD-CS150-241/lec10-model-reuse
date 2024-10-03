from enum import StrEnum, auto


class Verdict(StrEnum):
    CORRECT = auto()
    TOO_HIGH = auto()
    TOO_LOW = auto()
    OUT_OF_BOUNDS = auto()
    GAME_IS_OVER = auto()


class GuessingGameModel:
    def __init__(self, answer: int, attempts_left: int, min_guess: int, max_guess: int):
        self._answer = answer
        self._attempts_left = attempts_left
        self._min_guess = min_guess
        self._max_guess = max_guess
        self._is_game_over = False
        self._did_player_win = False

    @property
    def did_player_win(self):
        return self._did_player_win

    @property
    def answer(self):
        return self._answer

    @property
    def max_guess(self):
        return self._max_guess

    @property
    def min_guess(self):
        return self._min_guess

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def attempts_left(self) -> int:
        return self._attempts_left

    def make_guess(self, guess: int) -> Verdict:
        verdict = self._check_guess(guess)

        match verdict:
            case Verdict.CORRECT:
                self._is_game_over = True
                self._did_player_win = True
                self._attempts_left -= 1

            case Verdict.TOO_LOW | Verdict.TOO_HIGH:
                self._attempts_left -= 1

            case _:
                pass

        if self._attempts_left == 0:
            self._is_game_over = True

        return verdict

    def _check_guess(self, guess: int) -> Verdict:
        if self._is_game_over:
            return Verdict.GAME_IS_OVER
        elif guess < self._min_guess or guess > self._max_guess:
            return Verdict.OUT_OF_BOUNDS
        elif guess == self._answer:
            return Verdict.CORRECT
        elif guess < self._answer:
            return Verdict.TOO_LOW
        else:
            return Verdict.TOO_HIGH
