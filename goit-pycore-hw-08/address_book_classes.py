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
                    congratulation_date = user_birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date})

        return upcoming_birthdays
