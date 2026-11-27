# VIGERITH

**Cross-Domain Security Intelligence and Systems Assurance**

**RAVENSCROFT INDUSTRIES**

VIGERITH is a security engineering research project focused on trustworthy telemetry, reproducible analysis and the assurance of software, firmware, embedded hardware and cyber-physical systems.

The objective is to turn individual observations into defensible findings without losing their identity, context or evidence. Structural validity is not proof of authenticity. Correlation is not causation.

RAVENSCROFT INDUSTRIES is the research identity. VanceBlackwood is a planned product initiative. VIGERITH complements SILIARCH in the broader engineering portfolio. These names describe intended project relationships, not legal incorporation or commercial availability.

## Editorial Review Snapshot

This branch supports [draft pull request #3](https://github.com/0xravenscroft/vbi-vigerith/pull/3). Its source is an older development snapshot. It does not contain the schema contract preflight or unified ingestion module.

| Component | State in this snapshot |
| --- | --- |
| Baseline event validator | Implemented |
| Strict JSON parser | Implemented |
| Security event schema v0.2 | Defined |
| Event schema validator | Implemented |
| Schema contract preflight | Not present |
| Unified ingestion interface | Not present |
| Test inventory | 36 methods, including a repeated description length test |

The active [development branch](https://github.com/0xravenscroft/vbi-vigerith/tree/feature/event-schema-v0.2) supersedes this snapshot. It contains the contract preflight and unified ingestion interface, with 49 test methods by source inspection. Development CI is pending. The [default branch](https://github.com/0xravenscroft/vbi-vigerith/tree/main) remains at the initial validator milestone.

## Snapshot Architecture

```text
Raw JSON text
    parse_event_json(raw)
    validate_event_schema(event)
        Read and parse the versioned schema
        Apply supported rules to the event
```

The caller must invoke parsing and validation in sequence in this snapshot. Unsupported keywords are checked only in rules visited during event validation. The active development branch adds a separate recursive preflight and a unified entry point.

| Path | Responsibility |
| --- | --- |
| `src/validate_event.py` | Independent baseline validator |
| `src/event_json.py` | JSON parsing and input policy |
| `src/event_schema.py` | Schema loading and structural validation |
| `schemas/security-event.v0.2.schema.json` | Versioned event contract |
| `examples/security-event.v0.2.json` | Synthetic test fixture |
| `tests/` | Baseline, parser and schema tests |
| `.github/workflows/python-tests.yml` | Automated test workflow |

## Verification

Run from this branch's repository root.

```bash
python3 -m unittest discover -s tests -v
```

The source contains seven baseline tests, eleven parser tests and eighteen event schema tests. These counts do not establish a successful run. The current development usage examples and test inventory belong to the active development branch.

## Change Control

The active development README is maintained directly on its own branch. This editorial README describes only the historical snapshot. Do not merge this snapshot-specific document over the active development README. No source code merge or release is implied by the editorial review.

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
