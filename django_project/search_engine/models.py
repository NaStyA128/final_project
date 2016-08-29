from django.db import models

# Create your models here.


class Image(models.Model):
    image_url = models.URLField()
    search_url = models.URLField()
    word_search = models.CharField(max_length=100)

    def __str__(self):
        return self.image_url
