import json
import re

import js2py

from pornhub import data, DATA_FILE_STORE
from pornhub.items import *


class Spider(scrapy.Spider):

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    def parse_detail(self, response):
        item = Mp4Item()
        item['key'] = response.request.url.split("=")[-1]
        item['title'] = ''.join(response.xpath('//h1//text()').extract()).strip()
        item['categories'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="categoriesWrapper"]/a/text()').extract()))
        item['uploader'] = response.xpath('//div[@class="video-info-row"]/div/span[@class="usernameBadgesWrapper"]/a/text()').extract_first()
        item['pornstars'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="pornstarsWrapper"]/a/text()').extract()))
        item['productions'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="productionWrapper"]/a/text()').extract()))
        item['tags'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="tagsWrapper"]/a/text()').extract()))
        item['url'] = self.exeJs(''.join(response.xpath('//div[@id="player"]/script[1]/text()').extract_first().split("\n")[:-8]))
        item['filename'] = item['url'].split("?")[0].split("/")[-1]
        # 将数据保存到data数据库中
        if item["key"] not in data:
            dict_item = dict(item)
            dict_item.pop("url")
            data[item["key"]] = dict_item
        yield item
        items = self.get_recommended_items(response)
        for item in items:
            yield item
            url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % item["key"]
            yield scrapy.Request(url, callback=self.parse_detail)

    def get_mainpage_items(self, response):
        recommends = map(lambda x: x.split("=")[-1], response.xpath('//*[@class="phimage"]/div/a/@href').extract())
        titles = response.xpath('//*[@class="phimage"]/div/a/@title').extract()
        webems = response.xpath('//*[@class="phimage"]/div/a/img/@data-mediabook').extract()
        return self.get_webm_items(recommends, titles, webems)

    def get_recommended_items(self, response):
        recommends = map(lambda x: x.split("=")[-1], response.xpath("//div[@class='video-wrapper js-relatedRecommended']//div[@class='phimage']/div/a/@href").extract())
        titles = response.xpath("//div[@class='video-wrapper js-relatedRecommended']//div[@class='phimage']/div/a/@title").extract()
        webems = response.xpath("//div[@class='video-wrapper js-relatedRecommended']//div[@class='phimage']/div/a/img/@data-mediabook").extract()
        return self.get_webm_items(recommends, titles, webems)

    def get_webm_items(self, recommends, titles, webems):
        items = []
        for (key, title, url) in zip(recommends, titles, webems):
            item = WebmItem()
            item["url"] = url
            item["filename"] = url.split("?")[0].split("/")[-1]
            item["key"] = key
            item["title"] = title
            items.append(item)
        return items

    def closed(self, reason):
        with open(DATA_FILE_STORE, 'w') as f:
            f.write(json.dumps(data, indent=True))

    def exeJs(self, js):
        flashvars = re.findall('flashvars_\d+', js)[0]
        res = js2py.eval_js(js + flashvars)
        if res.quality_1080p:
            return res.quality_1080p
        if res.quality_720p:
            return res.quality_720p
        elif res.quality_480p:
            return res.quality_480p
        elif res.quality_240p:
            return res.quality_240p
        else:
            self.logger.error('parse url error')
