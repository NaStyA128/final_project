import redis
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from .actions import get_task_keyword, create_task


class SearchForm(forms.Form):
    """It form for the searching.

    Attributes:
        keyword: a keyword for the searching.
    """
    keyword = forms.CharField(max_length=100)

    def is_valid(self):
        """It handles the form.

        The user press the button and a request with keyword
        comes in here. Function gets forms data and finds tasks
        with this word. If such tasks is in the database, it
        redirect at the page with results. Otherwise - create it
        creates new task and send requests on redis-server.

        Args:
            request: the data of the user.
            args: additional options.
            kwargs: additional options.

        Returns:
            A redirecting at page with results.
        """
        task = get_task_keyword(self.data.get('keyword', ''))
        if task:
            # logging.info('Redirect at result images2.')
            # logging.debug('Redirect at result images.')
            return HttpResponseRedirect('/%d/' % task.id)
        else:
            task = create_task(self.data.get('keyword', ''))
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.lpush('google-spider:start_urls',
                    self.data.get('keyword', ''))
            r.lpush('yandex-spider:start_urls',
                    self.data.get('keyword', ''))
            r.lpush('instagram-spider:start_urls',
                    self.data.get('keyword', ''))
            # if r.llen('google-spider:start_urls') == 0
            return HttpResponse('in process..')
