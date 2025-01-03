# Напишите программу для расчета скорости объекта во время его соприкосновения с землей.
# Пользователь должен задать высоту в метрах, с которой объект будет отпущен. Поскольку объекту не будет придаваться
# ускорение, примем его начальную скорость за 0 м/с. Предположим, что ускорение свободного падения равно 9,8 м/с2.
# При известных начальной скорости (vi), ускорении (a) и дистанции (d) можно вычислить скорость при соприкосновении
# объекта с землей по формуле
# (vi**2 + 2*a*d)**0.5

G = 9.8

print('Данная программа расчитывает скорость соприкосновения объекта с землёй, после свободного падения')
#v_start = float(input('Введите начальную скорость объекта: '))
h = float(input('Введите начальную высоту падения объекта: '))
#v = (v_start**2 + 2*G*h)**0.5
v = (2*G*h)**0.5
print(f'Скорость столкновения объекта, сброшенного с высоты в {h} метров, с землёй будет составлять {v} м/с.')