from pornhub.items import *
import re
import js2py

class Spider(scrapy.Spider):

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

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
