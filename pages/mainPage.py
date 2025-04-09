#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/30 22:25
@Author  : Poco Ray
@File    : mainPage.py
@Software: PyCharm
@Desc    : 首页
"""
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from pages.basePage import BasePage


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def to_course(self, course: WebElement):
        """
        跳转到课程页面对象
        :param course: 课程相关的元素对象
        :return:
        """
        self.click(course)
        from pages.coursePage import CoursePage
        course_page = CoursePage(self.driver)
        return course_page

    def close_ad(self):
        """
        关闭广告
        :return:
        """
        try:
            ad_ele = (AppiumBy.ID, 'cn.com.open.mooc:id/ivCancel')
            if self.is_clickable(ad_ele):
                self.click(ad_ele)
        except Exception as e:
            print(f"广告关闭失败: {e}")

    def search(self, text: str):
        """
        搜索课程
        :param text: 课程名称
        :return:
        """
        search_ele = (AppiumBy.ID, 'cn.com.open.mooc:id/tvKeywords')
        search_input = (AppiumBy.ID, 'cn.com.open.mooc:id/etSearchKey')
        search_btn = (AppiumBy.ID, 'cn.com.open.mooc:id/ivSearchIcon')

        self.click(search_ele)
        self.type(search_input, text)
        self.click(search_btn)
