# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from search_engine.models import Task, Image


class SaveImageInDBPipeline(object):
    """It process data.
    """

    def process_item(self, item, spider):
        """It save data in database.

        Args:
            item: a current item.
            spider: a current spider.

        Returns:
            An item.
        """
        task = Task.objects.get(keywords=spider.keyword)
        Image.objects.create(
            task=task,
            image_url=item['image_url'],
            rank=item['rank']
        )
        return item
