import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class NotesDashboardPage(BasePage):
    # Route for the notes list view
    URL_PATH = "" # Inherits base_url/notes/ from settings

    def __init__(self, page: Page):
        """
        Initialize locators for the Notes Dashboard.
        Using data-testid for high-stability selectors (Industry Standard).
        """
        super().__init__(page)

        # Primary Dashboard Elements
        self._welcome_message = self.page.get_by_test_id("welcome-message")
        self._notes_list_text = self.page.get_by_role("link", name="MyNotes")
        self._add_note_button = self.page.get_by_test_id("add-new-note")

        # Identity and Navigation
        self._logout_button = self.page.get_by_test_id("logout-button")

        # Dynamic Note Elements (Used in Hybrid 20% validation)
        self._note_items = self.page.get_by_test_id("note-item")

    def is_welcome_message_visible(self) -> bool:
        """Verifies successful login by checking the welcome banner."""
        logger.info("Verifying welcome message visibility")
        return self._welcome_message.is_visible()

    def get_header_text(self) -> str:
        """Returns the dashboard header text."""
        return self.get_text(self._notes_list_text)

    def click_logout(self):
        """Performs logout to return to the login screen."""
        logger.info("Clicking logout from dashboard")
        self.click(self._logout_button, name="Logout Button")

    def is_note_visible(self, title: str) -> bool:
        """
        Hybrid/UI Check: Verifies if a specific note title exists in the list.
        Crucial for Phase 5.2 Hybrid scenarios.
        """
        # Locates a note item that contains the specific text
        note = self._note_items.filter(has_text=title)
        return note.is_visible()