# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   type_judgment.py
@Time   :   2020-11-17 9:46
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   一些常见的数据类型判断
"""
import traceback


def is_dict(value):
    """
    判断是否为字典或者json
    """
    if type(value).__name__ == 'dict':
        return True
    else:
        return False


def is_string(value):
    """
    判断是否为字符串
    """
    if type(value).__name__ == 'str':
        return True
    else:
        return False


def is_int(value):
    """
    判断是否为字典
    """
    if type(value).__name__ == 'int':
        return True
    else:
        return False


def is_float(value):
    """
    判断是否为字典
    """
    if type(value).__name__ == 'float':
        return True
    else:
        return False


def is_list(value):
    """
    判断是否为字典
    """
    if type(value).__name__ == 'list':
        return True
    else:
        return False


def is_Null(value):
    """
    判断数据类型是否为空
    """
    try:
        if value is None or len(value) == 0:
            return True
        else:
            return False
    except:
        print(traceback.format_exc(), value)
        return True


# 这里有个bug 如果li=['', environment.properties],使用is_None_in_list(*li)时 传入的为元祖（‘’, environment.properties）,然而此时None类型为<class 'str'>，导致判断错误
def is_None_in_list(li):
    sum_1 = 0
    for i in li:
        i = str(i)
        if not is_Null(i):
            sum_1 += 1
    if sum_1 > 0:
        return False
    else:
        return True


if __name__ == '__main__':
    args = ('auth', '', '')
    print(args)
    # print(is_None_in_list(args))
    # # args = ''
    # # print(is_Null(args))
    # # args = environment.properties
    # # print(is_Null(args))
    # # args = 'environment.properties'
    # # print(is_Null(args))
    # # args = '1'
    # # print(is_Null(args))

    print(is_Null(''))
