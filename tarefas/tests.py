from django.test import TestCase

from .models import Task


class TaskModelTest(TestCase):
    def test_str_retorna_titulo(self):
        task = Task(titulo="Estudar Django")
        self.assertEqual(str(task), "Estudar Django")
