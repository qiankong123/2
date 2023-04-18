# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# @Time    : 2023/3/1 18:50
# @Author  : LXJ
# @FileName: 封装.py
# @Software: PyCharm
import os

log_path =os.path.join(__file__,"../log.txt")

print(log_path)
import logging
class LogUtils:
    def __init__(self,loggername=None):
        self.log_path_name = log_path
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG) #设置最低级别
        # 创建日志格式对象
        formatter = logging.Formatter("%(asctime)s-  -%(levelname)s- %(lineno)d - %(message)s ")
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.INFO)
        self.sh.setFormatter(formatter)
        self.log.addHandler(self.sh)

        self.fh = logging.FileHandler("./log.text",encoding="utf-8")
        self.fh.setLevel(logging.WARNING)
        self.fh.setFormatter(formatter)
        self.log.addHandler(self.fh)
        # self.log.warning("测试")

        #为了保证日志不重复打印
        # self.sh.close()
        # self.fh.close()

    def get_log(self):
        return self.log
    
logger = LogUtils().get_log()

if __name__ == '__main__':
    logger.critical("测试")
    logger.info("test")
