# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebmItem(scrapy.Item):
    url = scrapy.Field()
    filename = scrapy.Field()
    key = scrapy.Field()
    title = scrapy.Field()


class Mp4Item(scrapy.Item):
    url = scrapy.Field()
    filename = scrapy.Field()
    key = scrapy.Field()
    title = scrapy.Field()
    categories = scrapy.Field()
    uploader = scrapy.Field()
    pornstars = scrapy.Field()
    productions = scrapy.Field()
    tags = scrapy.Field()
