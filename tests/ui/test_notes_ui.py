from datetime import time, datetime
from playwright.sync_api import expect, Page
from pages.login.login_page import LoginPage
from pages.notes.notes_dashboard_page import NotesDashboardPage
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

def test_full_manual_note_creation_journey(page: Page, login_page: LoginPage, notes_dashboard_page: NotesDashboardPage):
    """
    STRATEGY: 10% Pure UI E2E Test.
    """
    # Use a timestamp to make the title unique
    unique_id = datetime.now().microsecond
    note_title = f"Manual Note {unique_id}"
    note_desc = "Testing pure UI flow with cleanup"

    # 1. Manual Login Flow
    logger.info("UI TEST: Starting manual login journey.")
    page.goto(settings.UI_BASE_URL+"/app/login")
    login_page.login(settings.USER_EMAIL, settings.USER_PASSWORD)

    # Verify login success by checking URL or dashboard element
    expect(page).to_have_url(f"{settings.UI_BASE_URL}/app")
    logger.info("UI TEST: Manual login successful.")

    # 2. Manual Note Creation

    logger.info(f"UI TEST: Creating note '{note_title}' via form.")
    notes_dashboard_page.add_note(note_title, note_desc, "Personal")

    # 3. Verification of UI feedback
    # Check for the card appearing
    try:
        expect(page.get_by_test_id("note-card-title").filter(has_text=note_title)).to_be_visible()

        logger.info("UI TEST: Success! Note created and verified manually.")

    finally:
        # 3. Cleanup: Keep the dashboard clean!
        logger.info(f"UI CLEANUP: Deleting note '{note_title}' via UI.")
        notes_dashboard_page.delete_note_by_title(note_title)

        # Final check: The card should be gone
        expect(page.get_by_test_id("note-card-title").filter(has_text=note_title)).not_to_be_visible()
        logger.info("UI CLEANUP: Verified note is gone from dashboard.")