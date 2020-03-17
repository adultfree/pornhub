# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os

from scrapy.pipelines.files import FilesPipeline

from . import settings
from .items import *


class pornhubFilesPipeline(FilesPipeline):
    webem_logger = logging.getLogger('webem_logger')
    mp4_logger = logging.getLogger('mp4_logger')

    def item_completed(self, results, item, info):
        items = super().item_completed(results, item, info)
        return items

    def get_media_requests(self, item, info):
        # 检查目录中是否存在
        if os.path.exists(os.path.join(settings.FILES_STORE, item['filename'])):
            info.spider.logger.warning("忽略已下载的文件: %s" % item['filename'])
            return
        if isinstance(item, WebmItem):
            if settings.DOWNLOAD_WEBM_VIDEO:
                yield scrapy.Request(item['url'], meta={'filename': item['filename']})
            else:
                self.webem_logger.info(item['url'])
        else:
            if settings.DOWNLOAD_MP4_VIDEO:
                yield scrapy.Request(item['url'], meta={'filename': item['filename']})
            else:
                self.mp4_logger.info(item['url'])

    def file_path(self, request, response=None, info=None):
        # file_path必须使用相对路径，因为在scrapy中会用源路径.join(相对路径)
        return request.meta['filename']
