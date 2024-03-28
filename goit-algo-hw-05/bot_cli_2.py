"""
Доробіть консольного бота помічника з попереднього домашнього завдання та додайте обробку помилок за допомоги декораторів.

Вимоги до завдання:
1. Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. 
Цей декоратор відповідає за повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо.
2. Декоратор input_error повинен обробляти винятки, що виникають у функціях - handler і це винятки: 
KeyError, ValueError, IndexError. Коли відбувається виняток декоратор повинен повертати відповідну відповідь користувачеві.
 Виконання програми при цьому не припиняється.
"""


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Invalid name. Enter an existing name."
        except TypeError:  # На майбутнє. Зараз це закрито блоком "else"
            return "Wrong command. To see all commands enter: help"
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter name and phone please"
        except Exception as e:
            return e.args[0]

    return inner


def name_and_phone_check(name: str, phone: str) -> None:

    # Перевірки чи ім'я складається з літер
    if not name.isalpha():
        raise Exception("Name must contain only letters.")

    # Перевірка чи номер складається з цифр та кількість цифр вірна
    if not phone.isdigit() or len(phone) != 10:
        raise Exception("The phone number must contain only numbers and be 10 characters long.")


def parse_input(user_input: str):

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


@input_error
def add_contact(args: list, contacts: dict) -> str:

    name, phone = args

    name_and_phone_check(name, phone)

    # Перевірка чи існує контакт з даним ім'ям
    if name in contacts:
        raise Exception("Contact already exists. You can change an existing contact or create one with a different name.")

    # Додавання нового контакта
    contacts[name] = phone

    return f"Added new contact: '{name}' with phone: {phone}."


@input_error
def change_contact(args: list, contacts: dict) -> str:

    name, phone = args

    name_and_phone_check(name, phone)

    # Перевірка чи існує контакт для редагування
    if name not in contacts:
        raise Exception("No such contact.")

    # Зміна номеру телефона
    contacts[name] = phone

    return f"Changed phone to '{phone}' for contact '{name}'."


def show_help() -> str:

    info = """
    "add <name> <phone number>          - adds contact"
    "change <name> <new phone number>   - changes contact"
    "phone <name>                       - show phone by name"
    "all                                - shows all contacts"
    "close, exit, quit or q             - for exit"
    """

    return info


@input_error
def show_phone(args: list, contacts: dict) -> str:

    name = args[0]

    # Перевірки чи ім'я складається з літер
    if not name.isalpha():
        raise Exception("Name must contain only letters.")

    # Перевірка чи існує контакт для виводу
    if name not in contacts:
        raise Exception("No such contact.")

    phone = contacts[name]

    return f"{name} : {phone}"


@input_error
def show_all(contacts: dict) -> str:

    # Перевірка чи існують контакти для виводу
    if not contacts:
        raise Exception("No contacts. Add new contacts.")

    # Формування рядка контактів для виводу
    all_contacts = ""

    for key, value in contacts.items():
        all_contacts += f"{key:<10} : {value}\n"

    return all_contacts


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
            print(show_help())
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
