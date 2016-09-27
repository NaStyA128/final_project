import re
import json
import scrapy
import redis
from scraping_images.items import ImageItem
from scraping_images import settings
from scrapy_redis.spiders import RedisSpider
from search_engine.models import Task


class InstagramSpider(RedisSpider):
    """Spider for scraping the page in instagram.com.

    It based at RedisSpider. Comes the keyword and formed a link.
    It perform request end return response. Later it parse the page.
    Later it send message at chanel in redis server.

    Attributes:
        name: a name of the spider.
        allowed_domains: allowed domains.
        quantity: image counter.
    """

    name = 'instagram-spider'
    allowed_domains = ['instagram.com']
    quantity = 0
    top = False

    def __init__(self):
        self.keyword = None
        super(InstagramSpider, self).__init__()

    def parse(self, response):
        """The parse of the pages.

        It create instance ImageItem and save needed information in
        this object. If there is a link to the next page - add to
        URL list for requests and run this request.

        Args:
            response: response from the request.
        """
        javascript = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        json_data = json.loads("".join(re.findall(r'window._sharedData = (.*);', javascript)))
        # with open('hi.txt', 'w') as f:
        #     f.write(json.dumps(json_data, indent=4))
        data_media = json_data["entry_data"]["TagPage"][0]["tag"]["media"]["nodes"]
        data_top = json_data["entry_data"]["TagPage"][0]["tag"]["top_posts"]["nodes"]
        for img in data_top:
            if not self.top:
                if self.quantity < settings.QUANTITY_IMAGES:
                    item = self.add_item(img)
                    self.quantity += 1
                    yield item
                else:
                    self.quantity = 0
                    return
        self.top = True
        for img in data_media:
            if self.quantity < settings.QUANTITY_IMAGES:
                item = self.add_item(img)
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return

        next_href = json_data["entry_data"]["TagPage"][0]["tag"]["media"]["page_info"]["has_next_page"]
        if next_href:
            url = response.urljoin(
                '?max_id=' +
                json_data["entry_data"]["TagPage"][0]["tag"]["media"]["page_info"]["end_cursor"])
            yield scrapy.Request(url, self.parse)

    def add_item(self, my_img):
        """It save needed information in object.

        Args:
            my_img: information about the item.

        Returns:
            An item.
        """
        item = ImageItem()
        item['image_url'] = my_img["display_src"]
        item['rank'] = 1
        item['site'] = 3
        return item

    def make_request_from_data(self, data):
        """The formation of the link.

        Args:
            data: data is an URL.
        """
        self.keyword = data
        new_url = 'https://www.instagram.com/explore/tags/%s/' % data
        if '://' in new_url:
            return self.make_requests_from_url(new_url)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, new_url)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits.
        """
        if self.keyword:
            Task.objects.filter(keywords=self.keyword).update(
                instagram_status='done')
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.publish('instagram-channel', self.keyword)
            self.keyword = None
        super(InstagramSpider, self).spider_idle()
