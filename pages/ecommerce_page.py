import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EcommercePage:
    def __init__(self, driver):
        self.driver = driver

    # Example locators (update with actual locators after inspecting the site)
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    CART_BUTTON = (By.ID, 'cart-btn')
    ADD_TO_CART_BUTTON = (By.XPATH, '//*[normalize-space(text())="Add to cart"]')
    FAVORITE_BUTTON = (By.CSS_SELECTOR, '.add-to-favorites')
    PRODUCT_LIST = (By.CSS_SELECTOR, '.product-list .product-item')
    SORT_DROPDOWN = (By.ID, 'sort-products')
    CHECKOUT_BUTTON = (By.ID, 'checkout-btn')
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(@class,'user-name')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.alert-danger, .error-message')

    def login(self, email, password):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        # time.sleep(5)

    def add_first_product_to_cart(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON))
        add_to_cart_btns = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        ActionChains(self.driver).move_to_element(add_to_cart_btns[0]).perform()
        add_to_cart_btns[0].click()

    def add_first_product_to_favorites(self):
        self.driver.find_elements(*self.FAVORITE_BUTTON)[0].click()

    def get_cart_count(self):
        return int(self.driver.find_element(By.XPATH, "//span[contains(@class,'bg-qa-clr')]").text)

    def get_favorites_count(self):
        return int(self.driver.find_element(By.ID, 'favorites-count').text)

    def sort_products(self, sort_option):
        dropdown = self.driver.find_element(*self.SORT_DROPDOWN)
        dropdown.click()
        dropdown.find_element(By.XPATH, f".//option[text()='{sort_option}']").click()

    def proceed_to_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()

    def get_success_message(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return self.driver.find_element(*self.SUCCESS_MESSAGE).is_displayed()
        except:
            return None

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).text
        except:
            return None

