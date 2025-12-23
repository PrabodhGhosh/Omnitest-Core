import json
import os
from jsonschema import validate, ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

def validate_json_schema(data, schema_file_name):
    """
    Validates a JSON object against a schema file in data/schemas/
    """
    # 1. Get the directory of the current file (utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Go up one level to the Project Root
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    # 3. Build the absolute path to the schema file
    schema_path = os.path.join(project_root, "data", "schemas", schema_file_name)

    logger.info(f"DEBUG: Looking for schema at: {schema_path}")

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at expected Windows path: {schema_path}")

    with open(schema_path, 'r') as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        logger.info(f"SCHEMA VALIDATION: Passed for {schema_file_name}")
        return True
    except ValidationError as e:
        logger.error(f"SCHEMA VALIDATION FAILED: {e.message}")
        # Raise an exception so the test fails immediately on contract breach
        raise AssertionError(f"API Contract Breach in {schema_file_name}: {e.message}")