def a_plus_abs_b(a, b):
    if b > 0:
        c = a + b
    else:
        c = a - b
    return c

print(a_plus_abs_b(3, -2))
