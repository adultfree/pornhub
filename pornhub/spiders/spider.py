import pickle
import re

import js2py

from pornhub import settings, data
from pornhub.items import *


class Spider(scrapy.Spider):

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    def parse_detail(self, response):
        depth = response.request.meta["depth"]
        item = Mp4Item()
        item['key'] = response.request.url.split("=")[-1]
        item['title'] = ''.join(response.xpath('//h1//text()').extract()).strip()
        item['categories'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="categoriesWrapper"]/a/text()').extract()))
        item['uploader'] = response.xpath('//div[@class="video-info-row"]/div/span[@class="usernameBadgesWrapper"]/a/text()').extract_first()
        item['pornstars'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="pornstarsWrapper"]/a/text()').extract()))
        item['productions'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="productionWrapper"]/a/text()').extract()))
        item['tags'] = list(map(lambda x: x.strip(), response.xpath('//div[@class="tagsWrapper"]/a/text()').extract()))
        item['murl'] = self.exeJs(''.join(response.xpath('//div[@id="player"]/script[1]/text()').extract_first().split("\n")[:-8]))
        yield item
        if settings.CRAWL_RELATED_VIDEOS and depth < settings.CRAWL_RELATED_DEPTH:
            items = self.get_recommended_items(response)
            for item in items:
                yield item
                url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % item["key"]
                yield scrapy.Request(url, callback=self.parse_detail)

    def get_mainpage_items(self, response):
        items = []
        recommends = map(lambda x: x.split("=")[-1], response.xpath('//*[@class="phimage"]/div/a/@href').extract())
        titles = response.xpath('//*[@class="phimage"]/div/a/@title').extract()
        webems = response.xpath('//*[@class="phimage"]/div/a/img/@data-mediabook').extract()
        for (key, title, url) in zip(recommends, titles, webems):
            item = WebmItem()
            item["wurl"] = url
            item["key"] = key
            item["title"] = title
            items.append(item)
        return items

    def get_recommended_items(self, response):
        items = []
        recommends = map(lambda x: x.split("=")[-1], response.xpath("//div[@class='video-wrapper js-relatedRecommended']//div[@class='phimage']/div/a/@href").extract())
        titles = response.xpath("//div[@class='video-wrapper js-relatedRecommended']//div[@class='phimage']/div/a/@title").extract()
        webems = response.xpath("//div[@class='video-wrapper js-relatedRecommended']//div[@class='phimage']/div/a/img/@data-mediabook").extract()
        for (key, title, url) in zip(recommends, titles, webems):
            item = WebmItem()
            item["wurl"] = url
            item["key"] = key
            item["title"] = title
            items.append(item)
        return items

    def closed(self, reason):
        with open('./data.pkl', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

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
