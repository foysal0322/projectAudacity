from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DragDropPage:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    # Example locators (update with actual locators after inspecting the site)
    LIST_ITEMS = (By.CSS_SELECTOR, '.draggable-list .draggable-item')
    # If there is a handle for dragging, update this locator
    DRAG_HANDLE = (By.CSS_SELECTOR, '.draggable-list .drag-handle')

    def get_items_text(self):
        items = self.driver.find_elements(*self.LIST_ITEMS)
        return [item.text for item in items]

    def drag_and_drop(self, source_index, target_index):
        items = self.driver.find_elements(*self.LIST_ITEMS)
        source = items[source_index]
        target = items[target_index]
        self.actions.click_and_hold(source).move_to_element(target).release().perform()

    def is_accessible(self):
        # Example: check for aria attributes or tabIndex
        items = self.driver.find_elements(*self.LIST_ITEMS)
        return all(item.get_attribute('tabindex') is not None for item in items)

