import datetime
import json
import logging
import os

from pornhub.settings import FILES_STORE, DOWNLOAD_MP4_VIDEO, DOWNLOAD_WEBM_VIDEO, DATA_FILE_STORE


def setup_logger(logger_name, log_file, level=logging.INFO):
    log_setup = logging.getLogger(logger_name)
    fileHandler = logging.FileHandler(log_file, mode='a')
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    # 不跟随parent logger
    log_setup.propagate = False
    # 若需要把数据打到屏幕上，则解注释此行
    # streamHandler = logging.StreamHandler()
    # log_setup.addHandler(streamHandler)

current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# 不下载的时候，把链接保存到本地目录
if not DOWNLOAD_WEBM_VIDEO:
    setup_logger("webem_logger", "./%s-webem.log" % current_datetime)
if not DOWNLOAD_MP4_VIDEO:
    setup_logger("mp4_logger", "./%s-mp4.log" % current_datetime)

data = {}
if os.path.exists(DATA_FILE_STORE):
    with open(DATA_FILE_STORE, 'r') as f:
        data = json.loads(f.read())
