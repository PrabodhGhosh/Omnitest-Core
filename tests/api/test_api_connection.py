from playwright.sync_api import sync_playwright
from api_services.notes_client import NotesApiClient

def test_connection():
    with sync_playwright() as p:
        # Create a fresh context
        request_context = p.request.new_context()
        client = NotesApiClient(request_context)

        # Test Login
        token = client.login()
        print(f"Successfully logged in! Token: {token[:10]}...")

        # Test Get Notes
        response = client.get_notes()
        print(f"Notes Status: {response.status}")