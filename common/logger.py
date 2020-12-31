# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   logger.py
@Time   :   2020-11-10 14:05
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import logging
import yaml

from global_variables import get_abspath


class Logger:
    def __init__(self, file_path):
        
        self.my_logger = None
        with open(file=get_abspath(file_path), mode='r', encoding="utf-8") as file:
            logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
            # print(logging_yaml)
            # 配置logging日志：主要从文件中读取handler的配置、formatter（格式化日志样式）、logger记录器的配置
            logging.basicConfig(**logging_yaml)
            
        # 获取根记录器：配置信息从yaml文件中获取，只会输出到日志文件
        self.my_logger = logging.getLogger()
        # 创建输出到控制台的输出流
        console = logging.StreamHandler()
        # 设置日志等级
        console.setLevel(logging_yaml['level'])
        # 设置日志格式
        console.setFormatter(logging.Formatter(logging_yaml['format']))
        # 添加到logger输出
        self.my_logger.addHandler(console)


# 日志
logger = Logger('config/logger.yaml').my_logger


if __name__ == "__main__":
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning('WARNING')
    logger.error('ERROR')
    try:
        int('A')
    except Exception as e:
        logger.exception(e)
