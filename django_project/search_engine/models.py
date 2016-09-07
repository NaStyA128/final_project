from django.db import models

# Create your models here.


class Task(models.Model):
    """Task-model.

    This model intended for use with a table Task
    in the database.

    Attributes:
        keywords: a keyword for the task.
        google_status: the status of implementation of the parsing in google.com
        yandex_status: the status of implementation of the parsing in yandex.ua
        instagram_status: the status of implementation of the parsing in instagram.com
        quantity_images: a quantity images at runtime parsing.
    """
    keywords = models.CharField(max_length=100, unique=True)
    STATUS_CHOICES = (
        ('scheduled', 'scheduled'),
        ('done', 'done'),
    )
    google_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
    )
    yandex_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
    )
    instagram_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
    )
    quantity_images = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.keywords


class Image(models.Model):
    """Image-model.

    This model intended for use with a table Image
    in the database.

    Attributes:
        task: a number of task.
        date: date added to database.
        image_url: a network link.
        rank: an importance.
    """
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    rank = models.IntegerField()

    def __str__(self):
        return self.image_url
