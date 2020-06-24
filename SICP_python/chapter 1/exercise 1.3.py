def sum_two_max_squares(a1,a2,a3):
    numbers = [a1,a2,a3]
    numbers.sort()
    x1, x2 = numbers[1:3]
    return x1**2 + x2**2


print(sum_two_max_squares(3,2,1))