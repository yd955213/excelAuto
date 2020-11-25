#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : inter.py
@Time   : 2020/11/25 9:06
@Author : yd
@Version: 1.0
@ToDo    : 接口类
"""
import json
import sys
import traceback
import requests

from common.logger import logger
from global_variables import cell_config


class Inter:

    def __init__(self, host):
        self.url = host
        self.path = None
        self.session = requests.session()
        self.session.headers['Content-Type'] = 'application/json;charset=utf-8'
        self.params = None
        self.response = None
        self.method = None
        self.module = sys.modules[__name__]

    def get(self):
        try:
            self.response = self.session.get(url=self.path, json=self.params)
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.response = None
        return self.response

    def post(self):
        try:
            self.response = self.session.post(url=self.path, json=self.params)
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.response = None
        return self.response

    def put(self):
        try:
            self.response = self.session.put(url=self.path, json=self.params)
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.response = None
        return self.response

    def delete(self):
        try:
            self.response = self.session.delete(url=self.path, params=self.params)
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.response = None
        return self.response

    def set_case(self, case):
        """
        设置用例
        :param case: disc类型
        :return:
        """
        if not case[cell_config.get('path') - 1].startswith('http'):
            path = "/" + case[cell_config.get('path') - 1]
            self.path = self.url + path.replace("//", "/")
        else:
            self.path = case[cell_config.get('path') - 1]

        if case[cell_config.get('method') - 1] is not None:
            self.method = case[cell_config.get('method') - 1]
        try:
            self.params = json.loads(case[cell_config.get('params') - 1])
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.params = None


if __name__ == '__main__':
    interface = Inter('DownloadAuthorityData')
