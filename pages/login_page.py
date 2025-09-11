from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from locators.login_locators import LoginLocators
from .base_page import BasePage

class LoginPage(BasePage):
    def go_to(self, url):
        self.driver.get(url)

    def login(self, email, password):
        self.driver.find_element(*LoginLocators.EMAIL_INPUT).clear()
        self.driver.find_element(*LoginLocators.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*LoginLocators.PASSWORD_INPUT).clear()
        self.driver.find_element(*LoginLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginLocators.LOGIN_BUTTON).click()

    def get_error_message(self):
        try:
            return self.driver.find_element(*LoginLocators.ERROR_MESSAGE).text
        except NoSuchElementException:
            return None

    def go_to_registration(self):
        self.driver.find_element(*LoginLocators.REGISTRATION_LINK).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('/registration'))

    def go_to_forgot_password(self):
        self.driver.find_element(*LoginLocators.FORGOT_PASSWORD_LINK).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('/forgot-password'))

    def is_field_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_password_masked(self):
        password_field = self.driver.find_element(*LoginLocators.PASSWORD_INPUT)
        return password_field.get_attribute('type') == 'password'

    def is_password_autocomplete_off(self):
        password_field = self.driver.find_element(*LoginLocators.PASSWORD_INPUT)
        return password_field.get_attribute('autocomplete') in ['off', 'new-password']

    def leave_feedback(self, feedback_text):
        self.driver.find_element(*LoginLocators.FEEDBACK_TEXTAREA).clear()
        self.driver.find_element(*LoginLocators.FEEDBACK_TEXTAREA).send_keys(feedback_text)
        self.driver.find_element(*LoginLocators.FEEDBACK_SUBMIT).click()

    def feedback_in_list(self, feedback_text):
        feedback_list = self.driver.find_element(*LoginLocators.FEEDBACK_LIST)
        return feedback_text in feedback_list.text
