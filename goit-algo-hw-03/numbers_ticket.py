"""
Щоб виграти головний приз лотереї, необхідний збіг кількох номерів на лотерейному квитку з числами, 
що випали випадковим чином і в певному діапазоні під час чергового тиражу. 
Наприклад, необхідно вгадати шість чисел від 1 до 49 чи п'ять чисел від 1 до 36 тощо.

Вам необхідно написати функцію get_numbers_ticket(min, max, quantity), 
яка допоможе генерувати набір унікальних випадкових чисел для таких лотерей.

Вона буде повертати випадковий набір чисел у межах заданих параметрів, 
причому всі випадкові числа в наборі повинні бути унікальні.
"""


from random import randint


def get_numbers_ticket(min, max, quantity):

    numbers = []

    # Поки довжина списку не буде дорівнювати кількості цифр для виводу,
    # генеруємо нове число та перевіряємо чи таке є у скписку, та додаємо унікальне число до списку
    while len(numbers) < quantity:
        number = randint(min, max)
        if number not in numbers:
            numbers.append(number)

    # Сортуємо список
    numbers.sort()

    return numbers


def main():

    # Введення та валідація мінімального значення
    while True:
        try:
            min = int(input("Input Min number (from 1 to 1000): "))
            if min < 1 or min > 1000:
                raise Exception
            else:
                break
        except (ValueError, Exception):
            print("Sorry. Min number must be int (from 1 to 1000)\n")

    # Введення та валідація максимального значення
    while True:
        try:
            max = int(input("Input Max number (less than 1000): "))
            if max > 1000 or max < 1:
                raise Exception
            else:
                break
        except (ValueError, Exception):
            print("Sorry. Max number must be int (from 1 to 1000)\n")

    # Введення та валідація клькості цифр для виводу
    while True:
        try:
            quantity = int(input("Input Quantity of numbers: "))
            if quantity > max - min or quantity < 1:
                raise Exception
            else:
                break
        except (ValueError, Exception):
            print(f"Sorry. Quantity must be int from 1 to {max - min}\n")

    lottery_numbers = get_numbers_ticket(min, max, quantity)
    print(f"Your lottery numbers: {lottery_numbers}")


if __name__ == "__main__":
    main()
