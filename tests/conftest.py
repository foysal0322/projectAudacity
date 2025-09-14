import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver is not None:
            # Prepare log folder and unique subfolder
            logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            test_name = item.name.replace('/', '_').replace('\\', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            subfolder = os.path.join(logs_dir, f"{test_name}_{timestamp}")
            os.makedirs(subfolder, exist_ok=True)
            # Save screenshot
            screenshot_path = os.path.join(subfolder, 'screenshot.png')
            try:
                driver.save_screenshot(screenshot_path)
            except Exception as e:
                with open(os.path.join(subfolder, 'screenshot_error.txt'), 'w') as f:
                    f.write(str(e))
            # Save browser console logs
            try:
                logs = driver.get_log('browser')
                with open(os.path.join(subfolder, 'browser_console.log'), 'w', encoding='utf-8') as f:
                    for entry in logs:
                        f.write(f"{entry['level']}: {entry['message']}\n")
            except Exception as e:
                with open(os.path.join(subfolder, 'browser_console_error.txt'), 'w') as f:
                    f.write(str(e))
            # Save error reason/log
            with open(os.path.join(subfolder, 'error.log'), 'w', encoding='utf-8') as f:
                f.write(str(rep.longrepr))
