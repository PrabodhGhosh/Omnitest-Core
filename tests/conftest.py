import pytest
from playwright.sync_api import Page, APIRequestContext
from pages.login.login_page import LoginPage
from pages.notes.notes_dashboard_page import NotesDashboardPage
# In the future, we will import the API Client here

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture to provide a LoginPage instance to UI and Hybrid tests."""
    return LoginPage(page)

@pytest.fixture
def notes_dashboard_page(page: Page) -> NotesDashboardPage:
    """Fixture to provide a NotesDashboardPage instance to UI and Hybrid tests."""
    return NotesDashboardPage(page)

# placeholder for Step 3.2 & 3.3
# We will add api_client and authenticated_page fixtures here next.