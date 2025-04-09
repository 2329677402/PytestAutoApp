#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/28 23:23
@Author  : Poco Ray
@File    : test_imooc.py
@Software: PyCharm
@Desc    : Description
"""
import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.mainPage import MainPage


@pytest.mark.parametrize('course_name', ["软件测试基础-概念篇"])
@allure.epic("慕课网App")
@allure.story("Appium自动化测试")
class TestImooc:
    @allure.feature("课程搜索")
    def test_imooc01(self, driver, course_name):
        main_page = MainPage(driver)
        main_page.close_ad()
        main_page.click_by_text("免费课")
        main_page.click_by_text("全部")
        main_page.click_by_text("运维&测试")
        main_page.click_by_text("全部")
        main_page.click_by_text("最热")
        assert main_page.is_visible((AppiumBy.ANDROID_UIAUTOMATOR, f'text("{course_name}")'))

    @allure.feature("课程评分")
    def test_imooc02(self, driver, course_name):
        # 回到首页
        driver.execute_script('mobile:startActivity', {
            'intent': 'cn.com.open.mooc/com.imooc.component.imoocmain.index.MCMainActivity',
        })
        main_page = MainPage(driver)
        main_page.close_ad()
        main_page.search('概念篇')
        course_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'text("{course_name}")')
        assert main_page.is_visible(course_locator)

        course_page = main_page.to_course(main_page.find_element(course_locator))
        course_page.click_by_text(course_name)
        assert course_page.get_score() > 9.9
