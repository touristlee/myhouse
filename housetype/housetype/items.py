# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousetypeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    #images = scrapy.Field()
    image_url = scrapy.Field()
    page = scrapy.Field()
    name = scrapy.Field()
    layout = scrapy.Field()
