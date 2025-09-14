import pytest
from pages.login_page import LoginPage
from locators.login_locators import LoginLocators

URL = "https://practice.qabrains.com/"
VALID_EMAIL = "qa_testers@qabrains.com"
VALID_PASSWORD = "Password123"
INVALID_EMAIL = "invalid@qabrains.com"
INVALID_PASSWORD = "WrongPass"

@pytest.mark.login
@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and provide a Selenium WebDriver instance for login tests."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.login
@pytest.fixture
def login_page(driver):
    """Fixture to provide a LoginPage object and navigate to the login URL."""
    page = LoginPage(driver)
    page.go_to(URL)
    return page

@pytest.mark.login
@pytest.mark.positive
def test_successful_login(login_page):
    """Test successful login with valid credentials."""
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    assert login_page.get_error_message() == "Login Successful"

@pytest.mark.login
@pytest.mark.negative
def test_negative_login(login_page):
    """Test login with invalid credentials and expect failure message."""
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    assert login_page.get_error_message() ==  "Your email and password both are invalid!"


@pytest.mark.login
def test_navigation_to_registration(login_page):
    """Test navigation to the registration page from the login page."""
    login_page.go_to_registration()
    assert "registration" in login_page.driver.current_url.lower()


@pytest.mark.login
def test_navigation_to_forgot_password(login_page):
    """Test navigation to the forgot password page from the login page."""
    login_page.go_to_forgot_password()
    assert "forgot-password" in login_page.driver.current_url.lower()


@pytest.mark.login
def test_fields_and_buttons_present(login_page):
    """Test that all necessary fields and buttons are present on the login page."""
    assert login_page.is_field_present(LoginLocators.EMAIL_INPUT)
    assert login_page.is_field_present(LoginLocators.PASSWORD_INPUT)
    assert login_page.is_field_present(LoginLocators.LOGIN_BUTTON)
    assert login_page.is_field_present(LoginLocators.REGISTRATION_LINK)
    assert login_page.is_field_present(LoginLocators.FORGOT_PASSWORD_LINK)

@pytest.mark.login
def test_password_field_masking_and_autocomplete(login_page):
    """Test that the password field is masked and autocomplete is turned off."""
    assert login_page.is_password_masked() == True
    assert login_page.is_password_autocomplete_off() == True

@pytest.mark.login
def test_leave_feedback(login_page):
    """Test leaving feedback through the login page."""
    feedback_text = "Automated feedback test"
    login_page.leave_feedback(feedback_text)
    assert login_page.feedback_in_list(feedback_text)
