import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FormPage:
    def __init__(self, driver):
        self.driver = driver


    NAME_INPUT = (By.ID, 'name')
    EMAIL_INPUT = (By.ID, 'email')
    CONTACT_NO = (By.ID, 'contact')
    UPLOAD_FILE = (By.ID, 'file')
    SELECT_RED = (By.ID, 'Red')
    SELECT_PASTA = (By.ID, 'Pasta')
    SELECT_COUNTRY = (By.ID, 'country')
    SELECT_BANGLADESH = (By.XPATH, '//*[@value="Bangladesh"]')
    SUBMIT_BTN = (By.XPATH, '//button[@data-slot="button"]')

    SUCCESS_MESSAGE = (By.XPATH, "//h2[normalize-space(text())='successfully submitted']")
    MISSING_ERROR_MESSAGE = (By.XPATH, "//*[contains(@class,'text-red-500') and normalize-space(text())='Name is a required field']")
    INVALID_ERROR_MESSAGE = (By.XPATH, "//*[contains(@class,'text-red-500') and normalize-space(text())='Email must be a valid email']")

    def fill_form(self, name, email, contact_no):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.NAME_INPUT))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        name_input = self.driver.find_element(*self.NAME_INPUT)
        name_input.clear()
        name_input.send_keys(name)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input = self.driver.find_element(*self.EMAIL_INPUT)
        email_input.clear()
        email_input.send_keys(email)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.CONTACT_NO))
        contact_input = self.driver.find_element(*self.CONTACT_NO)
        contact_input.clear()
        contact_input.send_keys(contact_no)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.UPLOAD_FILE))
        self.driver.find_element(*self.UPLOAD_FILE).send_keys("C:/Users/Toufik/OneDrive/Desktop/images.png")

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SELECT_RED))
        self.driver.find_element(*self.SELECT_RED).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SELECT_PASTA))
        self.driver.find_element(*self.SELECT_PASTA).click()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SELECT_COUNTRY))
        self.driver.find_element(*self.SELECT_COUNTRY).click()
        time.sleep(1)
        self.driver.find_element(*self.SELECT_BANGLADESH).click()
        self.driver.find_element(*self.SUBMIT_BTN).click()



    def get_success_message(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return self.driver.find_element(*self.SUCCESS_MESSAGE).text
        except:
            return None

    def get_missing_error_message(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.MISSING_ERROR_MESSAGE))
            return self.driver.find_element(*self.MISSING_ERROR_MESSAGE).text
        except:
            return None

    def is_invalid_error_message_visible(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.INVALID_ERROR_MESSAGE))
            return self.driver.find_element(*self.INVALID_ERROR_MESSAGE).is_displayed()
        except:
            return None
    def get_label_text(self, for_id):
        try:
            label = self.driver.find_element(By.XPATH, f'//label[@for="{for_id}"]')
            return label.text[:-1]
        except:
            return None
