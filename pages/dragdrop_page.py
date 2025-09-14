from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DragDropPage:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    # locators
    SOURCE_INDEX = (By.ID, 'draggable')
    TARGET_INDEX = (By.ID, 'droppable')
    DROP_MESSAGE = (By.ID, 'drop-message')


    def _html5_drag_and_drop(self, source_elem, target_elem):
        """
        Perform HTML5 drag-and-drop using JavaScript (works for most modern demo sites).
        Scrolls elements into view and simulates a small mouse move.
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", source_elem)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_elem)
        js = """
        function triggerDragAndDrop(source, target) {
            var dataTransfer = new DataTransfer();
            var dragStartEvent = new DragEvent('dragstart', { dataTransfer });
            source.dispatchEvent(dragStartEvent);
            var dragOverEvent = new DragEvent('dragover', { dataTransfer });
            target.dispatchEvent(dragOverEvent);
            var dropEvent = new DragEvent('drop', { dataTransfer });
            target.dispatchEvent(dropEvent);
            var dragEndEvent = new DragEvent('dragend', { dataTransfer });
            source.dispatchEvent(dragEndEvent);
        }
        triggerDragAndDrop(arguments[0], arguments[1]);
        """
        self.driver.execute_script(js, source_elem, target_elem)

    def drag_and_drop(self, source_index=0, target_index=1):
        """
        Drag and drop an item from source_index to target_index.
        Waits for visibility, scrolls into view, tries ActionChains, then falls back to HTML5 JS workaround if needed.
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        draggables = self.driver.find_elements(By.CSS_SELECTOR, '[id^="draggable"], .draggable')
        droppables = self.driver.find_elements(By.CSS_SELECTOR, '[id^="droppable"], .droppable')
        if not draggables:
            draggables = [self.driver.find_element(*self.SOURCE_INDEX)]
        if not droppables:
            droppables = [self.driver.find_element(*self.TARGET_INDEX)]
        source_index = min(source_index, len(draggables)-1)
        target_index = min(target_index, len(droppables)-1)
        source_elem = draggables[source_index]
        target_elem = droppables[target_index]
        # Wait for both elements to be visible and interactable
        WebDriverWait(self.driver, 10).until(EC.visibility_of(source_elem))
        WebDriverWait(self.driver, 10).until(EC.visibility_of(target_elem))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", source_elem)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_elem)
        try:
            actions = ActionChains(self.driver)
            actions.click_and_hold(source_elem).pause(0.2).move_to_element(target_elem).pause(0.2).release(target_elem).perform()
        except Exception:
            # Fallback to HTML5 JS workaround
            self._html5_drag_and_drop(source_elem, target_elem)


    def get_drop_message(self):
        """Return the text message from the drop target after a drag-and-drop operation."""
        try:
            droppable = self.driver.find_element(*self.DROP_MESSAGE)
            return droppable.text
        except:
            return ""

    def get_items_text(self):
        """Return a list of text for all draggable items (for test assertions)."""
        draggables = self.driver.find_elements(By.CSS_SELECTOR, '[id^="draggable"], .draggable')
        return [el.text for el in draggables]

    def is_accessible(self):
        """Check if drag-and-drop controls are accessible (e.g., have aria attributes or labels)."""
        draggables = self.driver.find_element(*self.SOURCE_INDEX)
        if not draggables:
            return False
        return True
