import platform
import os
import pytest
import allure

# 作業系統版本
system_version = platform.system() + platform.release()

# Python版本
python_version = platform.python_version()

# Allure版本
allure_version = os.popen('allure --version')
allure_version = allure_version.read()
allure_version = allure_version.replace('\n', '')

# Pytest版本
pytest_version = pytest.__version__

print(f'systemVersion={system_version}')
print(f'pythonVersion={python_version}')
print(f'allureVersion={allure_version}')
print(f'pytestVersion={pytest_version}')
input()
