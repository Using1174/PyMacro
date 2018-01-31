# -*- coding: utf-8 -*-
"""
这儿是debug的代码，当DEBUG_SWITCH开关开启的时候，会将各种信息存在本地，方便检查故障
"""
import os
import sys
import shutil
from PIL import ImageDraw
from common import config

config = config.get_dic()
screenshot_backup_dir = 'screenshot_backups/'
img_path = config['img_path']


def make_debug_dir(screenshot_backup_dir):
    """
    创建备份文件夹
    """
    if not os.path.isdir(screenshot_backup_dir):
        os.mkdir(screenshot_backup_dir)


def backup_screenshot(ts):
    """
    为了方便失败的时候 debug
    """
    make_debug_dir(screenshot_backup_dir)
    shutil.copy(img_path, '{}{}.png'.format(screenshot_backup_dir, ts))


def save_debug_screenshot(ts, im, screen_width, screen_height):
    """
    对 debug 图片加上详细的注释
    """
    make_debug_dir(screenshot_backup_dir)
    draw = ImageDraw.Draw(im)
    # draw something in picture
    del draw
    im.save('{}{}_d.png'.format(screenshot_backup_dir, ts))


def dump_device_info():
    """
    显示设备信息
    """
    size_str = os.popen('adb shell wm size').read()
    device_str = os.popen('adb shell getprop ro.product.device').read()
    phone_os_str = os.popen('adb shell getprop ro.build.version.release').read()
    density_str = os.popen('adb shell wm density').read()
    print("""**********
Screen: {size}
Density: {dpi}
Device: {device}
Phone OS: {phone_os}
Host OS: {host_os}
Python: {python}
**********""".format(
        size=size_str.strip(),
        dpi=density_str.strip(),
        device=device_str.strip(),
        phone_os=phone_os_str.strip(),
        host_os=sys.platform,
        python=sys.version
    ))
