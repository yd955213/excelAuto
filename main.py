import os
import time
import pytest

import global_variables
from global_variables import get_abspath, time_start, time_end
from common.my_email import MyEmail

os.system(r'rd myreport\temp\ /s/q')
os.system(r'rd logs\log.log /s/q')

global_variables.time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 使用allure 需要自行下载安装allure
pytest.main(["-s", "script/", "--alluredir", "./myreport/temp"])
# 执行命令行，生成allure测试报告
os.system('allure generate ./myreport/temp -o ./myreport/report --clean')
os.system('copy {} {}'.format(get_abspath('environment.properties'),
                              get_abspath('myreport/temp/')))
os.system('copy {} {}'.format(get_abspath('environment.properties'),
                              get_abspath('myreport/report/')))

global_variables.time_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 邮件发送
MyEmail('data/cases/result_人脸设备接口.xlsx').send()

# 部署到tomcat 便于别人查看allure报告
os.system('cd E:/testingEnvironment/apache-tomcat-8.5.46/bin/&shutdown.bat')
os.system(r'rd/s/q E:\testingEnvironment\apache-tomcat-8.5.46\webapps\inter\\')
os.system(r'xcopy/s/q/a E:\pythonWorkPlace\excelAuto\excelAuto\myreport\report E:\testingEnvironment\apache-tomcat-8.5.46\webapps\inter\ /e')
os.system('cd E:/testingEnvironment/apache-tomcat-8.5.46/bin/&startup.bat')