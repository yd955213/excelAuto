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

        assert code == expect, 'Code断言失败：预期Code:{}，实际Code:{}'. format(expect, code)
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
    else:
        assert False, 'Msg断言失败：预期Msg:{}，实际响应内容为:{}'.format(expect, result_text)


def assert_jsonpath(response, jsonpath_str, expect):
    result, result_text = __get_result(response)
    # 断言data
    if is_dict(result):
        try:
            value = jsonpath.jsonpath(result, jsonpath_str)
            if not value:
                assert False, "断言Data失败,实际:{}，无jsonpath路径:{}".format(result_text, jsonpath_str)
                return False

            assert value == expect, "断言Data失败,预期:{}，实际:{}".format(value, expect)
        except:
            assert False, "断言Data失败,实际:{}，无jsonpath路径:{}".format(result_text, jsonpath_str)


    else:
        assert False, 'Data断言失败：预期Data:{}，实际响应内容为:{}'.format(expect, result_text)


# if __name__ == '__main__':
    # st = '{"Code": "0","Data": {"Detail": [],"Page": 1,"PageCount": 0,"QueryCount": -30,"TotalCount": 0},"Msg": "OK","TimeStamp": "2020-11-27 20:13:42"}'
    # print(assert_code(st, '0'))

