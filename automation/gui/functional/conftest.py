import pytest
from selenium import webdriver
from urllib3.exceptions import MaxRetryError
from selenium.common.exceptions import WebDriverException, NoSuchWindowException


@pytest.fixture(scope='session')
def set_driver():
    driver = webdriver.Chrome()
    return driver


def pytest_addoption(parser):
    parser.addoption('--url', action='store', help='input url')
    parser.addoption('--account', action='store', help='input account')
    parser.addoption('--password', action='store', help='input password')
    parser.addoption('--lotto_name', action='store', help='input lotto_name')
    parser.addoption('--play_first', action='store', help='input play_first')
    parser.addoption('--play_second', action='store', help='input play_second')
    parser.addoption('--single_bet_amount', action='store', help='input single_bet_amount')
    parser.addoption('--pump', action='store', help='input pump')
    parser.addoption('--api_key', action='store', help='input api_key')
    parser.addoption('--telegram_id', action='store', help='input telegram_id')


@pytest.fixture(scope='session')
def get_login_information(request):
    params = dict()
    params['url'] = request.config.getoption('--url')
    params['account'] = request.config.getoption('--account')
    params['password'] = request.config.getoption('--password')
    return params


@pytest.fixture(scope='session')
def get_join_lotto_information(request):
    params = dict()
    params['lotto_name'] = request.config.getoption('--lotto_name')
    return params


@pytest.fixture(scope='session')
def get_test_information(request):
    params = dict()
    params['lotto_name'] = request.config.getoption('--lotto_name')
    params['play_first'] = request.config.getoption('--play_first')
    params['play_second'] = request.config.getoption('--play_second')
    params['single_bet_amount'] = request.config.getoption('--single_bet_amount')
    params['pump'] = request.config.getoption('--pump')
    params['api_key'] = request.config.getoption('--api_key')
    params['telegram_id'] = request.config.getoption('--telegram_id')
    return params


@pytest.fixture(scope='session', autouse=True)
def close_driver(set_driver):
    yield
    driver = set_driver
    try:
        driver.quit()
    except (WebDriverException, MaxRetryError, NoSuchWindowException):
        pass
