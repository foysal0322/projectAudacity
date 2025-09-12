import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pages.form_page import FormPage

FORM_URL = "https://practice.qabrains.com/form-submission"

@pytest.fixture
def form_page(driver):
    page = FormPage(driver)
    driver.get(FORM_URL)
    return page

def test_successful_form_submission(form_page):
    form_page.fill_form("Test User", "testuser@example.com", "01711223344")
    assert form_page.get_success_message() == "SUCCESSFULLY SUBMITTED"

def test_form_validation_missing_fields(form_page):
    form_page.fill_form("", "testuser@example.com", "01711223344")
    assert form_page.get_missing_error_message() == "Name is a required field"

def test_form_validation_invaid_email(form_page):
    form_page.fill_form("test user", "", "01711223344")
    form_page.fill_form("test user", "invalidEmail", "01711223344")
    assert form_page.is_invalid_error_message_visible() == True



def test_form_labels_accessible(form_page):
    # Check that each field has a label and it's correct (update expected labels as needed)
    assert form_page.get_label_text('name') == 'Name'
    assert form_page.get_label_text('email') == 'Email'
    assert form_page.get_label_text('contact') == 'Contact Number'
    assert form_page.get_label_text('date') == 'Dat'
    assert form_page.get_label_text('color') == 'Select any color from the following colors'
    assert form_page.get_label_text('food') == 'Select any food from the menu'
    assert form_page.get_label_text('country') == 'Select Country'
