import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    # Industry Standard: Define the static route within the Page Object
    URL_PATH = "app/login"

    def __init__(self, page: Page):
        """
        Initialize locators for the ExpandTesting Notes App.
        Aligned with Phase 3.2: Structural Layer.
        """
        super().__init__(page)
        # Updated to Notes App specific selectors
        self._email_field = self.page.get_by_test_id("login-email")
        self._password_field = self.page.get_by_test_id("login-password")
        self._login_button = self.page.get_by_test_id("login-submit")

        # Error messages often appear in specific alert components
        self._error_message = self.page.get_by_test_id("alert-message")

    def navigate_to_login(self):
        """
        Navigates to the /notes/login endpoint.
        Uses the composition logic: base_url + endpoint.
        """
        self.navigate(self.URL_PATH)
        self.wait_for_load()

    def login(self, email, password):
        """
        Performs the UI login flow.
        10% Strategy: Pure UI interaction for E2E testing.
        """
        logger.info(f"UI Login Attempt: {email}")

        self.fill(self._email_field, email, name="Email Input")
        self.fill(self._password_field, password, name="Password Input", secret=True)
        self.click(self._login_button, name="Login Button")

    def get_error_message(self) -> str:
        """
        Retrieves the text from the error alert if a login fails.
        """
        return self.get_text(self._error_message)