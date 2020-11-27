# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   get_photo_base64.py
@Time   :   2020-11-27 17:21
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import base64
import os

from global_variables import get_abspath


def to_base64(image):
    with open(image, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
    return image_base64


def listdir(path):  #传入存储的list
    list_name = []
    for file in os.listdir(get_abspath(path)):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
             listdir(file_path, list_name)
        else:
            list_name.append(get_abspath(file_path))
    return list_name


photo_dic = {}

file_list = listdir('data/photoTest/')

for file in file_list:
    name = os.path.basename(file)
    photo_base64 = to_base64(file)
    photo_dic[name] = photo_base64
    if name.__contains__('杨党'):
        # base64不完整
        photo_dic['base64low.jpg'] = photo_base64[:100] + photo_base64[105:]
        # 含头文件
        photo_dic['base64header.jpg'] = 'data:image/jpg;base64,' + photo_base64

