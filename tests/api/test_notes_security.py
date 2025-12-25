import pytest
from config.settings import settings
from utils.logger import get_logger


logger = get_logger(__name__)

class TestNotesSecurity:

    def test_unauthorized_access_is_rejected(self, api_context):
        """
        STRATEGY: Authentication check.
        Verifies that requests without a token are rejected with 401.
        """
        logger.info("TEST: Attempting to fetch notes without an auth token.")

        # Calling raw api_context without x-auth-token header
        response = api_context.get(f"{settings.API_BASE_URL}/notes")

        assert response.status == 401
        assert response.json()["success"] is False
        logger.info("SUCCESS: API correctly rejected unauthorized request.")

    def test_cross_user_deletion_is_forbidden(self, notes_api, secondary_token, api_context):
        """
        STRATEGY: IDOR (Insecure Direct Object Reference).
        Ensures User B cannot delete User A's data even if they have the ID.
        """
        # 1. SETUP: Create a note as User A (the main user)
        note_title = "User A Private Note"
        response = notes_api.create_note(note_title, "Sensitive Content", "Personal")
        note_id = response.json()["data"]["id"]
        logger.info(f"SETUP: User A created note {note_id}")

        try:
            # 2. ATTACK: Attempt to delete User A's note using User B's token
            logger.info(f"ATTACK: User B attempting to delete Note ID: {note_id}")

            attack_res = api_context.delete(
                f"{settings.API_BASE_URL}/notes/{note_id}",
                headers={"x-auth-token": secondary_token}
            )

            # 3. VERIFY: Access should be Forbidden (403), Not Found (404), or Bad Request (400)
            # A status of 200/204 here would mean a critical security bug!
            assert attack_res.status in [400, 403, 404], (
                f"SECURITY VULNERABILITY: User B was able to interact with User A's note. "
                f"Status: {attack_res.status}"
            )
            logger.info("SUCCESS: API successfully blocked cross-user data manipulation.")

        finally:
            # 4. CLEANUP: Ensure User A's note is deleted regardless of test outcome
            notes_api.delete_note(note_id)
            logger.info(f"CLEANUP: User A note {note_id} deleted.")