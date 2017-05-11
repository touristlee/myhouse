# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_url']:
            yield scrapy.Request(image_url,meta={'item':item,'index':item['image_url'].index(image_url)})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        index = request.meta['index']
        FolderName = item['name']
        nowpage = item['page']
        image_guid = item['layout'][index]+nowpage+'_'+str(index)+'.'+request.url.split('/')[-1].split('.')[-1]
        filename = u'full/{0}/{1}'.format(FolderName, image_guid)
        return filename
