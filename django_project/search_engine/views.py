import subprocess
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect

from .models import Image
from .forms import SearchForm
# from scraping_images.scraping_images.spiders.all_spiders import (
#     GoogleSpider,
#     YandexSpider,
#     InstagramSpider
# )

# Create your views here.


class HomeView(ListView, FormView):
    model = Image
    form_class = SearchForm
    context_object_name = 'images'
    template_name = 'index.html'
    paginate_by = 12

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        form.is_valid()
        if self.request.GET:
            q = Image.objects.filter(word_search=form.cleaned_data['word'])
            if q:
                return q
            else:
                spiders = ['google-spider', 'yandex-spider', 'instagram-spider']
                for spider in spiders:
                    process = subprocess.Popen(
                        'scrapy crawl ' + spider + ' -a search_word=' + form.cleaned_data['word'],
                        cwd=r'/home/user/final_project/scraping_images/scraping_images',
                        shell=True,
                        stdout=subprocess.PIPE
                    )
                    out = process.communicate()
                    print(out)
                # return HttpResponseRedirect('/')
                q = Image.objects.filter(word_search=form.cleaned_data['word'])
                return q
        return ''

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.GET.get('word'):
            context['search_word'] = self.request.GET.get('word')
        return context

    @staticmethod
    def filter(word):
        q = Image.objects.filter(
            word_search__icontains=word)
        return q

    # def post(self, request, *args, **kwargs):
    #     search_word = request.POST.get('word', '')
