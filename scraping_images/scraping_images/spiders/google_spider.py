import scrapy
from scraping_images.items import ImageItem
from scraping_images import settings
from scrapy_redis.spiders import RedisSpider


class GoogleSpider(RedisSpider):
    name = 'google-spider'
    allowed_domains = ['google.com.ua']
    quantity = 0

    def parse(self, response):
        # inspect_response(response, self)
        for td in response.css('.images_table tr td'):
            if self.quantity < settings.QUANTITY_IMAGES:
                item = ImageItem()
                item['image_url'] = td.xpath('.//a/img/@src').extract()[0]
                item['rank'] = 1
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return

        next_href = response.css('#nav td.b a.fl')
        if next_href:
            url = response.urljoin(next_href.xpath('@href').extract()[0])
            yield scrapy.Request(url, self.parse)

    def make_request_from_data(self, data):
        # By default, data is an URL.
        self.keyword = data
        new_url = 'https://www.google.com.ua/search?q=%s&tbm=isch' % data
        if '://' in new_url:
            return self.make_requests_from_url(new_url)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, new_url)
