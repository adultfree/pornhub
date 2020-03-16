from pornhub.items import *
from pornhub.spiders.spider import Spider
from pornhub import settings

class TopRatedSpider(Spider):
    name = "top_rated"
    start_urls = ['https://www.pornhub.com/video?o=tr']

    def parse(self, response):
        vkeys = response.xpath('//*[@class="phimage"]/div/a/@href').extract()
        gif_keys = response.xpath('//*[@class="phimage"]/div/a/img/@data-mediabook').extract()
        for (vkey, url) in zip(vkeys, gif_keys):
            item = WebmItem()
            item["url"] = url
            item["name"] = vkey.split("=")[-1]
            if settings.DOWNLOAD_VIDEO:
                yield item
            url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % item["name"]
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        title = ''.join(response.xpath('//h1//text()').extract()).strip()
        js_temp = response.xpath('//script/text()').extract()
        for j in js_temp:
            if 'flashvars' in j:
                js = ''.join(j.split('\n')[:-8])
                videoUrl = self.exeJs(js)
                item = Mp4Item()
                item['url'] = videoUrl
                item['name'] = title
                self.logger.info("下载地址: %s" % videoUrl)
                continue
