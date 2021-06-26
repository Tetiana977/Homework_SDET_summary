from typing import Callable, Any

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

driver = ...

wait = WebDriverWait(
    driver,
    4,
    poll_frequency=0.1,
    ignored_exceptions=(WebDriverException,)
)


class empty_value_in_element:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, driver):
        return driver.find_element(self.selector).get_attribute('value') == ''


class element_exact_text():

    def __init__(self, selector, value):
        self.selector = selector
        self.value = value

    def __call__(self, driver):
        return driver.find_element(self.selector).text == self.value


class element_attribute:

    def __init__(self, selector, name, value):
        self.selector = selector
        self.value = value
        self.name = name

    def __call__(self, driver):
        return driver.find_element(self.selector)\
                   .get_attribute(self.name) == self.value


class element_command_passed():
    def __init__(self, selector, command: Callable[[WebElement], Any]):
        self.selector = selector
        self.command = command

    def __call__(self, driver):
        return self.command(driver.find_element(self.selector))


class Element:
    def __init__(self, selector):
        self.selector = selector

    def should_be_blank(self):
        return self.should_have_exact_text('')\
            .should_have_attribute('value', '')

    def should_have_exact_text(self, value):
        wait.until(element_exact_text(self.selector, value))
        return self

    def should_have_attribute(self, name, value):
        wait.until(element_attribute(self.selector, name, value))
        return self

    def set_value(self):
        def clear_and_send_keys(webelement):
            webelement.clear()
            webelement.send_keys()

        wait.until(element_command_passed(self.selector, clear_and_send_keys))
        return self

    def clear(self):
        wait.until(element_command_passed(
            self.selector,
            lambda webelement: webelement.clear()
            )
        )
        return self

    def type(self):
        wait.until(element_command_passed(
            self.selector,
            lambda webelement: webelement.send_keys()
            )
        )
        return self
