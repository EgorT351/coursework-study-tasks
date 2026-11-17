"""Проверки операций и хранения с изоляцией файлов."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from task_manager import (add_task, complete_task, delete_task,
                          load_tasks, save_tasks, validate_tasks)


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.tasks = []

    def test_add_and_unique_id(self):
        first = add_task(self.tasks, " Отчёт ", "Качество ИС")
        second = add_task(self.tasks, "Тесты", "Качество ИС")
        self.assertEqual(first["title"], "Отчёт")
        self.assertEqual([first["id"], second["id"]], [1, 2])
        self.assertEqual(second["status"], "Не выполнено")

    def test_empty_fields(self):
        for title, subject in [("  ", "ИС"), ("Отчёт", " ")]:
            with self.assertRaises(ValueError):
                add_task(self.tasks, title, subject)
        self.assertEqual(self.tasks, [])

    def test_complete(self):
        add_task(self.tasks, "Отчёт", "ИС")
        self.assertTrue(complete_task(self.tasks, 1))
        self.assertEqual(self.tasks[0]["status"], "Выполнено")
        self.assertTrue(complete_task(self.tasks, 1))
        self.assertFalse(complete_task(self.tasks, 99))

    def test_delete(self):
        add_task(self.tasks, "Отчёт", "ИС")
        self.assertFalse(delete_task(self.tasks, 99))
        self.assertTrue(delete_task(self.tasks, 1))
        self.assertEqual(self.tasks, [])

    def test_roundtrip_and_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            self.assertEqual(load_tasks(path), [])
            add_task(self.tasks, "Отчёт", "ИС")
            save_tasks(self.tasks, path)
            self.assertEqual(load_tasks(path), self.tasks)

    def test_invalid_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            for text in ["{", "{}", '[{"id": 1}]']:
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_tasks(path)

    def test_invalid_records(self):
        task = add_task(self.tasks, "Отчёт", "ИС")
        for field, value in [("id", True), ("id", 0),
                             ("title", " "), ("status", "Готово")]:
            with self.assertRaises(ValueError):
                validate_tasks([{**task, field: value}])
        with self.assertRaises(ValueError):
            validate_tasks([task, task.copy()])

    def test_failed_replace_preserves_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            save_tasks([], path)
            original = path.read_bytes()
            add_task(self.tasks, "Отчёт", "ИС")
            with patch.object(Path, "replace", side_effect=OSError("Отказ")):
                with self.assertRaises(OSError):
                    save_tasks(self.tasks, path)
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse(path.with_name("tasks.json.tmp").exists())


if __name__ == "__main__":
    unittest.main()
