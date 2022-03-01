import pytest
import allure
from time import sleep
from logging import getLogger
from selenium.webdriver.common.by import By
from allure_commons.types import AttachmentType
from automation.gui.functional.get_log import FrameLog

logger = getLogger()


@allure.feature('測試前置')
@allure.title('進入彩票投注頁')
@allure.description('確認能夠正常進入所選的彩票投注頁')
@pytest.mark.dependency(depends=['login'], scope='session')
@pytest.mark.dependency(name='join_lotto')
def test_join_lotto(set_driver, get_join_lotto_information):
    driver = set_driver
    inform = get_join_lotto_information
    driver.implicitly_wait(10)

    # 縮放網頁比例90%
    driver.execute_script("document.body.style.transform='scale(0.9)'")

    # 往下拖曳
    sleep(1)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)

    # 移動到彩種選單上
    sleep(1)
    FrameLog.move_element(driver, By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[1]/div[2]/div[2]/span').perform()

    # 獲得每個彩種的class，符合選取項目就點擊進入頁面
    sleep(2)
    elements = FrameLog.locator_elements(driver, By.CLASS_NAME, 'lott-item')
    for element in elements:
        # print(element.get_attribute('textContent'))
        if element.get_attribute('textContent') == inform['lotto_name']:
            # 點擊符合的彩種
            sleep(1)
            element.click()
            break
        elif element == elements[-1] and element.get_attribute('textContent') != inform['lotto_name']:
            logger.error(f'into lotto fail,not get {inform["lotto_name"]}. element:{element}, ')
            allure.attach(driver.get_screenshot_as_png(), name='進入彩種失敗', attachment_type=AttachmentType.PNG)
            driver.quit()
            pytest.fail('進入彩種失敗')

    # 縮放網頁比例回100%
    sleep(1)
    driver.execute_script("document.body.style.transform='scale(1)'")
