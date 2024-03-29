"""
У вас є текстовий файл, який містить інформацію про котів. 
Кожен рядок файлу містить унікальний ідентифікатор кота, його ім'я та вік, розділені комою.

Наприклад:
60b90c1c13067a15887e1ae1,Tayson,3
60b90c2413067a15887e1ae2,Vika,1
60b90c2e13067a15887e1ae3,Barsik,2
60b90c3b13067a15887e1ae4,Simon,12
60b90c4613067a15887e1ae5,Tessi,5

Ваше завдання - розробити функцію get_cats_info(path), яка читає цей файл та повертає список словників з інформацією про кожного кота.

Вимоги до завдання:
1. Функція get_cats_info(path) має приймати один аргумент - шлях до текстового файлу (path).
2. Файл містить дані про котів, де кожен запис містить унікальний ідентифікатор, ім'я кота та його вік.
3. Функція має повертати список словників, де кожен словник містить інформацію про одного кота.
"""


def get_cats_info(path: str) -> list:

    cats_info = []
    cat = {}

    with open(path, "r", encoding="utf-8") as fh:

        # Читаємо рядки з файлу
        for line in fh:

            # У змінні записуємо відповідні данні
            id, name, age = line.strip().split(",")

            # Модифікуємо данні у словнику для відповідного кота
            cat["id"] = id
            cat["name"] = name
            cat["age"] = age

            # Додаємо словник до списку
            cats_info.append(cat)

    return cats_info


def main():
    cats_info = get_cats_info("cats_file.txt")
    print(cats_info)


if __name__ == "__main__":
    main()
