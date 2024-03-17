from pathlib import Path
import sys
from colorama import Fore, Style

def visualize_directory_structure(directory_path, prefix='', indent=0):
    try:
        items = sorted(directory_path.iterdir(), key=lambda item: item.name)
        for i, entry in enumerate(items):
            if entry.is_dir():
                if i == len(items) - 1:
                    print(prefix + "┗━📂 " + entry.name)
                    visualize_directory_structure(entry, prefix + "     ", indent + 1)
                else:
                    print(prefix + "┣━📂 " + entry.name)
                    visualize_directory_structure(entry, prefix + "┃    ", indent + 1)
            else:
                if i == len(items) - 1:
                    print(prefix + "┗━📜 " + entry.name)
                else:
                    print(prefix + "┣━📜 " + entry.name)
    except FileNotFoundError:
        print(Fore.RED + "Шлях не знайдено або не є директорією.")
        sys.exit(1)
    except PermissionError:
        print(Fore.RED + "Відмовлено в доступі до файлу або директорії.")
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Виникла помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Використання: python script.py <шлях до директорії>")
        sys.exit(1)

    directory_path = Path(sys.argv[1])
    if not directory_path.is_dir():
        print("Вказаний шлях не є директорією.")
        sys.exit(1)

    print(Fore.YELLOW + "Структура директорії:")
    visualize_directory_structure(directory_path)
