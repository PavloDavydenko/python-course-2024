"""
В цьому домашньому завданні ви повинні додати функціонал збереження адресної книги на диск та відновлення з диска.

Для минулого домашнього завдання ви маєте вибрати pickle протокол серіалізації/десеріалізації даних та реалізувати методи, 
які дозволять зберегти всі дані у файл і завантажити їх із файлу.

Головна мета, щоб застосунок не втрачав дані після виходу із застосунку та при запуску відновлював їх з файлу. 
Повинна зберігатися адресна книга з якою ми працювали на попередньому сеансі.

Реалізуйте функціонал для збереження стану AddressBook у файл при закритті програми і відновлення стану при її запуску.

Приклади коду які стануть в нагоді.
Серіалізація з pickle

import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

Інтеграція збереження та завантаження в основний цикл
def main():
    book = load_data()

    # Основний цикл програми

    save_data(book)  # Викликати перед виходом з програми
"""

import pickle
from address_book_classes import AddressBook, Record


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


def name_check(name: str) -> None:
    """
    Перевірки чи ім'я складається з літер
    """

    if not name.isalpha():
        raise Exception("Name must contain only letters.")


def phone_check(phone: str) -> None:
    """
    Перевірка чи номер складається з цифр та чи вірна кількість цифр
    """

    if not phone.isdigit() or len(phone) != 10:
        raise Exception("The phone number must contain only numbers and be 10 characters long.")


def parse_input(user_input: str):
    """
    Парсить рядок вводу на команду та аргументи
    """

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    Створює новий контакт з ім'ям та телефоном.
    Чи додає телефон до існуючого контакту.
    """

    name, phone = args

    name_check(name)
    phone_check(phone)

    # Додавання нового контакта або телефону
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Added new contact: '{name}' with phone: {phone}."
    if phone:
        record.add_phone(phone)

    save_data(book)  # Зберігаємо дані після змін

    return message


@input_error
def delete_contact(args: list, book: AddressBook) -> str:
    """
    Видаляє контакт з адресної книги
    """
    name = args[0]

    # Перевірки чи ім'я складається з літер
    name_check(name)

    record = book.find(name)
    if record:
        # record = Record(name)
        book.delete(name)
        return f"Contact '{name}' deleted."
    else:
        return "No such contact."


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    """
    Замінює телефон в контакті з старого на новий
    """

    name, old_phone, new_phone = args

    name_check(name)
    phone_check(old_phone)
    phone_check(new_phone)

    # Перевірка чи існує контакт для редагування
    if name not in book.data:
        raise Exception("No such contact.")

    # Зміна номеру телефона
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)

    save_data(book)  # Зберігаємо дані після змін

    return f"Changed phone '{old_phone}' to '{new_phone}' for contact '{name}'."


def show_help() -> str:
    """
    Виводить підказку з командами
    """

    info = """
    "add <name> <phone number>                            - adds contact"
    "del <name>                                           - delete contact"
    "change <name> <old phone number> <new phone number>  - changes contact"
    "phone <name>                                         - show phone by name"
    "all                                                  - shows all contacts"
    "add-birthday <name> <birthday date>                  - adds birthday date to contact"
    "show-birthday <name>                                 - shows birthday date for contact"
    "birthdays                                            - shows birthdays for next week"
    "hello                                                - bot greating message"
    "close, exit, quit or q                               - for exit"
    """

    return info


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    """
    Повертає список телефонів для контакту
    """

    name = args[0]

    # Перевірки чи ім'я складається з літер
    name_check(name)

    # Перевірка чи існує контакт для виводу
    if name not in book.data:
        raise Exception("No such contact.")

    record = book.find(name)

    return f"{record.name}: {'; '.join(str(p) for p in record.phones)}."


@input_error
def show_all(book: AddressBook) -> str:
    """
    Виводить всі існуючі контакти
    """

    # Перевірка чи існують контакти для виводу
    if not book.data:
        raise Exception("No contacts. Add new contacts.")

    # Формування рядка контактів для виводу
    all_contacts = ""

    for record in book.data.values():
        all_contacts += f"{record}\n"

    return all_contacts


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    """
    Додає дату дня народження до контакту користувача
    """

    name, birthday = args

    name_check(name)

    # Перевірка чи існує контакт для редагування
    if name not in book.data:
        raise Exception("No such contact.")

    # Додавання дня народження
    record = book.find(name)
    record.add_birthday(birthday)

    save_data(book)  # Зберігаємо дані після змін

    return f"Added birthday '{birthday}' for contact '{name}'."


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    """
    Виводить дату дня народження для імені контакту
    """

    name = args[0]
    name_check(name)

    # Перевірка чи існує контакт для редагування
    if name not in book.data:
        raise Exception("No such contact.")

    record = book.find(name)

    return f"{name}: {record.birthday}"


@input_error
def birthdays(book: AddressBook) -> str:
    """
    Виводить список користувачів, кого потрібно привітати на наступному тижні
    """

    upcoming_birthdays = book.get_upcoming_birthdays()

    # Формуємо рядок з днями народженнями
    all_birthdays = "Upcoming birthdays:\n"
    if upcoming_birthdays:
        for birthday in upcoming_birthdays:
            all_birthdays += f"{birthday['name']} - {birthday['congratulation_date']}\n"
        return all_birthdays
    else:
        return "No upcoming birthdays."


def save_data(book, filename="addressbook.pkl"):
    """
    Збереження у файл адресної книги
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """
    Завантаження адресної книги з фалу або створення нової
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Створення нової адресної книги, якщо файл не знайдено


def main():

    book = load_data()  # Відновлення даних при запуску

    print("Welcome to the assistant bot!")
    print("For commands syntax type: help")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit", "q"]:
            save_data(book)  # Зберігаємо дані перед виходом
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(show_help())
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "del":
            print(delete_contact(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
