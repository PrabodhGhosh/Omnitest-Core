import pytest
from playwright.sync_api import Page
# Remove 'src.' because your screenshot shows 'pages' is at the root
from pages.login.login_page import LoginPage
from pages.login.secure_page import SecurePage

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture
def secure_page(page: Page) -> SecurePage:
    return SecurePage(page)