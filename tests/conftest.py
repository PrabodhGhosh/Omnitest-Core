import pytest
from playwright.sync_api import Page, APIRequestContext

from config.settings import settings
from pages.login.login_page import LoginPage
from pages.notes.notes_dashboard_page import NotesDashboardPage
from api_services.notes_client import NotesApiClient


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture to provide a LoginPage instance to UI and Hybrid tests."""
    return LoginPage(page)

@pytest.fixture
def notes_dashboard_page(page: Page) -> NotesDashboardPage:
    """Fixture to provide a NotesDashboardPage instance to UI and Hybrid tests."""
    return NotesDashboardPage(page)

@pytest.fixture(scope="session")
def api_context(playwright):
    """Creates a session-wide API request context."""
    request_context = playwright.request.new_context(base_url=settings.API_BASE_URL)
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session")
def auth_token(api_context):
    """Logs in via API once per session and returns the token."""
    client = NotesApiClient(api_context)
    token = client.login()
    return token


@pytest.fixture
def authenticated_page(browser, auth_token):
    """
    Creates a Page object with the Auth token already in LocalStorage.
    This skips the UI Login page entirely!
    """
    context = browser.new_context()
    page = context.new_page()

    # 1. Navigate to the site so we are on the correct domain
    page.goto(settings.UI_BASE_URL)

    # 2. Inject the token into localStorage (ExpandTesting uses 'token')
    page.evaluate(f"window.localStorage.setItem('token', '{auth_token}');")

    # 3. Reload or navigate to the dashboard - you are now logged in!
    page.goto(f"{settings.UI_BASE_URL}/app",wait_until="domcontentloaded")

    yield page
    context.close()

@pytest.fixture
def notes_api(api_context, auth_token):
    """Provides a logged-in API client for setup/teardown."""
    client = NotesApiClient(api_context)
    client.token = auth_token  # Re-use the session token
    return client

@pytest.fixture(scope="session")
def secondary_token(api_context):
    """A simple, raw API call using the full absolute URL to avoid path errors."""
    # Note the /api/ in the path
    url = f"{settings.API_BASE_URL}/users/login"

    payload = {
        "email": settings.USER_EMAIL_2,
        "password": settings.USER_PASSWORD_2
    }


    response = api_context.post(url, data=payload)

    return response.json()["data"]["token"]