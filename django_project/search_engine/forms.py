import redis
from django import forms
from .actions import get_task_keyword, create_task, get_task


class SearchForm(forms.Form):
    """It form for the searching.

    Attributes:
        keyword: a keyword for the searching.
    """
    keyword = forms.CharField(label='Tag', max_length=100, required=True)

    def save(self):
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
        existing_task = get_task(self.data.get('keyword', ''))
        if existing_task:
            task = get_task_keyword(self.data.get('keyword', ''))
            if task:
                return task
            else:
                return False
        else:
            # print(self.data.get('keyword', ''))
            create_task(self.data.get('keyword', ''))
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.lpush('google-spider:start_urls',
                    self.data.get('keyword', ''))
            # r.lpush('yandex-spider:start_urls',
            #         self.data.get('keyword', ''))
            # r.lpush('instagram-spider:start_urls',
            #         self.data.get('keyword', ''))
            return False
