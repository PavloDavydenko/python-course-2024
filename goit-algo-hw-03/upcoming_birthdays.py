"""
У межах вашої організації, ви відповідаєте за організацію привітань колег з днем народження. 
Щоб оптимізувати цей процес, вам потрібно створити функцію get_upcoming_birthdays, 
яка допоможе вам визначати, кого з колег потрібно привітати.

У вашому розпорядженні є список users, кожен елемент якого містить інформацію про ім'я користувача 
та його день народження. Оскільки дні народження колег можуть припадати на вихідні, 
ваша функція також повинна враховувати це та переносити дату привітання на наступний робочий день, якщо необхідно.

Вимоги до завдання:
1. Параметр функції users - це список словників, де кожен словник містить ключі name (ім'я користувача, рядок) 
та birthday (день народження, рядок у форматі 'рік.місяць.дата').
2. Функція має визначати, чиї дні народження випадають вперед на 7 днів включаючи поточний день. 
Якщо день народження припадає на вихідний, дата привітання переноситься на наступний понеділок.
3. Функція повертає список словників, де кожен словник містить інформацію про користувача (ключ name) 
та дату привітання (ключ congratulation_date, дані якого у форматі рядка 'рік.місяць.дата').
"""


from datetime import datetime, timedelta


def get_upcoming_birthdays(users):

    today = datetime.today()
    upcoming_birthdays = []

    for user in users:

        # Створюємо об'єкт datetime з дати дня народження користувача
        user_birthday = datetime.strptime(user["birthday"], "%Y.%m.%d")

        # Визначаємо дату народження в поточному році
        user_birthday_this_year = user_birthday.replace(year=today.year)

        # Якщо день народження пройшов в цьому році, переносимо його на наступний
        if user_birthday_this_year.date() < today.date():
            user_birthday_this_year = user_birthday_this_year.replace(year=today.year + 1)

        # Визначаємо кількість до дня народження
        days_until_birthday = (user_birthday_this_year.date() - today.date()).days

        # Додаєм користувача до списку, якщо день народження випаданя на найближчі 7 днів, з сьогоднішнім включно.
        if 0 <= days_until_birthday <= 7:

            # Якщо день народження припадає на вихідні, переносимо дату поздоровлення на наступний понеделок.
            if user_birthday_this_year.weekday() >= 5:
                days_until_birthday = (7 - user_birthday_this_year.weekday())
                user_birthday_this_year += timedelta(days=days_until_birthday)

            # Перетворюємо об'єкт datetime в строку
            congratulation_date = user_birthday_this_year.strftime("%Y.%m.%d")
            upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date})

    return upcoming_birthdays


def main():
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
        {"name": "19", "birthday": "1992.03.19"},
        {"name": "14", "birthday": "1992.03.14"},
        {"name": "15", "birthday": "1992.03.15"},
        {"name": "Kate", "birthday": "1992.03.18"},
        {"name": "Pall", "birthday": "1983.03.13"},
        {"name": "Oleg", "birthday": "1992.03.17"},
        {"name": "Liza", "birthday": "1992.03.16"}
    ]

    upcoming_birthdays = get_upcoming_birthdays(users)
    print("Список привітань на цьому тижні:", upcoming_birthdays)


if __name__ == "__main__":
    main()
