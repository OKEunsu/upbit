# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'trader.log')

def setup_logger():
    """로거 설정"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger("autotrader")
    if logger.hasHandlers():
        return logger # 이미 설정되었다면 바로 반환

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 콘솔 핸들러
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 파일 핸들러 (5MB 마다 파일 분할, 최대 5개 파일 유지)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
