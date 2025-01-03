# Программа, которую вы напишете, должна начинаться с запроса у пользователя суммы заказа в ресторане. После этого
# должен быть произведен расчет налога и чаевых официанту. Вы можете использовать принятую  в вашем регионе налоговую
# ставку для подсчета суммы сборов. В качестве чаевых мы оставим 18 % от стоимости заказа без учета налога.
# На выходе программа должна отобразить отдельно налог, сумму чаевых и итог, включая обе составляющие.
# Форматируйте вывод таким образом, чтобы все числа отображались с двумя знаками после запятой.

TAX_RATE = 0.13
TIPS_RATE = 0.18

print('Эта программа расчитывает стоимость заказа, включая налоги и чаевые.')
cost = int(input('введите стоимость заказа в рублях: '))
tax = cost * TAX_RATE
tips = cost * TIPS_RATE
total = cost + tips
print(f'Налог: {tax:.2f} руб., чаевые: {tips:.2f} руб., общая сумма, включая налоги и чаевые: {total:.2f} руб.')

