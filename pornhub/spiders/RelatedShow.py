from pornhub.items import *
from pornhub.spiders.spider import Spider


class RelatedShowSpider(Spider):
    name = "related_show"
    # 贴上喜欢的URL，下载其关联的URL，关联深度在settings.py中定义
    start_urls = ['https://www.pornhub.com/view_video.php?viewkey=ph5f5bf00b43be0']

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_detail)
