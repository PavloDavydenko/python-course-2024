"""
У вас є текстовий файл, який містить інформацію про місячні заробітні плати розробників у вашій компанії. 
Кожен рядок у файлі містить прізвище розробника та його заробітну плату, які розділені комою без пробілів.

Наприклад:
Alex Korp,3000
Nikita Borisenko,2000
Sitarama Raju,1000

Ваше завдання - розробити функцію total_salary(path), яка аналізує цей файл і повертає загальну та середню суму заробітної плати всіх розробників.

Вимоги до завдання:

1. Функція total_salary(path) має приймати один аргумент - шлях до текстового файлу (path).
2. Файл містить дані про заробітні плати розробників, розділені комами. Кожен рядок вказує на одного розробника.
3. Функція повинна аналізувати файл, обчислювати загальну та середню суму заробітної плати.
4. Результатом роботи функції є кортеж із двох чисел: загальної суми зарплат і середньої заробітної плати.
"""


def total_salary(path: str) -> tuple:

    with open(path, "r", encoding="utf-8") as fh:

        salaries = []

        # Читаємо рядки з файлу
        for line in fh:

            #  У змінну salary записуэмо значення зарплати
            _, salary = line.strip().split(",")

            # Перетворюємо значення заралати та додаємо до списку зарплат
            salaries.append(float(salary))

    # Розраховуємо загальну суму та середнє значення
    total = sum(salaries)
    average = total / len(salaries)

    return (total, average)


def main():
    total, average = total_salary("./salary_file.txt")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")


if __name__ == "__main__":
    main()
