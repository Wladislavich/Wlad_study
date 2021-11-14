# Определить с помощью включения-исключения вероятность того, что в случайной строке длины 20 над алфавитом из 10
# символов встретятся все 10 символов.

import random

L = 20
circles_cnt = 10000
alhabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и']
counter = 0

for _ in range(circles_cnt):
    string = ''
    for _ in range(L):
        string += random.choice(alhabet)
        letter_cnt = len(set(string))
    if letter_cnt == 10:
        counter += 1
#print(string, len(string), letter_cnt)
print(counter / circles_cnt)