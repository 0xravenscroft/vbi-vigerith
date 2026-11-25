
from src.event_json import parse_event_json
from src.event_schema import validate_event_schema


def ingest_event(raw: str) -> dict[str, object]:
    """Parse and structurally validate one security event."""
    event = parse_event_json(raw)
    validate_event_schema(event)
    return event
