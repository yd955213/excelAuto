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


def __get_result(response):
    if response is None:
        assert False, '错误，无返回'
    else:
        try:
            result = json.loads(response.text)
        except Exception as e:
            result = response.text
    return result


def assert_code(response, expect):
    result = __get_result(response)
    # 断言Code
    try:
        assert result.get('Code') == expect, 'Code断言失败：预期Code:{}，实际Code:{}'.format(expect, result.get('Code') if result.get(
            'Code') is not None else result)
        return True
    except Exception as e:
        raise e
        # return False
        return e


def assert_msg(response, expect):
    result = __get_result(response)
    try:
        # 断言Msg
        assert result.get('Msg') == expect, 'Msg断言失败：预期Msg:{}，实际Msg:{}'.format(expect, result.get('Msg') if result.get(
            'Code') is not None else result)
        return True
    except Exception as e:
        raise e
        # return False
        return e


def assert_jsonpath(response, jsonpath_str, expect):
    result = __get_result(response)
    # 断言data
    try:
        value = jsonpath.jsonpath(result, jsonpath_str)
        if not value:
            assert False, "断言data失败,预期:{}，无jsonpath路径:{}".format(result, jsonpath_str)
            return False
        assert value == expect, "断言data失败,预期:{}，实际:{}".format(value, expect)
        return True
    except Exception as e:
        raise e
        # return False
        return e
