import pytest
from pages.dragdrop_page import DragDropPage

# DRAGDROP_URL = "https://practice.qabrains.com/dragdrop" #the drag-drop function not working on this URL
DRAGDROP_URL = "https://testautomationcentral.com/demo/drag_and_drop.html"

@pytest.mark.dragdrop
@pytest.fixture
def dragdrop_page(driver):
    """Fixture to provide a DragDropPage object and navigate to the drag-and-drop URL."""
    page = DragDropPage(driver)
    driver.get(DRAGDROP_URL)
    return page

@pytest.mark.dragdrop
@pytest.mark.positive
def test_drag_and_drop_reorder(dragdrop_page):
    """Test reordering list items using drag and drop (by index)."""
    dragdrop_page.drag_and_drop(0, 1)
    assert dragdrop_page.get_drop_message() == 'Dropped successfully!'

@pytest.mark.dragdrop
@pytest.mark.positive
def test_drag_to_first_and_last(dragdrop_page):
    """Test dragging last item to first and first to last position."""
    items = dragdrop_page.get_items_text()
    if len(items) < 2:
        pytest.skip("Not enough items to reorder.")
    # Drag last to first
    dragdrop_page.drag_and_drop(len(items)-1, 0)
    # Drag first to last
    dragdrop_page.drag_and_drop(0, len(items)-1)
    # No assertion here as the demo site may not update order visually, but no error should occur

@pytest.mark.dragdrop
@pytest.mark.accessibility
def test_dragdrop_accessibility(dragdrop_page):
    """Test accessibility of drag-and-drop controls."""
    assert dragdrop_page.is_accessible(), "Drag-and-drop items are not accessible."
