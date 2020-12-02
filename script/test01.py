#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : test01.py
@Time   : 2020/11/25 10:42
@Author : yd
@Version: 1.0
@ToDo    : 
"""
import os

import allure
import pytest
import common.my_assert as obj
from api.inter import Inter
from common.excel_tool import ExcelTool
from common.logger import logger
from global_variables import get_abspath, host_dev, cell_config


@allure.feature('达实人脸HTTP接口协议接口测试')
class TestDev01:
    excel = ExcelTool(get_abspath('data/cases/test.xlsx'))

    def setup_class(self):
        # self.excel = ExcelTool(get_abspath('data/cases/test.xlsx'))
        self.excel.copy()
        self.sheet_names = self.excel.get_sheet_names()
        self.my_inter = Inter(host=host_dev)

    def run_step(self, method, url, params):
        func = getattr(self.my_inter, method)
        self.my_method(url)
        self.my_params(params)
        return func()

    @allure.step('请求地址:{url}')
    def my_method(self, url):
        pass

    @allure.step('请求参数:{params}')
    def my_params(self, params):
        pass

    @allure.step('响应结果:{response}')
    def my_response(self, response):
        pass

    @allure.step('响应结果:{assert_result}')
    def my_assert(self, assert_result):
        pass

    def __step(self, assert_result, response_contain, url, params):
        self.my_assert(assert_result)
        self.my_response(response_contain)
        self.my_method(url)
        self.my_params(params)

    # 每个方法执行参数化之前，都需要设置sheet页后，在读取excel获取对应的cases
    ca = excel.read("Sheet1")
    print(ca)

    # 每个sheet为一类测试用例
    @allure.story(ca[0][cell_config.get('model') - 1] + ':' + ca[0][cell_config.get('path') - 1])
    @pytest.mark.parametrize("cases", ca)
    def test01(self, cases):
        allure.dynamic.title(cases[cell_config.get('case_name') - 1])
        allure.dynamic.description(cases[cell_config.get('interface_name') - 1])
        sheet_name = 'Sheet1'
        logger.info(cases)
        # 调用即可方法下
        try:
            self.my_inter.set_case(cases)
            response = getattr(self.my_inter, cases[cell_config.get('method') - 1])()

            if response is not None:
                # 写请求返回结果
                self.excel.write(sheet_name=sheet_name, row=cases[-1], column=cell_config.get('result'),
                                 value=response.text)
        except Exception as e1:
            # 写请求返回结果
            self.excel.write(sheet_name=sheet_name, row=cases[-1], column=cell_config.get('result'), value="None",
                             color='FF0000')
        assert_result = ''
        if response is not None:
            try:
                func = getattr(obj, cases[cell_config.get('assert_model') - 1])
                if func == 'assert_jsonpath':
                    func(response, cases[cell_config.get('expect_param1') - 1],
                                     cases[cell_config.get('expect_param2') - 1])
                else:
                    func(response, cases[cell_config.get('expect_param1') - 1])

                assert_result = '断言成功!'
                self.__step(assert_result=assert_result, response_contain=response.text, url=self.my_inter.path,
                            params=cases[cell_config.get('params') - 1])

                self.excel.write(sheet_name=sheet_name, row=cases[-1], column=cell_config.get('expect_result'),
                                 value=assert_result)
                # 写测试结果 字体颜色绿色
                self.excel.write(sheet_name=sheet_name, row=cases[-1], column=cell_config.get('status'),
                                 value='PASS！', color='00FF00')
                assert True
            except Exception as e:
                self.__step(assert_result=e, response_contain=response.text, url=self.my_inter.path,
                            params=cases[cell_config.get('params') - 1])
                # 写测试结果 字体颜色红色
                self.excel.write(sheet_name=sheet_name, row=cases[-1], column=cell_config.get('expect_result'),
                                 value=str(e), color='FF0000')
                # 写测试结果 字体颜色红色
                self.excel.write(sheet_name=sheet_name, row=cases[-1], column=cell_config.get('status'),
                                 value='FAIL', color='FF0000')
                assert False


if __name__ == '__main__':
    os.system(r'rd ..\myreport\temp\ /s/q')
    # 使用allure 需要自行下载安装allure
    pytest.main(["-s", "test01.py", "--alluredir", "../myreport/temp"])
    # 执行命令行，生成allure测试报告
    os.system('allure generate ../myreport/temp -o ../myreport/report --clean')
