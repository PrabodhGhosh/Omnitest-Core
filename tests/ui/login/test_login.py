import pytest

from config.settings import settings


def test_successful_login(login_page,secure_page):
    """
    Test Case: Verify that a user can log in with valid credentials.
    Using ExpandTesting credentials: practice / SuperSecretPassword!
    """

    # 1. Navigate to the login page
    login_page.navigate_to_login()

    # 2. Perform Login
    login_page.login(settings.USER_NAME, settings.PASSWORD)

    # 3. Assertions using the SecurePage
    assert "Secure Area" in secure_page.get_main_header_text()
    assert "Welcome to the Secure Area. When you are done click logout below." in secure_page.get_sub_header_text()

def test_invalid_login(login_page):
    """
    Test Case: Verify that an error message is shown for invalid credentials.
    """
    login_page.navigate_to_login()
    login_page.login("invalid_user", "wrong_password")

    assert "Your username is invalid!" in login_page.get_status_message()