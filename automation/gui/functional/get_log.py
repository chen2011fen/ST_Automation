import allure
import pytest
import logging
from datetime import date
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, NoSuchElementException

today = date.today()


class FrameLog:
    @staticmethod
    def get_log():
        # 創建日誌
        logger = logging.getLogger()
        # 設置預設輸出等級
        logger.setLevel(logging.WARNING)
        # 創建格式 -> 錯誤級別:時間 | 執行檔案:錯誤的行數 [錯誤訊息]
        formatter = logging.Formatter(fmt='%(levelname)s:%(asctime)s | %(filename)s:%(lineno)d [%(message)s]', datefmt='%Y/%m/%d %X')
        # 創建控制台
        # file_handler = logging.FileHandler(f'C:/Users/user/Documents/Test_reports/logs/{str(today)}_test.log')
        file_handler = logging.FileHandler(f'./functional_reports/logs/{str(today)}_test.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def switch_frame(set_driver, *args):
        driver = set_driver
        logger = logging.getLogger()
        try:
            driver.switch_to.frame(driver.find_element(*args))
            logger.info(f'switch to iframe successful, element:{args[1]}')
        except Exception as e:
            logger.error(f'switch to iframe fail, element:{args[1]}, {str(e)}')

    @staticmethod
    def locator_element(set_driver, *args):
        driver = set_driver
        logger = logging.getLogger()
        global element
        try:
            element = driver.find_element(*args)
            logger.info(f'locator element successful, element:{args[1]}')
        except Exception as e:
            logger.error(f'locator element fail, element:{args[1]}, {str(e)}')
            allure.attach(driver.get_screenshot_as_png(), name=f'unable locator element_{args[1]}', attachment_type=AttachmentType.PNG)
            driver.quit()
            pytest.fail(f'unable locator element_{args[1]}')

        return element

    @staticmethod
    def locator_elements(set_driver, *args):
        driver = set_driver
        logger = logging.getLogger()
        global elements
        try:
            elements = driver.find_elements(*args)
            logger.info(f'locator elements successful, element:{args[1]}')
        except Exception as e:
            logger.error(f'locator elements fail, element:{args[1]}, {str(e)}')
            allure.attach(driver.get_screenshot_as_png(), name=f'unable locator elements_{args[1]}', attachment_type=AttachmentType.PNG)
            driver.quit()
            pytest.fail(f'unable locator elements_{args[1]}')

        return elements

    @staticmethod
    def wait_element(set_driver, timeout, *args):
        driver = set_driver
        logger = logging.getLogger()
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((args[0], args[1])))
            logger.info(f'wait successful, element:{args[1]}')
        except Exception as e:
            logger.error(f'wait fail, element:{args[1]}, {str(e)}')
            allure.attach(driver.get_screenshot_as_png(), name=f'{args[1]}_timeout', attachment_type=AttachmentType.PNG)
            driver.quit()
            pytest.fail(f'{args[1]}_timeout')

    @staticmethod
    def move_element(set_driver, *args):
        driver = set_driver
        logger = logging.getLogger()
        global element
        try:
            element = ActionChains(driver).move_to_element(driver.find_element(*args))
            logger.info(f'move to element successful, element:{args[1]}')
        except (NoSuchElementException, WebDriverException, NoSuchWindowException):
            logger.error(f'move to element fail, element:{args[1]}')
            allure.attach(driver.get_screenshot_as_png(), name=f'move fail_{args[1]}', attachment_type=AttachmentType.PNG)

        return element
