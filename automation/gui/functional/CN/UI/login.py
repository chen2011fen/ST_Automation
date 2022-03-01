import pytest
import allure
from time import sleep
from logging import getLogger
from selenium.webdriver.common.by import By
from automation.gui.functional.get_log import FrameLog

FrameLog.get_log()
logger = getLogger()


@allure.feature('測試前置')
@allure.title('確認登入功能')
@allure.description('測試是否能正常登入')
@pytest.mark.dependency(name='login')
def test_login(set_driver, get_login_information):
    driver = set_driver

    inform = get_login_information
    url = inform['url']
    acc = inform['account']
    pwd = inform['password']


    sleep(1)
    driver.implicitly_wait(10)
    driver.get(url)
    sleep(2)
    driver.maximize_window()

    # 等待第一個彈窗
    FrameLog.wait_element(driver, 11, By.CLASS_NAME, 'br_imodal_content')
    # 關閉彈窗
    FrameLog.locator_element(driver, By.CLASS_NAME, 'br_imodal_cmclose').click()
    sleep(1)

    # 輸入帳號
    account = FrameLog.locator_element(driver, By.XPATH, '//input[@placeholder="账号"]')
    account.send_keys(acc)
    sleep(1)
    # 輸入密碼
    password = FrameLog.locator_element(driver, By.XPATH, '//input[@placeholder="密码"]')
    password.send_keys(pwd)
    sleep(1)
    # 點擊登入
    sign_in = FrameLog.locator_element(driver, By.XPATH, '//button[text()="登录"]')
    sign_in.click()
    sleep(1)

    # 等待第二個彈窗
    FrameLog.wait_element(driver, 30, By.CLASS_NAME, 'br_imodal_content')
    # 關閉彈窗
    FrameLog.locator_element(driver, By.CLASS_NAME, 'br_imodal_cmclose').click()
    sleep(1)
