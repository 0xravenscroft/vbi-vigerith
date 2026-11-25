
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.event_ingestion import ingest_event
from src.event_schema import SCHEMA_PATH

FIXTURE = (
    SCHEMA_PATH.parents[1]
    / "examples"
    / "security-event.v0.2.json"
)


class EventIngestionTests(unittest.TestCase):
    def setUp(self):
        self.raw = FIXTURE.read_text(encoding="utf-8")

    def test_valid_event_is_returned(self):
        self.assertEqual(
            ingest_event(self.raw),
            json.loads(self.raw),
        )

    def test_malformed_json_stops_before_validation(self):
        with patch("src.event_ingestion.validate_event_schema") as validator:
            with self.assertRaises(json.JSONDecodeError):
                ingest_event('{"event_id":')
            validator.assert_not_called()

    def test_duplicate_key_stops_before_validation(self):
        raw = '{"event_id":"first","event_id":"second"}'

        with patch("src.event_ingestion.validate_event_schema") as validator:
            with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
                ingest_event(raw)
            validator.assert_not_called()

    def test_invalid_severity_is_rejected(self):
        event = json.loads(self.raw)
        event["severity"] = "critical"

        with self.assertRaisesRegex(
            ValueError, r"\$\.severity: unsupported value"
        ):
            ingest_event(json.dumps(event))

    def test_invalid_contract_is_rejected(self):
        schema = json.loads(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )

        schema["properties"]["evidence_refs"]["items"]["minLenght"] = 1

        with TemporaryDirectory() as directory:
            path = Path(directory) / "schema.json"
            path.write_text(json.dumps(schema), encoding="utf-8")

            with patch("src.event_schema.SCHEMA_PATH", path):
                with self.assertRaisesRegex(NotImplementedError, "minLenght"):
                    ingest_event(self.raw)
