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


# tomcat 地址
test_url = 'http://172.168.120.230:8080/inter/index.html#behaviors'

# 主机地址和端口
host_dev = 'http://172.168.120.59:8090/DevApi'
host_server = 'http://172.168.120.69:8090/ServerApi'


time_start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
time_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# app自动化链接参数：
appium_config = {
    'platformName': 'Android',
    'platformVersion': '9.0',
    'deviceName': '3e5d55a',
    'appPackage': 'com.tencent.mobileqq',
    'appActivity': '.activity.SplashActivity',
    'noReset': True,        # 清除缓存记录，微信小程序测试必须加上
    'unicodeKeyboard': True,
    'resetKeyboard': True,      # 用来在自动化输入中文
    'automationName': 'uiautomator1'    # 小程序 如果还是操作不了， 与uiautomator2互换
}

# excel（xlxs格式）数据对应的列
cell_config = {
    'id': 1,
    'model': 2,
    'case_name': 3,
    'interface_name': 4,
    'path': 5,
    'method': 6,
    'params': 7,
    'result': 8,
    'assert_model': 9,
    'expect_param1': 10,
    'expect_param2': 11,
    'expect_result': 12,
    'is_run': 13,
    'status': 14,
    'desc': 15
}

email_config = {'reportTitle': '人脸HTTP接口测试',
                'tester': 'yd',
                'developer': '樊文斌，胡威',
                'appVersion': '361.1.2.0',
                'interface': 'V1.2.24',
                'runtype': 'HTTP',
                'caseVersion': 'V1.0',
                'mailFrom': '664720125@qq.com',
                'senderNickName': 'yd',
                'passWord': 'yjlsrkowzszfbbhc',
                'mailTo': '664720125@qq.com',
                # 'mailTo': '664720125@qq.com,1565890608@qq.com,1773087583@qq.com,457958791@qq.com,545476870@qq.com,2236807036@qq.com,670767661@qq.com,814491080@qq.com,9538631@qq.com,2586472986@qq.com,1770520605@qq.com,2955903779@qq.com',
                'mailTitle': '接口自动化测试报告',
                'mailModule': 'module2.html'}
