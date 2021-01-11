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
from common.my_color import MyColor
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

    def run_case(self, cases):
        # logger.info(cases)
        allure.dynamic.feature(cases[ui_cell_config.get('group') - 1])
        allure.dynamic.title(cases[ui_cell_config.get('id') - 1] + '--' + cases[ui_cell_config.get('case_name') - 1])
        # allure 用例描述
        allure.dynamic.description(
            cases[ui_cell_config.get('case_name') - 1] + '，' + cases[ui_cell_config.get('case_describe') - 1]
        )
        cases = cases[-1]
        num = 0
        run_cases_success = True
        fail_msg = ""
        for case in cases:
            # 测试开始
            logger.debug(case)
            num = num + 1
            key_word = case[1]
            self.row = case[-2]
            self.sheet_name = case[-1]
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
                self.__write_excel(False, column=ui_cell_config.get('status'), value='FAIL')
                self.__write_excel(False, column=ui_cell_config.get('describe'), value='后台不支持该关键字！！{}'
                                   .format(e.__str__()))
                assert False
            # 获取参数
            params = case[2:5]
            try:
                # params[:params.index('')] 会过滤 ’‘字段，这里定义，excel文档中要输入''时，使用字符串'null'代替,这里做转换
                params = params[:params.index('')]
                # for i in range(0, params.__len__()):
                #     if params[i].lower() == 'null':
                #         params[i] = ''
            except Exception as e:
                logger.exception(e)
                # pass
            # 执行关键字函数
            try:
                if fun is not None:
                    with allure.step('{}、{}'.format(num, case[0])):
                        print('params =', params)
                        status = fun(*params)
                        if not status:
                            is_ok = False
                        # allure.attach(self.key_ui.driver.get_screenshot_as_png(), '截图', allure.attachment_type.PNG)
            except Exception as e:
                is_ok = False
                logger.exception(e)
                self.__write_excel(status=False, column=ui_cell_config.get('status'), value='FAIL')
                self.__write_excel(status=False, column=ui_cell_config.get('describe'), value='参数输入错误!!! {}'
                                   .format(e.__str__()))

            # logger.debug("is_ok = {}".format(is_ok))
            # if key_word.__contains__('assert'):
            #     allure.attach(self.key_ui.driver.get_screenshot_as_png(), '断言截图', allure.attachment_type.PNG)

            if not is_ok:
                run_cases_success = False
                fail_msg = fail_msg + '步骤：{}，关键字：{}，参数值：{}；'.format(case[0], key_word, params)
                allure.attach(self.key_ui.driver.get_screenshot_as_png(), '步骤（{}）测试失败截图'
                              .format(case[0]), allure.attachment_type.PNG)
        else:
            assert run_cases_success, '测试失败:{}'.format(fail_msg)

    def __write_excel(self, status, column, value):
        if status:
            color = MyColor.BlACK
            if column == ui_cell_config.get('status'):
                fg_color = MyColor.GREEN
            else:
                fg_color = MyColor.WHITE
        else:
            if column == ui_cell_config.get('status'):
                color = MyColor.BlACK
                fg_color = MyColor.RED
            else:
                color = MyColor.RED
                fg_color = MyColor.WHITE

        self.excel.write(sheet_name=self.sheet_name,
                         row=self.row,
                         column=column,
                         value=value,
                         color=color,
                         fg_color=fg_color)


# if __name__ == '__main__':
#     u = UiModel('data/cases/test.xlsx')
#     u.row = 8
#     u.sheet_name = u.excel.get_sheet_names()[0]
#     u.write_excel(True, 8, 'test123')
#     u.row = 9
#     u.write_excel(False, 8, 'test123')
#     u.row = 10
#     u.write_excel(True, 12, 'test123')
#     u.row = 11
#     u.write_excel(True, ui_cell_config.get('status'), 'test123')
#     u.row = 12
#     u.write_excel(False, ui_cell_config.get('status'), 'test123')
#     u.excel.save()

