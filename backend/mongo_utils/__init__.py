# -*- coding: utf-8 -*-
"""
@File       : __init__.py.py
@Author     : Yuka
@Time       : 2021/4/2 15:14
@Version    : 1.0.0
@Description: 
"""
# 连接池
import atexit
from logger_utils import logger

CLIENT_POOL = {}


@atexit.register
def close_all_client():
    logger.info("检测到程序正在退出，将关闭所有mongo连接...")
    for client in CLIENT_POOL.values():
        client.close()
    logger.info("mongo连接关闭完成。")
