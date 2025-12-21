import pytest
from config.settings import settings

class TestLogin:
    """
    These tests verify the full browser flow without API shortcuts.
    """

    def test_successful_notes_login(self, login_page, notes_dashboard_page):
        """
        Test Case: Verify that a registered user can log in via the UI.
        Target: https://practice.expandtesting.com/notes/login
        """
        # 1. Navigate to the Notes Login page
        login_page.navigate_to_login()

        # 2. Perform Login using Pydantic settings
        login_page.login(settings.USER_EMAIL, settings.USER_PASSWORD)

        # 3. Assertions using the Dashboard Page Object
        # Verifies we are on the correct dashboard view
        assert "MyNotes" in notes_dashboard_page.get_header_text()

    def test_invalid_notes_login(self, login_page):
        """
        Test Case: Verify that invalid credentials trigger the correct UI error message.
        """
        # 1. Navigate to the Notes Login page
        login_page.navigate_to_login()

        # 2. Attempt login with a non-existent user
        login_page.login("nonexistent_user@example.com", "wrongpassword123")

        # 3. Verify the UI error alert contains expected text
        error_text = login_page.get_error_message()
        assert "Incorrect email address or password" in error_text or "not found" in error_text, f"Unexpected error message: {error_text}"