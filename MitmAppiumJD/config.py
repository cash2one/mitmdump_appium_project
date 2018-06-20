import os

# 平台
PLATFORM = 'Android'

# 设备名称 通过 adb devices -l 获取
DEVICE_NAME = '127.0.0.1:21503'

# APP路径
APP = os.path.abspath('.') + 'jd/.apk'

# Appium地址
DRIVER_SERVER = 'http://localhost:4723/wd/hub'
# 等待元素加载时间
TIMEOUT = 2000

# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 700


# 滑动间隔
SCROLL_SLEEP_TIME = 2

KEYWORD = 'r1'