def cubrt(x):
    return cub_iter(1.0 , x, None)

def cub_iter(guess, x, old_guess):
    if good_enough(guess, x, old_guess):
        return guess
    else:
        return cub_iter(improve(guess, x), x, guess)


def improve(guess, x):
    imp = (x / guess**2 + 2*guess)/3
    return imp


def good_enough(guess, x, old_guess):
    if old_guess:
        return abs((guess-old_guess)/old_guess) < 0.001
    else:
        return False

print(cubrt(64))