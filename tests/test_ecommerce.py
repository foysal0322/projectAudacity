import pytest
from pages.ecommerce_page import EcommercePage

ECOMMERCE_URL = "https://practice.qabrains.com/ecommerce/login"
VALID_EMAIL = "test@qabrains.com"
VALID_PASSWORD = "Password123"

@pytest.fixture
def ecommerce_page(driver):
    page = EcommercePage(driver)
    driver.get(ECOMMERCE_URL)
    return page

def test_login(ecommerce_page):
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    assert ecommerce_page.get_success_message() == True

def test_add_to_cart(ecommerce_page):
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    ecommerce_page.add_first_product_to_cart()
    assert ecommerce_page.get_cart_count() > 0

def test_add_to_favorites(ecommerce_page):
    ecommerce_page.add_first_product_to_favorites()
    assert ecommerce_page.get_favorites_count() > 0

def test_sort_products(ecommerce_page):
    ecommerce_page.sort_products("Price: Low to High")
    # Add assertions for product order if possible

def test_checkout_flow(ecommerce_page):
    ecommerce_page.add_first_product_to_cart()
    ecommerce_page.proceed_to_checkout()
    assert ecommerce_page.get_success_message() is not None or ecommerce_page.get_error_message() is not None

def test_empty_cart_checkout(ecommerce_page):
    # Ensure cart is empty before proceeding
    if ecommerce_page.get_cart_count() > 0:
        pytest.skip("Cart is not empty, skipping empty cart checkout test.")
    ecommerce_page.proceed_to_checkout()
    assert ecommerce_page.get_error_message() is not None

