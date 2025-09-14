import pytest
from pages.form_page import FormPage

FORM_URL = "https://practice.qabrains.com/form-submission"

@pytest.mark.form
@pytest.fixture
def form_page(driver):
    """Fixture to provide a FormPage object and navigate to the form submission URL."""
    page = FormPage(driver)
    driver.get(FORM_URL)
    return page

@pytest.mark.form
@pytest.mark.positive
def test_successful_form_submission(form_page):
    """Test form submission with valid data and expect a success message."""
    form_page.fill_form("Test User", "testuser@example.com", "01711223344")
    assert form_page.get_success_message() == "SUCCESSFULLY SUBMITTED"

@pytest.mark.form
@pytest.mark.negative
def test_form_validation_missing_fields(form_page):
    """Test form validation when required fields are missing (name field left blank)."""
    form_page.fill_form("", "testuser@example.com", "01711223344")
    assert form_page.get_missing_error_message() == "Name is a required field"

@pytest.mark.form
@pytest.mark.negative
def test_form_validation_invaid_email(form_page):
    """Test form validation with invalid email input."""
    form_page.fill_form("test user", "", "01711223344")
    form_page.fill_form("test user", "invalidEmail", "01711223344")
    assert form_page.is_invalid_error_message_visible() == True

@pytest.mark.form
@pytest.mark.accessibility
def test_form_labels_accessible(form_page):
    """Test that all form fields have correct and accessible labels."""
    assert form_page.get_label_text('name') == 'Name'
    assert form_page.get_label_text('email') == 'Email'
    assert form_page.get_label_text('contact') == 'Contact Number'
    assert form_page.get_label_text('date') == 'Dat'
    assert form_page.get_label_text('color') == 'Select any color from the following colors'
    assert form_page.get_label_text('food') == 'Select any food from the menu'
    assert form_page.get_label_text('country') == 'Select Country'
