# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   appiumUI.py
@Time   :   2020-12-07 14:28
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import os
import threading
import time
import traceback

from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy as By
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from common import type_judgment
from common.logger import logger
from common.read_xml import ReadSetInfo
from global_variables import ui_cell_config, get_abspath


def _get_value(value='None', is_select=False):
    if not is_number(value):
        if value == '关闭' or value == '自动' or value == '限识别区域' or value == '反序' or value.lower() == 'false':
            value = '2 or False'
        elif value == '打开' or value == '一周' or value == '不限识别区域' or value == '常开' or value == '正序' or value.lower() == 'true':
            value = '1 or True'
        elif value == '一天' or value == '常关' or value == '设备不支持' or value == '卡号':
            value = '0'
        elif value == '人脸框':
            value = 'rect'
        elif value == '隐藏':
            value = 'none'
        elif value == '姓名':
            value = 'true' if is_select else 'false'
        elif value == '工号':
            value = 'true' if is_select else 'false'
        elif value == '部门':
            value = 'true' if is_select else 'false'
        elif value == '维根34':
            value = '34'
        elif value == '维根26':
            value = '26'
        elif value == '人脸ID':
            value = '34'
        else:
            value = '未定义（{}）'.format(value)
    return value


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class AppiumUI:
    """
    app UI 自动化关键字封装类
    """

    def __init__(self):
        # driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', appium_config)
        # driver.implicitly_wait(10)
        self.driver = None
        self.port = None
        self.excel = None
        self.excel_write_row = 1
        self.sheet_name = None
        self.relation = None
        self.set_info = None
        self.temp_dict = None
        self.temp_str = None

    def start_appium(self, appium_path='', port='4723'):
        """
        使用node启动appium服务
        :param appium_path: appium的安装路径
        :param port: 服务的发布端口
        :return:
        """
        self.port = port
        cmd = "node " + appium_path + r'\resources\app\node_modules\appium\build\lib\main.js -p' + port
        th = threading.Thread(target=os.system, args=(cmd,))
        # 子线程开始工作
        th.start()
        time.sleep(5)

    def stop_appium(self, port='4723'):
        """
        停止appium服务
        :param port: 需要停止的appium的端口号
        :return:
        """
        cmd = 'netstat -aon | findstr ' + port
        res = os.popen(cmd).read().split('\n')
        res = res[0].split(' ')
        if len(res) > 1:
            pid = res[len(res) - 1]
            cmd = 'taskkill /F /PID ' + pid
            os.system(cmd)
        else:
            print('端口未占用')

    def startapp(self, conf='{}', t='10'):
        """
        启动APP
        :param conf: 连接appium，启动APP的配置，json格式字符串
        '''appium_config = {
                'platformName': 'Android',
                'platformVersion': '9',
                'deviceName': '1234567890',
                'appPackage': 'com.das.face',
                'appActivity': '.activity.LoadingActivity',
                'noReset': True,  # 清除缓存记录，微信小程序测试必须加上
                'unicodeKeyboard': True,
                'resetKeyboard': True,  # 用来在自动化输入中文
                'automationName': 'uiautomator2'  # 小程序 如果还是操作不了， uiautomator1与uiautomator2互换
            }'''
        :param t: 启动APP需要等待的时间
        :return:
        """
        # conf = str(conf).replace('\n', '')
        # conf = json.loads(conf)
        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.port), conf)
        self.driver.implicitly_wait(5)
        time.sleep(float(t))

    def __find_element(self, locator="None"):
        """
        兼容3中查找方式：id、xpath、accessibility
        格式如下：id :com.das.face:id/etIp4
                xpath：//*[@text="设备名称"]/../*[3]
                accessibility： 部分APP软件会使用该定位
        :param locator:
        :return:
        """
        element = None
        try:
            if not locator == 'None':
                if locator.find(':id/') > 0:
                    element = self.driver.find_element_by_id(locator)
                elif locator.startswith('//'):
                    element = self.driver.find_element_by_xpath(locator)
                else:
                    element = self.driver.find_element_by_accessibility_id(locator)
                self.__write_excel(True)
            # else:
            #     self.__write_excel(False, '定位表达式为空')
        except Exception as e:
            element = None
            logger.exception(e.__str__())
            self.__write_excel(False, dsc='未定位到元素，请检查定位表达式是否正确；错误信息：{}'.format(e.__str__()))

        logger.info('locator = {}，element = {}'.format(locator, element))

        return element

    def sleep(self, t='1.0'):
        try:
            time.sleep(float(t))
        except:
            time.sleep(1.0)

    def long_press(self, locator="None", t="3.0"):
        """
        长安元素，默认3s
        :param locator: 元素定位表达式
        :param t:  默认长按3s
        :return:
        """
        self.sleep()
        touchAction = TouchAction(self.driver)
        # el = self.__find_element("com.das.face:id/ivLogo")
        el = self.__find_element(locator)
        if el is not None:
            self.__write_excel(True)
            touchAction.long_press(el, t * 1000).perform()
            return True
        else:
            return False

    def click(self, locator="None", t='1.0'):
        """
        点击元素
        :param locator: 元素定位表达式
        :param t: 默认点击之前等待1.0秒
        :return:
        """
        self.sleep(t)

        el = self.__find_element(locator)

        if el is not None:
            el.click()
            return True
        else:
            return False

    def input(self, locator="None", value='None', t='1.0'):
        """
        文本框输入值
        :param locator:  元素定位表达式
        :param value； 需要输入的值
        :param t:  默认点击之前等待1.0秒
        :return:
        """
        self.sleep(t)

        el = self.__find_element(locator)

        if el is not None:
            el.clear()
            if not (value == 'None' or value == ''):
                el.send_keys(value)
            return True
        else:
            return False

    def swipe(self, location1="(1,1)", location2="(100,100)", t="1"):
        """
        滑动
        :param location1: 第一个坐标的起始位置，格式为（x1,y1）
        :param location2: 第二个坐标的起始位置，格式为（x2,y2）
        :return:
        """
        self.sleep(t)

        lo1 = eval(location1)
        lo2 = eval(location2)
        TouchAction(self.driver).press(x=lo1[0], y=lo1[1]).move_to(x=lo2[0], y=lo2[1]).release().perform()
        return True

    def either_or_click(self, locator1="None", locator2='None', t='1.0'):
        """
        该关键字模拟：有些测试场景测试功能会切换界面，失败则不会；当locator1定位到元素则点击locator1元素，当locator1无法定位后，使用
        locator2进行定位
        :param locator1: 
        :param locator2: 
        :param t: 
        :return: 
        """
        self.sleep(t)
        el = self.__find_element(locator1)
        if el is None:
            el = self.__find_element(locator2)

        if el is None:
            self.__write_excel(True, '', '未定位到元素')
            # return True
        else:
            el.click()
            # self.__write_excel(True)
        return True

    def quit(self):
        """
        退出appium
        :return:
        """
        self.driver.quit()

    def assert_find_element(self, locator='None', value='True', t='1'):
        """
        断言是否可以找到元素，主要用于界面切换，检查是否切换成功
        :param locator: 元素定位表达式
        :param value: 是否找到元素(True, False),默认True
        :param t: 断言前默认等待1s
        :return:
        """
        self.sleep(t)
        el = self.__find_element(locator)
        value = str(value).lower()

        if el is None and value == 'false':
            flag = True
            result = False
        elif el is not None and value == 'true':
            flag = True
            result = True
        else:
            flag = False
            result = False

        if flag:
            msg = '断言成功'
        else:
            msg = '断言失败'

        self.__write_excel(flag, '{}，预期：{}，实际：{}'.format(msg, value, result))
        return result

    def assert_element_text(self, locator='None', value='None', t='1'):
        """
        断言元素的文本值是否包含预期值
        :param locator:
        :param value:
        :param t:
        :return:
        """
        self.sleep(t)
        el = self.__find_element(locator)
        if el is not None:
            result = el.text
            if el.text.__contains__(value):
                self.__write_excel(True, '断言成功，预期：{}，实际：{}'.format(value, result))
                return True
            else:
                self.__write_excel(False, '断言失败，预期：{}，实际：{}'.format(value, result))
                return False

    def assert_toast(self, locator='None', value='None'):
        try:
            # 显示等待
            WebDriverWait(self.driver, timeout=5, poll_frequency=0.2).until(
                EC.presence_of_element_located((By.XPATH, locator)))
            self.__write_excel(True, '断言成功，预期toast弹框提示：{}，实际：toast弹窗可以找的'.format(value))
            return True
        except Exception as e:
            self.__write_excel(False, '断言失败，预期toast弹框提示：{}，实际：未定位到元素，错误信息：{}'.format(value, e.__str__()))
            return False

    def __get_set_info(self, file_name='SetInfo.xml'):
        """
        获取app的系统设置的配置文件，当配置文件发生变化时，需要修改路径： data/data/com.das.face/shared_prefs
        :param file_name: 默认对去文件：SetInfo.xml
        :return:
        """
        file_path = get_abspath('config/{}'.format(file_name))
        if os.path.exists(file_path):
            os.system('del /s/q {}'.format(file_path))
        os.system('adb root')
        os.system(r'adb pull data/data/com.das.face/shared_prefs/{} {}'.format(file_name, get_abspath('config/')))
        return ReadSetInfo(file_name).get_setInfo()

    def exit_screen_saver(self):
        """
        退出屏幕保护；在屏幕位置之中点击一下
        :return:
        """
        self.sleep(0.1)
        touchAction = TouchAction(self.driver)
        touchAction.tap(x=100, y=100).release().perform()
        self.__write_excel(True)
        return True

    def set_sheet_name(self, sheet_name):
        self.sheet_name = sheet_name

    def set_excel(self, excel):
        self.excel = excel

    def __write_excel(self, status=False, msg='', dsc=''):
        """
        写入关键字运行结果
        :param status: 运行的状态
        :param msg: 实际运行结果
        :param dsc: 备注信息
        :return: 无
        """
        if status is True:
            self.excel.write(self.sheet_name, self.excel_write_row, ui_cell_config.get('status'), "PASS", '000000')
        elif status is False:
            self.excel.write(self.sheet_name, self.excel_write_row, ui_cell_config.get('status'), "FAIL", 'FF0000')
        else:
            self.excel.write(self.sheet_name, self.excel_write_row, ui_cell_config.get('status'), str(status), 'FF0000')

        if not type_judgment.is_Null(msg):
            # 有时候实际结果过长，我们就只保存前30000个字符
            msg = str(msg)
            if len(msg) > 30000:
                msg = msg[0:30000]
            self.excel.write(self.sheet_name, self.excel_write_row, ui_cell_config.get('result'), str(msg))

        if not type_judgment.is_Null(dsc):
            try:
                self.excel.set_sheet(self.sheet_name)
                # print('******************read_cell = ({}, {})**********************'
                #       .format(self.excel_write_row, ui_cell_config.get('describe')))
                logger.debug('read_cell = ({}, {})'.format(self.excel_write_row, ui_cell_config.get('describe')))
                dsc = str(dsc) + self.excel.read_cell(self.excel_write_row, ui_cell_config.get('describe'))
            except Exception as e:
                logger.exception(e)
            self.excel.write(self.sheet_name, self.excel_write_row, ui_cell_config.get('describe'), str(dsc))

    def get_element_text(self, locator='None'):
        el = self.__find_element(locator)
        if el is not None:
            self.temp_str = el.text if not el.text == '' else str(el.is_selected())
            self.__write_excel(True)
            return True
        else:
            self.temp_str = "未定位到元素"
            self.__write_excel(False)
        return False

    def clean_temp_dict(self):
        """
        初始化临时字典，用于对比
        :return:
        """
        self.temp_dict = {}
        self.temp_str = "None"
        self.__write_excel(True)
        return True

    def add_temp_dict(self, key='None', value='None'):
        """
        添加临时字典，用于对比; value为空时，为get_element_text（）获取的值，适用于开关UI按钮
        :param key:键
        :param value:值
        :return:
        """
        if key == '':
            key = 'None'
        if value == 'None' or value == '':
            self.temp_dict[key] = _get_value(self.temp_str)
        else:
            self.temp_dict[key] = value
        self.__write_excel(True, dsc=self.temp_dict)
        return True

    def assert_temp_dict(self):
        """
        对配置文件进行断言，使用方法：
        1、使用前有限调用方法：clean_temp_dict（），初始化临时字典：self.temp_dict；
        2、调用get_element_text（），获取UI元素的文本值；
        3、再调用：add_temp_dict（key），对程序内部self.temp_dict进行赋值；
        4、再调用本方法，进行断言，
        :return:
        """
        self.sleep(1)
        config_dict = self.__get_set_info('SetInfo.xml')
        dic = self.__get_set_info('settingParam.xml')
        for key in dic.keys():
            config_dict[key] = dic[key]
        flag = True
        msg = '断言失败，'
        for key in self.temp_dict.keys():
            if not str(self.temp_dict.get(key)).lower().__contains__(str(config_dict.get(key)).lower()):
                flag = False
                msg += '预期：{}={}，实际：{}={}；'.format(key, self.temp_dict.get(key), key, config_dict.get(key))
        if flag:
            msg = '断言成功！预期：{}'.format(self.temp_dict)

        self.back_to_system()
        self.__write_excel(flag, msg=msg)
        return flag

    def assert_is_select(self, locator='None', value='None'):
        """
        断言元素是否被选中
        :param locator:
        :param value: 预期结果值
        :return: boolean
        """
        el = self.__find_element(locator)
        if el is not None:
            result = el.is_selected()
            if str(result).lower() == value.lower():
                self.__write_excel(True, '断言成功，预期：{}，实际：{}'.format(value, result))
                return True
            else:
                self.__write_excel(False, '断言失败，预期：{}，实际：{}'.format(value, result))
                return False
        else:
            self.__write_excel(False, '断言失败，预期：{}，实际：{}'.format(value, '未找到元素'))
            return False

    def select_check_box(self, locator='None', value='true'):
        """
        是否选中复选框，value:true为选中，其他为不选中
        :param locator:
        :param value: true为选中，其他为不选中
        :return:
        """
        el = self.__find_element(locator)
        if el is not None:
            if value.lower() == 'true':
                if not el.is_selected():
                    el.click()
            elif value.lower() == 'false':
                if el.is_selected():
                    el.click()
            return True
        else:
            return False

    def back_to_home_screen(self, times='3'):
        """
        回退带设备待机界面
        :param times: 回退次数，没退出一个界面，次数减1
        :return:
        """
        for i in range(0, times):
            self.sleep(0.2)
            self.driver.back()
        return True

    def back_to_system(self, locator='//*[@text="系统管理"]'):
        """
        界面回退包含locator定位元素的界面
        :param locator:
        :return:
        """
        while True:
            el = self.__find_element(locator)
            if el is not None:
                # __find_element 未找到元素时，会在 dsc 栏写异常信息，这里循环查找到后，清除异常信息
                self.__write_excel(True, dsc='')
                break
            else:
                self.driver.back()
                # self.__write_excel(False)   # 可要可不要
        return True
