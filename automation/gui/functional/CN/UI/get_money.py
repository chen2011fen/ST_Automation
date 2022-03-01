from logging import getLogger
from selenium.webdriver.common.by import By
from automation.gui.functional.get_log import FrameLog

logger = getLogger()


def _get_money(driver):
    # driver.switch_to.default_content()
    # driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/div[1]/div[3]/div/span').click()
    # sleep(3)
    # money = float(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/span').text)

    money = float(FrameLog.locator_element(driver, By.XPATH, '//div[@class="balance-price"]/span').text)

    return money
