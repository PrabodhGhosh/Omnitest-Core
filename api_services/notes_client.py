from playwright.sync_api import APIRequestContext
from config.settings import settings

class NotesApiClient:
    def __init__(self, request_context:APIRequestContext):
        """
        Initializes the API client using Playwright's request context.
        """
        self.request = request_context
        self.base_url = settings.API_BASE_URL
        self.token = None

    def login(self) -> str:
        """
        Authenticates via the /users/login endpoint.
        Uses credentials from your Windows .env file.
        """
        payload = {
            "email": settings.USER_EMAIL,
            "password": settings.USER_PASSWORD
        }

        response = self.request.post(f"{self.base_url}/users/login", data=payload)

        if not response.ok:
            raise Exception(f"Login Failed: {response.status} - {response.text()}")

        result = response.json()
        self.token = result.get("data", {}).get("token")
        return self.token

    def get_notes(self):
        """Fetches all notes for the authenticated user."""
        return self.request.get(
            f"{self.base_url}/notes",
            headers={"x-auth-token": self.token}
        )

    def create_note(self, title: str, description: str, category: str):
        """Creates a new note using the stored token."""
        payload = {
            "title": title,
            "description": description,
            "category": category
        }
        return self.request.post(
            f"{self.base_url}/notes",
            data=payload,
            headers={"x-auth-token": self.token}
        )
    def delete_note(self, note_id: str):
        """Deletes a specific note by ID."""
        headers = {"x-auth-token": self.token}
        return self.request.delete(
            f"{self.base_url}/notes/{note_id}",
            headers=headers
        )