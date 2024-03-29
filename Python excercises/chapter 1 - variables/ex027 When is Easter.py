# Пасха традиционно празднуется в воскресенье, следующее за первым
# полнолунием после дня весеннего равноденствия. Поскольку здесь есть
# зависимость от фазы луны, фиксированной даты для этого праздника
# в григорианском календаре не существует. Фактически Пасха может вы-
# пасть на любую дату между 22 марта и 25 апреля. День и месяц Пасхи для
# конкретного года можно вычислить по следующему алгоритму:
# Напишите программу, реализующую этот алгоритм. Пользователь дол-
# жен ввести год, для которого его интересует дата Пасхи, и получить ответ
# на свой вопрос.


print(f'Программа расчитывает дату Пасхи для выбранного года')
year = int(input('Введите год, для которого необходимо расчитать дату Пасхи: '))
a = year % 19
b = year // 100
c = year % 100
d = b // 4
e = b % 4
f = (b + 8) // 25
g = (b - f + 1) // 3
h = (19*a + b - d - g +15) % 30
i = c // 4
k = c % 4
l = (32 + 2*e + 2*i - h - k) % 7
m = (a + 11*h + 22*l) // 451
month = (h + l + 7*m + 114) // 31
day = 1 + (h + l - 7*m + 114) % 31
print(f'Пасха будет {day}.{month}.{year}')
