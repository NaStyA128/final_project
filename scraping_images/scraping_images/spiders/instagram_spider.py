import re
import json
import scrapy
import redis
from scraping_images.items import ImageItem
from scraping_images import settings
from scrapy_redis.spiders import RedisSpider
from search_engine.models import Task


class InstagramSpider(RedisSpider):
    name = 'instagram-spider'
    allowed_domains = ['instagram.com']
    quantity = 0
    top = False

    def __init__(self):
        self.keyword = None
        super(InstagramSpider, self).__init__()

    def parse(self, response):
        javascript = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        json_data = json.loads("".join(re.findall(r'window._sharedData = (.*);', javascript)))
        with open('hi.txt', 'w') as f:
            f.write(json.dumps(json_data, indent=4))
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
        item = ImageItem()
        item['image_url'] = my_img["display_src"]
        item['rank'] = 1
        return item

    def make_request_from_data(self, data):
        # By default, data is an URL.
        self.keyword = data
        new_url = 'https://www.instagram.com/explore/tags/%s/' % data
        if '://' in new_url:
            return self.make_requests_from_url(new_url)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, new_url)

    def spider_idle(self):
        if self.keyword:
            Task.objects.filter(keywords=self.keyword).update(
                instagram_status='done')
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.publish('instagram-channel', self.keyword)
            self.keyword = None
        super(InstagramSpider, self).spider_idle()
