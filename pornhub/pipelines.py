# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from scrapy.pipelines.files import FilesPipeline

from . import settings
from .items import *
from . import data


class pornhubFilesPipeline(FilesPipeline):
    webem_logger = logging.getLogger('webem_logger')
    mp4_logger = logging.getLogger('mp4_logger')

    def item_completed(self, results, item, info):
        items = super().item_completed(results, item, info)
        return items

    def get_media_requests(self, item, info):
        if isinstance(item, WebmItem):
            # 如果此时key已存在，代表该视频应该已经被下载过，直接返回即可
            if item['key'] in data:
                return
            data[item['key']] = dict(item)
            if settings.DOWNLOAD_WEBM_VIDEO:
                yield scrapy.Request(item['url'], meta={'filename': item['key'] + ".webm"})
            else:
                self.webem_logger.info(item["url"])
        else:
            # key应该是一定存在的，但如果tags存在，则说明已被更新过，应该已被下载，直接返回
            if item['key'] in data and "tags" in data[item['key']]:
                return
            data[item['key']].update(dict(item))
            if settings.DOWNLOAD_MP4_VIDEO:
                yield scrapy.Request(item['url'], meta={'filename': item['key'] + ".mp4"})
            else:
                self.mp4_logger.info(item["url"])

    def file_path(self, request, response=None, info=None):
        # file_path必须使用相对路径，因为在scrapy中会用源路径.join(相对路径)
        return request.meta["filename"]
