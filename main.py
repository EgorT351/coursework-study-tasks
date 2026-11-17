"""Консольный интерфейс учёта учебных заданий."""
from pathlib import Path
from task_manager import (add_task, complete_task, delete_task,
                          load_tasks, save_tasks)

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
    path = Path(__file__).with_name("tasks.json")
    try:
        tasks = load_tasks(path)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"Ошибка чтения файла: {error}")
        print("Работа остановлена. Проверьте файл tasks.json.")
        return
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "0":
                save_tasks(tasks, path)
                print("Данные сохранены.")
                print("Работа завершена.")
                return
            elif choice == "1":
                title = input("Название задания: ")
                subject = input("Дисциплина: ")
                updated = [task.copy() for task in tasks]
                add_task(updated, title, subject)
                save_tasks(updated, path)
                tasks = updated
                print("Задание добавлено.")
            elif choice == "2":
                show_tasks(tasks)
            elif choice in ("3", "4"):
                task_id = int(input("Номер задания: "))
                updated = [task.copy() for task in tasks]
                if choice == "3":
                    found = complete_task(updated, task_id)
                else:
                    found = delete_task(updated, task_id)
                if found:
                    save_tasks(updated, path)
                    tasks = updated
                    print("Задание изменено.")
                else:
                    print("Задание с таким номером не найдено.")
            else:
                print("Некорректный пункт меню.")
        except OSError as error:
            print(f"Ошибка записи файла: {error}")
        except ValueError as error:
            print(f"Ошибка ввода: {error}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван. Сохранённые изменения доступны при запуске.")
