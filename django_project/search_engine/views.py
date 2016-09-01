# import subprocess
# from django.shortcuts import render, redirect
import redis
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect

from .models import (
    Image,
    Task
)
from .forms import SearchForm
from .actions import *

# Create your views here.


class HomeView(ListView, FormView):
    model = Task
    form_class = SearchForm
    context_object_name = 'results'
    template_name = 'index.html'

    def get_queryset(self):
        # tasks = task_action.get_all_tasks().reverse()[:5]
        tasks = get_all_tasks()
        return tasks

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = get_task_keyword(form.cleaned_data['keyword'])
            if task:
                return HttpResponseRedirect('/%d/' % task.id)
            else:
                task = create_task(form.cleaned_data['keyword'])
                print(task)
                r = redis.StrictRedis(host='localhost', port=6379, db=0)
                r.lpush('google-spider:start_urls',
                        form.cleaned_data['keyword'])
                r.lpush('yandex-spider:start_urls',
                        form.cleaned_data['keyword'])
                r.lpush('instagram-spider:start_urls',
                        form.cleaned_data['keyword'])
                while True:
                    if r.llen('google-spider:start_urls') == 0 \
                            and r.llen('yandex-spider:start_urls') == 0 \
                            and r.llen('instagram-spider:start_urls') == 0:
                        update_status_in_task(task.id)
                        return HttpResponseRedirect('/%d/' % task.id)


class ResultView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'result.html'
    paginate_by = 12

    def get_queryset(self):
        images = get_images(self.args[0])
        return images

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['task'] = get_task_id(self.args[0])
        return context
