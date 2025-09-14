import pytest
from pages.ecommerce_page import EcommercePage

ECOMMERCE_URL = "https://practice.qabrains.com/ecommerce/login"
VALID_EMAIL = "test@qabrains.com"
VALID_PASSWORD = "Password123"

@pytest.mark.ecommerce
@pytest.fixture
def ecommerce_page(driver):
    """Fixture to provide an EcommercePage object and navigate to the e-commerce login URL."""
    page = EcommercePage(driver)
    driver.get(ECOMMERCE_URL)
    return page

@pytest.mark.ecommerce
@pytest.mark.positive
def test_login(ecommerce_page):
    """Test login functionality on the e-commerce site with valid credentials."""
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    assert ecommerce_page.get_success_message() == True
    ecommerce_page.logout()

@pytest.mark.ecommerce
@pytest.mark.positive
def test_add_to_cart(ecommerce_page):
    """Test adding a product to the cart and verify the cart updates correctly."""
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    ecommerce_page.add_first_product_to_cart()
    assert ecommerce_page.get_cart_count() > 0
    ecommerce_page.logout()


@pytest.mark.ecommerce
@pytest.mark.positive
def test_add_to_favorites(ecommerce_page):
    """Test adding a product to favorites and verify its presence in the favorites list."""
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    ecommerce_page.add_first_product_to_favorites()
    assert ecommerce_page.get_favorites_btn_color() == "color: rgb(255, 0, 0);"
    assert ecommerce_page.get_favorites_success_messege() == "Added to favorites"
    ecommerce_page.logout()

@pytest.mark.ecommerce
@pytest.mark.positive
def test_sort_products(ecommerce_page):
    """Test sorting products by price and verify the correct order."""
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    ecommerce_page.sort_products()
    assert ecommerce_page.get_product_prices() == sorted(ecommerce_page.get_product_prices())
    ecommerce_page.logout()

@pytest.mark.ecommerce
@pytest.mark.positive
def test_checkout_flow(ecommerce_page):
    """Test the complete checkout flow and assert success message on completion."""
    ecommerce_page.login(VALID_EMAIL, VALID_PASSWORD)
    ecommerce_page.add_first_product_to_cart()
    ecommerce_page.proceed_to_checkout()
    assert ecommerce_page.check_is_text_visible('Checkout: Complete!') == True
    ecommerce_page.logout()
