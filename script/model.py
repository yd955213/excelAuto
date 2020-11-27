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
import traceback
import common.my_assert as obj
from api.inter import Inter
from common.excel_tool import ExcelTool
from common.logger import logger
from global_variables import get_abspath, cell_config, host_dev


class ModelScript:

    def __init__(self, file_path='data/cases/人脸设备接口.xlsx'):
        # 实例化Inter接口
        self.my_inter = Inter(host=host_dev)
        # 实例化ExcelTool类
        self.excel = ExcelTool(get_abspath(file_path))
        # 每个方法执行参数化之前，都需要设置sheet页后，在读取excel获取对应的cases
        self.sheet_names = self.excel.get_sheet_names()
        self.name = None

    @allure.step('请求地址:{url}')
    def my_method(self, url):
        pass

    @allure.step('请求参数')
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
        self.my_method(url)
        self.my_params(params)
        self.my_response(response_contain)

    def model_case(self, cases):
        name = cases[cell_config.get('model') - 1] + ':' + cases[cell_config.get('path') - 1]
        if not self.name == name:
            allure.dynamic.feature(name)
            self.name = name
        else:
            allure.dynamic.feature(self.name)
        # 设置allure报告的title
        allure.dynamic.title(cases[cell_config.get('case_name') - 1])
        # 设置allure报告的 描述
        allure.dynamic.description(cases[cell_config.get('interface_name') - 1] + cases[cell_config.get('case_name') - 1])
        # allure.severity()
        # 写日志
        logger.info(cases)
        # 调用即可方法下
        response = None
        # print(cases[::-1])
        try:
            logger.info('正在执行的用例为：{}'.format(cases))
            self.my_inter.set_case(cases)
            # 通过反射获取Inter类的函数
            response = getattr(self.my_inter, cases[cell_config.get('method') - 1])()

            if response is not None:
                # 写请求返回结果
                self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('result'),
                                 value=response.text)
        except Exception as e1:
            # 写请求返回结果 字体颜色红色
            self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('result'), value="None", color='FF0000')
            # 写测试结果 字体颜色红色
            self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('status'),
                             value='FAIL', color='FF0000')

        if response is not None:
            try:
                # 通过反射获取模块my_assert.py的函数
                func = getattr(obj, cases[cell_config.get('assert_model') - 1])
                # 执行反射获取的函数
                assert_result = ''
                if func == 'assert_jsonpath':
                    func(response, cases[cell_config.get('expect_param1') - 1],
                         cases[cell_config.get('expect_param2') - 1])
                else:
                    func(response, cases[cell_config.get('expect_param1') - 1])

                assert_result = '断言成功'

                logger.info('断言接口是：{}'.format(assert_result))
                # allure上显示测试步骤
                self.__step(assert_result=assert_result, response_contain=response.text, url=self.my_inter.path,
                            params=cases[cell_config.get('params') - 1])
                # 写断言结果 字体颜色绿色
                self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('expect_result'),
                                 value=assert_result, color='00FF00')
                # 写测试结果 字体颜色绿色
                self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('status'),
                                 value='PASS', color='00FF00')
                assert True
            except Exception as e:
                logger.error('断言接口是：{}'.format(e))
                self.__step(assert_result=e, response_contain=response.text, url=self.my_inter.path,
                            params=cases[cell_config.get('params') - 1])
                # 写断言结果 字体颜色红色
                self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('expect_result'),
                                 value=str(e), color='FF0000')
                # 写测试结果 字体颜色红色
                self.excel.write(sheet_name=cases[-2], row=cases[-1], column=cell_config.get('status'),
                                 value='FAIL', color='FF0000')
                assert False

        else:
            self.my_method(self.my_inter.path)
            self.my_params(cases[cell_config.get('params') - 1])
            self.my_response('None')
            assert False
