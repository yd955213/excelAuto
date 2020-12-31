# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   testUI.py
@Time   :   2020-12-02 17:37
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   appUI脚本录制
"""
import time
import traceback
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
# 361
# appium_config = {
#     'platformName': 'Android',
#     'platformVersion': '8.1.0',
#     'deviceName': '172.168.120.53:5558',
#     'appPackage': 'com.das.face',
#     'appActivity': '.activity.LoadingActivity',
#     'noReset': True,  # 清除缓存记录，微信小程序测试必须加上
#     'unicodeKeyboard': True,
#     'resetKeyboard': True,  # 用来在自动化输入中文
#     'automationName': 'uiautomator2'  # 小程序 如果还是操作不了， 与uiautomator2互换
# }


appium_config = {
    'platformName': 'Android',
    'platformVersion': '9',
    'deviceName': '1234567890',
    'appPackage': 'com.das.face',
    'appActivity': '.activity.LoadingActivity',
    'noReset': True,  # 清除缓存记录，微信小程序测试必须加上
    'unicodeKeyboard': True,
    'resetKeyboard': True,  # 用来在自动化输入中文
    'automationName': 'uiautomator2'  # 小程序 如果还是操作不了， 与uiautomator2互换
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', appium_config)
driver.implicitly_wait(10)
"""
新机开机设置界面
"""
# # 设置远程IP地址
# 设置错误远程IPd地址，点击保存
try:
    time.sleep(3)
    el = driver.find_element_by_id("com.das.face:id/etIp1")
    new_set = True
except:
    new_set = False

if new_set:
    el = driver.find_element_by_id("com.das.face:id/etIp1")
    el.clear()
    el.send_keys('172')

    el = driver.find_element_by_id("com.das.face:id/etIp2")
    el.clear()
    el.send_keys('168')

    el = driver.find_element_by_id("com.das.face:id/etIp3")
    el.clear()
    el.send_keys('120')

    el = driver.find_element_by_id("com.das.face:id/etIp4")
    el.clear()
    el.send_keys('230')

    # 远程端口号输入
    el = driver.find_element_by_xpath('//*[@text="远程端口"]/../*[3]')
    el.clear()
    el.send_keys('19005')
    el = driver.find_element_by_xpath('//*[@text="设备密码"]/../*[3]')
    el.clear()
    el.send_keys('654321')
    el = driver.find_element_by_xpath('//*[@text="设备名称"]/../*[3]')
    el.clear()
    el.send_keys('这是一个UI自动化测试')

    # 设备模式
    el = driver.find_element_by_id('android:id/text1')
    el.click()
    # 选择门禁一体机
    el = driver.find_element_by_xpath('//*[@text="门禁一体机"]')
    el.click()

    # 保存参数按钮
    el = driver.find_element_by_id("com.das.face:id/btnConfirm")
    el.click()
    time.sleep(1)

    # toast弹窗 需要安装appium-uiautomator2-driver
    try:
        xpath = '//*[contains(@text,"远程地址IP格式错误")]'
        WebDriverWait(driver, 5, 0.1).until(expected_conditions.presence_of_element_located((MobileBy.XPATH, xpath)))
        print('find')
    except Exception as e:
        print(traceback.format_exc())
        print('no find')
    time.sleep(10)
"""
输入密码进入设置界面
"""
# 进入设置界面
time.sleep(5)
touchAction = TouchAction(driver)
touchAction.press(x=100, y=100).release().perform()
el = driver.find_element_by_id("com.das.face:id/ivLogo")
touchAction.long_press(el, 6000).perform()
# 输入密码
el = driver.find_element_by_id("com.das.face:id/et_dialog_pwd")
# el.send_keys("654321")
el.send_keys('123456')
# 点击取消
# el = driver.find_element_by_id("android:id/button2")
# el.click()
# 点击确定
el = driver.find_element_by_id("android:id/button1")
el.click()
# 提示信息 com.das.face:id/tv_dialog_info
"""
员工管理
# el = driver.find_element_by_id("com.das.face:id/btn_employee")
# el.click()
"""


"""
# # 通行记录
# el = driver.find_element_by_id("com.das.face:id/btn_pass")
# el.click()
"""
# # 日期控件确定按钮
# el = driver.find_element_by_id("com.das.face:id/btnSubmit")
# el.click()
# # 日期控件：年
# el_year = driver.find_element_by_id("com.das.face:id/year")
# el_mouth = driver.find_element_by_id("com.das.face:id/mouth")
# el_day = driver.find_element_by_id("com.das.face:id/day")
# el_hour = driver.find_element_by_id("com.das.face:id/hour")
# el_min = driver.find_element_by_id("com.das.face:id/min")
# el_second = driver.find_element_by_id("com.das.face:id/second")
#
#
# """
# 系统设置
# """
# # # 系统设置
# el = driver.find_element_by_id("com.das.face:id/btn_system")
# el.click()
# time.sleep(1)
# # 设备名称
# el = driver.find_element_by_xpath('//*[@text="设备名称"]//../*[2]')
# el.clear()
# el.send_keys('你是魔鬼吗')
# # 设备id
# el = driver.find_element_by_xpath('//*[@text="设备ID"]//../*[2]')
# print(el.is_enabled())
# print(el.text)
# # 远程IP地址
# el = driver.find_element_by_id('com.das.face:id/etIp1')
# el.clear()
# el.send_keys('192')
# el = driver.find_element_by_id('com.das.face:id/etIp2')
# el.clear()
# el.send_keys('192')
# el = driver.find_element_by_id('com.das.face:id/etIp3')
# el.clear()
# el.send_keys('192')
# el = driver.find_element_by_id('com.das.face:id/etIp4')
# el.clear()
# el.send_keys('192')
# # 远程端口号
# el = driver.find_element_by_xpath('//*[@text="远程端口号"]/../*[2]')
# el.clear()
# el.send_keys('250')
# # 设备模式下拉框
# el = driver.find_element_by_id('android:id/text1')
# el.click()
# time.sleep(1)
# # el = driver.find_element_by_xpath("//*[contains(@text, \"仅身份识别\")]")
# # el = driver.find_element_by_xpath("//*[contains(@text, \"普通门禁\")]")
# # el = driver.find_element_by_xpath("//*[contains(@text, \"高级门禁\")]")
# el = driver.find_element_by_xpath("//*[contains(@text, \"门禁一体机\")]")
# el.click()
# # 修改设备密码
# el = driver.find_element_by_xpath('//*[contains(@text, "修改设备密码")]')
# el.click()
# time.sleep(1)
# el = driver.find_element_by_xpath("//*[contains(@text, \"原始密码\")]/../*[2]")
# el.clear()
# el.send_keys('654321')
# el = driver.find_element_by_xpath("//*[@text=\"新密码\"]/../*[2]")
# el.clear()
# el.send_keys('123456')
# el = driver.find_element_by_xpath("//*[contains(@text, \"确认新密码\")]/../*[2]")
# el.clear()
# el.send_keys('123456')
# el = driver.find_element_by_id("com.das.face:id/tvSave")
# el.click()
#
# # 进入高级设置
# el = driver.find_element_by_xpath("//*[@text=\"版本号\"]/following::*[1]")
# el.click()
# time.sleep(1)
#
# # 自动重启
# el = driver.find_element_by_xpath('//*[@text="自动重启"]/../*[2]')
# if not el.is_selected():
#     el.click()
#     time.sleep(1)
#     # 自动重启关闭变成打开，设置重庆时间为06：30
#     el = driver.find_element_by_accessibility_id("切换到文字输入模式来输入时间。")
#     el.click()
#     time.sleep(1)
#     el = driver.find_element_by_id("android:id/input_hour")
#     el.clear()
#     el.send_keys("06")
#     el = driver.find_element_by_id("android:id/input_minute")
#     el.clear()
#     el.send_keys("30")
#     el = driver.find_element_by_id("android:id/button1")
#     el.click()
#     time.sleep(1)
# else:
#     el.click()
# # 重启周期下拉框
# el = driver.find_element_by_id("android:id/text1")
# el.click()
# # 设置重庆周期
# # el = driver.find_element_by_xpath('//*[@text="一天"]')
# el = driver.find_element_by_xpath('//*[@text="一周"]')
# el.click()
# # 二维码识别
# el = driver.find_element_by_xpath('//*[@text="二维码识别"]/../*[2]')
# el.click()
# # 卡加人脸
# el = driver.find_element_by_xpath('//*[@text="卡加人脸"]/../*[2]')
# el.click()
# # 刷卡
# el = driver.find_element_by_xpath('//*[@text="刷卡"]/../*[2]')
# el.click()
# # 呼梯
# el = driver.find_element_by_xpath('//*[@text="呼梯"]/../*[2]')
# el.click()
# # 屏保
# el = driver.find_element_by_xpath('//*[@text="屏保"]/../*[2]')
# el.click()
# # 调试模式
# el = driver.find_element_by_xpath('//*[@text="调试模式"]/../*[2]')
# el.click()
#
# # 清理人员/初始化应用 弹出初始化应用选择框
# el = driver.find_element_by_xpath("//*[@text=\"清理人员/初始化应用\"]")
# el.click()
# time.sleep(1)
# # # 初始化应用选择框点击返回
# # el = driver.find_element_by_id("android:id/button3")
# # el.click()
# # 初始化应用选择框点击 只清空人员
# el = driver.find_element_by_id("android:id/button2")
# el.click()
# # 弹出请输入密码清空人员数据确认框
# # 输入密码
# el = driver.find_element_by_id("com.das.face:id/et_dialog_pwd")
# el.clear()
# el.send_keys("8888")
# # 密码输入后确认清除  密码输入错误提示：密码错误，需重新 输入
# el = driver.find_element_by_id("android:id/button1")
# el.click()
# # 点击取消 返回至高级设置界面
# el = driver.find_element_by_id("android:id/button2")
# el.click()
#
# # 初始化应用选择框点击 初始化应用
# el = driver.find_element_by_id("android:id/button1")
# el.click()
#
# # 清理记录 弹出输入密码确认框
# el = driver.find_element_by_xpath("//*[@text=\"清理记录\"]")
# # el.click()
# print(el.text)
# time.sleep(1)
# # 清理日志 弹出输入密码确认框
# el = driver.find_element_by_xpath("//*[@text=\"清理日志\"]")
# # el.click()
# print(el.text)
# time.sleep(1)
#
# # 批量导入 弹出批量导入进度提示框  文本提示：正在加载中…  find_element_by_id("android:id/alertTitle")
# el = driver.find_element_by_xpath("//*[@text=\"批量导入\"]")
# # el.click()
# print(el.text)
# time.sleep(1)
#
# # 人脸框设置(单选框：人脸框、隐藏)
# # 选中人脸框
# el = driver.find_element_by_id("com.das.face:id/rbShowFaceRect")
# el.click()
# # 隐藏人脸框
# el = driver.find_element_by_id("com.das.face:id/rbHideFaceRect")
# el.click()
#
# # 首页UI类型（单选框：不限制识别区域、限制识别区域）
# # 不限制识别区域
# el = driver.find_element_by_id("com.das.face:id/rbAllArea")
# el.click()
# # 限制识别区域
# el = driver.find_element_by_id("com.das.face:id/rbLimitArea")
# el.click()
# '''识别信息显示 没有显示出了，需要滑动'''
# screen_size = driver.get_window_size()
# # 向上滑动屏幕 x轴不变 y轴由大变小
# driver.swipe(screen_size['width'] * 0.9, screen_size['height'] * 0.9, screen_size['width'] * 0.9,
#              screen_size['height'] * 0.3)
# # 识别信息显示（复选框：姓名、工号、部门）
# el = driver.find_element_by_xpath('//*[@text="识别信息显示"]/../*[2]')
# el.click()
# # 姓名
# el = driver.find_element_by_id("com.das.face:id/cbName")
# el.click()
# # 工号
# el = driver.find_element_by_id("com.das.face:id/cbEmpno")
# el.click()
# # 部门
# el = driver.find_element_by_id("com.das.face:id/cbDepartment")
# el.click()
# print('********点击返回，重新进入查询*****')
# # 点击返回
# el = driver.find_element_by_xpath("//*[@text=\"高级设置\"]/../*[1]")
# el.click()
# 保存  高级设置
# el = driver.find_element_by_id("com.das.face:id/tvSaveSetting")
# el.click()
# time.sleep(1)
"""
# 识别设置
"""
# el = driver.find_element_by_id("com.das.face:id/btn_recognize")
# el.click()
# time.sleep(1)
# el = driver.find_element_by_xpath('//*[contains(@text, "人脸阈值")]/../*[2]')
# el.clear()
# el.send_keys('70')
# print('人脸阈值 =', el.text)
#
# # 识别距离
# el = driver.find_element_by_xpath("//*[@text=\"识别距离\"]/../*[2]")
# el.click()
# time.sleep(0.1)
# # # # 近（0.5米以内）
# # # el = driver.find_element_by_xpath("//*[@text=\"近（0.5米以内）\"]")
# # # el.click()
# # # # 中（1.5米以内）
# # # el = driver.find_element_by_xpath("//*[@text=\"中（1.5米以内）\"]")
# # # el.click()
# # # 远（2米以内）
# el = driver.find_element_by_xpath("//*[@text=\"远（2米以内）\"]")
# el.click()
#
# el = driver.find_element_by_xpath('//*[contains(@text, "AE模式")]/../*[2]')
# el.click()
# el = driver.find_element_by_xpath('//*[@text="活体"]/../*[2]')
# el.click()
# # 活体阈值(30-70) 输入数字不在范围内，toast弹窗提示：活体阈值范围为30-70
# el = driver.find_element_by_xpath("//*[@text=\"活体阈值(30-70)\"]/../*[2]")
# el.clear()
# el.send_keys(30)
#
# # 最小活体阈值 下拉框：0 、 10 、20 、30
# el = driver.find_element_by_xpath("//*[@text=\"最小活体阈值\"]/../*[2]")
# print(el.text)
# el.click()
# el = driver.find_element_by_xpath('//*[@text="20"]')
# el.click()
# # 白色补光灯 下拉框： 常关、常开、自动
# el = driver.find_element_by_xpath("//*[@text=\"白色补光灯\"]/../*[2]")
# el.click()
# el = driver.find_element_by_xpath("//*[@text=\"常开\"]")
# el.click()
# # 补光灯开始时间
# el = driver.find_element_by_id("com.das.face:id/tv_other_set_start_time")
# print(el.text)
# # 补光灯结束时间
# el = driver.find_element_by_id("com.das.face:id/tv_other_set_end")
# print(el.text)
#
# el = driver.find_element_by_xpath('//*[@text="红外补光灯"]/../*[2]')
# el.click()
# print('红外补光灯 is_selected =', el.is_selected())
# # 识别间隔(ms)文本框不让输入
# # el = driver.find_element_by_xpath('//*[contains(@text, "识别间隔(ms)")]/../*[2]')
# # el.clear()
# # el.send_keys('2000')
# el = driver.find_element_by_xpath('//*[contains(@text, "刷脸|刷卡等待时间(s)")]/../*[2]')
# el.clear()
# el.send_keys('9')
# # 点击保存
# time.sleep(1)
# el = driver.find_element_by_id("com.das.face:id/tvSave")
# el.click()
# print('********点击保存，重新进入查询*****')
#

"""
输出设置
"""
# el = driver.find_element_by_id("com.das.face:id/btn_io")
# el.click()
# # 维根输出类型 下拉框：设备不支持、韦根26、韦根34
# el = driver.find_element_by_xpath('//*[@text="维根输出类型"]/../*[2]')
# el.click()
# el = driver.find_element_by_xpath('//*[@text="韦根34"]')
# el.click()
# # 输出卡号 / 人脸ID 下拉框：卡号、人脸ID
# el = driver.find_element_by_xpath('//*[@text="输出卡号/人脸ID"]/../*[2]')
# el.click()
# el = driver.find_element_by_xpath('//*[@text="卡号"]')
# el.click()
#
# # 维根输出顺序 下拉框：正序、反序
# el = driver.find_element_by_xpath('//*[@text="维根输出顺序"]/../*[2]')
# el.click()
# el = driver.find_element_by_xpath('//*[@text="反序"]')
# el.click()
#
# # 继电器设置 脉冲时间（ms）
# el = driver.find_element_by_id("com.das.face:id/et_relay_time")
# el.clear()
# el.send_keys(500)
#
# # 继电器(识别成功)
# el = driver.find_element_by_xpath('//*[@text="继电器(识别成功)"]/../*[2]')
# el.click()
# # 继电器(识别失败)
# el = driver.find_element_by_xpath('//*[@text="继电器(识别失败)"]/../*[2]')
# el.click()
#
# # 超时报警时间（ms）
# el = driver.find_element_by_id("com.das.face:id/et_timeout_alarm_time")
# el.clear()
# el.send_keys(500)
#
# # 门磁检测 switch开关
# el = driver.find_element_by_xpath('//*[@text="门磁检测"]/../*[2]')
# el.click()
# # 保存输出设置
# el3 = driver.find_element_by_id("com.das.face:id/include_time_picker_save")
# el3.click()
#
# # 语音提示
# el1 = driver.find_element_by_id("com.das.face:id/btVoiceSetting")
# el1.click()
# el = driver.find_element_by_xpath("//*[@text=\"识别成功\"]/../*[2]")
# el.clear()
# el.send_keys('识别成功')
# # el = driver.find_elements_by_xpath("//*[@text=\"工作时间\"]/../*[2]")
# # print(el.text)
# el = driver.find_element_by_xpath("//*[@text=\"上班前\"]/../*[2]")
# el.clear()
# el.send_keys('识别成功')
# el = driver.find_element_by_xpath("//*[@text=\"下班后\"]/../*[2]")
# el.clear()
# el.send_keys('识别成功')
# el = driver.find_element_by_xpath("//*[@text=\"识别失败\"]/../*[2]")
# el.clear()
# el.send_keys('未授权')
#
# # 保存语音提示
# el3 = driver.find_element_by_id("com.das.face:id/tvSave")
# el3.click()
