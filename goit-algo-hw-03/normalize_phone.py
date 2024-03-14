"""
У вашій компанії ведеться активна маркетингова кампанія за допомогою SMS-розсилок. 
Для цього ви збираєте телефонні номери клієнтів із бази даних, але часто стикаєтеся з тим, 
що номери записані у різних форматах. Наприклад:

"    +38(050)123-32-34"
"     0503451234"
"(050)8889900"
"38050-111-22-22"
"38050 111 22 11   "

Ваш сервіс розсилок може ефективно відправляти повідомлення лише тоді, коли номери телефонів представлені у коректному форматі. 
Тому вам необхідна функція, яка автоматично нормалізує номери телефонів до потрібного формату, 
видаляючи всі зайві символи та додаючи міжнародний код країни, якщо потрібно.

Розробіть функцію normalize_phone(phone_number), що нормалізує телефонні номери до стандартного формату, 
залишаючи тільки цифри та символ '+' на початку. Функція приймає один аргумент - рядок з телефонним номером у будь-якому форматі 
та перетворює його на стандартний формат, залишаючи тільки цифри та символ '+'. 
Якщо номер не містить міжнародного коду, функція автоматично додає код '+38' (для України). 
Це гарантує, що всі номери будуть придатними для відправлення SMS.

Вимоги до завдання:
Параметр функції phone_number - це рядок з телефонним номером у різноманітних форматах.
Функція видаляє всі символи, крім цифр та символу '+'.
Якщо міжнародний код відсутній, функція додає код '+38'. Це враховує випадки, 
коли номер починається з '380' (додається лише '+') та коли номер починається без коду (додається '+38').
Функція повертає нормалізований телефонний номер у вигляді рядка.
"""

import re


def normalize_phone(phone_number):

    pattern = r"[\D]"
    replacement = ""

    # Прибираємо з номеру все окрім цифр
    normalized_phone = re.sub(pattern, replacement, phone_number)

    # Доповнюємо номер до формату +380ххххххххх
    if normalized_phone.startswith("380"):
        normalized_phone = f"+{normalized_phone}"
    elif normalized_phone.startswith("80"):
        normalized_phone = f"+3{normalized_phone}"
    elif normalized_phone.startswith("0"):
        normalized_phone = f"+38{normalized_phone}"

    return normalized_phone


def main():

    raw_numbers = [
        "067\\t123 4567",
        "(095) 234-5678\\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]

    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    print("Normalized phone numbers for SMS-sending:", sanitized_numbers)


if __name__ == "__main__":
    main()