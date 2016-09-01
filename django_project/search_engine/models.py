from django.db import models

# Create your models here.


class Task(models.Model):
    keywords = models.CharField(max_length=100, unique=True)
    STATUS_CHOICES = (
        ('scheduled', 'scheduled'),
        ('done', 'done'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
    )
    quantity_images = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.keywords


class Image(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    rank = models.IntegerField()

    def __str__(self):
        return self.image_url
