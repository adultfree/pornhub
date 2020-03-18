# Scrapy settings for pornhub project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import datetime
import os

BOT_NAME = 'pornhub'

SPIDER_MODULES = ['pornhub.spiders']
NEWSPIDER_MODULE = 'pornhub.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'pornhub (+http://www.yourdomain.com)'

# 当DOWNLOAD_MP4_VIDEO设为True时，程序会试图下载视频
# 在大陆地区下载速度非常慢，因此强烈建议仅获取地址(设为False)
# 当以下两项设为False时，视频链接会被保存到"日期-时间-类型.log"文件中
# 打开文件，将地址批量拷贝，放入迅雷中下载，速度会快很多
DOWNLOAD_MP4_VIDEO = False
DOWNLOAD_WEBM_VIDEO = False

# 相关视频下载的深度，默认下载当前页面的视频(不下载相关视频)
# 注意：每增加一层深度，下载视频数会呈指数级增加
DEPTH_LIMIT = 1

# 以下类型的视频不下载(暂未实现)
CATEGORY_BLACK_LIST = [
    # 'Big Dick',
    # 'Cumshot',
]

TAGS_BLACK_LIST = [
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# 此处的LOG LEVEL最好设置为INFO，避免大量无用数据
LOG_LEVEL = 'INFO'
# 解注释此行则保存到文件中
# LOG_FILE = "./scrapy-%s.log" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'pornhub.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'pornhub.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pornhub.pipelines.pornhubFilesPipeline': 1,
}

CURRENT_DIR = os.path.abspath(os.curdir)
FILES_STORE = os.path.join(CURRENT_DIR, "data")
DATA_FILE_STORE = os.path.join(CURRENT_DIR, "data", "data.json")

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
RETRY_TIMES = 10

# 下载超时时间，如果这么长时间还未下载成功则认为下载失败
DOWNLOAD_TIMEOUT = 10000
DOWNLOAD_MAXSIZE = 0
DOWNLOAD_WARNSIZE = 0
