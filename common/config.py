# -*- coding: utf-8 -*-
"""
调取配置文件和屏幕分辨率的代码
"""
import os
import sys
import json
import re

inited = False
_global_dict = {}


def _init():
    """
    调用配置文件
    """
    global _global_dict
    # screen_size = get_screen_size()
    config_file = "{path}/config/config.json".format(
        path=sys.path[0]
    )
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("Load config file from {}".format(config_file))
            _global_dict = json.load(f)
            global inited
            inited = True
            return _global_dict
    else:
        print("Load default config fail")
        return _global_dict


def get_dic():
    global inited
    if inited:
        return _global_dict
    else:
        return _init()


def get_screen_size():
    """
    获取手机屏幕大小
    """
    size_str = os.popen('adb shell wm size').read()
    if not size_str:
        print('请安装 ADB 及驱动并配置环境变量')
        sys.exit()
    m = re.search(r'(\d+)x(\d+)', size_str)
    if m:
        return "{height}x{width}".format(height=m.group(2), width=m.group(1))
    return "1920x1080"
