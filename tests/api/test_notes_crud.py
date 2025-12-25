from api_services.notes_client import NotesApiClient
from utils.logger import get_logger

logger = get_logger(__name__)
class TestNotesCRUD:
    def test_note_full_lifecycle(self, notes_api: NotesApiClient):
        """
        STRATEGY: Functional E2E API Lifecycle.
        Tests the full 'Happy Path' of a resource from birth to death.
        """
        # 1. CREATE
        title = "Lifecycle Test"
        description = "Testing the full CRUD flow"
        category = "Work"

        create_res = notes_api.create_note(title, description, category)
        assert create_res.status == 200
        note_id = create_res.json()["data"]["id"]
        logger.info(f"CRUD: Created note {note_id}")

        # 2. READ (Verify data integrity)
        get_res = notes_api.request.get(
            f"{notes_api.base_url}/notes/{note_id}",
            headers={"x-auth-token": notes_api.token}
        )
        assert get_res.status == 200
        assert get_res.json()["data"]["title"] == title
        logger.info("CRUD: Read verification successful")

        # 3. UPDATE (Change state)
        # Assuming the client has an update_note or use raw request
        update_payload = {
            "title": f"{title} - UPDATED",
            "description": description,
            "category": category,
            "completed": True
        }
        update_res = notes_api.request.put(
            f"{notes_api.base_url}/notes/{note_id}",
            data=update_payload,
            headers={"x-auth-token": notes_api.token}
        )
        assert update_res.status == 200
        assert update_res.json()["data"]["completed"] is True
        logger.info("CRUD: Update verification successful")

        # 4. DELETE
        delete_res = notes_api.delete_note(note_id)
        assert delete_res.status == 200
        logger.info("CRUD: Delete successful")

        # 5. VERIFY DELETION (Final check)
        final_check = notes_api.request.get(
            f"{notes_api.base_url}/notes/{note_id}",
            headers={"x-auth-token": notes_api.token}
        )
        assert final_check.status == 404
        logger.info("CRUD: Final 404 verification successful. Note is truly gone.")