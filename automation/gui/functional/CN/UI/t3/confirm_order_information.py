import pytest
import allure
from time import sleep
from logging import getLogger
from selenium.webdriver.common.by import By
from allure_commons.types import AttachmentType
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from automation.gui.functional.get_log import FrameLog
from automation.gui.functional.CN.UI.t3.get_time import _get_seconds

logger = getLogger()


def _confirm_inprogress_order(driver, element, lotto_name, play_second, bet_amount, status):
    # 如果倒數<3 or >=55，等鎖定期結束才按按鈕(timer-lock出現的error handle)
    total_timer = _get_seconds(driver)
    if total_timer >= 55:
        sleep(4)

    # 點擊投注紀錄
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[1]').click()
    FrameLog.locator_element(driver, By.XPATH, '//div[@class="feature-button-record"]').click()
    sleep(2)

    while True:
        try:
            window_status = driver.find_elements_by_class_name('status')
            str(window_status[1].text)
            break
        except (NoSuchElementException, IndexError):
            sleep(1)

    if status == '进行中':
        while True:
            try:
                window_lotto_name = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[2]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[3]').text
                window_play = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[2]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[5]').text
                window_bet_content = driver.find_elements_by_class_name('bet-content')
                window_bet_amount = float(driver.find_element_by_class_name('log-divTable-body-cell').get_attribute('textContent'))
                str(window_status[1].text)
                break
            except (NoSuchElementException, IndexError):
                sleep(1)

        # 確定彩種、玩法、投注選號內容、投注額、訂單狀態是否正確
        if window_lotto_name == lotto_name:
            pass
        else:
            logger.error(f'Pick number:{element}, in progress order detail lotto name error. correct:{lotto_name}, display:{window_lotto_name}')
            allure.attach(driver.get_screenshot_as_png(), name='進行中-訂單資訊錯誤', attachment_type=AttachmentType.PNG)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            pytest.fail(f'進行中-訂單資訊錯誤. 正確資訊:{lotto_name},實際顯示:{window_lotto_name}')

        if window_play == play_second:
            pass
        else:
            logger.error(f'Pick number:{element}, in progress order detail second play error. correct:{play_second}, display:{window_play}')
            allure.attach(driver.get_screenshot_as_png(), name='進行中-訂單資訊錯誤', attachment_type=AttachmentType.PNG)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            pytest.fail(f'進行中-訂單資訊錯誤. 正確資訊:{play_second},實際顯示:{window_play}')

        if window_bet_content[0].text == str(element):
            pass
        else:
            logger.error(f'Pick number:{element}, in progress order detail bet content error. correct:{element}, display:{window_bet_content[0].text}')
            allure.attach(driver.get_screenshot_as_png(), name='進行中-訂單資訊錯誤', attachment_type=AttachmentType.PNG)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            pytest.fail(f'進行中-訂單資訊錯誤. 正確資訊:{element},實際顯示:{window_bet_content[0].text}')

        if window_bet_amount == bet_amount:
            pass
        else:
            logger.error(f'Pick number:{element}, in progress order detail bet amount error. correct:{bet_amount}, display:{window_bet_amount}')
            allure.attach(driver.get_screenshot_as_png(), name='進行中-訂單資訊錯誤', attachment_type=AttachmentType.PNG)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            pytest.fail(f'進行中-訂單資訊錯誤. 正確資訊:{bet_amount},實際顯示:{window_bet_amount}')

        if window_status[1].text == status:
            pass
        else:
            logger.error(f'Pick number:{element}, in progress order detail status error. correct:{status}, display:{window_status[1].text}')
            allure.attach(driver.get_screenshot_as_png(), name='進行中-訂單資訊錯誤', attachment_type=AttachmentType.PNG)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            pytest.fail(f'進行中-訂單資訊錯誤. 正確資訊:{status},實際顯示:{window_status[1].text}')

    # 如果倒數<3 or >=55，等鎖定期結束才按按鈕(timer-lock出現的error handle)
    total_timer = _get_seconds(driver)
    if total_timer < 3:
        sleep(7)
    elif total_timer >= 55:
        sleep(4)

    # 關閉投注記錄彈窗
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
    FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()


def _confirm_over_order(driver, element, status):
    # 如果倒數<3 or >=55，等鎖定期結束才按按鈕(timer-lock出現的error handle)
    total_timer = _get_seconds(driver)
    if total_timer >= 55:
        sleep(4)

    # 點擊投注紀錄
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[1]').click()
    FrameLog.locator_element(driver, By.XPATH, '//div[@class="feature-button-record"]').click()
    sleep(2)

    while True:
        try:
            window_status = driver.find_elements_by_class_name('status')
            str(window_status[1].text)
            break
        except (NoSuchElementException, IndexError):
            sleep(1)

    if status == '未中奖':
        while True:
            try:
                if window_status[1].text == status:
                    break
                else:
                    logger.error(f'Pick number:{element}, not winning order detail status error. correct:{status},display:{window_status[1].text}')
                    allure.attach(driver.get_screenshot_as_png(), name='未中獎-投注紀錄資訊不正確', attachment_type=AttachmentType.PNG)
                    # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
                    FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
                    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                    FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                    sleep(4)
                    pytest.fail(f'未中獎-投注紀錄資訊不正確.正確狀態:{status}, 投注紀錄狀態顯示:{window_status[1].text}')
            except StaleElementReferenceException:
                # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
                FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
                sleep(1)
                # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[1]').click()
                FrameLog.locator_element(driver, By.XPATH, '//div[@class="feature-button-record"]').click()
                sleep(2)
    # 中獎 投注記錄獎金、獎金總覽對應的獎金
    else:
        # 投注記錄獎金
        bonus = float(window_status[1].text)
        # 獎金總覽對應獎金
        prize = float(status)
        try:
            # 比對獎金總覽、投注記錄獎金
            if bonus == prize:
                pass
            else:
                logger.error(f'Pick number:{element}, winning order detail bonus error. correct:{prize},display:{window_status[1].text}')
                allure.attach(driver.get_screenshot_as_png(), name='已中獎-投注紀錄獎金金額顯示不正確', attachment_type=AttachmentType.PNG)
                # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
                FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(4)
                pytest.fail(f'已中獎-投注紀錄獎金金額顯示不正確. 正確金額:{prize},投注紀錄狀態顯示:{window_status[1].text}')
        except StaleElementReferenceException:
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
            sleep(1)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="feature-button-record"]').click()
            sleep(2)

    # 如果倒數<3 or >=55，等鎖定期結束才按按鈕(timer-lock出現的error handle)
    total_timer = _get_seconds(driver)
    if total_timer < 3:
        sleep(7)
    elif total_timer >= 55:
        sleep(4)

    # 關閉投注記錄彈窗
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[1]').click()
    FrameLog.locator_element(driver, By.XPATH, '//div[@class="popup-close"]').click()
