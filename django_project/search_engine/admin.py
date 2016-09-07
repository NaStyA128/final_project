from django.contrib import admin
from .models import Image, Task

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    """It's admin model - Image.

    Attributes:
        list_display: display fields from DB.
    """
    list_display = ['id', 'task', 'date', 'image_url', 'rank', ]


class TaskAdmin(admin.ModelAdmin):
    """It's admin model - Task.

        Attributes:
            list_display: display fields from DB.
        """
    list_display = ['id', 'keywords', 'google_status', 'yandex_status', 'instagram_status', 'quantity_images', ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Task, TaskAdmin)
