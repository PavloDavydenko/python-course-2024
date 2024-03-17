"""
Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, 
та буде відповідати відповідно до введеної команди.

Бот помічник повинен стати для нас прототипом застосунку-асистента, який ми розробимо в наступних домашніх завданнях. 
Застосунок-асистент в першому наближенні повинен вміти працювати з книгою контактів та календарем.

У цій домашній роботі зосередимося на інтерфейсі самого бота. 
Найпростіший і найзручніший на початковому етапі розробки інтерфейс - це консольний застосунок CLI (Command Line Interface). 
CLI достатньо просто реалізувати. Будь-який CLI складається з трьох основних елементів:

Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та модифікаторів команд.
Функції обробники команд - набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
Цикл запит-відповідь. Ця частина застосунку відповідає за отримання від користувача даних та повернення користувачеві відповіді від функції - handler-а.

На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, 
знаходити номер телефону за ім'ям, змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. 
Щоб реалізувати таку нескладну логіку, скористаємося словником. У словнику будемо зберігати ім'я користувача, як ключ, і номер телефону як значення.

Вимоги до завдання:
1. Програма повинна мати функцію main(), яка управляє основним циклом обробки команд.
2. Реалізуйте функцію parse_input(), яка розбиратиме введений користувачем рядок на команду та її аргументи. 
Команди та аргументи мають бути розпізнані незалежно від регістру введення.
3. Ваша програма повинна очікувати на введення команд користувачем та обробляти їх за допомогою відповідних функцій. 
В разі введення команди "exit" або "close", програма повинна завершувати виконання.
4. Напишіть функції обробники для різних команд, такі як add_contact(), change_contact(), show_phone() тощо.
5. Використовуйте словник Python для зберігання імен і номерів телефонів. Ім'я буде ключем, а номер телефону – значенням.
6. Ваша програма має вміти ідентифікувати та повідомляти про неправильно введені команди.
"""


def parse_input(user_input: str):

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def add_contact(args: list, contacts: dict) -> str:

    # Перевірка кількості аргументів
    if len(args) != 2:
        return "You must enter 2 argument (add <name> <phone number>)."

    # Перевірки чи ім'я складається з літер
    elif not args[0].isalpha():
        return "Name must contain only letters."

    # Перевірка чи номер складається з цифр та кількість цифр вірна
    elif not args[1].isdigit() or len(args[1]) != 10:
        return "The phone number must contain only numbers and be 10 characters long."

    # Перевірка чи існує контакт з даним ім'ям
    elif contacts.get(args[0]):
        return "Contact already exists. You can change an existing contact or create one with a different name."

    # Парсинг аргументів та додавання нового контакта
    name, phone = args
    contacts[name] = phone

    return "Contact added."


def change_contact(args: list, contacts: dict) -> str:

    # Перевірка кількості аргументів
    if len(args) != 2:
        return "You must enter 2 argument (change <name> <new phone number>)."

    # Перевірки чи ім'я складається з літер
    elif not args[0].isalpha():
        return "Name must contain only letters."

    # Перевірка чи номер складається з цифр та кількість цифр вірна
    elif not args[1].isdigit() or len(args[1]) != 10:
        return "The phone number must contain only numbers and be 10 characters long."

    # Перевірка чи існує контакт для редагування
    elif contacts.get(args[0]) is None:
        return "No such contact."

    # Парсинг аргументів та зміна номеру телефона
    name, phone = args
    contacts[name] = phone

    return "Contact updated."


def show_help():
    print()
    print("add <name> <phone number> - adds contact")
    print("change <name> <new phone number> - changes contact")
    print("phone <name> - show phone by name")
    print("all - shows all contacts")
    print("close, exit, quit or q - for exit")
    print()


def show_phone(args: list, contacts: dict) -> str:

    # Перевірка кількості аргументів
    if len(args) != 1:
        return "You must enter 1 argument (phone <name>)."

    # Перевірки чи ім'я складається з літер
    elif not args[0].isalpha():
        return "Name must contain only letters."

    # Перевірка чи існує контакт для виводу
    elif contacts.get(args[0]) is None:
        return "No such contact."

    name = args[0]
    phone = contacts[name]

    return f"{name} : {phone}"


def show_all(contacts: dict):

    # Перевірка чи існують контакти для виводу
    if not contacts:
        print("No contacts. Add new contacts.")

    for key, value in contacts.items():
        print(f"{key:<10} : {value}")


def main():

    contacts = {}

    print("Welcome to the assistant bot!")
    print("For commands syntax type: help")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit", "q"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            show_help()
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            show_all(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
