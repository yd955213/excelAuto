# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   test_361_apk_ui.py
@Time   :   2020-12-25 16:06
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import os

import allure
import pytest

from global_variables import appium_config
from script.ui_model import UiModel


@allure.epic('人脸apk UI测试')
class Test_361_Ui:
    # model = None
    model = UiModel('data/cases/UI自动化测试用例.xlsx')
    cases = []

    def setup_class(self):
        # self.model = UiModel()
        print('测试开始**************************************************')
        self.model.key_ui.start_appium(r'C:\Users\yangdang\AppData\Local\Programs\Appium')
        self.model.key_ui.startapp(appium_config)

    def teardown_class(self):
        self.model.excel.save()
        self.model.key_ui.quit()
        self.model.key_ui.stop_appium()
        print('测试结束**********************************************************')

    def teardown(self):
        self.model.excel.save()

    cases = model.excel.read_ui_excel()
    li = []
    for i in range(0, cases.__len__()):
        li.append(i)

    @pytest.mark.parametrize('my_row', li)
    def test_ui_1(self, my_row):
        self.model.run_case(self.cases[my_row])


if __name__ == '__main__':
    pytest.main(["-s", "test_361_apk_ui.py", "--alluredir", "./myreport/temp"])
    os.system('allure generate ../myreport/temp -o ../myreport/report --clean')
