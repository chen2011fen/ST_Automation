import pytest
import allure
from time import sleep
from logging import getLogger
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from automation.gui.functional.get_log import FrameLog
from automation.gui.functional.CN.UI.get_money import _get_money
from automation.gui.functional.CN.UI.t3.get_time import _get_seconds

logger = getLogger()


def _betting_process(driver, element, bet_number, total_bet_amount, money):
    new_money = float()

    # 點擊直接投注
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[4]/dl[5]/dt[2]').click()
    FrameLog.locator_element(driver, By.XPATH, '//dt[@class="options-betting-one-key-bet-btn enabled"]').click()
    # 等待投注信息彈框出現，超時跳過這輪
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'x-pop')))
    except TimeoutException:
        logger.error(f'Pick number:{element}, betting process bet popup wait time out.')
        allure.attach(driver.get_screenshot_as_png(), name=f'投注信息彈框-等待超時', attachment_type=AttachmentType.PNG)
        driver.refresh()
        # sleep(9)
        # driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/iframe'))
        FrameLog.wait_element(driver, 15, By.XPATH, '//iframe[@class="lotteryIframe"]')
        FrameLog.switch_frame(driver, By.XPATH, '//iframe[@class="lotteryIframe"]')
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
        FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
        sleep(4)
        # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div[1]/dl/div/dd[1]').click()
        FrameLog.locator_element(driver, By.XPATH, '//div[@class="play-group-list"]/dd[1]').click()
        pytest.fail('投注信息彈框-等待超時')

    # if driver.find_element_by_xpath('//*[@id="modal-betConfirm"]/div/div[2]/div/h2').get_attribute('textContent') == '请确认投注信息':
    if FrameLog.locator_element(driver, By.XPATH, '//div[@class="x-pop"]/h2').get_attribute('textContent') == '请确认投注信息':
        # 判斷注數
        # window_bet_number = driver.find_element_by_xpath('//*[@id="modal-betConfirm"]/div/div[2]/div/dl/dd[1]').text
        window_bet_number = FrameLog.locator_element(driver, By.XPATH, '//dl[@class="lott-rs-pop clearfix"]/dd[1]').text
        window_bet_number = window_bet_number.replace(window_bet_number[-1:], '')
        window_bet_number = int(window_bet_number)
        if window_bet_number == bet_number:
            pass
        else:
            logger.error(f'Pick number:{element}, bet number value incorrect. correct bet:{bet_number},display:{window_bet_number}')
            allure.attach(driver.get_screenshot_as_png(), name='投注信息彈框- 注數不正確', attachment_type=AttachmentType.PNG)
            driver.refresh()
            # sleep(9)
            # driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/iframe'))
            FrameLog.wait_element(driver, 15, By.XPATH, '//iframe[@class="lotteryIframe"]')
            FrameLog.switch_frame(driver, By.XPATH, '//iframe[@class="lotteryIframe"]')
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div[1]/dl/div/dd[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="play-group-list"]/dd[1]').click()
            pytest.fail(f'投注信息彈框-注數不正確\n正確注數:{bet_number},顯示:{window_bet_number}')

        # 判斷投注額
        # window_bet_amount = float(driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/dl/dd[2]').text)
        window_bet_amount = float(FrameLog.locator_element(driver, By.XPATH, '//dl[@class="lott-rs-pop clearfix"]/dd[2]').text)
        if window_bet_amount == total_bet_amount:
            pass
        else:
            logger.error(f'Pick number:{element}, popup display total bet amount value incorrect. correct amount:{total_bet_amount},display:{window_bet_amount}')
            allure.attach(driver.get_screenshot_as_png(), name='投注信息彈框-投注額不正確', attachment_type=AttachmentType.PNG)
            driver.refresh()
            # sleep(9)
            # driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/iframe'))
            FrameLog.wait_element(driver, 15, By.XPATH, '//iframe[@class="lotteryIframe"]')
            FrameLog.switch_frame(driver, By.XPATH, '//iframe[@class="lotteryIframe"]')
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div[1]/dl/div/dd[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="play-group-list"]/dd[1]').click()
            pytest.fail(f'投注信息彈框-投注額不正確\n正確投注額:{total_bet_amount},顯示:{window_bet_amount}')
        # driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/input[2]').click()
        FrameLog.locator_element(driver, By.XPATH, '//input[@value="是"]').click()
    # elif driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]').get_attribute('textContent') == '生成订单失败':
    elif FrameLog.locator_element(driver, By.XPATH, '/html/body/div[4]/div/div/div[2]').get_attribute('textContent') == '生成订单失败':
        logger.error(f'Pick number:{element}, order generation failed.')
        allure.attach(driver.get_screenshot_as_png(), name='投注信息彈框-生成訂單失敗', attachment_type=AttachmentType.PNG)
        # 如果倒數<3 or >=55，等鎖定期結束才按按鈕(timer-lock出現的error handle)
        total_timer = _get_seconds(driver)
        if total_timer < 3:
            sleep(7)
        elif total_timer >= 55:
            sleep(4)
        # driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/input').click()
        FrameLog.locator_element(driver, By.XPATH, '/html/body/div[4]/div/div/div[3]/input').click()

        # 確認回到投注頁
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'select-number-row-ball')))
        FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'select-number-row-ball')

        # 判斷錢包金額及沒更新的處理
        # driver.switch_to.default_content()
        # click_count = 1
        timer_count = 0
        sleep(2)
        while new_money != money:
            if timer_count >= 11:
                logger.error(f'Pick number:{element}, order generation failed then wallet amount incorrect. correct money:{money},display:{new_money}')
                allure.attach(driver.get_screenshot_as_png(), name='投注信息彈框-投注失敗後錢包金額錯誤', attachment_type=AttachmentType.PNG)
                # 如果金額不正確跳過這輪測試，等待一期後再繼續進行測試
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(4)
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(4)
                pytest.fail(f'投注信息彈框-投注失敗後錢包金額錯誤\n原錢包金額:{money}, 投注失敗後錢包金額:{new_money}')

            while True:
                try:
                    # new_money = float(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/span').text)
                    new_money = _get_money(driver)
                    break
                except ValueError:
                    sleep(1)
            timer_count += 1
        pytest.fail('投注信息彈框-生成訂單失敗')

    # 等待訂單結果彈框出現
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'x-pop')))
    except TimeoutException:
        logger.error(f'Pick number:{element}, order result popup wait time out.')
        allure.attach(driver.get_screenshot_as_png(), name='訂單結果彈框-等待超時', attachment_type=AttachmentType.PNG)
        driver.refresh()
        # sleep(9)
        FrameLog.wait_element(driver, 15, By.XPATH, '//iframe[@class="lotteryIframe"]')
        FrameLog.switch_frame(driver, By.XPATH, '//iframe[@class="lotteryIframe"]')
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
        FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
        sleep(4)
        # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div[1]/dl/div/dd[1]').click()
        FrameLog.locator_element(driver, By.XPATH, '//div[@class="play-group-list"]/dd[1]').click()
        pytest.fail('訂單結果彈框-等待超時')

    # if driver.find_element_by_xpath('//*[@id="modal-"]/div/div[2]/div/h2').get_attribute('textContent') == '生成订单成功':
    if FrameLog.locator_element(driver, By.XPATH, '//div[@class="x-pop"]/h2').get_attribute('textContent') == '生成订单成功':
        # 判斷投注總額
        window_bet_amount = float(driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/div/table/tbody/tr[2]/td[2]').text)
        if window_bet_amount == total_bet_amount:
            pass
        else:
            logger.error(f'Pick number:{element}, order result popup display total bet amount value incorrect. correct bet amount:{total_bet_amount},display:{window_bet_amount}')
            allure.attach(driver.get_screenshot_as_png(), name='訂單結果彈框-投注總額不正確', attachment_type=AttachmentType.PNG)
            driver.refresh()
            # sleep(9)
            # driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/iframe'))
            FrameLog.wait_element(driver, 15, By.XPATH, '//iframe[@class="lotteryIframe"]')
            FrameLog.switch_frame(driver, By.XPATH, '//iframe[@class="lotteryIframe"]')
            # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)
            # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div[1]/dl/div/dd[1]').click()
            FrameLog.locator_element(driver, By.XPATH, '//div[@class="play-group-list"]/dd[1]').click()
            pytest.fail(f'訂單結果彈框-投注總額不正確\n正確總投注額:{total_bet_amount}, 實際顯示:{window_bet_amount}')
        sleep(5)

        # 判斷錢包金額及沒更新的處理
        # driver.switch_to.default_content()
        # click_count = 1
        timer_count = 0
        while (money - total_bet_amount) != new_money:
            if timer_count >= 11:
                logger.error(f'Pick number:{element}, successful betting, but wallet without deduction of total bet amount. correct money:{money}, display:{new_money}')
                allure.attach(driver.get_screenshot_as_png(), name='訂單結果彈框-投注成功後錢包金額不正確', attachment_type=AttachmentType.PNG)
                # 如果金額不正確跳過這輪測試，等待一期後再繼續進行測試
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(4)
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(4)
                pytest.fail(f'訂單結果彈框-投注成功後錢包金額不正確\n原錢包金額:{money}, 投注成功後錢包金額:{new_money}')

            while True:
                try:
                    # new_money = float(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/span').text)
                    new_money = _get_money(driver)
                    break
                except ValueError:
                    sleep(1)
            timer_count += 1

    # elif driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]').get_attribute('textContent') == '生成订单失败':
    elif FrameLog.locator_element(driver, By.XPATH, '/html/body/div[4]/div/div/div[2]').get_attribute('textContent') == '生成订单失败':
        logger.error(f'Pick number:{element}, order generation failed.')
        allure.attach(driver.get_screenshot_as_png(), name='訂單結果彈框- 生成訂單失敗', attachment_type=AttachmentType.PNG)
        # 如果倒數<3 or >=55，等鎖定期結束才按按鈕(timer-lock出現的error handle)
        # timer_num = driver.find_elements_by_class_name('timer-num')
        # ten = int(timer_num[4].text) * 10
        # ones = int(timer_num[5].text)
        # total_timer = ten + ones
        total_timer = _get_seconds(driver)
        if total_timer < 3:
            sleep(7)
        elif total_timer >= 55:
            sleep(4)
        # driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/input').click()
        FrameLog.locator_element(driver, By.XPATH, '/html/body/div[4]/div/div/div[3]/input').click()

        # 投注失敗後確認錢包
        # driver.switch_to.default_content()
        # click_count = 1
        timer_count = 0
        sleep(2)
        while new_money != money:
            if timer_count >= 11:
                logger.error(f'Pick number:{element}, order generation failed then wallet amount incorrect. correct money:{money},display:{new_money}')
                allure.attach(driver.get_screenshot_as_png(), name='訂單結果彈框-投注失敗後錢包金額錯誤', attachment_type=AttachmentType.PNG)
                # 如果金額不正確跳過這輪測試，等待一期後再繼續進行測試
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(5)
                # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
                FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
                sleep(5)
                pytest.fail(f'訂單結果彈框-投注失敗後錢包金額錯誤\n原錢包金額:{money}, 投注失敗後錢包金額:{new_money}')

            while True:
                try:
                    # new_money = float(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/span').text)
                    new_money = _get_money(driver)
                    break
                except ValueError:
                    sleep(1)
            timer_count += 1
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'timer-lock-message')))
        FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
        sleep(4)
        pytest.fail('訂單結果彈框-生成訂單失敗')

    return new_money
