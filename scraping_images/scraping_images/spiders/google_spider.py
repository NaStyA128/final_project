import scrapy
import redis
from scraping_images.items import ImageItem
from scraping_images import settings
from scrapy_redis.spiders import RedisSpider
from search_engine.models import Task
from scrapy.http import Request


class GoogleSpider(RedisSpider):
    """Spider for scraping the page in google.com.

    It based at RedisSpider. Comes the keyword and formed a link.
    It perform request end return response. Later it parse the page.
    Later it send message at chanel in redis server.

    Attributes:
        name: a name of the spider.
        allowed_domains: allowed domains.
        quantity: image counter.
    """

    name = 'google-spider'
    allowed_domains = ['google.com.ua']

    def __init__(self):
        # self.keyword = None
        super(GoogleSpider, self).__init__()

    def parse(self, response):
        """The parse of the pages.

        It create instance ImageItem and save needed information in
        this object. If there is a link to the next page - add to
        URL list for requests and run this request.

        Args:
            response: response from the request.
        """
        quantity = response.meta.get('quantity', 0)
        for td in response.css('.images_table tr td'):
            if quantity < settings.QUANTITY_IMAGES:
                item = ImageItem()
                item['image_url'] = td.xpath('.//a/img/@src').extract()[0]
                item['rank'] = 1
                item['site'] = 1
                item['keyword'] = response.meta['keyword']
                quantity += 1
                yield item
            else:
                # self.keyword = None
                Task.objects.filter(keywords=response.meta['keyword']).update(
                    google_status='done')
                r = redis.StrictRedis(host='localhost', port=6379, db=0)
                r.publish('google', response.meta['keyword'])
                # quantity = 0
                return

        next_href = response.css('#nav td.b a.fl')
        if next_href:
            url = response.urljoin(next_href.xpath('@href').extract()[0])
            yield scrapy.Request(url, self.parse, meta={'keyword': response.meta['keyword'], 'quantity': quantity})

    def make_request_from_data(self, data):
        """The formation of the link.

        Args:
            data: data is an URL.
        """
        # self.keyword = data
        new_url = 'https://www.google.com.ua/search?q=%s&tbm=isch' % data
        if '://' in new_url:
            # return self.make_requests_from_url(url=new_url)
            return Request(new_url, dont_filter=True, meta={'keyword': data})
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, new_url)
