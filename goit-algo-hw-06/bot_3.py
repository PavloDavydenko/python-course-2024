"""
У цій домашній роботі ми продовжимо розвивати нашого віртуального асистента з CLI інтерфейсом.
Наш асистент вже вміє взаємодіяти з користувачем за допомогою командного рядка, отримуючи команди та аргументи, та виконуючи потрібні дії. 
У цьому завданні потрібно буде попрацювати над внутрішньою логікою асистента, над тим, як зберігаються дані, 
які саме дані і що з ними можна зробити. Саму логіку ми додамо в бота в наступному домашньому завданні.
Застосуємо для цих цілей об'єктно-орієнтоване програмування. Спершу виділимо декілька сутностей (моделей), з якими працюватимемо.
У користувача буде адресна книга або книга контактів. Ця книга контактів містить записи. Кожен запис містить деякий набір полів.
Таким чином ми описали сутності (класи), які необхідно реалізувати. Далі розглянемо вимоги до цих класів та встановимо їх взаємозв'язок, 
правила, за якими вони будуть взаємодіяти.
Користувач взаємодіє з книгою контактів, додаючи, видаляючи та редагуючи записи. 
Також користувач повинен мати можливість шукати в книзі контактів записи за одним або кількома критеріями (полями).
Про поля також можна сказати, що вони можуть бути обов'язковими (ім'я) та необов'язковими (телефон або email наприклад). 
Також записи можуть містити декілька полів одного типу (декілька телефонів наприклад). Користувач повинен мати можливість додавати/видаляти/редагувати поля у будь-якому записі.

Технічне завдання
Розробіть систему для управління адресною книгою.

Сутності:
Field: Базовий клас для полів запису.
Name: Клас для зберігання імені контакту. Обов'язкове поле.
Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
AddressBook: Клас для зберігання та управління записами.

Функціональність:
AddressBook:
Додавання записів.
Пошук записів за іменем.
Видалення записів за іменем.
Record:
Додавання телефонів.
Видалення телефонів.
Редагування телефонів.
Пошук телефону.
"""


from collections import UserDict


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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    locky_record = Record("Locky")
    locky_record.add_phone("0000000000")
    locky_record.add_phone("7777777777")
    locky_record.add_phone("9999999999")
    book.add_record(locky_record)

    pal_record = Record("Pal")
    pal_record.add_phone("1111111111")
    book.add_record(pal_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    print("-" * 50)
    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    print("-" * 50)
    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print("-" * 50)
    # Видалення запису Jane
    book.delete("Jane")

    # Видалення телефону Locky
    locky = book.find("Locky")
    locky.delete_phone("9999999999")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)