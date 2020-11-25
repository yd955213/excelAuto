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
