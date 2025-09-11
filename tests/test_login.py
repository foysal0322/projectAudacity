import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from locators.login_locators import LoginLocators

URL = "https://practice.qabrains.com/"
VALID_EMAIL = "qa_testers@qabrains.com"
VALID_PASSWORD = "Password123"
INVALID_EMAIL = "invalid@qabrains.com"
INVALID_PASSWORD = "WrongPass"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--start-fullscreen')
    driver = webdriver.Chrome(options=options)
    # driver.fullscreen_window()
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.go_to(URL)
    return page

def test_successful_login(login_page):
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    # Assert login success by checking absence of error or presence of a dashboard element
    assert login_page.get_error_message() == "Login Successful"

def test_negative_login(login_page):
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    assert login_page.get_error_message() ==  "Your email and password both are invalid!"


def test_navigation_to_registration(login_page):
    login_page.go_to_registration()
    assert "register" in login_page.driver.current_url.lower()
    login_page.go_to(URL)  # Return to login for next tests

def test_navigation_to_forgot_password(login_page):
    login_page.go_to_forgot_password()
    assert "forgot" in login_page.driver.current_url.lower()
    login_page.go_to(URL)

def test_fields_and_buttons_present(login_page):
    assert login_page.is_field_present(LoginLocators.EMAIL_INPUT)
    assert login_page.is_field_present(LoginLocators.PASSWORD_INPUT)
    assert login_page.is_field_present(LoginLocators.LOGIN_BUTTON)
    assert login_page.is_field_present(LoginLocators.REGISTRATION_LINK)
    assert login_page.is_field_present(LoginLocators.FORGOT_PASSWORD_LINK)

def test_password_field_masking_and_autocomplete(login_page):
    assert login_page.is_password_masked()
    assert login_page.is_password_autocomplete_off()

def test_leave_feedback(login_page):
    feedback_text = "Automated feedback test"
    login_page.leave_feedback(feedback_text)
    assert login_page.feedback_in_list(feedback_text)
