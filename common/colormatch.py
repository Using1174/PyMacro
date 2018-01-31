# -*- coding: utf-8 -*-
import struct
import colorsys
import math


# 返回 tuple: (r,g,b,a)
def get_pixels(pixels, x, y):
    return pixels[x, y]


# 使用RGB色彩全屏找色, 接收字符 #FFFFFF, 返回查找的结果x,y
# 若x==-1 && y==-1, 表示找不到
def find_color(im, pixels, hex_val, same_rate):
    w, h = im.size
    return find_color_area(pixels, 0, 0, w, h, hex_val, False, same_rate)


# 使用HSV色彩全屏找色, 接收字符 #FFFFFF, 返回查找的结果x,y
# 若x==-1 && y==-1, 表示找不到
def find_color_hsv(im, pixels, hex_val, same_rate):
    w, h = im.size
    return find_color_area(pixels, 0, 0, w, h, hex_val, True, same_rate)


# 在指定范围内查找
# 若x==-1&&y==-1,表示找不到
# same_rate 颜色相似率(0-1)
def find_color_area(pixels, x1, y1, x2, y2, hex_val, use_hsv, same_rate):
    hex_str = hex_val[1:]
    # rgb (0-255)
    rgb = hex2rgb(hex_str)

    if use_hsv:
        for i in range(x1, x2):
            for j in range(y1, y2):
                pixel = pixels[i, j]
                if match_color_hsv(rgb, pixel, same_rate):
                    return (i, j)
    else:
        for i in range(x1, x2):
            for j in range(y1, y2):
                pixel = pixels[i, j]
                if match_color(rgb, pixel, same_rate):
                    return (i, j)

    return (-1, -1)


# same_rate为颜色的相似程度
def match_color_hsv(rgb1, rgb2, same_rate):
    # hsv h:0-1, s:0-1, v:0-1
    hsv1 = colorsys.rgb_to_hsv(rgb1[0] / 255, rgb1[1] / 255, rgb1[2] / 255)
    hsv2 = colorsys.rgb_to_hsv(rgb2[0] / 255, rgb2[1] / 255, rgb2[2] / 255)

    if color_distance_hsv(hsv1, hsv2) <= 1.0 - same_rate:
        return True
    else:
        return False


# 多点比色
# match_list [(x,y,(r,g,b))]
def multi_color_match(pixels, match_list, same_rate):
    for tp in match_list:
        pixel = pixels[tp[0], tp[1]]
        rgb = tp[2]
        if not (match_color(rgb, pixel) <= 1.0 - same_rate):
            return False
    # 所有点都满足条件
    return True


def match_color(rgb1, rgb2, same_rate):
    if color_distance_rgb(rgb1, rgb2) <= 1.0 - same_rate:
        return True
    else:
        return False


# RGB色彩空间，计算差值在0.1 以内时，基本可以判定为相似颜色
# 值越小，说明颜色越相近(0.0-1.0)
def color_distance_rgb(rgb1, rgb2):
    tp = tuple(((a - b) / 255) ** 2 for a, b in zip(rgb1, rgb2))
    return math.sqrt(sum(tp))


# HSV色彩空间，计算差值在0.1 以内时，基本可以判定为相似颜色
# 值越小，说明颜色越相近(0.0-1.0)
def color_distance_hsv(hsv1, hsv2):
    # 灰度值是个循环，需取最小值判定
    h_dis = min((hsv1[0] - hsv2[0]) ** 2, (hsv1[0] + hsv2[0] - 1.0) ** 2)
    s_dis = (hsv1[1] - hsv2[1]) ** 2
    v_dis = (hsv1[2] - hsv2[2]) ** 2

    return math.sqrt(h_dis + v_dis + s_dis)


# RGB元素范围(0-255)
def hex2rgb(hex_str):
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))
    return tuple([val for val in int_tuple])


# RGB元素范围(0-1)
def hex_to_rgb(hex_str):
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))
    return tuple([val / 255 for val in int_tuple])


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
