import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EcommercePage:
    """Page object model for the e-commerce site, providing methods to interact with and test e-commerce functionality."""
    def __init__(self, driver):
        """Initialize with a Selenium WebDriver instance."""
        self.driver = driver

    # Example locators (update with actual locators after inspecting the site)
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    CART_BUTTON = (By.XPATH, "//span[contains(@class,'bg-qa-clr')]")
    ADD_TO_CART_BUTTON = (By.XPATH, '//*[normalize-space(text())="Add to cart"]')
    FAVORITE_BUTTON = (By.XPATH, '//button[@class=" cursor-pointer"]')
    PRODUCT_LIST = (By.CSS_SELECTOR, '.product-list .product-item')
    SORT_DROPDOWN = (By.XPATH, '//button[@data-slot="popover-trigger"]')
    SELECT_SORT_OPTION = (By.XPATH, "//*[@data-slot='command-item' and normalize-space(text())='Low to High (Price)']")
    PRICE_ELEMENTS = (By.XPATH, "//span[@class='text-lg font-bold text-black']")
    CHECKOUT_BUTTON = (By.XPATH, '//*[text()="Checkout"]')
    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder,'Ex. John')]")
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(@class,'user-name')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.alert-danger, .error-message')

    def click_by_text(self, text):
        """Scroll to and click the element containing the specified text."""
        actions = ActionChains(self.driver)
        element = self.driver.find_element(By.XPATH, f'//*[text()="{text}"]')
        actions.move_to_element(element).perform()
        element.click()

    def check_is_text_visible(self, text):
        """Return True if the specified text is visible on the page, else False."""
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, f'//*[text()="{text}"]')))
            return True
        except:
            return False

    def login(self, email, password):
        """Log in to the e-commerce site with the provided email and password."""
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def add_first_product_to_cart(self):
        """Add the first product in the product list to the cart."""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON))
        add_to_cart_btns = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        ActionChains(self.driver).move_to_element(add_to_cart_btns[0]).perform()
        add_to_cart_btns[0].click()

    def add_first_product_to_favorites(self):
        """Add the first product in the product list to favorites."""
        fav_btns = self.driver.find_elements(*self.FAVORITE_BUTTON)
        ActionChains(self.driver).move_to_element(fav_btns[0]).perform() #scroll to first fav button
        fav_btns[0].click()

    def get_cart_count(self):
        """Return the number of items currently in the cart as an integer."""
        return int(self.driver.find_element(By.XPATH, "//span[contains(@class,'bg-qa-clr')]").text)

    def get_favorites_success_messege(self):
        """Return the success message text after adding a product to favorites."""
        return self.driver.find_element(By.XPATH, "//*[text()='Added to favorites']").text

    def get_favorites_btn_color(self):
        """Return the CSS style attribute of the favorite button (used to check if it's active)."""
        return self.driver.find_element(*self.FAVORITE_BUTTON).get_attribute("style")

    def sort_products(self):
        """Sort products by price from low to high using the sort dropdown."""
        self.driver.find_element(*self.SORT_DROPDOWN).click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.SELECT_SORT_OPTION))
        self.driver.find_element(*self.SELECT_SORT_OPTION).click()
        time.sleep(2)  # Wait for sorting to take effect

    def get_product_prices(self):
        """Return a list of product prices (as floats) currently displayed on the page."""
        prices = self.driver.find_elements(*self.PRICE_ELEMENTS)
        return [float(price.text.replace('$', '').replace(',', '')) for price in prices]

    def proceed_to_checkout(self):
        """Complete the checkout process for the first product in the cart using default data."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CART_BUTTON))
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.driver.find_element(*self.CART_BUTTON).click()
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
        self.driver.find_element(*self.FIRST_NAME).send_keys("Test user")
        self.click_by_text('Continue')
        self.click_by_text('Finish')

    def get_success_message(self):
        """Return True if the success message is visible after login, else False."""
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False
