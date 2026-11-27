# VIGERITH

**Cross-Domain Security Intelligence and Systems Assurance**

**RAVENSCROFT INDUSTRIES**

VIGERITH is a security engineering research project focused on trustworthy telemetry, reproducible analysis and the assurance of software, firmware, embedded hardware and cyber-physical systems.

The objective is to turn individual observations into defensible findings without losing their identity, context or evidence. Structural validity is not proof of authenticity. Correlation is not causation.

RAVENSCROFT INDUSTRIES is the research identity. VanceBlackwood is a planned product initiative. VIGERITH complements SILIARCH in the broader engineering portfolio. These names describe intended project relationships, not legal incorporation or commercial availability.

## Implementation Status

This document describes [feature/event-schema-v0.2](https://github.com/0xravenscroft/vbi-vigerith/tree/feature/event-schema-v0.2), the active development branch. Check out that branch to reproduce the examples below. The default branch remains at the initial validator milestone until the development work is reviewed and merged.

| Component | Responsibility | State |
| --- | --- | --- |
| Baseline validator | Minimal event checks | Implemented |
| Strict JSON parser | Controlled conversion from JSON text | Implemented |
| Security event contract v0.2 | Versioned field constraints | Defined |
| Schema contract preflight | Inspect supported rules throughout the schema tree | Implemented |
| Event schema validator | Apply the supported rules to an event | Implemented |
| Event ingestion | Connect parsing and structural validation through one function | Implemented |
| Verification | Unit and integration tests | 49 test methods present, development CI pending |

The implementation inventory was checked at [49460300263d](https://github.com/0xravenscroft/vbi-vigerith/commit/49460300263d42d0fc75186c3c5ef954835e478d). Test counts reflect methods in the source, not a passing execution result.

## Architecture and Dependencies

```text
ingest_event(raw)
    parse_event_json(raw)
        UTF-8 size and JSON parsing checks
        Duplicate key and nonstandard constant rejection
        Return event dictionary
    validate_event_schema(event)
        Read security-event.v0.2.schema.json
        parse_event_json(schema_text)
        validate_schema_contract(schema)
            Walk nested properties and items
        _check(event, schema, "$")
            Apply supported event constraints
    Return structurally validated event dictionary
```

The sequence stops if any operation raises an exception. A schema loading or configuration error is not the same as an invalid event.

`event_ingestion.py` imports the parser and event validator. The event validator imports the parser and contract preflight. The contract module owns the supported keyword set and has no dependency on the event validator. The baseline validator remains independent of the new pipeline.

The JSON schema is a runtime dependency. The synthetic example is a test fixture, not a runtime dependency of ingestion. No network or database service is required by the current implementation.

## Repository Guide

| Path | Responsibility |
| --- | --- |
| `src/__init__.py` | Python package initialization |
| `src/validate_event.py` | Independent baseline validator |
| `src/event_json.py` | JSON text parsing and rejection policies |
| `src/schema_contract.py` | Supported keywords and recursive schema preflight |
| `src/event_schema.py` | Schema loading, preflight invocation and event validation |
| `src/event_ingestion.py` | Unified ingestion interface |
| `schemas/security-event.v0.2.schema.json` | Versioned event contract |
| `examples/security-event.v0.2.json` | Synthetic event fixture |
| `tests/test_validate_event.py` | Baseline tests |
| `tests/test_event_json.py` | Parsing and input boundaries |
| `tests/test_schema_contract.py` | Schema definition and preflight integration tests |
| `tests/test_event_schema.py` | Event field and boundary tests |
| `tests/test_event_ingestion.py` | Pipeline behavior and failure ordering |
| `.github/workflows/python-tests.yml` | Automated Python test workflow |

## Interface Boundaries

| Interface | Input | Success | Failure |
| --- | --- | --- | --- |
| `validate_event(event)` | Python object | Boolean | Returns false for rejected baseline input |
| `parse_event_json(raw)` | JSON text | Dictionary | TypeError or parsing and policy exceptions |
| `validate_schema_contract(schema)` | Parsed schema | None | Invalid or unsupported rule exception |
| `validate_event_schema(event)` | Parsed event | None | Schema loading, contract or event validation exception |
| `ingest_event(raw)` | JSON text | Structurally validated dictionary | Propagates exceptions without returning an accepted event |

The ingestion interface is the intended entry point for raw event text. Direct use of the event validator does not enforce the parser input policy on that event. Schema errors and invalid event data are not yet represented by separate application exception classes.

## Security Event Contract

| Field | Constraint or meaning |
| --- | --- |
| `schema_version` | Must equal `0.2.0` |
| `event_id` | Nonblank proposed record identifier |
| `event_name` | Nonblank readable label |
| `event_type` | Nonblank declared event type |
| `event_description` | Nonblank string, at most 1024 Unicode code points |
| `source` | Nonblank reported source identifier |
| `severity` | `low`, `medium` or `high` |
| `observed_at` | Date-time under the current validator policy, including a time zone |
| `evidence_refs` | Array of distinct nonblank strings, may be empty |

All nine fields are required. Additional properties are rejected by the current contract. The parser limits UTF-8 input to 16 KiB. This byte limit is independent of the description length constraint.

## Usage

From the repository root on the active development branch:

```python
from pathlib import Path
from src.event_ingestion import ingest_event

raw = Path("examples/security-event.v0.2.json").read_text(encoding="utf-8")
event = ingest_event(raw)
print(event["event_id"])
```

`ingest_event(raw)` returns a dictionary only after the parser, schema loading, contract preflight and event checks complete. Exceptions propagate to the caller. The returned dictionary is mutable and is not an authenticated or immutable evidence record.

## Verification

```bash
python3 -m json.tool examples/security-event.v0.2.json > /dev/null
python3 -m json.tool schemas/security-event.v0.2.schema.json > /dev/null
python3 -m unittest discover -s tests -v
```

| Test group | Methods |
| --- | ---: |
| Baseline validator | 7 |
| JSON parser | 11 |
| Event schema validator | 17 |
| Schema contract preflight | 9 |
| Event ingestion | 5 |
| Total | 49 |

The ingestion tests exercise valid event return, malformed JSON, duplicate keys, invalid severity and an invalid nested schema rule. Parser failures are checked to ensure they stop before event validation. Outstanding contract tests cover contradictory length limits, a nonboolean uniqueItems rule and additionalProperties set to true. Outstanding ingestion tests cover a nonobject root, a missing schema file and a missing required event field. These six cases are planned additions, not part of the current test inventory.

GitHub Actions uses Python 3.13 and runs on pushes to `main` and pull requests targeting `main`. The [latest inspected baseline CI run](https://github.com/0xravenscroft/vbi-vigerith/actions/runs/45661956680) completed seven tests on main. It does not verify this development branch. Merge readiness requires a passing run for the proposed changes and review of the remaining limitations.

## Known Limitations

The validator implements a restricted JSON Schema Draft 2020-12 subset. Schema preflight checks supported keywords and selected rule definitions, not every possible semantic inconsistency. Date-time handling is a project policy, not full RFC 3339 conformance. Python regular expression and equality semantics have not been comprehensively compared with the specification.

The parser rejects explicit nonstandard numeric constants but has not been validated against every numerical overflow, nesting or resource consumption case. The schema is read, parsed and checked for each event. The preflight checks rule definitions but does not authenticate the schema file or guarantee that every security constraint remains present. The byte limit is applied after the input has already been received as a Python string. No production throughput or latency claims are supported.

Structural validation does not authenticate the source, guarantee unique event identifiers, verify evidence references, establish event occurrence or prove the declared severity. No persistence, deduplication, event classification taxonomy or correlation engine is implemented.

## Research Direction

| Domain | Focus |
| --- | --- |
| Security telemetry and detection | Event contracts, ingestion, correlation and detection evaluation |
| Threat intelligence and forensics | Source evaluation, evidence provenance and reproducible findings |
| Malware intelligence and reverse engineering | Contained analysis and defensive indicators |
| Firmware and embedded security | Boot integrity, secure updates and hardware interfaces |
| FPGA and trusted hardware assurance | RTL security properties and hardware-software trust boundaries |
| Cyber-physical and UAS assurance | Unarmed simulation, read-only telemetry and resilience |
| AI-assisted analysis | Explainable assistance and measurable analytical quality |

These are research directions, not deployed capabilities.

## Research Boundaries

Use only owned, explicitly authorized or isolated laboratory environments. Keep malware analysis contained. Cyber-physical work is limited to unarmed simulation, read-only telemetry and assurance research. Live control and weapon-related capabilities are outside the current scope. Do not commit credentials, sensitive records, restricted materials or unreviewed research artifacts.

## Engineering Practice

Define the problem, interfaces, assumptions and acceptance criteria before implementation. Trace dependencies and affected files. Verify accepted inputs, rejection paths and regression behavior. Preserve reproducible evidence and document limitations before review. Keep implementation, verification and documentation aligned.

## Development Priorities

1. Complete contract and ingestion boundary tests and verify the development branch in CI.
2. Compare the supported schema subset with a reference Draft 2020-12 validator and document intentional differences.
3. Measure schema loading and validation costs before optimizing.
4. Establish event identity, source provenance and duplicate-delivery semantics.
5. Research correlation and detection with independently traceable records, controlled datasets and measured error rates.
6. Expand validated interfaces to isolated cross-domain assurance research.

No operational ingestion service, storage engine, correlation engine or public product release is claimed.
