# Создайте программу, в которой пользователь сможет ввести временной
# промежуток в виде количества дней, часов, минут и секунд и узнать общее
# количество секунд, составляющее введенный отрезок.

DAYS_TO_SECONDS = 24 * 60 * 60
HOURS_TO_SECONDS = 60 * 60
MINUTES_TO_SECONDS = 60

print('Программа переводит время, заданное пользователем в крупных единицах, в секунды.')
units_of_time = ['дней', 'часов', 'минут', 'секунд']
days, hours, minutes, seconds = [int(input(f'Введите количество {units_of_time[i]}: ')) \
                                 for i in range(len(units_of_time))]
to_seconds = days * DAYS_TO_SECONDS + hours * HOURS_TO_SECONDS + minutes * MINUTES_TO_SECONDS + seconds
print(f'Это время аналогично {to_seconds} секундам.')
