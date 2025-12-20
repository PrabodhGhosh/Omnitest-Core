import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):

    def __init__(self, page:Page):
        """
        Initialize the page with the modern Playwright locator strategies.
        These are 'lazy', meaning they won't look for the element until
        an action is performed.
        """
        super().__init__(page)
        # Using User-Facing Locators for resilience and accessibility
        self._username_field = self.page.get_by_label("Username")
        self._password_field = self.page.get_by_label("Password")
        self._login_button = self.page.get_by_role("button", name="Login")

        # ExpandTesting uses an alert role for flash messages
        self._flash_alert = self.page.get_by_role("alert")

    def navigate_to_login(self):
        """
        Navigates to the /login endpoint of the ExpandTesting site.
        Uses the base_url defined in the Pydantic settings.
        """
        self.navigate("login")
        self.wait_for_load()

    def login(self, username, password):
        """
        Main action flow.
        """
        logger.info(f"Attempting login for user: {username}")

        self.fill(self._username_field, username, name="Username Input")
        self.fill(self._password_field, password, name="Password Input", secret=True)
        self.click(self._login_button, name="Login Button")

    def get_status_message(self) -> str:
        """
        Returns the text from the flash alert (Success or Error).
        The BasePage.get_text handles waiting and whitespace stripping.
        """
        return self.get_text(self._flash_alert)