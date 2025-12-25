import pytest
from playwright.sync_api import expect, Page
from api_services.notes_client import NotesApiClient
from utils.logger import get_logger

logger = get_logger(__name__)

def test_mass_api_notes_appear_in_ui(notes_api: NotesApiClient, authenticated_page: Page):
    """
    STRATEGY: Hybrid - Mass Data Injection.
    Injects 3 notes via API and verifies UI renders the correct count.
    """
    # 1. SETUP: Clean slate and create 3 notes via API
    notes_api.delete_all_notes()
    note_titles = [f"Note {i}" for i in range(1, 4)]

    for title in note_titles:
        notes_api.create_note(title, "Bulk creation test", "Work")

    logger.info(f"HYBRID SETUP: Created {len(note_titles)} notes via API.")

    # 2. ACTION: Refresh the UI
    authenticated_page.reload(wait_until="domcontentloaded")

    # 3. VERIFICATION: Check the count of note cards in the UI
    # We use the test-id for the card container
    note_cards = authenticated_page.get_by_test_id("note-card")

    # Playwright 'expect' will wait for the cards to appear
    expect(note_cards).to_have_count(3)

    # Verify the specific titles are present
    for title in note_titles:
        expect(authenticated_page.get_by_text(title)).to_be_visible()

    logger.info("HYBRID SUCCESS: All API-created notes verified in UI.")