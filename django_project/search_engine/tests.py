from django.test import TestCase
from .models import Task, Image

# Create your tests here.


class TasksTestCase(TestCase):

    def setUp(self):
        Task.objects.create(keywords='pen')

    def test_tasks(self):
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
