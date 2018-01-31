# -*- coding: utf-8 -*-
"""
手机屏幕截图的代码
"""
import subprocess
import os
import sys
from PIL import Image

# SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
SCREENSHOT_WAY = 3


def pull_screenshot(img_path):
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            'adb shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        lenb = len(binary_screenshot)
        if lenb > 0:
            f = open(img_path, 'wb')
            f.write(binary_screenshot)
            f.close()
        else:
            print("error! no screenshot data!")
    elif SCREENSHOT_WAY == 0:
        screenshot_name = "screenshot.png"
        os.system('adb shell screencap -p /sdcard/{}'.format(screenshot_name))
        os.system('adb pull /sdcard/{} {}'.format(screenshot_name, img_path))


def check_screenshot(img_path):
    """
    检查获取截图的方式
    """
    global SCREENSHOT_WAY
    # 每次提交不删除旧的文件
    # if os.path.isfile(img_path):
    #     try:
    #         os.remove(img_path)
    #     except Exception:
    #         pass
    if SCREENSHOT_WAY < 0:
        print('暂不支持当前设备截屏')
        return
        # sys.exit()
    # upload image
    pull_screenshot(img_path)
    try:
        # Image.open(img_path).load()
        Image.open(img_path)
        print('采用方式 {} 获取截图：{}'.format(SCREENSHOT_WAY, img_path))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot(img_path)
