from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        if hasattr(spider, 'user_agent'):
            request.headers.setdefault('User-Agent', spider.user_agent)
        else:
            new_ua = self.ua.random
            request.headers.setdefault('User-Agent', new_ua)
