#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/31 19:57
@Author  : Poco Ray
@File    : log.py
@Software: PyCharm
@Desc    : Description
"""
import logging
import os.path

from config.config import Config

log_path = Config.log_path


class Log:
    def __init__(self, log_dir=log_path, log_file='test.log'):
        logging.basicConfig(level=logging.WARNING)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(log_dir, log_file), encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @property
    def log(self):
        return self.logger


logger = Log().log
