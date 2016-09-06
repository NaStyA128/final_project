# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from search_engine.models import Task, Image


class SaveImageInDBPipeline(object):

    def process_item(self, item, spider):
        task = Task.objects.get(keywords=spider.keyword)
        # task = Task.objects.get(keywords="summer")
        Image.objects.create(
            task=task,
            image_url=item['image_url'],
            rank=item['rank']
        )
        return item

    # def close_spider(self, spider):
    #     r = redis.StrictRedis(host='localhost', port=6379, db=0)
    #     r.publish('our-channel', "True")
