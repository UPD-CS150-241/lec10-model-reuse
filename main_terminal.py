import random

from model import GuessingGameModel, Verdict


class GuessingGameView:
    def ask_for_guess(self, min_guess: int, max_guess: int) -> int:
        return int(input('Enter a guess'
                         f' [{min_guess}-{max_guess}]: '))

    def print_verdict(self, verdict: Verdict, min_guess: int, max_guess: int):
        match verdict:
            case Verdict.CORRECT:
                print('You win!')
            case Verdict.TOO_LOW:
                print('Too low')
            case Verdict.TOO_HIGH:
                print('Too high')
            case Verdict.OUT_OF_BOUNDS:
                print('Guess must be between'
                      f'{min_guess} and {max_guess} (inclusive)')
            case Verdict.GAME_IS_OVER:
                print('Game is over')

    def print_lose_message(self, answer: int):
        print(f'You lose; answer is {answer}')


class GuessingGameController:
    def __init__(self, model: GuessingGameModel, view: GuessingGameView):
        self._model = model
        self._view = view

    def start(self):
        model = self._model
        view = self._view

        while not model.is_game_over:
            guess = view.ask_for_guess(model.min_guess, model.max_guess)
            verdict = model.make_guess(guess)
            view.print_verdict(verdict, model.min_guess, model.max_guess)

        if not model.did_player_win:
            view.print_lose_message(model.answer)


def main():
    answer = random.randint(1, 100)
    model = GuessingGameModel(answer, 8, 1, 100)
    view = GuessingGameView()
    controller = GuessingGameController(model, view)

    controller.start()


if __name__ == '__main__':
    main()
