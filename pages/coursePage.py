#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/31 13:43
@Author  : Poco Ray
@File    : coursePage.py
@Software: PyCharm
@Desc    : Description
"""
from appium.webdriver.common.appiumby import AppiumBy
from pages.basePage import BasePage


class CoursePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_score(self):
        self.click((AppiumBy.XPATH,'(//android.widget.TextView[@text="评价"])[2]'))
        ele_score = (AppiumBy.ID, 'cn.com.open.mooc:id/tv_score')
        score = self.find_element(ele_score).text
        return float(score)
