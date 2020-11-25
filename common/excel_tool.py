#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : excel_tool.py
@Time   : 2020/11/25 8:57
@Author : yd
@Version: 1.0
@ToDo    : 使用openpyxl进行excel的读写操作
"""
import os
import shutil

from xlutils.copy import copy
import openpyxl
from openpyxl.styles import Font

from global_variables import get_abspath, cell_config


class ExcelTool:
    
    def __init__(self, file_path):
        self.file_path = get_abspath(file_path)
        self.result_file_path = os.path.dirname(file_path) + os.sep + 'result_' + os.path.basename(file_path)
        self.workbook = openpyxl.load_workbook(self.file_path)
        self.workbook_write = None
        self.sheet_write = None
        self.sheet = None
        self.row = None
        self.column = None
        self.reading_row = 1
    
    def get_sheet_names(self):
        return self.workbook.sheetnames
    
    def set_sheet(self, sheet_name):
        """
        进行excel读写之前，需要设置要读取或者写入的sheet
        :param sheet_name:
        :return:
        """
        self.sheet = self.workbook[sheet_name]
        self.sheet_write = self.sheet
        self.row = self.sheet.max_row
        self.column = self.sheet.max_column
        self.reading_row = 1
    
    def read(self, sheet_name):
        self.set_sheet(sheet_name)
        lines = []
        # 遍历每行数据，跳过第一行的标题拦
        print('row =', self.row)
        for i in range(2, self.row + 1):
            # line = {}
            line = []
            print(self.sheet.cell(i, cell_config.get('is_run')).value)
            if self.sheet.cell(i, cell_config.get('is_run')).value == '是':
                # line['path'] = self.sheet.cell(i, cell_config.get('path')).value.lower()
                # line['method'] = self.sheet.cell(i, cell_config.get('method')).value
                # line['params'] = self.sheet.cell(i, cell_config.get('params')).value
                # line['is_run'] = self.sheet.cell(i, cell_config.get('is_run')).value
                # line['expect'] = self.sheet.cell(i, cell_config.get('expect')).value
                # line['result'] = self.sheet.cell(i, cell_config.get('result')).value
                # line['desc'] = self.sheet.cell(i, cell_config.get('desc')).value
                for j in range(1, self.column + 1):
                    if self.sheet.cell(i, j).value is None:
                        line.append('')
                    else:
                        if j == cell_config.get('method'):
                            line.append(str(self.sheet.cell(i, j).value.lower().replace('\n', '').replace(' ', '')))
                        else:
                            line.append(str(self.sheet.cell(i, j).value.replace('\n', '').replace(' ', '')))
                else:
                    # 把row加入lines中， 方便其他地方调用
                    line.append(i)
                lines.append(line)
        return lines
    
    def write(self, sheet_name, row=1, column=1, value='', color='000000'):
        """
        按行列写入对应的excel对的cell,写完后记得保存
        :param sheet_name: 需要写的sheet页
        :param row: 行
        :param column: 列
        :param value: 值
        :param color: 字体颜色
        :return:
        """
        self.sheet_write = self.workbook_write[sheet_name]
        row = int(row)
        column = int(column)
        if row > 0 and column > 0:
            try:
                cell = self.sheet_write.cell(row=row, column=column, value=value)
                font = Font(name='Arial',
                            size=11,
                            bold=False,
                            italic=False,
                            vertAlign=None,
                            underline='none',
                            strike=False,
                            color=color)
                cell.font = font
            except Exception as e:
                self.sheet_write.cell(row, column).value = e
            self.save()
        else:
            print('输入的xlsx的行和列必须大于1')
    
    def save(self):
        self.workbook_write.save(self.result_file_path)

    def copy(self):
        print(self.file_path)
        print(self.result_file_path)
        shutil.copy(self.file_path, self.result_file_path)
        self.workbook_write = openpyxl.load_workbook(self.result_file_path)
        self.set_sheet(self.workbook_write.sheetnames[0])
