"""
Розробіть скрипт, який приймає шлях до директорії в якості аргументу командного рядка і візуалізує структуру цієї директорії, 
виводячи імена всіх піддиректорій та файлів. Для кращого візуального сприйняття, імена директорій та файлів мають відрізнятися за кольором.

Вимоги до завдання:
1. Створіть віртуальне оточення Python для ізоляції залежностей проєкту.
2. Скрипт має отримувати шлях до директорії як аргумент при запуску. Цей шлях вказує, де знаходиться директорія, структуру якої потрібно відобразити.
3. Використання бібліотеки colorama для реалізації кольорового виведення.
4. Скрипт має коректно відображати як імена директорій, так і імена файлів, використовуючи рекурсивний спосіб обходу директорій (можна, за бажанням, використати не рекурсивний спосіб).
5. Повинна бути перевірка та обробка помилок, наприклад, якщо вказаний шлях не існує або він не веде до директорії.
"""


from colorama import init, Fore
import sys
from pathlib import Path


def folder_info(directory: Path, prefix='', nesting_level=0):

    # Виводимо ім'я директорії від якої будуємо дерево
    if nesting_level == 0:
        print(Fore.MAGENTA + "📦 " + directory.name)

    # Отримуємо відсортований список елементів у директорії
    items = sorted(directory.iterdir(), key=lambda item: item.name)

    # Ідем по кожному елементу відсортованого списку
    for i, entry in enumerate(items):
        if entry.is_dir():

            # Якщо елемент директорія - друкуємо частину дерева та рекурсивно викликаємо функцію ще раз
            if i == len(items) - 1:
                print(Fore.LIGHTYELLOW_EX + prefix + " ┗━📂 " + Fore.MAGENTA + entry.name)
                folder_info(entry, Fore.LIGHTYELLOW_EX + prefix + "    ", nesting_level + 1)
            else:
                print(Fore.LIGHTYELLOW_EX + prefix + " ┣━📂 " + Fore.MAGENTA + entry.name)
                folder_info(entry, Fore.LIGHTYELLOW_EX + prefix + " ┃   ", nesting_level + 1)

        else:

            # Якщо елемент файл - друкуємо частину дерева
            if i == len(items) - 1:
                print(Fore.LIGHTYELLOW_EX + prefix + " ┗━📜 " + Fore.GREEN + entry.name)
            else:
                print(Fore.LIGHTYELLOW_EX + prefix + " ┣━📜 " + Fore.GREEN + entry.name)


def main():

    # Скидаємо налаштування для colorama після кожного виклику
    init(autoreset=True)

    # Перевіряємо кількість аргументів
    if len(sys.argv) == 2:
        directory = Path(sys.argv[1])
        print(directory)

    # Перевіряємо чи існує вказаний шлях
    if not directory.exists():
        print("No such directory.")
        sys.exit(1)

    # Виводимо заголовок дерева
    print(Fore.YELLOW + "Directory structure:")

    # Викликаємо функцію побудови дерева
    folder_info(directory)


if __name__ == "__main__":
    main()
