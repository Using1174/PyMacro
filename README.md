# PyMacro

Python版模拟按键精灵库，无需ROOT

功能包括：**模拟按键、模拟屏幕触摸、模拟文字输入、获取指定位置屏幕颜色、指定区域查找相似颜色等**

## 原理
手机连接电脑，并开启USB调试模式，使用ADB工具获取屏幕截图，分析并模拟各种操作。(需要自己写代码)

## 运行环境要求

1. Android4.4+
2. Python 3
3. [ADB](https://developer.android.com/studio/releases/platform-tools.html)驱动([下载](https://adb.clockworkmod.com/))
4. Python 依赖库

    pip install -r requirements.txt


## 示例
新建python文件，导入 auto_bot

    import auto_bot


    # 模拟按键
    auto_bot.key(KeyCode.KEYCODE_HOME.value)

    # 模拟文字输入
    auto_bot.text("&*test#@? 'c")

    # 模拟点击
    auto_bot.tap(887, 1664)

    # 模拟滑动
    auto_bot.swipe_time(887, 1664, 200, 1664, 200)

其他操作参考：[example.py](https://github.com/Using1174/PyMacro/blob/master/example.py)