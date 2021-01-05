#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
@File   : my_assert.py
@Time   : 2020/11/25 10:15
@Author : yd
@Version: 1.0
@ToDo    : 
"""
import json
import jsonpath
from common.logger import logger
from common.type_judgment import is_dict


def __get_result(response):
    if response is None:
        assert False, '错误，无返回'
    else:
        result_text = response.text
        # result_text = response
        try:
            result = json.loads(result_text)
        except Exception as e:
            result = result_text
    return result, result_text


def assert_code(response, expect):
    result, result_text = __get_result(response)
    # 断言Code
    if is_dict(result):
        try:
            code = result.get('Code')
        except:
            code = result_text

        if code is None:
            code = result_text

        assert code == expect, 'Code断言失败：预期Code:{}，实际Code:{}'.format(expect, code)

        return "断言Code成功,预期Code:{}，实际Code:{}".format(expect, code)
    else:
        assert False, 'Code断言失败：预期Code:{}，实际响应内容为:{}'.format(expect, result_text)


def assert_msg(response, expect):
    result, result_text = __get_result(response)
    # 断言Msg
    if is_dict(result):
        try:
            msg = result.get('Msg')
        except:
            msg = result_text
        if msg is None:
            msg = result_text
        assert msg == expect, 'Msg断言失败：预期Msg:{}，实际Msg:{}'.format(expect, msg)
        return "断言Msg成功,预期Msg:{}，实际Msg:{}".format(expect, msg)
    else:
        assert False, 'Msg断言失败：预期Msg:{}，实际响应内容为:{}'.format(expect, result_text)


def assert_jsonpath(response, jsonpath_str, expect):
    result, result_text = __get_result(response)
    # 断言data
    if is_dict(result):
        value = jsonpath.jsonpath(result, jsonpath_str)
        # logger.info(value)
        if not value:
            assert False, '断言jsonpath失败,无jsonpath路径: {}，实际返回{}'.format(jsonpath_str, result_text)
        else:
            assert str(value[0]) == str(expect), "断言Data失败,预期:{}，实际:{}".format(expect, value[0])
            return "断言jsonpath成功,预期:{}，实际:{}".format(expect, value[0])

    else:
        assert False, 'jsonpath断言失败：预期Data:{}，实际响应内容为:{}'.format(expect, result_text)


# if __name__ == '__main__':
    # st = r'{"Code":"0","Data":{"AppParams":{"AppPassword":"999999","AppVersion":"361.1.2.0"},"BasicParams":{"DailyRestartTime":"02:00:00","DeviceIP":"172.168.120.69","DeviceName":"测试设备","DevicePort":8090,"DeviceType":1,"DeviceUniqueCode":"FC2C0A","EnableScreenSaver":0,"FileServerUrl":"http://172.168.120.190:19605","HeartBeatInterval":300000,"IsAutoRestart":0,"IsKqUse":0,"IsSupportCard":0,"IsUploadPassImg":1,"MainUIType":1,"OpenDoorPassword":"123456","QrCodeSwitch":0,"RelayTime":1000,"ServerIP":"192.168.11.100","ServerPort":8000,"SystemID":"00034900","TriggerActionInterval":300000,"WiegandIn":0,"WiegandOut":1,"WiegandType":34},"FeatureParams":{"FeatureSDKValue":"SDK-2.2.8","FeatureType":3,"FeatureVersion":"FW-1.8.6-03.04.00"},"HardWareParams":{"DebugModeSwitch":0,"SuppleLightMode":1,"SuppleLightOpenTime":"18:00-07:00"},"RecognitionParams":{"IsAlive":2,"LivingThreshold":60.0,"MaxFacePixel":1000,"MinFacePixel":150,"SimilityThreshold":"75"},"VoiceTipParams":{"AfterJobTip":"@上班一天辛苦了","AttendanceTime":"09:00-18:00","BeforeJobTip":"@打卡成功","RecognizeErrorTip":"未登记","RecognizeSuccessTip":"@识别成功"}},"Msg":"OK","TimeStamp":"2020-11-30 16:22:06"}'
    # st = json.loads(st)
    # print(st)
    # print(jsonpath.jsonpath(st, '$.Data.FeatureParams.FeatureType'))
