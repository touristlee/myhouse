# -*- coding:UTF-8 -*-
import scrapy
from housetype.items import HousetypeItem
from scrapy.http.request import Request
from scrapy.selector import Selector
import urlparse
def printhxs(hxs):
    a=''
    for i in hxs:
        a=a+i.encode('utf-8')
    return a

def change_image(images):
    new_image=[]
    for i in images:
        new_image.append(i.split('_cm')[0]+i[-13:])
    return new_image
def get_urls(startpage,endpage):
    urls_list = []
    for x in range(endpage-startpage):
        urls_list.append("http://house.leju.com/zh/search/?page="+str(x+startpage))
    return urls_list
class MySpider(scrapy.Spider):
    name = "house"
    download_delay = 1
    allowed_domains = ["house.leju.com"]
#    start_urls = [
#        "http://house.leju.com/zh/search/?page=1"
#    ]
    start_urls=get_urls(11,440)
    def parse_item(self, response):
        sel = Selector(response)
        item = HousetypeItem()
        item['page'] = response.request.url.split('/p')[1].split('.shtml')[0]
        item['name'] = ''.join(sel.xpath('//div[@class="title"]/h1/text()').extract())
        item['image_url'] = change_image(sel.xpath('//div[@class="b_imgBox"]/img/@lsrc').extract())
        item['layout'] = sel.xpath('//div[@class="b_imgBox"]/img/@alt').extract()
        yield item
    def parse_pages(self, response):
        sel = Selector(response)
        pages = sel.xpath('//div[@class="b_pageBox clearfix z_pages"]/a/@href').extract()
        if pages:
            new_pages=list(set(pages))
            new_pages.sort
            for page_url in new_pages:
                yield Request(page_url ,callback=self.parse_item)
        else:
            item = HousetypeItem()
            item['page'] = '1'
            item['name'] = ''.join(sel.xpath('//div[@class="title"]/h1/text()').extract())
            item['image_url'] = change_image(sel.xpath('//div[@class="b_imgBox"]/img/@lsrc').extract())
            item['layout'] = sel.xpath('//div[@class="b_imgBox"]/img/@alt').extract()
            yield item
    def parse_layout(self, response):
        for sel in response.xpath('//div[@class="clearfix"]'):
            myurl = 'http://house.leju.com/'
            urls = printhxs(sel.xpath('ul/li/a/@href').extract())
            huxing = printhxs(sel.xpath('ul/li/a/text()').extract())
            if ("户型图" in huxing):
            	layout_url = myurl + urls.split('/')[1] + "/huxing/"
            	yield Request(layout_url ,callback=self.parse_pages)
    def parse(self, response):
        sel = response.xpath('//div[@id="ZT_searchBox"]')
        house_url = sel.xpath('div/div/a/@href').extract()
        for urls in house_url:
            yield Request(urls ,callback=self.parse_layout)    
