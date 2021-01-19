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
from dao.excel.excel_config import ExcelConfig, CaseStep
from dao.excel.excel_tool import ExcelTool
from common.logger import logger
from global_variables import get_abspath


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

    def run_case(self, cases):
        # logger.info(cases)
        allure.dynamic.feature(cases[ExcelConfig.GROUP])
        allure.dynamic.title(cases[ExcelConfig.ID] + '--' + cases[ExcelConfig.CASE_NAME])
        # allure 用例描述
        allure.dynamic.description(cases[ExcelConfig.CASE_NAME] + '，' + cases[ExcelConfig.CASE_DESCRIBE])
        # 每一个用例的测试步骤
        cases = cases[-1]
        num = 0
        run_cases_success = True
        fail_msg = ""
        fun = None
        for case in cases:
            # 测试开始
            logger.debug(case)
            num = num + 1
            key_word = case[CaseStep.method]
            self.row = case[CaseStep.excel_row]
            self.sheet_name = case[CaseStep.excel_sheet]
            self.key_ui.set_sheet_name(self.sheet_name)
            self.key_ui.excel_write_row = self.row
            is_ok = True
            # 反射获取要执行的关键字函数
            try:
                fun = getattr(self.key_ui, key_word)
            except Exception as e:
                is_ok = False
                logger.exception(e)
                logger.error(e)
                self.excel.write_result(False, row=self.row, column=ExcelConfig.getXlsxColumn(ExcelConfig.STATUS),
                                        value='FAIL')
                self.excel.write_result(False, row=self.row, column=ExcelConfig.getXlsxColumn(ExcelConfig.DESCRIBE),
                                        value='后台不支持该关键字！！{}'.format(e.__str__()))
                fail_msg += '步骤：{}，关键字：{}，错误原因：后台不支持该关键字；'.format(case[CaseStep.step_name], key_word)
            # 获取参数
            params = case[CaseStep.parameter1:CaseStep.describe]
            try:
                params = params[:params.index('')]
            except Exception as e:
                logger.exception(e)
                # pass
            # 执行关键字函数
            try:
                if fun is not None:
                    with allure.step('{}、{}'.format(num, case[CaseStep.step_name])):
                        print('params =', params)
                        status = fun(*params)
                        if not status:
                            is_ok = False
                        # allure.attach(self.key_ui.driver.get_screenshot_as_png(), '截图', allure.attachment_type.PNG)
            except Exception as e:
                is_ok = False
                logger.exception(e)
                self.excel.write_result(status=False, row=self.row,
                                        column=ExcelConfig.getXlsxColumn(ExcelConfig.STATUS), value='FAIL')
                self.excel.write_result(status=False, row=self.row,
                                        column=ExcelConfig.getXlsxColumn(ExcelConfig.DESCRIBE),
                                        value='参数输入错误!!! {}'.format(e.__str__()))

            if not is_ok:
                run_cases_success = False
                fail_msg = fail_msg + '步骤：{}，关键字：{}，参数值：{}；'.format(case[CaseStep.step_name], key_word, params)
                allure.attach(self.key_ui.driver.get_screenshot_as_png(), '步骤（{}）测试失败截图'
                              .format(case[CaseStep.step_name]), allure.attachment_type.PNG)
        else:
            assert run_cases_success, '测试失败:{}'.format(fail_msg)
