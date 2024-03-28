"""
Необхідно створити функцію generator_numbers, яка буде аналізувати текст, ідентифікувати всі дійсні числа, 
що вважаються частинами доходів, і повертати їх як генератор. Дійсні числа у тексті записані без помилок, 
чітко відокремлені пробілами з обох боків. Також потрібно реалізувати функцію sum_profit, 
яка буде використовувати generator_numbers для підсумовування цих чисел і обчислення загального прибутку.

Вимоги до завдання:
1. Функція generator_numbers(text: str) повинна приймати рядок як аргумент і повертати генератор, 
що ітерує по всіх дійсних числах у тексті. Дійсні числа у тексті вважаються записаними без помилок і чітко відокремлені пробілами з обох боків.
2. Функція sum_profit(text: str, func: Callable) має використовувати генератор generator_numbers 
для обчислення загальної суми чисел у вхідному рядку та приймати його як аргумент при виклику.
"""


import re
from typing import Callable


def generator_numbers(text: str):
    pattern = r"\b\d+\.\d{2}\b"
    matches = re.findall(pattern, text)

    for match in matches:
        yield float(match)


def sum_profit(text: str, func: Callable):
    total_income = sum(func(text))

    return total_income


def main():
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


if __name__ == "__main__":
    main()
