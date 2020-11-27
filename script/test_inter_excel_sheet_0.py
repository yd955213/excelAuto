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
import allure
import pytest
from script.model import ModelScript


@allure.epic('达实人脸HTTP接口协议接口测试')
class TestDev01:

    test_scr = ModelScript()
    test_scr.excel.set_sheet(test_scr.sheet_names[0])
    lines = test_scr.excel.read_all()
    # lines = []

    # def setup_class(self):
    #     self.test_scr = ModelScript()
    #     self.test_scr.excel.set_sheet(self.test_scr.sheet_names[0])
    #     self.lines = self.test_scr.model_lines
    #     print('self.lines =', self.lines)
    #
    # print(lines)

    @pytest.mark.parametrize("cases", lines)
    def test_l01(self, cases):
        self.test_scr.model_case(cases=cases)

    def teardown(self):
        self.test_scr.excel.save()


if __name__ == '__main__':
    os.system(r'rd ..\myreport\temp\ /s/q')
    os.system(r'rd ..\logs\log.log /s/q')
    # 使用allure 需要自行下载安装allure
    pytest.main(["-s", "test_inter_excel_sheet_0.py", "--alluredir", "../myreport/temp"])
    # 执行命令行，生成allure测试报告
    os.system('allure generate ../myreport/temp -o ../myreport/report --clean')
