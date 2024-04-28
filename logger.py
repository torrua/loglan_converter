# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""Configuration file"""
import logging
import time
from functools import wraps

detailed_format = "%(filename)s [LINE:%(lineno)03d] [%(asctime)s] %(levelname)-s %(funcName)s() %(message)s"
short_format = "[%(asctime)s] %(message)s"

logging.basicConfig(
    format=detailed_format, level=logging.INFO, datefmt="%y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)


def logging_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.time()
        log.info(
            f"{func.__name__} - Start time:"
            f" {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
        )
        result = func(*args, **kwargs)
        end_time = time.time()
        log.info(
            f"{func.__name__} - End time:"
            f" {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"
        )
        log.info(
            f"{func.__name__} - Duration:" f" {end_time - start_time:.2f} seconds\n"
        )
        return result

    return wrapper
