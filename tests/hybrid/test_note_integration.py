from playwright.sync_api import expect, Page

from api_services.notes_client import NotesApiClient
from utils.logger import get_logger

# Initialize the logger for this module
logger = get_logger(__name__)

def test_api_created_note_appears_in_ui(notes_api: NotesApiClient, authenticated_page :Page):
    # 1. SETUP: Create a note via API (Fast)
    note_title = "Hybrid Test Note"
    note_desc = "Created via API, verified via UI"
    note_cat = "Home"

    response = notes_api.create_note(note_title, note_desc, note_cat)
    assert response.ok, f"API Setup failed: {response.text()}"
    note_id = response.json()["data"]["id"]

    try:

        logger.info(f"API SUCCESS: Note ID {note_id} created and stored in DB.")

        # 2. UI ACTION: Synchronization
        logger.info(f"ACTION: Reloading authenticated_page at {authenticated_page.url}")
        with authenticated_page.expect_response("**/api/notes") as response:
            authenticated_page.reload(wait_until="domcontentloaded")
        logger.info(f"NETWORK: UI received notes list from server (Status: {response.value.status})")

        # 3. VERIFICATION: Assert the note is visible in the UI
        # We use Playwright's locator to find the card with our title
        note_card = authenticated_page.get_by_test_id("note-card-title").filter(has_text=note_title)
        # Use 'expect' for built-in retries/assertions
        expect(note_card).to_be_visible()

        print(f"\nSuccessfully verified note '{note_title}' in the UI!")

    finally:

       clean_up_res =  notes_api.delete_note(note_id)
       assert clean_up_res.ok
       print(f"\nCleanup successful: Note {note_id} deleted.")
