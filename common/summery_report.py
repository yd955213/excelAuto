#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : summery_report.py
@Time   : 2020/11/21 11:24
@Author : yd
@Version: 1.0
@ToDo    :  对执行后的用例结果进行汇总分析
"""
import global_variables
from dao.excel.excel_tool import ExcelTool
from global_variables import cell_config, get_abspath, email_config


class SummeryReport:

    def __init__(self, file_path):
        # 汇总信息：report_title, tester, developer, case_version, case_count, pass_rate, start_time, end_time
        self.summery_info = {}

        # 分组信息: group_name, group_case_count, pass_count, status
        self.group_info = []
        self.excel = ExcelTool(file_path)
        self.sheets = self.excel.get_sheet_names()

    def get_summery_info(self, ):
        """
        获取用例信息
        :param file_path: 用例文件路径
        :return:
        """
        # 重新赋值
        self.summery_info.clear()
        self.summery_info['title'] = email_config.get('reportTitle')
        self.summery_info['runtype'] = email_config.get('runtype')
        self.summery_info['tester'] = email_config.get('tester')
        self.summery_info['developer'] = email_config.get('developer')
        self.summery_info['appVersion'] = email_config.get('appVersion')
        self.summery_info['interface'] = email_config.get('interface')
        self.summery_info['casecount'] = ''
        self.summery_info['passrate'] = ''
        self.summery_info['starttime'] = global_variables.time_start
        self.summery_info['endtime'] = global_variables.time_end
        self.summery_info['status'] = ''

        case_pass_count = 0
        case_fail_count = 0
        case_block_count = 0
        case_not_run_count = 0
        for sheet in self.sheets:
            self.excel.set_sheet(sheet)
            for row in range(2, self.excel.row + 1):
                line = self.excel.read_no_pass_line(row)
                # 过滤写分组信息和用例名称的列
                if line[int(cell_config.get('method')) - 1] == '' and line[int(cell_config.get('path')) - 1] == '':
                    pass
                # 是一个可执行的测试用例
                elif not line[int(cell_config.get('method')) - 1] == '':
                    if line[int(cell_config.get('is_run')) - 1] == '是':
                        if line[int(cell_config.get('status')) - 1].upper() == 'FAIL':
                            case_fail_count += 1
                        elif line[int(cell_config.get('status')) - 1].upper() == 'PASS':
                            case_pass_count += 1
                        else:
                            case_block_count += 1
                    else:
                        case_not_run_count += 1

        case_count = case_fail_count + case_pass_count + case_block_count + case_not_run_count

        try:
            pass_rate = (int((case_pass_count * 10000) / (case_count - case_not_run_count))) / 100
        except Exception as e:
            pass_rate = 0.0

        self.summery_info['casecount'] = str(case_count)
        self.summery_info['passrate'] = str(pass_rate) + '%'
        if case_fail_count > 0 or case_block_count > 0:
            self.summery_info['status'] = 'FAIL'
        else:
            self.summery_info['status'] = 'PASS'

        # self.summery_info['case_fail_count'] = case_fail_count
        # self.summery_info['case_pass_count'] = case_pass_count
        # self.summery_info['case_block_count'] = case_block_count
        return self.summery_info

    def get_group_info(self):
        """
        获取分组信息
        :param file_path:
        :return:
        """
        self.group_info.clear()
        case_count = 0
        pass_count = 0
        group_smale = {}
        group_name = ''
        for sheet in self.sheets:
            self.excel.set_sheet(sheet)
            group_smale.clear()
            sign = False
            for i in range(2, self.excel.row + 1):
                line = self.excel.read_no_pass_line(i)
                if line[int(cell_config.get('is_run')) - 1] == '是':
                    if i == 2:
                        group_name = line[int(cell_config.get('model')) - 1]

                    if line[int(cell_config.get('status')) - 1].upper() == 'PASS':
                        pass_count += 1
                    else:
                        sign = True
                    case_count += 1

            # 分组
            if sign:
                status = 'FAIL'
            else:
                status = 'PASS'
            if case_count > 0:
                group_smale['group_name'] = group_name
                group_smale['case_count'] = case_count
                group_smale['pass_count'] = pass_count
                group_smale['fail_count'] = case_count - pass_count
                group_smale['status'] = status
                # print('group_smale =', group_smale)
                self.group_info.append(group_smale)
            case_count = 0
            pass_count = 0
            group_smale = {}
        return self.group_info


if __name__ == '__main__':
    test = SummeryReport(get_abspath('data/cases/人脸设备接口.xlsx'))
    print(test.get_summery_info())
    print(test.get_group_info())
