"""
Ми продовжимо робити консольного бота помічника. Настав час об'єднати наші попередні домашні завдання в одне.
По перше додамо додатковий функціонал до класів з попередньої домашньої роботи:

Додайте поле birthday для дня народження в клас Record . Це поле має бути класу Birthday. Це поле не обов'язкове, але може бути тільки одне.

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

Додайте функціонал роботи з Birthday у клас Record, а саме функцію add_birthday, яка додає день народження до контакту.
Додайте функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
Додайте та адаптуйте до класу AddressBook нашу функцію з четвертого домашнього завдання, тиждень 3, get_upcoming_birthdays, 
яка для контактів адресної книги повертає список користувачів, яких потрібно привітати по днях на наступному тижні.

Тепер ваш бот (4 домашнє завдання тиждень 5) повинен працювати саме з функціоналом класу AddressBook. 
Це значить, що замість словника contacts ми використовуємо book = AddressBook()

Для реалізації нового функціоналу також додайте функції обробники з наступними командами:
add-birthday - додаємо до контакту день народження в форматі DD.MM.YYYY
show-birthday - показуємо день народження контакту
birthdays - повертає список користувачів, яких потрібно привітати по днях на наступному тижні

@input_error
def add_birthday(args, book):
    # реалізація

@input_error
def show_birthday(args, book):
    # реалізація

@input_error
def birthdays(args, book):
    # реалізація

Тож в фіналі наш бот повинен підтримувати наступний список команд:
1. add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.
2. change [ім'я] [новий телефон]: Змінити телефонний номер для вказаного контакту.
3. phone [ім'я]: Показати телефонний номер для вказаного контакту.
4. all: Показати всі контакти в адресній книзі.
5. add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
6. show-birthday [ім'я]: Показати дату народження для вказаного контакту.
7. birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
8. hello: Отримати вітання від бота.
9. close або exit: Закрити програму.
"""


from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def validate_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return f"{self.birthday}"

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                user_birthday = record.birthday.date
                user_birthday_this_year = user_birthday.replace(year=today.year)

                if user_birthday_this_year < today.date():
                    user_birthday_this_year = user_birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (user_birthday_this_year - today.date()).days

                if 0 <= days_until_birthday <= 7:
                    if user_birthday_this_year.weekday() >= 5:
                        days_until_birthday = (7 - user_birthday_this_year.weekday())
                        user_birthday_this_year += timedelta(days=days_until_birthday)
                    congratulation_date = user_birthday_this_year.strftime("%Y.%m.%d")
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date})

        return upcoming_birthdays


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

    return message


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

    return f"Changed phone '{old_phone}' to '{new_phone}' for contact '{name}'."


def show_help() -> str:
    """
    Виводить підказку з командами
    """

    info = """
    "add <name> <phone number>                            - adds contact"
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


def main():

    book = AddressBook()

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
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
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
