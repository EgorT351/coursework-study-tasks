"""Операции над учебными заданиями."""


def add_task(tasks, title, subject):
    title = title.strip()
    subject = subject.strip()
    if not title:
        raise ValueError("Название задания не может быть пустым.")
    if not subject:
        raise ValueError("Дисциплина не может быть пустой.")
    task_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": task_id, "title": title, "subject": subject,
            "status": "Не выполнено"}
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Выполнено"
            return True
    return False


def delete_task(tasks, task_id):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            return True
    return False
