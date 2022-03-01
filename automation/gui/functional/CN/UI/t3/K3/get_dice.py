import pytest
import allure
from time import sleep
from logging import getLogger
from selenium.webdriver.common.by import By
from allure_commons.types import AttachmentType
from automation.gui.functional.get_log import FrameLog

logger = getLogger()


def _get_dice(driver, element):
    # 獲取點數的次數
    dice_count = 0

    while True:
        dice_count += 1
        # 獲取骰子點數
        # dice_1 = len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/dl/div[2]/div/li[1]/div/div/div"))
        # dice_2 = len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/dl/div[2]/div/li[2]/div/div/div"))
        # dice_3 = len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/dl/div[2]/div/li[3]/div/div/div"))
        # total_dice = dice_1 + dice_2 + dice_3
        # sleep(2)
        # dice_1 = len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/dl/div[2]/div/li[1]/div/div/div"))
        # dice_2 = len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/dl/div[2]/div/li[2]/div/div/div"))
        # dice_3 = len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/dl/div[2]/div/li[3]/div/div/div"))
        # total_dice1 = dice_1 + dice_2 + dice_3
        dice_1 = len(FrameLog.locator_elements(driver, By.XPATH, '//div[@class="draw-balls"]/li[1]/div/div/div'))
        dice_2 = len(FrameLog.locator_elements(driver, By.XPATH, '//div[@class="draw-balls"]/li[2]/div/div/div'))
        dice_3 = len(FrameLog.locator_elements(driver, By.XPATH, '//div[@class="draw-balls"]/li[3]/div/div/div'))
        total_dice = dice_1 + dice_2 + dice_3
        sleep(2)
        dice_1 = len(FrameLog.locator_elements(driver, By.XPATH, '//div[@class="draw-balls"]/li[1]/div/div/div'))
        dice_2 = len(FrameLog.locator_elements(driver, By.XPATH, '//div[@class="draw-balls"]/li[2]/div/div/div'))
        dice_3 = len(FrameLog.locator_elements(driver, By.XPATH, '//div[@class="draw-balls"]/li[3]/div/div/div'))
        total_dice1 = dice_1 + dice_2 + dice_3
        print(f'第{dice_count}次獲取開獎: {total_dice},{total_dice1}')

        if total_dice == total_dice1:
            break

        # 若確認13次還未開獎，等待一輪 下下輪才進行投注
        if dice_count >= 13:
            logger.error(f'Element:{element}, not normal draw')
            allure.attach(driver.get_screenshot_as_png(), name='無正常開獎', attachment_type=AttachmentType.PNG)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            pytest.fail(f'選號:{element} 無正常開獎')

    return dice_1, dice_2, dice_3
