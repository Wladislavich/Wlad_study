def sqrt(x):
    return sqrt_iter(1.0 , x, None)

def sqrt_iter(guess, x, old_guess):
    if good_enough(guess, x, old_guess):
        return guess
    else:
        return sqrt_iter(improve(guess, x), x, guess)


def improve(guess, x):
    return average(guess, x / guess)


def average(x, y):
    return (x + y) / 2


def good_enough(guess, x, old_guess):
    if old_guess:
        return abs((guess-old_guess)/old_guess) < 0.001
    else:
        return False





print(sqrt(0.00004))