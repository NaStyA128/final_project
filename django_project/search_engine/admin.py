from django.contrib import admin
from .models import Image, Task

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'date', 'image_url', 'rank', ]


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'keywords', 'status', 'quantity_images', ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Task, TaskAdmin)
