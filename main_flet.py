import random
from typing import Protocol

import flet as ft

from model import GuessingGameModel, Verdict


class GuessObserver(Protocol):
    def handle_guess(self, guess: int):
        ...


class GuessingGameView:
    def __init__(self, min_guess: int, max_guess: int):
        self._min_guess = min_guess
        self._max_guess = max_guess
        self._attempts_left_text = ft.Text()
        self._input_field = ft.TextField(label='Enter a guess'
                                         f'[{self._min_guess}-{self._max_guess}]',
                                         on_submit=self._on_guess)
        self._feedback_text = ft.Text()

        self._guess_observer: GuessObserver | None = None
        self._page: ft.Page | None = None

    def _refresh_page(self):
        if self._page:
            self._page.update()

    def _on_guess(self, _: ft.ControlEvent):
        if self._guess_observer:
            if self._input_field.value is None:
                return

            try:
                guess = int(self._input_field.value)
                self._guess_observer.handle_guess(guess)
            except ValueError:
                pass

            self._input_field.focus()

    def register_guess_observer(self, callback: GuessObserver):
        self._guess_observer = callback

    def update_attempts_left(self, attempts_left: int):
        self._attempts_left_text.value = f'Attempts left: {attempts_left}'

        self._refresh_page()

    def entrypoint(self, page: ft.Page):
        self._page = page

        page.add(self._attempts_left_text)
        page.add(self._input_field)
        page.add(self._feedback_text)

        self._input_field.focus()

    def show_verdict(self, verdict: Verdict):
        match verdict:
            case Verdict.CORRECT:
                self._feedback_text.value = 'You win!'
            case Verdict.TOO_HIGH:
                self._feedback_text.value = 'Too high'
            case Verdict.TOO_LOW:
                self._feedback_text.value = 'Too low'
            case Verdict.OUT_OF_BOUNDS:
                self._feedback_text.value = (
                    'Guess must be between'
                    f'{self._min_guess} and {self._max_guess} (inclusive)'
                )
            case Verdict.GAME_IS_OVER:
                self._feedback_text.value = 'Game is over'

        self._refresh_page()

    def show_lose_message(self, answer: int):
        self._feedback_text.value = f'You lose; answer is {answer}'
        self._refresh_page()


class GuessingGameController:
    def __init__(self, model: GuessingGameModel, view: GuessingGameView):
        self._model = model
        self._view = view

    def start(self):
        self._view.register_guess_observer(self)
        self._view.update_attempts_left(self._model.attempts_left)
        ft.app(self._view.entrypoint)

    def handle_guess(self, guess: int):
        model = self._model
        verdict = model.make_guess(guess)

        self._view.update_attempts_left(self._model.attempts_left)

        if model.is_game_over and not model.did_player_win:
            self._view.show_lose_message(model.answer)
        else:
            self._view.show_verdict(verdict)


def main():
    answer = random.randint(1, 100)
    min_guess = 1
    max_guess = 100
    model = GuessingGameModel(answer, 8, min_guess, max_guess)
    view = GuessingGameView(min_guess, max_guess)
    controller = GuessingGameController(model, view)

    controller.start()


if __name__ == '__main__':
    main()
