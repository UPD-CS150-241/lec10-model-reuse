from main import GuessingGameModel, Verdict

def test_make_guess_oob():
    answer = 50
    attempts = 8
    min_guess = 1
    max_guess = 100

    model = GuessingGameModel(answer, attempts, min_guess, max_guess)

    verdict = model.make_guess(101)

    assert verdict == Verdict.OUT_OF_BOUNDS
    assert not model.is_game_over
    assert model.attempts_left == attempts
    assert model.max_guess == max_guess
    assert model.min_guess == min_guess
    assert model.answer == answer
