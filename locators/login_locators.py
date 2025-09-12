from selenium.webdriver.common.by import By

class LoginLocators:
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

