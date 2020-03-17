import scrapy

from pornhub.spiders.spider import Spider


class TopRatedSpider(Spider):
    name = "top_rated"
    start_urls = ['https://www.pornhub.com/video?o=tr']

    def parse(self, response):
        items = self.get_mainpage_items(response)
        for item in items:
            yield item
            url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % item["key"]
            yield scrapy.Request(url, callback=self.parse_detail)
