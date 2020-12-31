#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : test_inter_excel_sheet_0.py
@Time   : 2020/11/25 10:42
@Author : yd
@Version: 1.0
@ToDo    : 
"""
import os
import traceback

import allure
import pytest

from common.logger import logger
from script.model import ModelScript


@allure.epic('人脸HTTP接口测试')
class TestDev01:

    test_scr = ModelScript()
    test_scr.excel.set_sheet(test_scr.sheet_names[0])
    lines = test_scr.excel.read_all()
    lines_1 = []

    # for i in range(0, 10):   # 测试用
    for i in range(0, len(lines)):
        lines_1.append(i)

    @pytest.mark.parametrize("cases", lines_1)
    def test_http_inter(self, cases):
        # allure.dynamic.e("361版本:361.1.2.0")
        # allure.MASTER_HELPER.environment("协议版本:V1.2.24")
        self.test_scr.model_case(cases=self.lines[cases])

    def teardown(self):
        self.test_scr.excel.save()


if __name__ == '__main__':
    os.system(r'rd ..\myreport\temp\ /s/q')
    os.system(r'rd ..\logs\log.log /s/q')
    # 使用allure 需要自行下载安装allure
    pytest.main(["-s", "test_inter_excel_sheet_0.py", "--alluredir", "../myreport/temp"])
    # 执行命令行，生成allure测试报告
    os.system('allure generate ../myreport/temp -o ../myreport/report --clean')
