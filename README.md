# Project Audacity: Automated Web Testing Suite

## Project Overview
Project Audacity is an automated web testing suite built with Python, Selenium, and Pytest. It is designed to test critical functionalities of the demo site https://practice.qabrains.com/, including form submission, drag-and-drop, and e-commerce workflows. The suite provides robust logging, reporting, and accessibility checks to ensure high-quality web application releases.

## Features
- Automated UI tests for login, form submission, drag-and-drop, and e-commerce flows
- Robust failure logging: screenshots, browser console logs, and error details saved per test
- Pytest-based test organization with custom markers for selective test runs
- HTML and console test reports
- Easy extensibility for new test cases and page objects

## Prerequisites
- Python 3.8 or higher
- Google Chrome browser (latest recommended)
- ChromeDriver (compatible with your Chrome version; see `drivers/` directory)
- Git (optional, for version control)

## Setup Instructions
1. **Clone the repository** (if not already):
   ```bash
   git clone <your-repo-url>
   cd projectAudacity
   ```

2. **Create and activate a virtual environment (.venv):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure ChromeDriver is available:**
   - Place the correct version of `chromedriver` in the `drivers/` directory or ensure it is in your system PATH.
   - Download from: https://chromedriver.chromium.org/downloads

## Running Tests
- **Run all tests:**
  ```bash
  pytest tests/
  ```
- **Run tests with a specific marker (e.g., only e-commerce tests):**
  ```bash
  pytest -m ecommerce
  ```
- **Run a specific test file or function:**
  ```bash
  pytest tests/test_ecommerce.py::test_add_to_cart
  ```

## Generating Reports
- **Console output:** Pytest prints a summary to the terminal by default.
- **HTML report (requires pytest-html):**
  ```bash
  pytest --html=reports/report.html --self-contained-html
  ```
- **Failure logs:**
  - On any test failure, a folder is created in `logs/` with the test name and timestamp.
  - Each folder contains:
    - `screenshot.png`: Screenshot at failure
    - `browser_console.log`: Browser console logs
    - `error.log`: Error details

## GUI Test Runner

A professional, user-friendly GUI test runner is included for easy test execution and management.

### Features
- Select test suites by pytest mark (or run all)
- Choose browser (Chrome, Firefox, Edge, Mobile Chrome, Mobile Safari)
- Toggle headless mode and parallel execution (multi-threaded)
- Specify rerun count for failed tests (requires pytest-rerunfailures)
- Option to generate HTML reports
- Kill switch to stop all running tests
- Real-time terminal output canvas
- All controls are disabled while tests are running for safety

### How to Use
1. **Install PyQt5 and required plugins:**
   ```bash
   pip install PyQt5 pytest-html pytest-xdist pytest-rerunfailures
   ```
2. **Run the GUI:**
   ```bash
   python test_runner_gui.py
   ```
3. **Select your options:**
   - Choose test suite, browser, headless/parallel, rerun count, and report options.
   - Click **Run** to start. Use the **Kill** button to stop tests at any time.
   - The terminal canvas will show real-time output.

### Notes
- For parallel execution, pytest-xdist must be installed.
- For rerun support, pytest-rerunfailures must be installed.
- For HTML reports, pytest-html must be installed.
- All options are available in the GUI for a seamless experience.

## Additional Notes
- **Test Data:** Test credentials and data are hardcoded for demo purposes. Update as needed for your environment.
- **Extending Tests:** Add new test files in `tests/` and new page objects in `pages/`.
- **CI/CD:** See `workflow/ci-cd-pipeline.yml` for example automation pipeline setup.
- **Troubleshooting:**
  - Ensure ChromeDriver matches your Chrome version.
  - Activate the virtual environment before running tests.
  - Check the `logs/` directory for detailed failure diagnostics.

## License
See the `LICENSE` file for license details.

---
For any issues or contributions, please open an issue or pull request on the repository. Or Email me at: `foysal0322@gmail.com`
