import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class SecurePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # We target the main heading and the logout button
        self._main_header = self.page.get_by_role("heading", level=1)
        self._sub_header = self.page.get_by_role(role="heading",name="Welcome to the Secure Area")
        self._logout_button = self.page.get_by_role("link", name="Logout")
        self._success_alert = self.page.get_by_role("alert")
        
    def get_main_header_text(self) -> str:
        """Verifies the page title 'Secure Area'."""
        return self.get_text(self._main_header)

    def get_sub_header_text(self) -> str:
        """Verifies the sub header text"""
        return self.get_text(self._sub_header)

    def click_logout(self):
        """Logs out using the versatile click method."""
        self.click(self._logout_button, name="Logout Button")

    def is_logout_success_present(self) -> bool:
        """Checks if the logout success message is visible."""
        return self._success_alert.is_visible()