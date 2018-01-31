# -*- coding: utf-8 -*-
import auto_bot
import colorsys
from common import colormatch
from common import KeyCode


def rgb_test():
    col1 = "FF0000"
    col2 = "ff000f"
    rgb1 = colormatch.hex_to_rgb(col1)
    rgb2 = colormatch.hex_to_rgb(col2)
    hsv1 = colorsys.rgb_to_hsv(rgb1[0], rgb1[1], rgb1[2])
    hsv2 = colorsys.rgb_to_hsv(rgb2[0], rgb2[1], rgb2[2])
    dis_hsv = colormatch.color_distance_hsv(hsv1, hsv2)
    rgb255_1 = colormatch.hex2rgb(col1)
    rgb255_2 = colormatch.hex2rgb(col2)
    dis_rgb = colormatch.color_distance_rgb(rgb255_1, rgb255_2)
    print(rgb1, rgb2, hsv1, hsv2)
    print(dis_hsv, dis_rgb)


def main():
    rgb_test()


if __name__ == '__main__':
    main()
