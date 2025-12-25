import pytest
from playwright.sync_api import APIResponse
from api_services.notes_client import NotesApiClient
from utils.logger import get_logger

logger = get_logger(__name__)

class TestNotesValidation:
    @pytest.mark.parametrize("invalid_category", ["Vacation", "School", "12345"])
    def test_create_note_with_invalid_category_fails(self, notes_api: NotesApiClient, invalid_category):
        """
        STRATEGY: Boundary/Enum Testing.
        Verifies that the API correctly rejects categories not in the allowed list.
        """
        logger.info(f"TEST: Creating note with invalid category: {invalid_category}")

        response = notes_api.create_note(
            title="Valid Title",
            description="Testing invalid category",
            category=invalid_category
        )

        # Assertions
        assert response.status == 400
        response_body = response.json()
        assert response_body["success"] is False
        assert "Category must be one of the categories: Home, Work, Personal" in response_body["message"]

        logger.info(f"SUCCESS: API correctly rejected invalid category '{invalid_category}'")

    def test_create_note_with_too_short_title_fails(self, notes_api: NotesApiClient):
        """
        STRATEGY: Negative Testing / Boundary Value Analysis.
        The API documentation requires titles to be at least 4 characters.
        """
        short_title = "abc"
        logger.info(f"TEST: Creating note with short title: '{short_title}'")

        response = notes_api.create_note(
            title=short_title,
            description="Title is only 3 chars",
            category="Home"
        )

        assert response.status == 400
        assert response.json()["success"] is False
        assert "Title must be between 4 and 100 characters" in response.json()["message"]

    def test_create_note_with_missing_required_fields(self, notes_api: NotesApiClient):
        """
        STRATEGY: Robustness / Error Handling.
        Verify API behavior when mandatory 'title' is missing.
        """
        logger.info("TEST: Creating note with missing 'title' field")

        # We call the raw request here because our client method might enforce titles
        # This tests the server-side validation specifically
        payload = {
            "description": "Missing title",
            "category": "Work"
        }

        response = notes_api.request.post(
            f"{notes_api.base_url}/notes",
            data=payload,
            headers={"x-auth-token": notes_api.token}
        )

        assert response.status == 400
        assert "Title must be between 4 and 100 characters" in response.json()["message"]
        logger.info("SUCCESS: API correctly identified missing required field.")