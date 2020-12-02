# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   my_email.py
@Time   :   2020-11-20 10:50
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   负责邮件发送
"""
import os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL
from common.summery_report import SummeryReport
from common.type_judgment import is_Null
from global_variables import email_config, get_abspath, test_url


class MyEmail:
    charset = 'utf-8'

    def __init__(self, file_path='data/cases/result_人脸设备接口.xlsx'):
        self.email_form = email_config.get('mailFrom')
        self.password = email_config.get('passWord')
        self.email_to = email_config.get('mailTo')
        self.smtp_server = 'smtp.' + self.email_form[self.email_form.find('@') + 1: len(self.email_form)]
        self.email_title = email_config.get('mailTitle')
        self.email_module = email_config.get('mailModule') if not is_Null(
            email_config.get('mailModule')) else 'module1.html'
        # 获取html用例模板
        with open(file=get_abspath('data/email_module/') + '/' + self.email_module, mode='r',
                  encoding=self.charset) as f1:
            self.email_content = f1.read()
        self.file_path = get_abspath(file_path)
        # 附件
        self.email_enclosure = [self.file_path, ]
        self.summery_report = SummeryReport(self.file_path)

    def send(self):
        server = SMTP_SSL(self.smtp_server)
        server.ehlo(self.smtp_server)
        server.login(self.email_form, self.password)
        message = self.__get_message()
        server.sendmail(self.email_form, self.email_to.split(','), message.as_string())
        server.quit()

    def __get_message(self):
        # 支持附件的邮件
        msg = MIMEMultipart(_charset=self.charset)
        # 添加自定义昵称
        h = Header("123", self.charset)
        h.append('<' + self.email_form + '>', self.charset)
        msg['From'] = h
        msg['From'] = self.email_form
        msg['To'] = self.email_to
        msg['Subject'] = self.email_title

        # 邮件正文内容
        msg.attach(MIMEText(self.__get_email_content_html(), 'html', self.charset))
        # 添加附件
        for i in range(len(self.email_enclosure)):
            att1 = MIMEText(open(self.email_enclosure[i], 'rb').read(), 'base64', _charset=self.charset)
            att1['Content-Type'] = 'application/octet-stream'
            att1.add_header('Content-Disposition',
                            'attachment',
                            filename=('gbk', '', os.path.basename(self.email_enclosure[i])))
            msg.attach(att1)
        return msg

    def __get_email_content_html(self):
        """
        生成可发送的html文件
        """
        return '详细测试信息请见：' + test_url + self.__get_summary().replace('mailbody', self.__get_details())

    def __get_summary(self):
        """
        获取邮件汇总信息
        :return:
        """
        summary = self.summery_report.get_summery_info()
        text = self.email_content
        text = text.replace('XXX自动化测试报告全局唯一', summary.get('title'))
        # 替换汇总信息
        # print(summary)
        for key in summary.keys():
            if summary[key] == "PASS":
                text = text.replace(
                    '<font style="font-weight: bold;font-size: 14px;color: #00d800;">status</font>',
                    '<font style="font-weight: bold;font-size: 14px;color: #00d800;">PASS</font>')
                text = text.replace('scolor', '#00d800;')
            elif summary[key] == "FAIL":
                text = text.replace(
                    '<font style="font-weight: bold;font-size: 14px;color: #00d800;">status</font>',
                    '<font style="font-weight: bold;font-size: 14px;color: red;">FAIL</font>')
                text = text.replace('scolor', 'red;')
            else:
                text = text.replace(key, str(summary[key]))

        return text

    def __get_details(self):
        """
        获取详解结果列表
        :return:
        """
        groups = self.summery_report.get_group_info()

        # 获取分组显示
        tr = '<tr><td width="100" height="28" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">分组信息</td><td width="80" height="28" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">用例总数</td><td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">通过数</td><td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc; color:scolor;">状态</td></tr>'
        trs = ""
        for i in range(len(groups)):
            tmp = tr.replace('分组信息', str(groups[i].get('group_name')))
            tmp = tmp.replace('用例总数', str(groups[i].get('case_count')))
            tmp = tmp.replace('通过数', str(groups[i].get('pass_count')))
            if str(groups[i].get('status')) == "PASS":
                tmp = tmp.replace('scolor', '#00d800')
            else:
                tmp = tmp.replace('scolor', 'red')
            tmp = tmp.replace('状态', str(groups[i].get('status')))
            trs = trs + tmp

        return trs


if __name__ == '__main__':
    email = MyEmail()
    email.send()