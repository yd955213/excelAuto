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
from common import get_photo_base64
from common.logger import logger
from global_variables import cell_config


class Inter:
    """
    接口自动化关键字封装类
    """
    # 关联字典拆分字符串
    arrow = '{->'
    r_arrow = '}'

    def __init__(self, host):
        self.url = host
        self.path = None
        self.session = requests.session()
        self.session.headers['Content-Type'] = 'application/json;charset=utf-8'
        self.params = None
        self.response = None
        self.method = None
        self.module = sys.modules[__name__]
        self.relation_dict = get_photo_base64.photo_dic
        self.relation_params_temp = None

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
        设置用例, 把Excel某一行赋值过来
        :param case: list类型
        :return:如果有关联的字符串，将其返回，并重新写Excel
        """
        # openpyxl 的行和列从1开始，这里进行减1操作
        if not case[cell_config.get('path') - 1].startswith('http'):
            path = "/" + case[cell_config.get('path') - 1]
            self.path = self.url + path.replace("//", "/")
        else:
            self.path = case[cell_config.get('path') - 1]

        if case[cell_config.get('method') - 1] is not None:
            self.method = case[cell_config.get('method') - 1]

        if case[cell_config.get('params') - 1] is None or case[cell_config.get('params') - 1] == '' or case[
            cell_config.get('params') - 1].lower() == 'none' or case[cell_config.get('params') - 1].lower() == 'null':
            self.params = None
        else:
            self.relation_params_temp = self._get_relations(case[cell_config.get('params') - 1])
            try:
                self.params = json.loads(self.relation_params_temp)
            except Exception as e:
                logger.exception(traceback.format_exc())
                self.params = None

    def _get_relations(self, params=None):
        """
        根据params获取关联self.relation_dict字典中的值 格式必须为:{->xxx}
        :return: 关联后的字符串
        """
        if params is None:
            return None
        if str(params).find(self.arrow) >= 0:
            for key in self.relation_dict.keys():
                params = str(params).replace(self.arrow + key + self.r_arrow, str(self.relation_dict.get(key)))

        return params


if __name__ == '__main__':
    interface = Inter('DownloadAuthorityData')
    # print(interface.relation_dict.keys())
    # print(interface._get_relations('->杨党.jpg<-'))
