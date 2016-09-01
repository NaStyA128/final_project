# from django.shortcuts import get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Image,
    Task,
)


def get_images(task):
    images = Image.objects.filter(task_id=task).order_by('rank')
    if images:
        return images
    else:
        return False


def get_all_tasks():
    return Task.objects.all()


def get_task_keyword(keyword):
    try:
        return Task.objects.get(keywords=keyword)
    except ObjectDoesNotExist:
        return False


def get_task_id(task_id):
    try:
        return Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        return False


def create_task(keyword):
    return Task.objects.create(
        status='scheduled',
        quantity_images=0,
        keywords=keyword
    )


def update_status_in_task(task_id):
    Task.objects.filter(id=task_id).update(status='done')
