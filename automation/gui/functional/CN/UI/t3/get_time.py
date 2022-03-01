from selenium.webdriver.common.by import By
from automation.gui.functional.get_log import FrameLog


def _get_seconds(driver):
    timer_num = FrameLog.locator_elements(driver, By.CLASS_NAME, 'timer-num')
    ten = int(timer_num[4].text) * 10
    ones = int(timer_num[5].text)
    total_timer = ten + ones

    return total_timer
