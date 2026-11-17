"""Консольный интерфейс учёта учебных заданий."""
from task_manager import add_task, complete_task, delete_task

MENU = """\nУчёт учебных заданий
1. Добавить задание
2. Просмотреть задания
3. Отметить выполнение
4. Удалить задание
0. Выход"""


def show_tasks(tasks):
    if not tasks:
        print("Сохранённых заданий нет.")
    for task in tasks:
        print(f'{task["id"]}. {task["title"]} | '
              f'{task["subject"]} | {task["status"]}')


def main():
    tasks = []
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "0":
                print("Работа завершена.")
                return
            elif choice == "1":
                title = input("Название задания: ")
                subject = input("Дисциплина: ")
                add_task(tasks, title, subject)
                print("Задание добавлено.")
            elif choice == "2":
                show_tasks(tasks)
            elif choice in ("3", "4"):
                task_id = int(input("Номер задания: "))
                if choice == "3":
                    found = complete_task(tasks, task_id)
                else:
                    found = delete_task(tasks, task_id)
                if found:
                    print("Задание изменено.")
                else:
                    print("Задание с таким номером не найдено.")
            else:
                print("Некорректный пункт меню.")
        except ValueError as error:
            print(f"Ошибка ввода: {error}")


if __name__ == "__main__":
    main()
