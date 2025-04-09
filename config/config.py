#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/28 21:32
@Author  : Poco Ray
@File    : config.py
@Software: PyCharm
@Desc    : Description
"""
import os
from utils import baseUtil


class Config:
    appium_server_url = 'http://localhost:4723'
    common_capabilities = {
        'platformName': 'Android',
        'appium:automationName': 'uiautomator2',
        'appium:deviceName': 'V2284A',
        'appium:udid': 'emulator-5554',
        # 'appium:autoGrantPermissions': True,  # 自动授予权限
    }

    _mda = {
        'appium:appPackage': 'com.saucelabs.mydemoapp.android',
        'appium:appActivity': '.view.activities.MainActivity',
        'appium:appWaitActivity': '.view.activities.MainActivity',
        'appium:app': os.path.abspath(os.path.join(os.path.dirname(__file__), '../files/apk/mda-2.0.1-22.apk')),
    }
    mda_capabilities = {**common_capabilities, **_mda}

    _api_demo = {
        'appium:appPackage': 'io.appium.android.apis',
        'appium:appActivity': '.ApiDemos',
        'chromedriverExecutable': os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../files/driver/chromedriver')),
        # 'chromedriverExecutableDir': chromedriverExecutableDir,
        'appium:app': os.path.abspath(os.path.join(os.path.dirname(__file__), '../files/apk/ApiDemos-debug.apk')),
    }
    api_demo_capabilities = {**common_capabilities, **_api_demo}

    _settings = {
        'appium:appPackage': 'com.android.settings',
        'appium:appActivity': '.Settings',
    }
    settings_capabilities = {**common_capabilities, **_settings}

    _imooc = {
        'appPackage': 'cn.com.open.mooc',
        'appActivity': 'com.imooc.component.imoocmain.index.MCMainActivity',
        'app': os.path.abspath(os.path.join(os.path.dirname(__file__), '../files/apk/imooc.apk')),
        'noReset': True,  # 启动时不重置应用程序状态
        'shouldTerminateApp': True,  # 结束后自动关闭App
        'forceAppLaunch': True,  # 强制启动应用
    }
    mooc_capabilities = {**common_capabilities, **_imooc}

    root_dir = baseUtil.get_root_dir()
    log_path = os.path.join(root_dir, 'logs')
    snap_path = os.path.join(root_dir, 'snapshots')
    report_path = os.path.join(root_dir, 'report')
    allure_results = os.path.join(root_dir, 'report', 'allure_results')
    allure_reports = os.path.join(root_dir, 'report', 'allure_reports')
