from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'toaster') and contains(@class,'bg-white')]")
    REGISTRATION_LINK = (By.ID, 'registration')
    FORGOT_PASSWORD_LINK = (By.ID, 'forgot-password')
    FEEDBACK_TEXTAREA = (By.ID, 'feedback')
    FEEDBACK_SUBMIT = (By.XPATH, "//button[contains(text(), 'Submit')]")
    FEEDBACK_LIST = (By.ID, 'feedback-list')

