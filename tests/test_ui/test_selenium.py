"""Selenium end-to-end tests for the HTMX UI.

Tests run with a visible Chrome browser to demonstrate UI functionality.
"""

import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Delay constants per requirements
FILL_DELAY = 0.1  # Delay between form fills
CLICK_DELAY = 0.5  # Delay after button clicks

BASE_URL = "http://127.0.0.1:8081"


@pytest.fixture(scope="module")
def server():
    """Start the MIAPPE-API server for testing."""
    import os
    import socket

    # Set working directory to miappe-api root
    cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    proc = subprocess.Popen(
        ["uv", "run", "uvicorn", "miappe_api.ui.routes:app", "--port", "8081"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
    )

    # Wait for server to be ready by polling the port
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", 8081))
            sock.close()
            if result == 0:
                break
        except Exception:
            pass
        time.sleep(0.5)
    else:
        # If server failed to start, print output for debugging
        output = proc.stdout.read().decode() if proc.stdout else ""
        proc.terminate()
        raise RuntimeError(f"Server failed to start within timeout. Output: {output}")

    time.sleep(0.5)  # Extra buffer for full initialization
    yield proc
    proc.terminate()
    proc.wait()


@pytest.fixture
def browser(server):  # noqa: ARG001
    """Create a visible Chrome browser for testing."""
    _ = server  # Ensure server is running
    options = Options()
    # Run in visible mode (no headless)
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    # Reset server state before each test
    import urllib.request

    try:
        req = urllib.request.Request(f"{BASE_URL}/reset", method="POST")
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Ignore errors if server not ready

    yield driver
    driver.quit()


def fill_field(driver, testid: str, value: str, trigger_change: bool = False):
    """Fill a form field by data-testid.

    Args:
        driver: Selenium WebDriver
        testid: The data-testid attribute value
        value: The value to fill
        trigger_change: If True, trigger a change event after filling (needed for HTMX)
    """
    element = driver.find_element(By.CSS_SELECTOR, f"[data-testid='{testid}']")

    # For date inputs, use JavaScript to set value directly (avoids locale issues)
    if element.get_attribute("type") == "date":
        driver.execute_script("arguments[0].value = arguments[1]", element, value)
    else:
        element.clear()
        element.send_keys(value)

    if trigger_change:
        # Trigger change event for HTMX handlers
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change', {bubbles: true}))", element
        )
        time.sleep(CLICK_DELAY)  # Wait for HTMX to process

    time.sleep(FILL_DELAY)


def click_button(driver, testid: str):
    """Click a button by data-testid and wait."""
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='{testid}']"))
    )
    button.click()
    time.sleep(CLICK_DELAY)


def click_element(driver, testid: str):
    """Click any element by data-testid and wait."""
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='{testid}']"))
    )
    element.click()
    time.sleep(CLICK_DELAY)


def element_exists(driver, testid: str) -> bool:
    """Check if an element with given data-testid exists."""
    elements = driver.find_elements(By.CSS_SELECTOR, f"[data-testid='{testid}']")
    return len(elements) > 0


def get_element_text(driver, testid: str) -> str:
    """Get the text content of an element by data-testid."""
    element = driver.find_element(By.CSS_SELECTOR, f"[data-testid='{testid}']")
    return element.text


def expand_optional_fields(driver):
    """Expand the optional fields section if collapsed."""
    try:
        toggle = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='section-optional-toggle']")
            )
        )
        # Check if collapsible content is visible
        parent = toggle.find_element(By.XPATH, "..")
        content = parent.find_element(By.CSS_SELECTOR, ".collapsible-content")
        if not content.is_displayed():
            toggle.click()
            time.sleep(CLICK_DELAY)
            # Wait for content to be visible
            WebDriverWait(driver, 5).until(EC.visibility_of(content))
    except Exception:
        pass  # Optional fields section may not exist


@pytest.mark.ui
class TestCreateInvestigationRequiredFields:
    """Test creating an Investigation with required fields only."""

    def test_create_investigation_required_fields(self, browser):
        """Create Investigation with only required fields."""
        # Navigate to home
        browser.get(BASE_URL)
        time.sleep(1)  # Wait for page to fully load

        # Click "+ Investigation" button
        click_button(browser, "btn-create-Investigation")

        # Verify form is displayed
        assert element_exists(browser, "form-entity")
        assert element_exists(browser, "input-unique-id")

        # Fill required field: unique_id
        fill_field(browser, "input-unique-id", "INV-TEST-001")

        # Fill required field: title (also required per MIAPPE spec)
        fill_field(browser, "input-title", "Test Investigation Required Fields")

        # Click Create button
        click_button(browser, "btn-create")

        # Verify entity appears in sidebar (tree node should exist)
        time.sleep(CLICK_DELAY)
        sidebar = browser.find_element(By.ID, "sidebar")
        assert "Test Investigation Required Fields" in sidebar.text

        # Verify notification shows success
        body_text = browser.find_element(By.TAG_NAME, "body").text
        assert "Created Investigation" in body_text


@pytest.mark.ui
class TestCreateInvestigationAllFields:
    """Test creating an Investigation with all fields."""

    def test_create_investigation_all_fields(self, browser):
        """Create Investigation with all available fields."""
        # Navigate to home
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Click "+ Investigation" button
        click_button(browser, "btn-create-Investigation")

        # Fill required fields
        fill_field(browser, "input-unique-id", "INV-TEST-002")
        fill_field(browser, "input-title", "Full Investigation Test")

        # Expand optional fields
        expand_optional_fields(browser)

        # Fill optional fields
        fill_field(browser, "input-description", "A comprehensive test investigation")
        fill_field(browser, "input-submission-date", "2024-03-15")
        fill_field(browser, "input-public-release-date", "2024-06-01")
        fill_field(browser, "input-license", "https://creativecommons.org/licenses/by/4.0/")
        fill_field(browser, "input-miappe-version", "1.1")

        # Fill associated_publications (textarea, one per line)
        fill_field(browser, "input-associated-publications", "https://doi.org/10.1234/test.001")

        # Click Create button
        click_button(browser, "btn-create")

        # Wait for HTMX to process and sidebar to refresh
        time.sleep(1)

        # Force refresh the page to ensure sidebar is updated
        browser.refresh()
        time.sleep(CLICK_DELAY)

        # Verify entity appears in sidebar
        sidebar = browser.find_element(By.ID, "sidebar")
        sidebar_text = sidebar.text
        assert (
            "Full Investigation Test" in sidebar_text
        ), f"Expected 'Full Investigation Test' in sidebar, got: {sidebar_text}"

        # Click on the created entity to verify values
        # Find the tree node with the correct label
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        target_node = None
        for node in tree_nodes:
            if "Full Investigation Test" in node.text:
                target_node = node
                break
        assert (
            target_node is not None
        ), f"Could not find tree node with 'Full Investigation Test', found: {[n.text for n in tree_nodes]}"
        target_node.click()
        time.sleep(CLICK_DELAY)

        # Verify form shows edit mode with preserved values
        unique_id_field = browser.find_element(By.CSS_SELECTOR, "[data-testid='input-unique-id']")
        assert unique_id_field.get_attribute("value") == "INV-TEST-002"

        title_field = browser.find_element(By.CSS_SELECTOR, "[data-testid='input-title']")
        assert title_field.get_attribute("value") == "Full Investigation Test"


@pytest.mark.ui
class TestAddNestedContacts:
    """Test adding nested contacts to an Investigation."""

    def test_add_nested_contacts(self, browser):
        """Create Investigation and add contacts through nested table."""
        # Navigate to home
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Click "+ Investigation" button
        click_button(browser, "btn-create-Investigation")

        # Fill required fields
        fill_field(browser, "input-unique-id", "INV-TEST-003")
        fill_field(browser, "input-title", "Investigation with Contacts")

        # Click Create button
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        # Click on the created entity to open edit form
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        assert len(tree_nodes) > 0
        tree_nodes[0].click()
        time.sleep(CLICK_DELAY)

        # Expand optional fields to access contacts button
        expand_optional_fields(browser)

        # Click on contacts nested field button
        click_button(browser, "btn-nested-contacts")

        # Verify table view is displayed
        assert element_exists(browser, "table-add-row")
        assert element_exists(browser, "table-save")

        # Click "+ Add Row" button
        click_button(browser, "table-add-row")
        time.sleep(CLICK_DELAY)

        # Fill contact fields in the new row (row index 0)
        # trigger_change=True to ensure HTMX saves each cell value
        fill_field(browser, "cell-0-name", "Dr. Jane Smith", trigger_change=True)
        fill_field(browser, "cell-0-email", "jane.smith@example.org", trigger_change=True)
        fill_field(browser, "cell-0-institution", "Research Institute", trigger_change=True)
        fill_field(browser, "cell-0-role", "Principal Investigator", trigger_change=True)
        fill_field(browser, "cell-0-orcid", "0000-0001-2345-6789", trigger_change=True)

        # Click "Save & Back" button
        click_button(browser, "table-save")
        time.sleep(CLICK_DELAY)

        # Verify we're back on the Investigation form
        assert element_exists(browser, "form-entity")

        # Expand optional fields to check contacts count
        expand_optional_fields(browser)

        # Verify contacts button shows count of 1
        contacts_btn = browser.find_element(By.CSS_SELECTOR, "[data-testid='btn-nested-contacts']")
        assert "(1)" in contacts_btn.text


@pytest.mark.ui
class TestEditInvestigation:
    """Test editing an existing Investigation."""

    def test_edit_investigation(self, browser):
        """Edit an existing Investigation and verify changes persist."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Create an Investigation first
        click_button(browser, "btn-create-Investigation")
        fill_field(browser, "input-unique-id", "INV-EDIT-001")
        fill_field(browser, "input-title", "Original Title")
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        # Click on the created entity in sidebar
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        target_node = None
        for node in tree_nodes:
            if "Original Title" in node.text:
                target_node = node
                break
        assert target_node is not None
        target_node.click()
        time.sleep(CLICK_DELAY)

        # Verify edit form is shown
        assert element_exists(browser, "btn-update")

        # Modify the title
        title_field = browser.find_element(By.CSS_SELECTOR, "[data-testid='input-title']")
        title_field.clear()
        title_field.send_keys("Updated Title")
        time.sleep(FILL_DELAY)

        # Click Update
        click_button(browser, "btn-update")
        time.sleep(CLICK_DELAY)

        # Refresh and verify the change persisted
        browser.refresh()
        time.sleep(CLICK_DELAY)

        sidebar = browser.find_element(By.ID, "sidebar")
        assert "Updated Title" in sidebar.text


@pytest.mark.ui
class TestDeleteInvestigation:
    """Test deleting an Investigation."""

    def test_delete_investigation(self, browser):
        """Delete an Investigation and verify it's removed from sidebar."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Create an Investigation
        click_button(browser, "btn-create-Investigation")
        fill_field(browser, "input-unique-id", "INV-DELETE-001")
        fill_field(browser, "input-title", "To Be Deleted")
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        browser.refresh()
        time.sleep(CLICK_DELAY)

        # Verify it exists in sidebar
        sidebar = browser.find_element(By.ID, "sidebar")
        assert "To Be Deleted" in sidebar.text

        # Find the delete button for this entity
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        target_node = None
        for node in tree_nodes:
            if "To Be Deleted" in node.text:
                target_node = node
                break
        assert target_node is not None

        # Get the node ID from the data-testid
        node_testid = target_node.get_attribute("data-testid")
        node_id = node_testid.replace("tree-node-", "")

        # Click delete button and accept confirmation
        delete_btn = browser.find_element(By.CSS_SELECTOR, f"[data-testid='btn-delete-{node_id}']")
        delete_btn.click()

        # Handle browser confirm dialog
        alert = browser.switch_to.alert
        alert.accept()
        time.sleep(CLICK_DELAY)

        # Verify entity is removed from sidebar
        sidebar = browser.find_element(By.ID, "sidebar")
        assert "To Be Deleted" not in sidebar.text


@pytest.mark.ui
class TestAddNestedStudy:
    """Test adding a nested Study to an Investigation."""

    def test_add_nested_study(self, browser):
        """Add a Study to an Investigation through nested table."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Create Investigation
        click_button(browser, "btn-create-Investigation")
        fill_field(browser, "input-unique-id", "INV-STUDY-001")
        fill_field(browser, "input-title", "Investigation with Study")
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        # Click on the created entity
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        for node in tree_nodes:
            if "Investigation with Study" in node.text:
                node.click()
                break
        time.sleep(CLICK_DELAY)

        # Expand optional fields
        expand_optional_fields(browser)

        # Click on studies nested field button
        click_button(browser, "btn-nested-studies")

        # Add a row
        click_button(browser, "table-add-row")
        time.sleep(CLICK_DELAY)

        # Fill study fields
        fill_field(browser, "cell-0-unique_id", "STU-001", trigger_change=True)
        fill_field(browser, "cell-0-title", "Field Trial 2024", trigger_change=True)

        # Save & Back
        click_button(browser, "table-save")
        time.sleep(CLICK_DELAY)

        # Verify studies count shows 1
        expand_optional_fields(browser)
        studies_btn = browser.find_element(By.CSS_SELECTOR, "[data-testid='btn-nested-studies']")
        assert "(1)" in studies_btn.text


@pytest.mark.ui
class TestValidationError:
    """Test validation error display."""

    def test_validation_error_missing_required(self, browser):
        """Submit form without required fields and verify error message."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Click create Investigation
        click_button(browser, "btn-create-Investigation")

        # Don't fill any fields, just click Create
        # The HTML5 validation should prevent submission, but if it gets through:
        create_btn = browser.find_element(By.CSS_SELECTOR, "[data-testid='btn-create']")

        # Check if unique_id field has required attribute
        unique_id = browser.find_element(By.CSS_SELECTOR, "[data-testid='input-unique-id']")
        assert unique_id.get_attribute("required") is not None

        # Fill unique_id but not title (both required)
        fill_field(browser, "input-unique-id", "INV-VAL-001")
        # Leave title empty

        # Try to submit - HTML5 validation should block
        create_btn.click()
        time.sleep(CLICK_DELAY)

        # The form should still be visible (not submitted)
        assert element_exists(browser, "form-entity")


@pytest.mark.ui
class TestProfileSwitch:
    """Test profile switching between miappe and isa."""

    def test_switch_profile_clears_state(self, browser):
        """Switch profile and verify state is cleared."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Create an Investigation in miappe profile
        click_button(browser, "btn-create-Investigation")
        fill_field(browser, "input-unique-id", "INV-PROFILE-001")
        fill_field(browser, "input-title", "Miappe Investigation")
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        browser.refresh()
        time.sleep(CLICK_DELAY)

        # Verify entity exists
        sidebar = browser.find_element(By.ID, "sidebar")
        assert "Miappe Investigation" in sidebar.text

        # Switch to ISA profile using the select dropdown
        profile_select = browser.find_element(By.ID, "profile-select")
        profile_select.click()
        time.sleep(FILL_DELAY)

        # Select ISA option
        isa_option = profile_select.find_element(By.CSS_SELECTOR, "option[value='isa']")
        isa_option.click()
        time.sleep(1)  # Wait for redirect

        # Verify state is cleared (no entities)
        sidebar = browser.find_element(By.ID, "sidebar")
        assert "No entities created yet" in sidebar.text
        assert "Miappe Investigation" not in sidebar.text

        # Switch back to miappe
        profile_select = browser.find_element(By.ID, "profile-select")
        miappe_option = profile_select.find_element(By.CSS_SELECTOR, "option[value='miappe']")
        miappe_option.click()
        time.sleep(1)

        # Verify miappe is selected but state was cleared
        sidebar = browser.find_element(By.ID, "sidebar")
        assert "No entities created yet" in sidebar.text


@pytest.mark.ui
class TestNestedEntityEditing:
    """Test editing nested entities by clicking on table rows."""

    def test_edit_nested_study(self, browser):
        """Click a Study row in table to open edit form for that Study."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Create Investigation with a Study
        click_button(browser, "btn-create-Investigation")
        fill_field(browser, "input-unique-id", "INV-NESTED-001")
        fill_field(browser, "input-title", "Investigation for Nested Edit")
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        # Click on the created entity
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        for node in tree_nodes:
            if "Investigation for Nested Edit" in node.text:
                node.click()
                break
        time.sleep(CLICK_DELAY)

        # Expand optional fields
        expand_optional_fields(browser)

        # Click on studies nested field button
        click_button(browser, "btn-nested-studies")

        # Add a Study row
        click_button(browser, "table-add-row")
        time.sleep(CLICK_DELAY)

        fill_field(browser, "cell-0-unique_id", "STU-NESTED-001", trigger_change=True)
        fill_field(browser, "cell-0-title", "Study for Nested Edit", trigger_change=True)

        # Save the Study first to ensure it's persisted
        click_button(browser, "table-save")
        time.sleep(CLICK_DELAY)

        # Go back to Studies table
        expand_optional_fields(browser)
        click_button(browser, "btn-nested-studies")
        time.sleep(CLICK_DELAY)

        # Click on the Study row to edit it
        click_element(browser, "row-0")
        time.sleep(CLICK_DELAY)

        # Verify we're now in Study edit form
        # Should show Study-specific fields
        assert element_exists(browser, "form-entity")

        # Verify breadcrumb shows navigation path
        assert element_exists(browser, "breadcrumb")
        breadcrumb = browser.find_element(By.CSS_SELECTOR, "[data-testid='breadcrumb']")
        assert "Investigation" in breadcrumb.text
        assert "studies" in breadcrumb.text

        # Verify the Study form has the correct values
        unique_id_field = browser.find_element(By.CSS_SELECTOR, "[data-testid='input-unique-id']")
        assert unique_id_field.get_attribute("value") == "STU-NESTED-001"

        # Verify back button exists
        assert element_exists(browser, "btn-back")

        # Click back button to return to table
        click_button(browser, "btn-back")
        time.sleep(CLICK_DELAY)

        # Verify we're back on the table view
        assert element_exists(browser, "table-save")

    def test_deep_nesting_navigation(self, browser):
        """Navigate from Investigation > Study > BiologicalMaterial."""
        browser.get(BASE_URL)
        time.sleep(CLICK_DELAY)

        # Create Investigation
        click_button(browser, "btn-create-Investigation")
        fill_field(browser, "input-unique-id", "INV-DEEP-001")
        fill_field(browser, "input-title", "Deep Nesting Investigation")
        click_button(browser, "btn-create")
        time.sleep(CLICK_DELAY)

        # Click on the created entity
        tree_nodes = browser.find_elements(By.CSS_SELECTOR, "[data-testid^='tree-node-']")
        for node in tree_nodes:
            if "Deep Nesting Investigation" in node.text:
                node.click()
                break
        time.sleep(CLICK_DELAY)

        # Expand optional fields and add a Study
        expand_optional_fields(browser)
        click_button(browser, "btn-nested-studies")
        click_button(browser, "table-add-row")
        time.sleep(CLICK_DELAY)

        fill_field(browser, "cell-0-unique_id", "STU-DEEP-001", trigger_change=True)
        fill_field(browser, "cell-0-title", "Deep Study", trigger_change=True)

        # Save and go back to Investigation
        click_button(browser, "table-save")
        time.sleep(CLICK_DELAY)

        # Go back to Studies table
        expand_optional_fields(browser)
        click_button(browser, "btn-nested-studies")
        time.sleep(CLICK_DELAY)

        # Click on Study row to edit it
        click_element(browser, "row-0")
        time.sleep(CLICK_DELAY)

        # Verify we're in Study form
        assert element_exists(browser, "form-entity")

        # Expand optional fields in Study form
        expand_optional_fields(browser)

        # Click on biological_materials nested field
        click_button(browser, "btn-nested-biological-materials")
        time.sleep(CLICK_DELAY)

        # Verify we're in BiologicalMaterial table view
        assert element_exists(browser, "table-add-row")

        # Add a BiologicalMaterial
        click_button(browser, "table-add-row")
        time.sleep(CLICK_DELAY)

        fill_field(browser, "cell-0-unique_id", "BM-001", trigger_change=True)
        fill_field(browser, "cell-0-organism", "Arabidopsis thaliana", trigger_change=True)

        # Save
        click_button(browser, "table-save")
        time.sleep(CLICK_DELAY)

        # Verify we're back in Study form
        assert element_exists(browser, "form-entity")

        # Go back to biological_materials table
        expand_optional_fields(browser)
        click_button(browser, "btn-nested-biological-materials")
        time.sleep(CLICK_DELAY)

        # Click on BiologicalMaterial row to edit
        click_element(browser, "row-0")
        time.sleep(CLICK_DELAY)

        # Verify breadcrumb shows full path
        assert element_exists(browser, "breadcrumb")
        breadcrumb = browser.find_element(By.CSS_SELECTOR, "[data-testid='breadcrumb']")
        breadcrumb_text = breadcrumb.text
        assert "Investigation" in breadcrumb_text
        assert "studies" in breadcrumb_text
        assert "biological_materials" in breadcrumb_text

        # Verify BiologicalMaterial form fields
        unique_id_field = browser.find_element(By.CSS_SELECTOR, "[data-testid='input-unique-id']")
        assert unique_id_field.get_attribute("value") == "BM-001"

        # Navigate all the way back using back buttons
        click_button(browser, "btn-back")  # Back to BM table
        time.sleep(CLICK_DELAY)
        assert element_exists(browser, "table-save")

        click_button(browser, "table-save")  # Back to Study form
        time.sleep(CLICK_DELAY)
        assert element_exists(browser, "form-entity")

        click_button(browser, "btn-back")  # Back to Studies table
        time.sleep(CLICK_DELAY)
        assert element_exists(browser, "table-save")

        click_button(browser, "table-save")  # Back to Investigation form
        time.sleep(CLICK_DELAY)
        assert element_exists(browser, "form-entity")

        # Verify we're back at Investigation level (btn-create or btn-update visible)
        assert element_exists(browser, "btn-update")
