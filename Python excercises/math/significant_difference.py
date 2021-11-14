# Критерий U достоверности различий выборок

from icecream import ic
import random
from scipy.stats import mannwhitneyu

min_bound_selection = 300
max_bound_selection = 400
min_bound_number1 = 0
max_bound_number1 = 100
min_bound_number2 = 0
max_bound_number2 = 105

#Генерация выборок

selection1 = []
selection2 = []
for i in range(random.randint(min_bound_selection, max_bound_selection)):
    selection1.append(random.uniform(min_bound_number1, max_bound_number1))
for i in range(random.randint(min_bound_selection, max_bound_selection)):
    selection2.append(random.uniform(min_bound_number2, max_bound_number2))
#selection1 = [i for i in range(0, 100)]
#selection2 = [i for i in range(101, 257)]
print(f'p - вероятность того, что нулевая гипотеза подтверждена случайным совпадением чисел, '
      f'без реальной разницы в параметрах распределения')
ic(len(selection1))
ic(len(selection2))

U1, p = mannwhitneyu(selection1, selection2, use_continuity=True, alternative='two-sided')
ic('non equal',U1, p)
U1, p = mannwhitneyu(selection1, selection2, use_continuity=True, alternative='less')
ic('less', U1, p)
U1, p = mannwhitneyu(selection1, selection2, use_continuity=True, alternative='greater')
ic('greater', U1, p)