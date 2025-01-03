# Количество энергии, требуемое для повышения температуры одного грамма материала на один градус Цельсия,
# называется удельной теплоемкостью материала и обозначается буквой C. Общее количество энергии (q),
# требуемое для повышения температуры m граммов материала на ΔT градусов Цельсия, может быть рассчитано по формуле:
# q = m*C*ΔT
# Напишите программу, запрашивающую у пользователя массу воды и требуемую разницу температур.
# На выходе вы должны получить количество энергии, которое необходимо добавить или отнять для достижения
# желаемого температурного изменения.
# Подсказка. Удельная теплоемкость воды равна 4,183 Дж / кг·К. Поскольку вода обладает плотностью 1 грамм на миллилитр,
# в данном упражнении можно взаимозаменять граммы и миллилитры.
# Расширьте свою программу таким образом, чтобы выводилась также стоимость сопутствующего нагрева воды.
# Обычно принято измерять электричество в кВт·ч, а не в джоулях. Для данного примера предположим,
# что электричество обходится нам в 4,7 рубля за один кВт·ч. Используйте свою программу для подсчета стоимости
# нагрева одной чашки кофе. Подсказка. Для решения второй части задачи вам придется найти способ перевода
# единиц электричества между джоулями и кВт·ч.

WATER_HEAT_CAPACITY = 4183
HEATER_EFFICIENCY = 0.7
JOULE_TO_KWH = 2.78e-7
COST_PER_KWH = 4.7

print('Данная программа расчитывает необходимое количество энергии для нагрева воды на указанную температу.')
mass = float(input('Введите массу воды (масса воды в килограммах и объём в литрах равны): '))
dt = float(input('На сколько градусов необходимо нагреть воду: '))

q = mass * WATER_HEAT_CAPACITY * dt
kwh = q / HEATER_EFFICIENCY * JOULE_TO_KWH
cost = kwh * COST_PER_KWH

print(f'Чтобы нагреть {mass:.1f} литров воды на {dt:.1f} градусов, понадобится {q:.0f} Джоулей, {kwh:.0f} кв/ч и {cost:.1f} рублей')

