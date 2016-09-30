# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy_djangoitem import DjangoItem
# from search_engine.models import Image


class ImageItem(scrapy.Item):
    """It item at the page.

    Args:
        image_url: a link at the image.
        rank: an importance.
    """
    image_url = scrapy.Field()
    rank = scrapy.Field()
    site = scrapy.Field()
    keyword = scrapy.Field()
