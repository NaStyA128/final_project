from django.test import TestCase
from .models import Task, Image
from .actions import *

# Create your tests here.


class TasksTestCase(TestCase):

    def setUp(self):
        Task.objects.create(keywords='pen')

    @staticmethod
    def test_tasks():
        pen = Task.objects.get(keywords='pen')
        return pen


class ImageTestCase(TestCase):

    def setUp(self):
        self.task = Task.objects.create(keywords='pen')
        Image.objects.create(
            task=self.task,
            image_url='http://...',
            rank=1
        )

    def test_tasks(self):
        image = Image.objects.get(task=self.task)
        return image


class TasksActionTestCase(TestCase):

    def setUp(self):
        self.task = create_task('tree')

    def test_tasks_actions(self):
        all_tasks = get_all_tasks()
        yield all_tasks
        first_task = get_task_keyword(self.task.keywords)
        yield first_task
        second_task = get_task_id(self.task.id)
        yield second_task


class ImageActionTestCase(TestCase):

    def setUp(self):
        self.task = create_task('tree')

    def test_tasks_actions(self):
        images = get_images(self.task.keywords)
        return images
