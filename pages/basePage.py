#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/3/29 17:38
@Author  : Poco Ray
@File    : basePage.py
@Software: PyCharm
@Desc    : Description
"""
from datetime import datetime
from typing import Union, Tuple, Type
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 元素定位器类型
Locator: Type[tuple] = Tuple[str, str]


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, locator: Locator) -> WebElement:
        """
        查找单个元素

        :param locator: 元素定位器, e.g. (AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素名称")')
        :return:
        :Usage:
            # 1. 直接传参
            self.find_element((AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素名称")'))

            # 2. 通过locator对象传参
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素名称")')
            self.find_element(locator)
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def _get_element(self, target_obj: Union[WebElement, Locator]) -> WebElement:
        """
        获取元素对象.
        :param target_obj: 元素对象或定位器
        :return: WebElement对象
        """
        if isinstance(target_obj, WebElement):
            return target_obj
        if isinstance(target_obj, tuple) and len(target_obj) == 2:
            return self.find_element(target_obj)
        raise ValueError("Invalid element type or locator format.")

    def _take_error_screenshot(self, info: str) -> None:
        """
        截图并保存到当前目录下，文件名为info_时间戳.png
        :param info: 截图信息
        :return:
        """
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # self.driver.save_screenshot(f"{info}_{timestamp}.png")
        pass

    def is_clickable(self, ele_obj: Union[WebElement, Locator]) -> bool:
        """
        判断元素是否可点击
        :param ele_obj: 元素对象或定位器
        :return:
        """
        try:
            element = self._get_element(ele_obj)
            self.wait.until(EC.element_to_be_clickable(element))
            return True
        except TimeoutException:
            return False

    def is_visible(self, ele_obj: Union[WebElement, Locator]) -> bool:
        """
        判断元素是否可见
        :param ele_obj: 元素对象或定位器
        :return:
        """
        try:
            element = self._get_element(ele_obj)
            self.wait.until(EC.visibility_of(element))
            return True
        except TimeoutException:
            return False

    def click(self, click_obj: Union[WebElement, Locator]) -> None:
        """
        点击元素.
        :param click_obj: 元素对象或定位器
        :return: None
        :Usage:
            # 1. 通过元素对象点击
            ele = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素名称")')
            self.click(ele)

            # 2. 通过定位器点击
            self.click(AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素名称")')
        """
        try:
            if self.is_clickable(click_obj):
                element: WebElement = self._get_element(click_obj)
                element.click()
            else:
                raise RuntimeError(f"Element {click_obj} is not clickable.")
        except Exception as e:
            self._take_error_screenshot("click_error")
            print(f"Error clicking element: {e}")

    def click_by_text(self, text: str) -> None:
        """
        通过文本点击元素.
        :param text: 元素文本
        :return: None
        :Usage:
            # 1. 点击文本为"元素名称"的元素
            self.click_by_text("元素名称")
        """
        locator: Locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'text("{text}")')
        self.click(locator)

    def type(self, input_obj: Union[WebElement, Locator], text: str) -> None:
        """
        输入文本.
        :param input_obj: 元素对象或定位器
        :param text: 输入的文本
        :return:
        :Usage:
            # 1. 通过元素对象输入
            ele = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("输入框名称")')
            self.type(ele, "输入内容")

            # 2. 通过定位器输入
            self.type(AppiumBy.ANDROID_UIAUTOMATOR, 'text("输入框名称")', "输入内容")
        """
        try:
            element = self._get_element(input_obj)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self._take_error_screenshot("input_error")
            print(f"Error typing in element: {e}")

    def find_elements(self, locator: Locator) -> list[WebElement]:
        """
        查找多个元素.
        :param locator: 元素定位器, e.g. (AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素名称")')
        :return:
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def swipe(
            self,
            kind: int,
            start_obj: Union[tuple, WebElement],
            end_obj: Union[tuple, WebElement],
            duration: int = 250
    ) -> None:
        """
        在屏幕上执行滑动操作
        :param kind: 滑动类型(1: 坐标滑动, 2: 屏幕百分比滑动, 3: 元素滑动)
        :param start_obj: 起始点对象
        :param end_obj: 结束点对象
        :param duration: 滑动持续时间(毫秒), 默认250ms
        :return:
        :Usage:
            # 1. 从坐标(100, 600)滑动到(100, 100)，持续时间为1000ms
            self.swipe(kind=1, start_obj=(100, 600), end_obj=(100, 100), duration=1000)

            # 2. 从屏幕的底部中间滑动到顶部中间，持续时间为1000ms
            self.swipe(kind=2, start_obj=(0.5, 1), end_obj=(0.5, 0), duration=1000)

            # 3. 从元素A滑动到元素B，持续时间为1000ms
            ele_a = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素A")')
            ele_b = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("元素B")')
            self.swipe(kind=3, start_obj=ele_a, end_obj=ele_b, duration=1000)
        """
        if kind == 1:
            start_point, end_point = start_obj, end_obj
        elif kind == 2:
            size = self.driver.get_window_size()
            start_x, start_y = int(size['width'] * start_obj[0]), int(size['height'] * start_obj[1])
            end_x, end_y = int(size['width'] * end_obj[0]), int(size['height'] * end_obj[1])
            start_point, end_point = (start_x, start_y), (end_x, end_y)
        elif kind == 3:
            def get_element_center(element):
                if isinstance(element, WebElement):
                    center_x = int(element.rect['x'] + element.rect['width'] / 2)
                    center_y = int(element.rect['y'] + element.rect['height'] / 2)
                    return center_x, center_y
                else:
                    raise TypeError("Element must be a WebElement instance.")

            start_point, end_point = get_element_center(start_obj), get_element_center(end_obj)
        else:
            raise ValueError("Invalid swipe kind.")

        self.driver.swipe(*start_point, *end_point, duration)

    def handle_alert(self, accept: bool = True, timeout: int = 3) -> bool:
        """
        尝试处理可能出现的Alert弹框 (优先使用Alert API)
        :param accept: True表示接受(accept), False表示拒绝(dismiss)
        :param timeout: 等待弹框出现的最长时间
        :return: True 如果成功处理了弹框, False 如果未找到弹框
        :Usage:
            # 1. 接受弹框
            self.handle_alert()

            # 2. 拒绝弹框
            self.handle_alert(accept=False)
        """
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            print(f"Alert pop-up detected: {alert.text}")
            if accept:
                alert.accept()
                print("Alert pop-up accepted.")
            else:
                alert.dismiss()
                print("Alert pop-up dismissed.")
            return True
        except TimeoutException:
            print(f"No Alert pop-up detected within {timeout} seconds.")
            return False
        except NoAlertPresentException:  # 理论上WebDriverWait会先超时，但以防万一
            print("No Alert pop-up found.")
            return False
