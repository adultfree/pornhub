import datetime
import logging

def setup_logger(logger_name, log_file, level=logging.INFO):
    log_setup = logging.getLogger(logger_name)
    fileHandler = logging.FileHandler(log_file, mode='a')
    streamHandler = logging.StreamHandler()
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    log_setup.addHandler(streamHandler)

current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
setup_logger("webem_logger", "./%s-webem.log" % current_datetime)
setup_logger("mp4_logger", "./%s-mp4.log" % current_datetime)
