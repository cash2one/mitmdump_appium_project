import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from time import sleep
from processor import Processor
from config import *
import time


class Moments():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        # 处理器
        self.processor = Processor()
    
    def login(self):
        """
        登录微信
        :return:
        """
        # 登录按钮
        login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d1w')))
        login.click()
        # 手机输入
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/bwm')))
        email.click()

        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/hx')))
        phone.set_text(USERNAME)

        # 密码
        password = self.driver.find_element_by_xpath(
            "//android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.EditText[1]")

        password.set_text(PASSWORD)
        # 提交
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/bwn')))
        submit.click()
    
    def enter(self):
        """
        进入朋友圈
        :return:
        """
        # 选项卡
        # time.sleep(30)
        # tab = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH,'//*[@resource-id="com.tencent.mm:id/c9d"][3]'))
        # )
        # 可以用xpath设置元素等待
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView[1]'))
        )
        # tab = self.driver.find_element_by_android_uiautomator("text(\"发现\")")
        tab.click()
        # 朋友圈
        moments = self.driver.find_element_by_android_uiautomator("text(\"朋友圈\")")
        moments.click()
    
    def crawl(self):
        """
        爬取
        :return:
        """
        while True:
            # time.sleep(10)
            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@resource-id="com.tencent.mm:id/ddn"]//android.widget.FrameLayout')))
            # 上滑
            # 这里有一个问题，如果使用虚拟机会报错，未知下拉错误
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            # 遍历每条状态
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('com.tencent.mm:id/apv').get_attribute('text')
                    # 正文
                    content = item.find_element_by_id('com.tencent.mm:id/deq').get_attribute('text')
                    # 日期，这里一直获取不到
                    date = item.find_element_by_id('com.tencent.mm:id/dag').get_attribute('text')
                    # 处理日期
                    date = self.processor.date(date)
                    print(nickname, content, date)
                    data = {
                        'nickname': nickname,
                        'content': content,
                        'date': date,
                    }
                    # 插入MongoDB， update设置去重
                    self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
                    sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                # except WebDriverException:
                    pass
    
    def main(self):
        """
        入口
        :return:
        """
        # 登录
        self.login()
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()


if __name__ == '__main__':
    moments = Moments()
    moments.main()
