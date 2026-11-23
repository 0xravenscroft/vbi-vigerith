
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.event_json import parse_event_json
from src.event_schema import SCHEMA_PATH, validate_event_schema
from src.schema_contract import validate_schema_contract

FIXTURE = SCHEMA_PATH.parents[1] / "examples" / "security-event.v0.2.json"


class SchemaContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = parse_event_json(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )

    def test_current_schema_is_supported(self):
        self.assertIsNone(validate_schema_contract(self.schema))

    def test_unknown_nested_keyword_is_rejected(self):
        self.schema["properties"]["evidence_refs"]["items"]["minLenght"] = 1
        with self.assertRaisesRegex(NotImplementedError, "minLenght"):
            validate_schema_contract(self.schema)

    def test_bad_regex_is_rejected(self):
        self.schema["properties"]["event_name"]["pattern"] = "["
        with self.assertRaisesRegex(ValueError, "invalid pattern"):
            validate_schema_contract(self.schema)

    def test_boolean_minimum_is_rejected(self):
        self.schema["properties"]["event_name"]["minLength"] = True
        with self.assertRaisesRegex(ValueError, "minLength"):
            validate_schema_contract(self.schema)

    def test_duplicate_required_name_is_rejected(self):
        self.schema["required"].append("event_id")
        with self.assertRaisesRegex(ValueError, "duplicate names"):
            validate_schema_contract(self.schema)

    def test_malformed_required_is_rejected(self):
        self.schema["required"] = ["event_id", 3]
        with self.assertRaisesRegex(ValueError, "required must be"):
            validate_schema_contract(self.schema)

    def test_invalid_items_rule_is_rejected(self):
        self.schema["properties"]["evidence_refs"]["items"] = "string"
        with self.assertRaisesRegex(ValueError, "schema rule must be an object"):
            validate_schema_contract(self.schema)

    def test_unsupported_dialect_is_rejected(self):
        self.schema["$schema"] = "https://example.org/other-schema"
        with self.assertRaisesRegex(ValueError, "Unsupported schema dialect"):
            validate_schema_contract(self.schema)

    def test_event_validation_calls_contract_preflight(self):
        event = parse_event_json(FIXTURE.read_text(encoding="utf-8"))
        self.schema["properties"]["evidence_refs"]["items"]["minLenght"] = 1

        with TemporaryDirectory() as directory:
            schema_file = Path(directory) / "schema.json"
            schema_file.write_text(
                json.dumps(self.schema), encoding="utf-8"
            )

            with patch("src.event_schema.SCHEMA_PATH", schema_file):
                with self.assertRaisesRegex(NotImplementedError, "minLenght"):
                    validate_event_schema(event)
