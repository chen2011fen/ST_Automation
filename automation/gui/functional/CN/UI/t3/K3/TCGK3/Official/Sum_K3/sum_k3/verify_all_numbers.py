import pytest
import allure
import tkinter as tk
from time import sleep
from flaky import flaky
from telebot import TeleBot
from logging import getLogger
from tkinter import messagebox
from allure_commons.types import AttachmentType
from urllib3.exceptions import MaxRetryError, NewConnectionError
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automation.gui.functional.get_log import FrameLog
from automation.gui.functional.get_test_data import YamlUtil
from automation.gui.functional.CN.UI.get_money import _get_money
from automation.gui.functional.CN.UI.t3.get_time import _get_seconds
from automation.gui.functional.CN.UI.t3.K3.get_dice import _get_dice
from automation.gui.functional.CN.UI.t3.betting_process import _betting_process
from automation.gui.functional.CN.UI.t3.confirm_order_information import _confirm_inprogress_order, _confirm_over_order

logger = getLogger()


# messagebox顯示時，只顯示對話框，隱藏主視窗
window = tk.Tk()
window.attributes('-topmost', True)
window.withdraw()

prizes = list()


@flaky()
@allure.feature('測試前置')
@allure.title('獲取K3和值獎金')
@allure.description('從獎金總覽內，獲取各個選號對應的獎金')
@pytest.mark.dependency(depends=['join_lotto'], scope='session')
@pytest.mark.dependency(name='get_prizes')
def test_get_prizes(set_driver):
    driver = set_driver

    # 切換frame
    FrameLog.wait_element(driver, 15, By.XPATH, '//iframe[@class="lotteryIframe"]')
    FrameLog.switch_frame(driver, By.XPATH, '//iframe[@class="lotteryIframe"]')

    # 確認投注頁倒數正常(判斷10次/秒)
    timer_count = 0
    while True:
        # 最多判斷10次
        if timer_count >= 11:
            logger.error('The countdown is abnormal after into lotto page.')
            allure.attach(driver.get_screenshot_as_png(), name='投注頁倒數不正常', attachment_type=AttachmentType.PNG)
            driver.quit()
            pytest.fail('投注頁倒數不正常')
            break

        try:
            timer_num = driver.find_elements_by_class_name('timer-num')
            ten = int(timer_num[4].text) * 10
            ones = int(timer_num[5].text)
            total_timer = ten + ones
            # 若秒數低於10秒，等到下一輪才點擊彈窗按鈕
            if total_timer <= 10:
                FrameLog.wait_element(driver, 30, By.CLASS_NAME, 'timer-lock-message')
                sleep(4)
            elif total_timer >= 55:
                sleep(4)
            break
        except (IndexError, ValueError):
            timer_count += 1
            sleep(1)

    # 點擊彈出的視窗，沒有彈窗則忽略Timeout錯誤(這個彈窗不是每個彩種都會出現)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="greetings-popup"]')))
        sleep(2)
        FrameLog.locator_element(driver, By.XPATH, '//div[@class="greetings-iknowit"]').click()
    except TimeoutException:
        pass

    # 點擊要測試的玩法
    FrameLog.locator_element(driver, By.XPATH, '//div[@class="play-group-list"]/dd[1]').click()

    global prizes
    sleep(3)
    # 從獎金總覽獲取獎金金額
    for n in FrameLog.locator_elements(driver, By.CLASS_NAME, 'prize')[2:]:
        prize = n.get_attribute('textContent')
        prize = prize.replace(prize[-1:], '')
        prizes.append(prize)
    templist = [num for num in reversed(prizes)]
    prizes += templist

    # 判斷有無獲得獎金
    if len(prizes) == 0:
        logger.error(f'{test_get_prizes.__name__}, prizes are null value')
        pytest.skip(f'{test_get_prizes.__name__}, prizes are null value')

    # 鎖定期視窗出現後，才進入測試function
    FrameLog.wait_element(driver, 90, By.CLASS_NAME, 'timer-lock-message')
    sleep(6)


@allure.feature('測試所有選號')
@allure.story('測試K3和值')
@allure.title('第{times}次測試-選號{element}')
# @pytest.mark.parametrize('times, element', [i for i in range(3, 19)])
@pytest.mark.parametrize('times, element', [(i, j) for i in range(1, YamlUtil.read_test_times()) for j in range(3, 19)])
@allure.description('確認K3和值的所有選號皆能正常投注、兌獎')
@pytest.mark.dependency(depends=['get_prizes'])
def test_sum_value(set_driver, get_test_information, element, times):
    # --------------------宣告變數--------------------
    driver = set_driver
    inform = get_test_information

    lotto_name = inform['lotto_name']
    play_first = inform['play_first']
    play_second = inform['play_second']

    pump = inform['pump']
    pump = float(pump)
    pump = pump / 100

    single_bet_amount = inform['single_bet_amount']
    single_bet_amount = float(single_bet_amount)

    api_key = inform['api_key']
    telegram_id = inform['telegram_id']

    new_money = float()

    # --------------------開始測試--------------------
    try:
        # 獲取錢包金額
        money = _get_money(driver)

        # 若秒數低於19秒，等到下一輪一開始才投(以免點擊或確認資訊過程有出現鎖定期彈窗會影響測試)
        total_timer = _get_seconds(driver)
        if total_timer <= 19:
            FrameLog.wait_element(driver, 30, By.CLASS_NAME, 'timer-lock-message')
            sleep(4)

        # --------------------投注流程--------------------
        # 點擊選號
        position = str(element - 2)
        # driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[3]/div[1]/dl' + '/div[' + position + ']/dt[1]').click()
        FrameLog.locator_element(driver, By.XPATH, f'//dl[@class="select-number-row"]/div[{position}]/dt[1]').click()

        # 獲得頁面的注數、總投注額
        sleep(1)
        # page_bet_number = int(driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[4]/dl[4]/dt[1]/span').get_attribute('textContent'))
        page_bet_number = int(FrameLog.locator_element(driver, By.XPATH, '//dl[@class="options-amount-bet"]/dt[1]/span').get_attribute('textContent'))
        print(page_bet_number)
        # page_bet_amount = float(driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[4]/dl[4]/dt[2]/span').get_attribute('textContent'))
        page_bet_amount = float(FrameLog.locator_element(driver, By.XPATH, '//dl[@class="options-amount-bet"]/dt[2]/span').get_attribute('textContent'))
        print(page_bet_amount)

        # 計算注數
        bet_number = 1
        # 計算總投注額(注數*投注額)
        total_bet_amount = bet_number*single_bet_amount

        # 判斷注數、總投注額數值正不正確
        if page_bet_number == bet_number:
            pass
        else:
            logger.error(f'Betting process bet_number numerical error. correct bet number:{bet_number},display:{page_bet_number}')
            allure.attach(driver.get_screenshot_as_png(), name='投注流程-注數數值不正確', attachment_type=AttachmentType.PNG)
            # 流程: 重整(重新獲得資訊)->切換進lotto frame->等待進下期->點和值進入玩法->此次測試fail
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
            pytest.fail(f'投注流程-注數數值不正確.\n正確注數:{bet_number},顯示注數:{page_bet_number}')

        if page_bet_amount == total_bet_amount:
            pass
        else:
            logger.error(f'Betting process total bet amount numerical error. correct total bet amount:{total_bet_amount},display amount:{page_bet_amount}')
            allure.attach(driver.get_screenshot_as_png(), name='投注流程-總投注額數值不正確', attachment_type=AttachmentType.PNG)
            # 流程: 重整(重新獲得資訊)->切換進lotto frame->等待進下期->點和值進入玩法->此次測試fail
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
            pytest.fail(f'投注流程-總投注額數值不正確.\n正確總投注額:{total_bet_amount},顯示總投注額:{page_bet_amount}')

        # 進入投注流程，若成功會回傳目前錢包金額
        money = _betting_process(driver, element, bet_number, total_bet_amount, money)
        sleep(2)

        # 如果投注成功開啟投注紀錄，確認進行中的投注資訊
        _confirm_inprogress_order(driver, element, lotto_name, play_second, total_bet_amount, '进行中')

        # --------------------兌獎流程--------------------
        # 用時間判斷此輪或下輪才需兌獎
        total_timer = _get_seconds(driver)
        if total_timer >= 55:
            sleep(12)
        elif total_timer >= 50:
            sleep(7)
        else:
            FrameLog.wait_element(driver, 60, By.CLASS_NAME, 'timer-lock-message')
            sleep(12)

        # 獲得骰子點數，計算總點數
        dice1, dice2, dice3 = _get_dice(driver, element)
        total_dice = dice1 + dice2 + dice3

        sleep(7)
        # 判斷中獎
        if element == total_dice:
            # 獎金總覽對應獎金
            prize = str(prizes[element - 3])
            prize = prize.replace(prize[-2:], '')

            # 開啟投注紀錄，確認中獎的投注資訊
            _confirm_over_order(driver, element, prize)

            # 確認回到投注頁
            # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'select-number-row-ball')))
            FrameLog.wait_element(driver, 30, By.CLASS_NAME, 'select-number-row-ball')

            # 判斷錢包金額及沒更新的處理
            # driver.switch_to.default_content()
            # click_count = 1
            timer_count = 0
            sleep(2)
            prize = float(prize)
            while round(new_money - money, 4) != prize-(prize*pump):
                if timer_count >= 16:
                    logger.error(f'Wallet amount incorrect after winning. before:{money},after winning:{new_money},correct:{prize - (prize * pump)}')
                    allure.attach(driver.get_screenshot_as_png(), name='已中獎-獲得獎金金額不正確', attachment_type=AttachmentType.PNG)
                    pytest.fail(f'已中獎-獲得獎金金額不正確.\n原錢包金額:{money},中獎後錢包金額:{new_money},應獲得獎金(扣除抽水):{prize - (prize * pump)}')

                while True:
                    try:
                        # new_money = float(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/span').text)
                        new_money = _get_money(driver)
                        break
                    except ValueError:
                        sleep(1)
                timer_count += 1

        # 未中獎判斷
        else:
            # 開啟投注紀錄，確認未中獎的投注資訊
            _confirm_over_order(driver, element, '未中奖')

            # 確認回到投注頁
            # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'select-number-row-ball')))
            FrameLog.wait_element(driver, 30, By.CLASS_NAME, 'select-number-row-ball')

            # 判斷錢包金額及沒更新的處理
            # driver.switch_to.default_content()
            # click_count = 1
            timer_count = 0
            sleep(2)
            while new_money != money:
                if timer_count >= 16:
                    logger.error(f'Wallet amount incorrect after not winning. before:{money},after not winning:{new_money}')
                    allure.attach(driver.get_screenshot_as_png(), name='未中獎-錢包金額不正確', attachment_type=AttachmentType.PNG)
                    pytest.fail(f'未中獎-錢包金額不正確.\n原錢包金額:{money},兌獎後錢包金額:{new_money}')

                while True:
                    try:
                        # new_money = float(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/span').text)
                        new_money = _get_money(driver)
                        break
                    except ValueError:
                        sleep(1)
                timer_count += 1

    # 若選擇結束測試，下一輪會退出測試
    except (MaxRetryError, NewConnectionError):
        pytest.exit('已結束測試')

    # 出現預期外的例外就會跳出警告視窗
    except Exception as e:
        return_value = messagebox.askokcancel(title='錯誤', message='測試出現例外狀況，是否要繼續測試?')

        if telegram_id == '':
            pass
        else:
            bot = TeleBot(api_key)
            bot.send_message(chat_id=telegram_id, text='測試中出現預期外錯誤，目前測試中斷')

        if return_value:
            # 繼續後面選號的測試，此輪報fail
            logger.error(f'Pick number:{element}, unexpected error occurred, Error message:{e}')
            allure.attach(driver.get_screenshot_as_png(), name=f'選號:{element}發生預期外錯誤', attachment_type=AttachmentType.PNG)
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
            pytest.fail(f'選號:{element}發生預期外錯誤.\n錯誤訊息:{e}')
        else:
            logger.error(f'Pick number::{element}, unexpected error occurred, Error message:{e}')
            allure.attach(driver.get_screenshot_as_png(), name=f'選號:{element}發生預期外錯誤', attachment_type=AttachmentType.PNG)
            driver.quit()
            pytest.fail(f'選號:{element}發生預期外錯誤.\n錯誤訊息:{e}')
