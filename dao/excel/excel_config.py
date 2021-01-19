# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   excel_config.py
@Time   :   2021-01-19 14:00
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""


class ExcelConfig:
    """
    改类 的变量与测试用例的标题（Excel）的列一一对应
    序号、分组信息、用例名、用例描述、测试步骤、关键字、输入1、输入2、输入3、是否执行、执行状态、实际结果、备注
    """
    ID = 0
    GROUP = 1
    CASE_NAME = 2
    CASE_DESCRIBE = 3
    CASE_STEP = 4
    METHOD = 5
    PARAMETER_1 = 6
    PARAMETER_2 = 7
    PARAMETER_3 = 8
    IS_RUN = 9
    STATUS = 10
    RESULT = 11
    DESCRIBE = 11

    @classmethod
    def getXlsxColumn(cls, column):
        """
        openpyxl 读取Excel的是从1开始，这里需要加1
        :param column:
        :return:
        """
        return column + 1


class CaseStep:
    """
    这里对应excel_tool 方法读取Excel时将测试步骤写list的顺序（下标）,
    顺序如下：
    测试步骤、关键字、输入1、输入2、输入3、备注、行、sheet页
    """
    step_name = 0
    method = 1
    parameter1 = 2
    parameter2 = 3
    parameter3 = 4
    describe = 5
    excel_row = 6
    excel_sheet = 7


if __name__ == '__main__':
    print(ExcelConfig.getXlsxColumn(ExcelConfig.ID))