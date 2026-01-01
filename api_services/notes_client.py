import allure
from playwright.sync_api import APIRequestContext
from config.settings import settings
from utils.logger import get_logger
from utils.schema_validator import validate_json_schema

logger = get_logger(__name__)

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
        Uses credentials from the .env file.
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

    def get_all_notes(self):
        """Fetches all notes and validates the array schema."""
        response = self.request.get(
        f"{self.base_url}/notes",
        headers={"x-auth-token": self.token}
    )

        if response.ok:
            # Validate that the response is a valid list of notes
             validate_json_schema(response.json(), "notes_list_schema.json")

        return response

    @allure.step("API: Create note '{title}'")
    def create_note(self, title: str, description: str, category: str):
        """Creates a new note using the stored token."""
        payload = {
            "title": title,
            "description": description,
            "category": category
        }
        response=  self.request.post(
            f"{self.base_url}/notes",
            data=payload,
            headers={"x-auth-token": self.token}
        )

        if response.ok:
            logger.info(f"API RESPONDED: {response.status}. Validating Schema...")
            validate_json_schema(response.json(), "note_schema.json")
        else:
            logger.error(f"API ERROR: {response.status} - {response.text()}")

        return response

    def delete_note(self, note_id: str):
        """Deletes a specific note by ID."""
        headers = {"x-auth-token": self.token}
        return self.request.delete(
            f"{self.base_url}/notes/{note_id}",
            headers=headers
        )

    @allure.step("API: Delete all existing notes")
    def delete_all_notes(self):
        """
        Utility to wipe all notes for the current user.
        Useful for 'Before' hooks to ensure a clean slate.
        """
        logger.info("CLEANUP: Fetching all notes for deletion...")
        response = self.get_all_notes() # This already has schema validation!

        if response.ok:
            notes = response.json().get("data", [])
            for note in notes:
                self.delete_note(note["id"])
            logger.info(f"CLEANUP: Deleted {len(notes)} notes.")