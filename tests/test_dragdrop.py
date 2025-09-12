import pytest
from pages.dragdrop_page import DragDropPage

DRAGDROP_URL = "https://practice.qabrains.com/dragdrop"  # Update if the actual URL is different

@pytest.fixture
def dragdrop_page(driver):
    page = DragDropPage(driver)
    driver.get(DRAGDROP_URL)
    return page

def test_drag_and_drop_reorder(dragdrop_page):
    initial_order = dragdrop_page.get_items_text()
    if len(initial_order) < 2:
        pytest.skip("Not enough items to reorder.")
    dragdrop_page.drag_and_drop(0, 1)
    new_order = dragdrop_page.get_items_text()
    assert initial_order[0] != new_order[0], "Order did not change after drag-and-drop."

def test_drag_to_first_and_last(dragdrop_page):
    items = dragdrop_page.get_items_text()
    if len(items) < 3:
        pytest.skip("Not enough items for edge case drag-and-drop.")
    # Drag last to first
    dragdrop_page.drag_and_drop(len(items)-1, 0)
    order_after_first = dragdrop_page.get_items_text()
    assert order_after_first[0] == items[-1]
    # Drag first to last
    dragdrop_page.drag_and_drop(0, len(items)-1)
    order_after_last = dragdrop_page.get_items_text()
    assert order_after_last[-1] == order_after_first[0]

def test_dragdrop_accessibility(dragdrop_page):
    assert dragdrop_page.is_accessible(), "Drag-and-drop items are not accessible."

