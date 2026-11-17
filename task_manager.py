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


def validate_tasks(tasks):
    """Проверить структуру данных перед использованием."""
    if not isinstance(tasks, list):
        raise ValueError("Ожидался список заданий.")
    seen = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Неверная запись задания.")
        if set(task) != {"id", "title", "subject", "status"}:
            raise ValueError("Неверный набор полей задания.")
        if type(task["id"]) is not int or task["id"] <= 0:
            raise ValueError("Номер должен быть положительным целым.")
        if task["id"] in seen:
            raise ValueError("Повтор номера задания.")
        seen.add(task["id"])
        for field in ("title", "subject"):
            if not isinstance(task[field], str) or not task[field].strip():
                raise ValueError("Пустое или неверное текстовое поле.")
        if task["status"] not in ("Не выполнено", "Выполнено"):
            raise ValueError("Недопустимый статус задания.")


def load_tasks(path):
    """Отсутствующий файл означает первый запуск."""
    import json
    from pathlib import Path

    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    tasks = json.loads(text)
    validate_tasks(tasks)
    return tasks


def save_tasks(tasks, path):
    """Записать через временный файл, сохранив старый при отказе."""
    import json
    from pathlib import Path

    validate_tasks(tasks)
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(tasks, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
