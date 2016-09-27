import redis
import logging
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse

from .models import (
    Image,
    Task
)
from .forms import SearchForm
from .actions import *

# Create your views here.

# FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
#          u'[%(asctime)s]  %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.DEBUG,
#                     filename=u'debug.log')
# logger = logging.getLogger(__name__)


class HomeView(ListView, FormView):
    """A displaying a home page.

    It contains the ability to display the home page.
    It allows you to perform the search. The user enters
    the word and receives the result - pictures from
    a different search engines: google.com, yandex.ua,
    instagram.com. It have parents: ListView and FormView.
    It have two overwritten methods.

    Attributes:
        model: class im model-ORM. Table in DB.
        form_class: form at the page.
        context_object_name: a variable for displaying in template.
        template_name: a name of the template.
    """

    model = Task
    form_class = SearchForm
    context_object_name = 'results'
    template_name = 'index.html'

    def get_queryset(self):
        """It takes requests that make users.

        Returns:
             The requests of users.
        """
        # tasks = task_action.get_all_tasks().reverse()[:5]
        tasks = get_all_tasks()
        return tasks

    # def post(self, request, *args, **kwargs):
    #     """It handles the form.
    #
    #     The user press the button and a request with keyword
    #     comes in here. Function gets forms data and finds tasks
    #     with this word. If such tasks is in the database, it
    #     redirect at the page with results. Otherwise - create it
    #     creates new task and send requests on redis-server.
    #
    #     Args:
    #         request: the data of the user.
    #         args: additional options.
    #         kwargs: additional options.
    #
    #     Returns:
    #         A redirecting at page with results.
    #     """
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         task = get_task_keyword(request.POST.get('keyword', ''))
    #         if task:
    #             # logging.info('Redirect at result images2.')
    #             # logging.debug('Redirect at result images.')
    #             return HttpResponseRedirect('/%d/' % task.id)
    #         else:
    #             task = create_task(request.POST.get('keyword', ''))
    #             r = redis.StrictRedis(host='localhost', port=6379, db=0)
    #             r.lpush('google-spider:start_urls',
    #                     request.POST.get('keyword', ''))
    #             r.lpush('yandex-spider:start_urls',
    #                     request.POST.get('keyword', ''))
    #             r.lpush('instagram-spider:start_urls',
    #                     request.POST.get('keyword', ''))
    #             # if r.llen('google-spider:start_urls') == 0
    #             return HttpResponse('in process..')


class ResultView(ListView):
    """A displaying a result page.

    It shows pictures that a user requests.
    It have a parent: ListView. It have two overwritten
    methods. And the pagination too.

    Attributes:
        model: class im model-ORM. Table in DB.
        context_object_name: a variable for displaying in template.
        template_name: a name of the template.
        paginate_by: a quantity of images at the page.
    """

    model = Image
    context_object_name = 'images'
    template_name = 'result.html'
    paginate_by = 12

    def get_queryset(self):
        """It takes requests that make users.

        Returns:
             The requests of users.
        """
        images = get_images(self.args[0])
        if images:
            return images

    def get_context_data(self, **kwargs):
        """It gets the data.

        Returns:
            A context for template.
        """
        context = super(ResultView, self).get_context_data(**kwargs)
        context['task'] = get_task_keyword(self.args[0])
        return context
