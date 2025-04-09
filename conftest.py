#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/28 21:33
@Author  : Poco Ray
@File    : conftest.py
@Software: PyCharm
@Desc    : Description
"""
import os
import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from config.config import Config
from utils.log import logger


@pytest.fixture
def driver(request):
    uiAutomatorOption = UiAutomator2Options()

    if not hasattr(request, 'param'):
        uiAutomatorOption.load_capabilities(Config.mooc_capabilities)
    else:
        if request.param == 'mda':
            uiAutomatorOption.load_capabilities(Config.mda_capabilities)
        elif request.param == 'api':
            uiAutomatorOption.load_capabilities(Config.api_demo_capabilities)
        elif request.param == 'settings':
            uiAutomatorOption.load_capabilities(Config.settings_capabilities)
        else:
            uiAutomatorOption.load_capabilities(Config.common_capabilities)

    driver = webdriver.Remote(Config.appium_server_url, options=uiAutomatorOption)
    try:
        driver.implicitly_wait(5)
        yield driver
    finally:
        if driver:
            driver.quit()


def pytest_collection_modifyitems(items) -> None:
    """
    解决中文字符在pytest报告中显示为unicode编码的问题
    :param items:
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    测试执行失败后，自动截图
    :param item:
    :return:
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver: WebDriver = item.funcargs.get('driver')
        if driver:
            try:
                if not os.path.exists(Config.snap_path):
                    os.makedirs(Config.snap_path)
                png_file = os.path.join(Config.snap_path, f"{item.name}_fail.png")
                logger.error(f'用例执行失败: {png_file}')
                driver.save_screenshot(png_file)
                allure.attach.file(png_file, f'{item.name}失败截图', allure.attachment_type.PNG)
            except Exception as e:
                logger.error(f'保存失败截图时出错: {e}')


@pytest.fixture(autouse=True, scope="session")
def disable_proxy():
    # 备份当前的代理设置
    original_proxies = {key: os.environ.get(key) for key in ['http_proxy', 'https_proxy', 'all_proxy']}
    # 清除代理设置
    for key in original_proxies:
        os.environ.pop(key, None)
    yield
    # 恢复原始的代理设置
    for key, value in original_proxies.items():
        if value is not None:
            os.environ[key] = value
