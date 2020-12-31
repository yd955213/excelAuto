# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   ui_model.py
@Time   :   2020-12-25 14:39
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import allure
from api.appiumUI import AppiumUI as AppiumUI
from common.excel_tool import ExcelTool
from common.logger import logger
from global_variables import get_abspath, ui_cell_config


class UiModel:
    def __init__(self, file_path='data/cases/UI自动化测试用例.xlsx'):
        # 实例化ExcelTool类
        self.excel = ExcelTool(get_abspath(file_path))
        # 实例化AppiumUI接口
        self.key_ui = AppiumUI()
        self.key_ui.set_excel(self.excel)
        # 每个方法执行参数化之前，都需要设置sheet页后，在读取excel获取对应的self.case
        self.sheet_name = None
        self.row = None
        self.name = None
        self.cases = None

    # @allure.step
    # def step(self, number, title):
    #     with allure.step('{}、{}'.format(number, title)):
    #         pass

    def run_case(self, cases):
        # logger.debug(cases)
        allure.dynamic.feature(cases[ui_cell_config.get('group') - 1])
        allure.dynamic.title(cases[ui_cell_config.get('id') - 1] + '--' + cases[ui_cell_config.get('case_name') - 1])
        allure.dynamic.description(
            cases[ui_cell_config.get('case_name') - 1] + '，' + cases[ui_cell_config.get('case_describe') - 1])
        cases = cases[-1]
        num = 0
        for case in cases:
            # 测试开始
            # logger.debug(case)
            is_ok = False
            num = num + 1
            key_word = case[1]

            self.row = case[-2]
            self.sheet_name = case[-1]
            self.key_ui.set_sheet_name(self.sheet_name)
            self.key_ui.excel_write_row = self.row

            try:
                fun = getattr(self.key_ui, key_word)
            except Exception as e:
                is_ok = False
                logger.exception(e)
                logger.error(e)
                self.__write_excel(False, column=ui_cell_config.get('status'), value='FAIL')
                self.__write_excel(False, column=ui_cell_config.get('describe'), value='后台不支持该关键字！！')
                assert False

            params = case[2:5]
            try:
                params = params[:params.index('')]
            except:
                pass

            try:
                if fun is not None:
                    with allure.step('{}、{}'.format(num, case[0])):
                        is_ok = fun(*params)
                        # allure.attach(self.key_ui.driver.get_screenshot_as_png(), '截图', allure.attachment_type.PNG)
            except Exception as e:
                is_ok = False
                logger.exception(e)
                self.__write_excel(status=False, column=ui_cell_config.get('status'), value='FAIL')
                self.__write_excel(status=False, column=ui_cell_config.get('describe'), value='参数输入错误!!!')

            # logger.debug("is_ok = {}".format(is_ok))
            # if key_word.__contains__('assert'):
            #     allure.attach(self.key_ui.driver.get_screenshot_as_png(), '断言截图', allure.attachment_type.PNG)

            # if not is_ok:
            #     allure.attach(self.key_ui.driver.get_screenshot_as_png(), '测试失败截图', allure.attachment_type.PNG)

            # with allure.step('{}、{}'.format(num, case[0])):
            assert is_ok, '{}:测试失败!'.format(case[0])

    def __write_excel(self, status, column, value):
        if status:
            color = '000000'
        else:
            color = 'FF0000'
        self.excel.write(sheet_name=self.sheet_name,
                         row=self.row,
                         column=column,
                         value=value,
                         color=color)
