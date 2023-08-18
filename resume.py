# -*- coding: utf-8 -*-
# Created by Inyhow | python 3.10
import sys

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time

class AutoRefreshResume:
    def __init__(self):
        # 需要自动刷新简历的网站
        self.zp_url = 'https://i.zhaopin.com/resume'
        self.lp_url = 'https://c.liepin.com/'

    def zhaopin(self):

        # 实例化Options,为启动GUI界面做准备

        options = Options()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('–disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        # options.add_argument("--auto-open-devtools-for-tabs")
        # 设置自定义的 User-Agent 标头
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200"
        options.add_argument(f"user-agent={user_agent}")

        # 实例化对象
        driver = Edge(options=options)
        driver.maximize_window()
        # 使用webdriver请求url
        driver.get(self.zp_url)
        # 定位元素，手机扫码，然后进行提交操作
        driver.find_element(By.CLASS_NAME, 'zppp-panel-normal-bar__img').click()
        time.sleep(20)
        t = driver.find_element(By.XPATH, "//p[contains(@class,'profile-pre-name')]").text
        if "陈先生" in t:
            print("智联招聘登录成功！\n")
        time.sleep(5)
        # 点击刷新

        # 等待刷新简历按钮加载完成并可点击
        refresh_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@zp-stat-content='刷新简历']"))
        )

        # 点击刷新简历按钮
        refresh_button.click()
        # 等待刷新成功提示出现
        time.sleep(1)
        # 等待resume-top元素的出现，设置最长等待时间为10秒
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "resume-top"))
            WebDriverWait(driver, 10).until(element_present)
            print("智联招聘简历刷新成功！")
        except TimeoutException:
            print("智联招聘简历刷新失败")
        # 打开第二个tab标签访问 猎聘网去执行刷新简历操作
        driver.execute_script("window.open('https://c.liepin.com/','secondtab');")
        # It is switching to second tab now
        driver.switch_to.window("secondtab")
        windowstabs = driver.window_handles
        # 获取当前浏览器的窗口
        currenttab = driver.current_window_handle
        # 切换到新窗口
        driver.switch_to.window(windowstabs[1]) # 第二个标签页面是猎聘网

        # 定位手机扫码元素
        driver.find_element(By.CLASS_NAME, 'jsx-3095314988').click()
        time.sleep(30)
        # 等待刷新简历按钮加载完成并可点击
        refresh_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='刷新简历']"))
        )
        # 点击刷新简历按钮
        refresh_button.click()
        # 匹配提示信息元素
        print("猎聘网刷新简历成功！\n")

        # 进入循环，这个循环从8点55到下午5点30,每隔2分钟刷新一次简历
        # 定义开始时间和结束时间
        start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 55)
        end_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 17, 30)
        # 初始化计数器
        count = 0
        # 循环直到结束时间
        while datetime.now() < end_time:
            # 递增计数器
            count += 1
            # 切换到第一个标签页
            driver.switch_to.window(windowstabs[0])
            driver.refresh()
            # 点击第一个标签页的刷新按钮
            refresh_btn1 = driver.find_element(By.XPATH, "//a[@zp-stat-content='刷新简历']")
            ActionChains(driver).click(refresh_btn1).perform()

            # 切换到第二个标签页
            driver.switch_to.window(windowstabs[1])
            driver.refresh()
            time.sleep(5)
            # 点击第二个标签页的刷新按钮
            driver.find_element(By.XPATH, "//p[text()='刷新简历']").click()
            # 输出已经执行的次数
            print(f"已执行第 {count} 次刷新")
            # 等待2分钟
            time.sleep(180)  # 3分钟等于120秒
        driver.quit
if __name__ == "__main__":
    job = AutoRefreshResume()
    job.zhaopin()
