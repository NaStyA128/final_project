import redis
import scrapy
from scraping_images.items import ImageItem
from scraping_images import settings
from scrapy_redis.spiders import RedisSpider
from search_engine.models import Task


class YandexSpider(RedisSpider):
    """Spider for scraping the page in yandex.ua.

    It based at RedisSpider. Comes the keyword and formed a link.
    It perform request end return response. Later it parse the page.
    Later it send message at chanel in redis server.

    Attributes:
        name: a name of the spider.
        allowed_domains: allowed domains.
        quantity: image counter.
    """

    name = 'yandex-spider'
    allowed_domains = ['yandex.ua']
    download_delay = 0.5
    quantity = 0

    def __init__(self):
        self.keyword = None
        super(YandexSpider, self).__init__()

    def parse(self, response):
        """The parse of the pages.

        It create instance ImageItem and save needed information in
        this object. If there is a link to the next page - add to
        URL list for requests and run this request.

        Args:
            response: response from the request.
        """
        for div in response.css('div.serp-item'):
            if self.quantity < settings.QUANTITY_IMAGES:
                item = ImageItem()
                item['image_url'] = 'https:' + div.xpath('.//img/@src').extract()[0]
                item['rank'] = 1
                item['site'] = 2
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return

        next_href = response.css('div.more_direction_next a.button2')
        if next_href:
            url = response.urljoin(next_href.xpath('@href').extract()[0])
            yield scrapy.Request(url, self.parse)

    def make_request_from_data(self, data):
        """The formation of the link.

        Args:
            data: data is an URL.
        """
        self.keyword = data
        new_url = 'https://yandex.ua/images/search?text=%s' % data
        if '://' in new_url:
            return self.make_requests_from_url(new_url)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, new_url)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits.
        """
        if self.keyword:
            Task.objects.filter(keywords=self.keyword).update(
                yandex_status='done')
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.publish('yandex-channel', self.keyword)
            self.keyword = None
        super(YandexSpider, self).spider_idle()
