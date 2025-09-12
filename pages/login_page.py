import time

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
        # Scroll to the bottom of the page before clicking LOGIN_BUTTON
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        # Scroll to LOGIN_BUTTON before clicking (robust for headless)
        login_button = self.driver.find_element(*LoginLocators.LOGIN_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", login_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON))
        login_button.click()

    def sign_in(self, email, password):

        self.driver.find_element(*LoginLocators.SIGN_IN_BUTTON).click()
        time.sleep(3)
        # Scroll to the bottom of the page before proceeding
        handles = self.driver.window_handles  # get all open window handles
        self.driver.switch_to.window(handles[1])  # switch to the first window
        # Wait for the email input to be present to ensure the page is loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(LoginLocators.EMAIL_INPUT)
        )
        # Scroll to the bottom of the page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(*LoginLocators.EMAIL_INPUT).clear()
        self.driver.find_element(*LoginLocators.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*LoginLocators.PASSWORD_INPUT).clear()
        self.driver.find_element(*LoginLocators.PASSWORD_INPUT).send_keys(password)
        # Scroll to SIGN_IN_BUTTON_2 before clicking
        self.driver.find_element(*LoginLocators.SIGN_IN_BUTTON_2).click()
        self.driver.switch_to.window(handles[0])


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
        password_field.send_keys('test-pass123')
        self.driver.refresh()
        time.sleep(5)
        if password_field.get_attribute('value') == '':
            return True
        else:
            return False

    def leave_feedback(self, feedback_text):
        self.sign_in('test_user@user.com', 'Testpass@123')
        time.sleep(3)
        self.driver.refresh()
        self.driver.find_element(*LoginLocators.FEEDBACK_TEXTAREA).clear()
        self.driver.find_element(*LoginLocators.FEEDBACK_TEXTAREA).send_keys(feedback_text)
        self.driver.find_element(*LoginLocators.FEEDBACK_SUBMIT).click()

    def feedback_in_list(self, feedback_text):
        # Wait for FEEDBACK_TEXTAREA to be visible
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(LoginLocators.FEEDBACK_TEXTAREA))
        feedback_textarea = self.driver.find_element(*LoginLocators.FEEDBACK_TEXTAREA)
        feedback_textarea.clear()
        feedback_textarea.send_keys(feedback_text)
        # Wait for FEEDBACK_SUBMIT to be clickable
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(LoginLocators.FEEDBACK_SUBMIT))
        feedback_submit = self.driver.find_element(*LoginLocators.FEEDBACK_SUBMIT)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", feedback_submit)
        feedback_submit.click()
