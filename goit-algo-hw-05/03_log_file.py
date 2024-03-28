"""
Розробіть Python-скрипт для аналізу файлів логів. Скрипт повинен вміти читати лог-файл, переданий як аргумент командного рядка, 
і виводити статистику за рівнями логування наприклад, INFO, ERROR, DEBUG. 
Також користувач може вказати рівень логування як другий аргумент командного рядка, щоб отримати всі записи цього рівня.

Файли логів – це файли, що містять записи про події, які відбулися в операційній системі, програмному забезпеченні або інших системах. 
Вони допомагають відстежувати та аналізувати поведінку системи, виявляти та діагностувати проблеми.

Для виконання завдання візьміть наступний приклад лог-файлу:
2024-01-22 08:30:01 INFO User logged in successfully.
2024-01-22 08:45:23 DEBUG Attempting to connect to the database.
2024-01-22 09:00:45 ERROR Database connection failed.
2024-01-22 09:15:10 INFO Data export completed.
2024-01-22 10:30:55 WARNING Disk usage above 80%.
2024-01-22 11:05:00 DEBUG Starting data backup process.
2024-01-22 11:30:15 ERROR Backup process failed.
2024-01-22 12:00:00 INFO User logged out.
2024-01-22 12:45:05 DEBUG Checking system health.
2024-01-22 13:30:30 INFO Scheduled maintenance.

Вимоги до завдання:
1. Скрипт повинен приймати шлях до файлу логів як аргумент командного рядка.
2. Скрипт повинен приймати не обов'язковий аргумент командного рядка, після аргументу шляху до файлу логів. 
Він відповідає за виведення всіх записи певного рівня логування. І приймає значення відповідно до рівня логування файлу. 
Наприклад аргумент error виведе всі записи рівня ERROR з файлу логів.
3. Скрипт має зчитувати і аналізувати лог-файл, підраховуючи кількість записів для кожного рівня логування (INFO, ERROR, DEBUG, WARNING).
4. Реалізуйте функцію parse_log_line(line: str) -> dict для парсингу рядків логу.
5. Реалізуйте функцію load_logs(file_path: str) -> list для завантаження логів з файлу.
6. Реалізуйте функцію filter_logs_by_level(logs: list, level: str) -> list для фільтрації логів за рівнем.
7. Реалізуйте функцію count_logs_by_level(logs: list) -> dict для підрахунку записів за рівнем логування.
8. Результати мають бути представлені у вигляді таблиці з кількістю записів для кожного рівня. 
Для цього реалізуйте функцію display_log_counts(counts: dict), яка форматує та виводить результати. 
Вона приймає результати виконання функції count_logs_by_level.
"""

from pathlib import Path
import sys


def parse_log_line(line: str) -> dict:
    """
    Парсимо рядок логів та перевіряємо лог-файл на вірний формат
    """
    parsed_dict = {}

    try:
        date, time, level, message = line.split(" ", 3)
    except ValueError:
        print("Неправильний формат лог-файлу.")
        sys.exit(1)

    parsed_dict["datetime"] = f"{date} {time}"
    parsed_dict["level"] = level
    parsed_dict["message"] = message.strip()

    return parsed_dict


def load_logs(file_path: str) -> list:
    """
    Відкриваємо лог файл і читаємо порядково.
    Перевіряємо наявність лог-фалу та наявність помилок читання.
    """
    logs_list = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                logs_list.append(parse_log_line(line))
    except FileNotFoundError:
        print("Відсутній файл логів.")
        sys.exit(1)
    except Exception as error:
        print(f"Помилка при завантаженні логів: {error}")
        sys.exit(1)

    return logs_list


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Відбираємо рядки тільки з відповідним рівнем логування
    """
    return [log for log in logs if log["level"] == level]


def count_logs_by_level(logs: list) -> dict:
    """
    Підраховуємо кількість помилок для кожного з рівнів логування
    """
    counts = {
        "DEBUG": 0,
        "ERROR": 0,
        "INFO": 0,
        "WARNING": 0
    }

    for log in logs:
        counts[log["level"]] += 1

    return counts


def display_log_counts(counts: dict) -> None:
    """
    Відображаємо кількість помилок для кожного з рівнів логування
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, value in counts.items():
        print(f"{level:<17}| {value}")


def display_logs_by_level(logs: list, level: str) -> None:
    """
    Відображаємо логи для відповідного рівня логування
    """
    print()
    print(f"Деталі логів для рівня '{level}':")
    for log in logs:
        print(f"{log["datetime"]} - {log["message"]}")


def main():

    # Перевіряємо введені аргументи
    if len(sys.argv) == 2:
        _, log_file_path = sys.argv
        log_level = None
    elif len(sys.argv) == 3:
        _, log_file_path, log_level = sys.argv
        log_level = log_level.upper()
    else:
        print("Enter python [name.py] /path/to/logfile.log <log_level>")

    logs = load_logs(log_file_path)

    count_logs = count_logs_by_level(logs)
    display_log_counts(count_logs)

    # Перевіряємо чи вводився log_level
    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        display_logs_by_level(filtered_logs, log_level)


if __name__ == "__main__":
    main()
