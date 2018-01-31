# -*- coding: utf-8 -*-
import auto_bot
import time
import random
from common.KeyCode import KeyCode


def touch_example():
    # 轻触
    auto_bot.tap(887, 1664)
    # 滑动
    auto_bot.swipe_time(887, 1664, 200, 1664, 200)
    auto_bot.swipe_time(543, 1536, 543, 1536, 710)


def key_press_example():
    # 按键模拟
    auto_bot.key(KeyCode.KEYCODE_HOME.value)


def text_example():
    # 文字输入
    auto_bot.text("&*test#@? 'c")


def main():
    ltc = time.localtime()

    auto_bot.init()
    while True:
        start = time.time()

        # 调用后台截取屏幕,更新缓存图片
        auto_bot.update_img()

        mid = time.time()
        print("updateimg cost: {}ms".format(mid - start))

        # 屏幕颜色获取
        x, y = 100, 200
        pixel = auto_bot.get_pixels(x, y)
        print('screen ({},{}) color_rgba:{}'.format(x, y, pixel))

        # 全屏查找相似颜色
        x, y = auto_bot.find_color("#FFFFFF", 0.9)
        print(x, y)

        # 指定区域查找相似颜色
        x, y = auto_bot.find_color_area(50, 100, 100, 200, "#FFFFFF", 0.9)
        print(x, y)

        # 按键示例
        key_press_example()

        # 屏幕点击示例
        touch_example()

        # 文字输入需激活输入框
        # text_example()

        end = time.time()
        print("cost time: {}ms".format(end - start))


# 暂停一会儿
# time.sleep(random.uniform(3, 5))


if __name__ == '__main__':
    main()
