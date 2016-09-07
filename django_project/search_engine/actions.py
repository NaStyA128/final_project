# from django.shortcuts import get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Image,
    Task,
)


def get_images(word):
    """It gets from database pictures with filter and ordering.

    Args:
        word: a keyword for the searching.

    Returns:
        A list of pictures or False.
    """
    taskl = get_task_keyword(word)
    if taskl:
        images = Image.objects.filter(task_id=taskl.id).order_by('rank')
        return images
    else:
        return False


def get_all_tasks():
    """It gets from database all tasks.
    """
    return Task.objects.all()


def get_task_keyword(keyword):
    """It gets one task with this keyword.

    Args:
        keyword: a keyword for filter in tasks.

    Returns:
        A one task or False.
    """
    try:
        return Task.objects.get(
            keywords=keyword,
            google_status='done',
            yandex_status='done',
            instagram_status='done'
        )
    except ObjectDoesNotExist:
        return False


def get_task_id(task_id):
    """It gets one task with this id.

    Args:
        task_id: id for filter in tasks.

    Returns:
        A one task or False.
    """
    try:
        return Task.objects.get(
            id=task_id,
            google_status='done',
            yandex_status='done',
            instagram_status='done'
        )
    except ObjectDoesNotExist:
        return False


def create_task(keyword):
    """It create new task.

    Args:
        keyword: a keyword for new task.

    Returns:
        A new task.
    """
    return Task.objects.create(
        google_status='scheduled',
        yandex_status='scheduled',
        instagram_status='scheduled',
        quantity_images=0,
        keywords=keyword
    )
