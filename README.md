# VIGERITH

**Cross-Domain Security Intelligence and Systems Assurance**

**RAVENSCROFT INDUSTRIES**

VIGERITH is a security engineering research project focused on trustworthy telemetry, reproducible analysis and the assurance of software, firmware, embedded hardware and cyber-physical systems.

The objective is to turn individual observations into defensible findings without losing their identity, context or evidence. Structural validity is not proof of authenticity. Correlation is not causation.

RAVENSCROFT INDUSTRIES is the research identity. VanceBlackwood is a planned product initiative. VIGERITH complements SILIARCH in the broader engineering portfolio. These names describe intended project relationships, not legal incorporation or commercial availability.

## Branch Status

This branch preserves the initial event validator milestone from the merged [pull request #2](https://github.com/juliangreyravenscroft/vbi-vigerith/pull/2).

| Component | State |
| --- | --- |
| Basic event validator | Implemented |
| Baseline unit tests | 7 test methods |
| GitHub Actions | Configured |
| Versioned schema and strict JSON parser | Development branch only |
| Contract preflight and integrated ingestion | Development branch only |

The original baseline CI result is available in [GitHub Actions](https://github.com/juliangreyravenscroft/vbi-vigerith/actions/runs/42461015045). This does not establish CI success for the unmerged v0.2 work.

Current development is documented on [feature/event-schema-v0.2](https://github.com/juliangreyravenscroft/vbi-vigerith/tree/feature/event-schema-v0.2). Follow that branch for the strict parser, schema preflight and integrated event ingestion.

## Baseline Interface

`src/validate_event.py` exposes `validate_event(event)`. It returns a boolean. It requires an object with nonblank string values for `event_id`, `source` and `severity`. Severity must be `low`, `medium` or `high`. It does not reject all additional fields or establish source identity, event uniqueness or factual accuracy.

```python
from src.validate_event import validate_event

event = {
    "event_id": "evt-0001",
    "source": "lab-host-01",
    "severity": "low",
}

assert validate_event(event)
```

## Repository Guide

| Path | Responsibility |
| --- | --- |
| `src/__init__.py` | Python package initialization |
| `src/validate_event.py` | Baseline structural checks |
| `tests/test_validate_event.py` | Independent baseline tests |
| `.github/workflows/python-tests.yml` | Automated tests on the configured GitHub Actions events |
| `README.md` | Project status and research scope |

## Verification

Run from the repository root with Python 3.13 or a compatible interpreter.

```bash
python3 -m unittest discover -s tests -v
```

The baseline contains seven test methods. CI runs on pushes to `main` and pull requests targeting `main`. Test counts are not guarantees of complete coverage.

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
