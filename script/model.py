# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   model.py
@Time   :   2020-11-27 10:44
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import allure
import pytest
import common.my_assert as obj
from api.inter import Inter
from common import type_judgment
from common.excel_tool import ExcelTool
from common.logger import logger
from common.my_color import MyColor
from global_variables import get_abspath, cell_config, host_dev


class ModelScript:

    def __init__(self, file_path='data/cases/人脸设备接口.xlsx'):
        # 实例化Inter接口
        self.my_inter = Inter(host=host_dev)
        # 实例化ExcelTool类
        self.excel = ExcelTool(get_abspath(file_path))
        # 每个方法执行参数化之前，都需要设置sheet页后，在读取excel获取对应的self.case
        self.sheet_names = self.excel.get_sheet_names()
        self.name = None
        self.case = None
        
    # @allure.step('请求地址:{url}')
    def my_method(self, url):
        with allure.step('请求地址: {}'.format(url)):
            pass

    @allure.step('点击查看请求参数:')
    def my_params(self, params):
        pass

    # @allure.step('响应结果:{response}')
    def my_response(self, response):
        with allure.step('响应结果: {}'.format(response)):
            pass

    # @allure.step('断言结果:{assert_result}')
    def my_assert(self, assert_result):
        with allure.step('断言结果: {}'.format(assert_result)):
            pass

    def __step(self, assert_result, response_contain, url, params):
        self.my_assert(str(assert_result))
        self.my_method(str(url))
        self.my_params(str(params))
        self.my_response(str(response_contain))

    def model_case(self, cases):
        self.case = cases
        self.__set_allure()
        response = self.__send()
        self.__update_allure(response)
        self.__assert(response)

    def __send(self):
        # 写日志 现在出现写特殊字符报错，后期解决
        try:
            logger.debug('正在执行的用例为：{}'.format(self.case))
        except Exception as e:
            logger.exception(e)
        # 反射调用接口关键字
        response = None
        # print(self.case[::-1])
        try:
            self.my_inter.set_case(self.case)
            # 关联成功后，修改result_xxx.xlsx 中的参数列
            if not type_judgment.is_Null(self.my_inter.params):
                self.case[cell_config.get('params') - 1] = self.my_inter.relation_params_temp
                self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('params'),
                                 value=self.my_inter.relation_params_temp)
            # 通过反射获取Inter类的函数
            response = getattr(self.my_inter, self.case[cell_config.get('method') - 1])()
        except Exception as e1:
            # 写请求返回结果 字体颜色红色
            self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('result'),
                             value=e1,
                             color=MyColor.RED)
            # 写测试结果 字体颜色红色
            self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('status'),
                             value='FAIL', fg_color=MyColor.RED)
        return response

    def __set_allure(self):
        name = self.case[cell_config.get('model') - 1]
        if not self.name == name:
            allure.dynamic.feature(name)
            self.name = name
        else:
            allure.dynamic.feature(self.name)
        # 设置allure报告的title
        allure.dynamic.title(self.case[cell_config.get('id') - 1] + ':' + self.case[cell_config.get('case_name') - 1])
        # 设置allure报告的 描述
        allure.dynamic.description(
            self.case[cell_config.get('interface_name') - 1] + "，" + self.case[cell_config.get('case_name') - 1])
        # allure.severity()

    def __update_allure(self, response):
        if response is None:
            allure.severity(allure.severity_level.BLOCKER)
            self.my_method(str(self.my_inter.path))
            self.my_params(str(self.case[cell_config.get('params') - 1]))
            self.my_response(response.text)
            # return False
            # raise Exception('无任何返回')
        # 写请求返回结果
        self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('result'),
                         value=response.text)

    def __assert(self, response):
        # 断言
        try:
            # 通过反射获取模块my_assert.py的函数
            func = getattr(obj, self.case[cell_config.get('assert_model') - 1])
            # 执行反射获取的函数

            if str(func).__contains__('assert_jsonpath'):
                assert_result = func(response, self.case[cell_config.get('expect_param1') - 1],
                                     self.case[cell_config.get('expect_param2') - 1])
            else:
                assert_result = func(response, self.case[cell_config.get('expect_param1') - 1])

            logger.debug('断言结果：{}'.format(assert_result))
            # allure上显示测试步骤
            self.__step(assert_result=assert_result, response_contain=response.text, url=self.my_inter.path,
                        params=self.case[cell_config.get('params') - 1])
            # 写断言结果 字体颜色绿色
            self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('expect_result'),
                             value=assert_result)
            # 写测试结果 字体颜色绿色
            self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('status'),
                             value='PASS', fg_color=MyColor.GREEN)
            assert True
        except Exception as e:
            allure.severity(allure.severity_level.CRITICAL)
            logger.debug('断言结果：{}'.format(e))
            self.__step(assert_result=e, response_contain=response.text, url=self.my_inter.path,
                        params=self.case[cell_config.get('params') - 1])
            # 写断言结果 字体颜色红色
            self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('expect_result'),
                             value=str(e), color=MyColor.RED)
            # 写测试结果 字体颜色红色
            self.excel.write(sheet_name=self.case[-2], row=self.case[-1], column=cell_config.get('status'),
                             value='FAIL', fg_color=MyColor.RED)

            pytest.mark.xfail(e)
            assert False
