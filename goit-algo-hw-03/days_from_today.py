"""
Створіть функцію get_days_from_today(date), яка розраховує кількість днів між заданою датою і поточною датою.
"""


from datetime import datetime


def get_days_from_today(date):

    now = datetime.today()
    input_date = datetime.strptime(date, "%Y-%m-%d")
    delta = now.toordinal() - input_date.toordinal()

    return delta


def main():
    while True:
        date = input("Input date (format YYYY-MM-DD): ")

        try:
            days_delta = get_days_from_today(date)
            break
        except ValueError:
            print("Invalid input! You have to input date as YYYY-MM-DD\n")

    print(f"Number of days between dates: '{days_delta}'")


if __name__ == "__main__":
    main()
