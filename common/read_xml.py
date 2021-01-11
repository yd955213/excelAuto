# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   read_xml.py
@Time   :   2020-12-31 10:11
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :  读取xml格式配置问题
"""
# from enum import Enum
import os

from global_variables import get_abspath

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# class SetInfo(Enum):
#     device_pwd = 'device_pwd'
#     dailyRestartTime = 'dailyRestartTime'
#     openDoorPassword = 'openDoorPassword'
#     deviceName = 'deviceName'
#     heartBeatInterval = 'heartBeatInterval'
#     qrCodeSwitch = 'qrCodeSwitch'
#     mainUIType = 'mainUIType'
#     IsAuth = 'IsAuth'
#     deviceMac = 'deviceMac'
#     servicePort = 'servicePort'
#     liveness_failed_count = 'liveness_failed_count'
#     isNativeChangeParam = 'isNativeChangeParam'
#     enableScreenSaver = 'enableScreenSaver'
#     isSupportCard = 'isSupportCard'
#     isDBNorma = 'isDBNorma'
#     isAutoRestart = 'isAutoRestart'
#     IsNotConfig = 'IsNotConfig'
#     deviceTypeInt = 'deviceTypeInt'
#     weiGenOut = 'weiGenOut'
#     weiGenType = 'weiGenType'
#     serviceIP = 'serviceIP'
#     isUploadPassImg = 'isUploadPassImg'
#     relayTime = 'relayTime'
#     autoRebootTimeSpace = 'autoRebootTimeSpace'
#     devicePort = 'devicePort'
#     weiGenIn = 'weiGenIn'


class ReadSetInfo:
    def __init__(self, file_name='SetInfo.xml'):
        self.tree_root = ET.ElementTree(file=get_abspath('config/{}'.format(file_name))).getroot()
        self.set_info = {}

    def get_setInfo(self):
        """
        获取xml文件的2及子节点的值
        :return: 返回字典格式数据
        """
        set_info = {}
        if self.tree_root is not None:
            for tree in self.tree_root:
                if tree.tag == 'string':
                    set_info[tree.get('name')] = tree.text
                else:
                    set_info[tree.get('name')] = tree.get('value')
                # print(tree.get('name') + " = " + set_info[tree.get('name')])
        return set_info

    def set_info_dict(self, key='None', value='None'):
        if key == 'isAutoRestart':
            value = 2 if value =='关闭' else 1
        elif key == 'autoRebootTimeSpace':
            value = 1 if value =='一周' else 0
        elif key == 'vdailyRestartTime':
            pass
        elif key == 'qrCodeSwitch':
            value = 2 if value =='关闭' else 1
        elif key == 'mainUIType':
            value = 1 if value =='人脸框' else 2
        elif key == 'isSupportCard':
            value = 2 if value =='关闭' else 1
        elif key == 'enableScreenSaver':
            value = 2 if value =='关闭' else 1
        elif key == 'face_debug_info_flag':
            value = 2 if value =='关闭' else 1
        elif key == '':
            value = 2 if value =='关闭' else 1
        elif key == '':
            value = 2 if value =='关闭' else 1
        elif key == '':
            value = 2 if value =='关闭' else 1
        elif key == '':
            value = 2 if value =='关闭' else 1
        elif key == '':
            value = 2 if value =='关闭' else 1

        self.set_info[key] = value


if __name__ == '__main__':
    os.system(r'adb root')
    os.system(r'adb pull data/data/com.das.face/shared_prefs/SetInfo.xml {}'.format(get_abspath('config/')))
    os.system(r'adb pull data/data/com.das.face/shared_prefs/settingParam.xml {}'.format(get_abspath('config/')))
    config_dict = ReadSetInfo().get_setInfo()
    dic = ReadSetInfo('settingParam.xml').get_setInfo()
    for key in dic.keys():
        config_dict[key] = dic[key]
    print(config_dict.get('relayTime'))
    print(config_dict.get('errorRelay'))
    print(config_dict.get('DoorContactFlag'))
    # print(SetInfo.devicePort.name)
    # print(rs.get(SetInfo.devicePort.value))
