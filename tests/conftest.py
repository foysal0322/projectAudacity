import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
from datetime import datetime

def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome', help='Browser to use: chrome, firefox, edge')
    parser.addoption('--headless', action='store_true', default=False, help='Run browser in headless mode')
    parser.addoption('--mobile', action='store_true', default=False, help='Emulate mobile device')

@pytest.fixture(scope="session")
def driver(request):
    browser = request.config.getoption('--browser').lower()
    headless = request.config.getoption('--headless')
    mobile = request.config.getoption('--mobile')
    driver = None
    if browser == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        if mobile:
            mobile_emulation = {"deviceName": "Pixel 2"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        if mobile:
            options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1")
        driver = webdriver.Firefox(options=options)
    elif browser == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        if mobile:
            # Edge does not support mobile emulation directly, fallback to user-agent
            options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1")
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
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
