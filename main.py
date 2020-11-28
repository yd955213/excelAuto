import os
import time
import pytest
import global_variables
from common.my_email import MyEmail

os.system(r'rd myreport\temp\ /s/q')

os.system(r'rd logs\log.log /s/q')

global_variables.time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 使用allure 需要自行下载安装allure
pytest.main(["-s", "script/", "--alluredir", "./myreport/temp"])
# 执行命令行，生成allure测试报告
os.system('allure generate ./myreport/temp -o ./myreport/report --clean')

global_variables.time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
MyEmail().send()
