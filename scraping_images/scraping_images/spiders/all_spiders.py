import re
import json
# from scrapy.shell import inspect_response
import scrapy
from scraping_images.items import ImageItem
from scraping_images import settings


class GoogleSpider(scrapy.Spider):
    name = 'google-spider'
    allowed_domains = ['google.com.ua']
    # start_urls = ['https://www.google.com.ua/search?q=cats&tbm=isch']
    quantity = 0

    def __init__(self, search_word, **kwargs):
        super(GoogleSpider, self).__init__(**kwargs)
        self.search_word = search_word

    def start_requests(self):
        links = ['https://www.google.com.ua/search?q=' + self.search_word + '&tbm=isch']
        for link in links:
            yield self.make_requests_from_url(link)

    def parse(self, response):
        # inspect_response(response, self)
        for td in response.css('.images_table tr td'):
            if self.quantity < settings.QUANTITY_IMAGES:
                item = ImageItem()
                item['image_url'] = td.xpath('.//a/img/@src').extract()[0]
                item['search_url'] = 'https://www.' + self.allowed_domains[0]
                item['word_search'] = self.search_word
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return


class YandexSpider(scrapy.Spider):
    name = 'yandex-spider'
    allowed_domains = ['yandex.ua']
    # start_urls = ['https://yandex.ua/images/search?text=cats']
    download_delay = 0.5
    quantity = 0

    def __init__(self, search_word, **kwargs):
        super(YandexSpider, self).__init__(**kwargs)
        self.search_word = search_word

    def start_requests(self):
        links = ['https://yandex.ua/images/search?text=' + self.search_word]
        for link in links:
            yield self.make_requests_from_url(link)

    def parse(self, response):
        for div in response.css('div.serp-item'):
            if self.quantity < settings.QUANTITY_IMAGES:
                item = ImageItem()
                item['image_url'] = 'https:' + div.xpath('.//img/@src').extract()[0]
                item['search_url'] = 'https://wwww.' + self.allowed_domains[0]
                item['word_search'] = self.search_word
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return


class InstagramSpider(scrapy.Spider):
    name = 'instagram-spider'
    allowed_domains = ['instagram.com']
    # start_urls = ['https://www.instagram.com/explore/tags/cats/']
    quantity = 0

    def __init__(self, search_word, **kwargs):
        super(InstagramSpider, self).__init__(**kwargs)
        self.search_word = search_word

    def start_requests(self):
        links = ['https://www.instagram.com/explore/tags/' + self.search_word + '/']
        for link in links:
            yield self.make_requests_from_url(link)

    def parse(self, response):
        javascript = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        json_data = json.loads("".join(re.findall(r'window._sharedData = (.*);', javascript)))
        data_media = json_data["entry_data"]["TagPage"][0]["tag"]["media"]["nodes"]
        data_top = json_data["entry_data"]["TagPage"][0]["tag"]["top_posts"]["nodes"]
        # item = self.my_for(data_top)
        # yield item
        # item = self.my_for(data_media)
        # yield item
        for img in data_top:
            if self.quantity < settings.QUANTITY_IMAGES:
                item = self.add_item(img)
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return
        for img in data_media:
            if self.quantity < settings.QUANTITY_IMAGES:
                item = self.add_item(img)
                self.quantity += 1
                yield item
            else:
                self.quantity = 0
                return

    def add_item(self, my_img):
        item = ImageItem()
        item['image_url'] = my_img["display_src"]
        item['search_url'] = 'https://www.' + self.allowed_domains[0]
        item['word_search'] = self.search_word
        return item

    # def my_for(self, data):
    #     for img in data:
    #         if self.quantity < settings.QUANTITY_IMAGES:
    #             item = self.add_item(img)
    #             self.quantity += 1
    #             yield item
    #         else:
    #             self.quantity = 0
    #             return
