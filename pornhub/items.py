# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebmItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()


class Mp4Item(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
