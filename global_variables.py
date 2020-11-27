#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : global_variables.py
@Time   : 2020/11/25 8:12
@Author : yd
@Version: 1.0
@ToDo    : 常用全局变量
"""
import os
import time


def get_abspath(file_path):
    """
    获取需要打开或者读取文件的绝对路径，文件不存在返回为空
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        return os.path.abspath(file_path)
    else:
        file_path = os.path.dirname(__file__) + os.sep + file_path
        if os.path.exists(file_path):
            return file_path
        else:
            return None


# 主机地址和端口
host_dev = 'http://172.168.120.69:8090/DevApi'
host_server = 'http://172.168.120.69:8090/ServerApi'


time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
time_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# excel数据对应的列
cell_config = {
    "id": 1,
    "model": 2,
    "case_name": 3,
    "interface_name": 4,
    "path": 5,
    "method": 6,
    "params": 7,
    "result": 8,
    "assert_model": 9,
    "expect_param1": 10,
    "expect_param2": 11,
    "expect_result": 12,
    "is_run": 13,
    "status": 14,
    "desc": 15
}

email_config = {'reportTitle': '人脸HTTP接口测试',
                'tester': 'yd',
                'developer': '樊文斌，胡威',
                'caseVersion': 'V1.0',
                'mailFrom': '664720125@qq.com',
                'senderNickName': 'yd',
                'passWord': 'yjlsrkowzszfbbhc',
                'mailTo': '664720125@qq.com,yangd@csdas.cn',
                # 'mailTo': '664720125@qq.com,1565890608@qq.com,1773087583@qq.com,457958791@qq.com,545476870@qq.com,2236807036@qq.com',
                'mailTitle': '接口自动化测试报告',
                'mailModule': 'module1.html'}
