# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline

from .items import *


class pornhubFilesPipeline(FilesPipeline):
    def item_completed(self, results, item, info):
        items = super().item_completed(results, item, info)
        return items

    def get_media_requests(self, item, info):
        if isinstance(item, WebmItem):
            yield scrapy.Request(item['url'], meta={'filename': item['name'] + ".webm"})
        else:
            yield scrapy.Request(item['url'], meta={'filename': item['name'] + ".mp4"})

    def file_path(self, request, response=None, info=None):
        # file_path必须使用相对路径，因为在scrapy中会用源路径.join(相对路径)
        return request.meta["filename"]
