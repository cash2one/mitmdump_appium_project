from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
server = 'http://localhost:4723/wd/hub'

desired_caps = {
    'platformName': 'Android',
    'deviceName': '127.0.0.1:21503',
    'appPackage': 'com.tencent.mm',
    'appActivity': '.ui.LauncherUI'
}

# desired_caps = {
#     'platformName': 'Android',
#     'deviceName': 'MI_NOTE_Pro',
#     'app': './weixin.apk'
# }

driver = webdriver.Remote(server, desired_caps)
wait = WebDriverWait(driver, 30)
login = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d1w')))
login.click()
# 手机输入
email = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/bwm')))
email.click()

phone = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/hx')))
phone.set_text('24554@qq.com')

# 密码
password = driver.find_element_by_xpath(
    "//android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.EditText[1]")

password.set_text('0476aa')