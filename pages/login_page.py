import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # Locators moved from LoginLocators
    EMAIL_INPUT = (By.XPATH, "//input[@name='email' or @id='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password' or @id='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    SIGN_IN_BUTTON = (By.XPATH, "//a[contains(text(),'Sign In')]")
    SIGN_IN_BUTTON_2 = (By.XPATH, '//button[@type="submit"]')
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'toaster') and contains(@class,'bg-white')]")
    REGISTRATION_LINK = (By.ID, 'registration')
    FORGOT_PASSWORD_LINK = (By.ID, 'forgot-password')
    FEEDBACK_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Write Comment...']")
    FEEDBACK_SUBMIT = (By.XPATH, "//button[contains(text(), 'Submit')]")
    FEEDBACK_LIST = (By.ID, 'scrollableDiv')
    SIGN_IN_POPUP_CLS_BTN = (By.XPATH, "//*[contains(@class,'ring-offset-background') and @data-slot='dialog-close']")
    SIGN_IN_POPUP = (By.XPATH, '//*[@role="dialog"]')

    def go_to(self, url):
        self.driver.get(url)

    def login(self, email, password):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        # Scroll to the bottom of the page before clicking LOGIN_BUTTON
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        # Scroll to LOGIN_BUTTON before clicking (robust for headless)
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", login_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()

    def sign_in(self, email, password):

        self.driver.find_element(*self.SIGN_IN_BUTTON).click()
        time.sleep(3)
        # Scroll to the bottom of the page before proceeding
        handles = self.driver.window_handles  # get all open window handles
        self.driver.switch_to.window(handles[1])  # switch to the first window
        # Wait for the email input to be present to ensure the page is loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        # Scroll to the bottom of the page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        # Scroll to SIGN_IN_BUTTON_2 before clicking
        self.driver.find_element(*self.SIGN_IN_BUTTON_2).click()
        self.driver.switch_to.window(handles[0])


    def get_error_message(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return self.driver.find_element(*self.ERROR_MESSAGE).text
        except NoSuchElementException:
            return None

    def go_to_registration(self):
        self.driver.find_element(*self.REGISTRATION_LINK).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('/registration'))

    def go_to_forgot_password(self):
        self.driver.find_element(*self.FORGOT_PASSWORD_LINK).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains('/forgot-password'))

    def is_field_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_password_masked(self):
        try:
            password_input = self.driver.find_element(*self.PASSWORD_INPUT)
            return password_input.get_attribute('type') == 'password'
        except NoSuchElementException:
            return False

    def is_password_autocomplete_off(self):
        try:
            password_input = self.driver.find_element(*self.PASSWORD_INPUT)
            return password_input.get_attribute('autocomplete') == 'off'
        except NoSuchElementException:
            return False

    def leave_feedback(self, feedback_text):
        textarea = self.driver.find_element(*self.FEEDBACK_TEXTAREA)
        textarea.clear()
        textarea.send_keys(feedback_text)
        self.driver.find_element(*self.FEEDBACK_SUBMIT).click()

    def feedback_in_list(self, feedback_text):
        feedbacks = self.driver.find_elements(*self.FEEDBACK_LIST)
        return any(feedback_text in fb.text for fb in feedbacks)
