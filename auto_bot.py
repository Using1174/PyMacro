# -*- coding: utf-8 -*-

"""
通过 adb shell 操作，截取手机屏幕，并根据界面模拟点击。
可以无需Root权限，实现按键精灵/触摸精灵/触动精灵等的脚本效果。
"""
from __future__ import print_function, division
import os
import time
from PIL import Image
import traceback

try:
    from common import debug, config, screenshot, colormatch
except Exception as ex:
    traceback.print_exc()
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(-1)

VERSION = "1.0.0"

# DEBUG 开关，需要调试的时候请改为 True，不需要调试的时候为 False
DEBUG_SWITCH = False

# 读取配置文件
config = config.get_dic()

screen_height = config['screen_height']
screen_width = config['screen_width']
img_path = config['img_path']
# 是否使用缓存图片，False 每次都更新截取新的图
keep_capture = False
# 缓存的图片
im = None
# 缓存的图片像素
im_pixels = None


def keep_cap():
    global keep_capture
    keep_capture = True


def release_cap():
    global keep_capture
    keep_capture = False


def _pull_screenshot():
    if not keep_capture:
        screenshot.check_screenshot(img_path)


def update_img():
    _pull_screenshot()
    global im, im_pixels
    im = Image.open(img_path)
    im_pixels = im.load()
    if DEBUG_SWITCH:
        ts = int(time.time())
        debug.save_debug_screenshot(ts, im, screen_width, screen_height)
        debug.backup_screenshot(ts)


# 返回 tuple: (r,g,b,a)
def get_pixels(x, y):
    return colormatch.get_pixels(im_pixels, x, y)


def find_color(hex_val, same_rate):
    return colormatch.find_color(im, im_pixels, hex_val, same_rate)


def find_color_hsv(hex_val, same_rate):
    return colormatch.find_color_hsv(im, im_pixels, hex_val, same_rate)


def find_color_area(x1, y1, x2, y2, hex_val, same_rate):
    return colormatch.find_color_area(im_pixels, x1, y1, x2, y2, hex_val, False, same_rate)


# 多点比色
# match_list [(x,y,(r,g,b))]
def multi_color_match(match_list, same_rate):
    return colormatch.multi_color_match(im_pixels, match_list, same_rate)


# 模拟滑动，默认持续时间
def swipe(x1, y1, x2, y2):
    swipe_time(x1, y1, x2, y2, 1)


# 模拟滑动，并指定持续时间
def swipe_time(x1, y1, x2, y2, press_time):
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        duration=press_time
    )
    adb_shell(cmd)


# 模拟轻触
def tap(x, y):
    cmd = 'adb shell input tap {} {}'.format(x, y)
    adb_shell(cmd)


# 按键事件
# Key Code ref: https://developer.android.com/reference/android/view/KeyEvent.html
def key(key_code):
    cmd = 'adb shell input keyevent {}'.format(key_code)
    adb_shell(cmd)


# 模拟输入文本, 不支持双引号"和unicode字符
# 若机器安装了ADB输入法：https://github.com/senzhk/ADBKeyBoard，则可使用unicode字符
def text(text):
    cmd = 'adb shell input text "{}"'.format(text)
    adb_shell(cmd)


# 模拟原理是对驱动发送消息，就是linux里面的input子系统。
# 命令格式： sendevent /dev/input/eventX [type] [key] [value]
# 其中/dev/input/eventX 对应的是设备，可以用getevent查看可用设备。
# ref: http://www.cnblogs.com/AsionTang/p/6211895.html
def send_event(idx, type, key, value):
    cmd = 'adb shell sendevent /dev/input/event{idx} {type} {key} {value}'.format(
        idx=idx,
        type=type,
        key=key,
        value=value
    )
    adb_shell(cmd)


def adb_shell(cmd):
    print(cmd)
    os.system(cmd)


def init():
    print('Bot Version：{}'.format(VERSION))
    debug.dump_device_info()
    screenshot.check_screenshot(img_path)
    global im, im_pixels
    im = Image.open(img_path)
    im_pixels = im.load()
