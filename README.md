# Kelvra Space (`kelvra-space`)

Umbrella platform dashboard, ecosystem telemetry poller, and service shell for the Kelvra developer suite.

Runs independently on port **8090**.

## Overview

Kelvra Space serves as the single pane of glass aggregating live health, telemetry, and capabilities across:
- **Kelvra Voice** (`http://localhost:8765`) — Speech intelligence and on-device dictation.
- **Kelvra Bench** (`http://localhost:8099`) — Multi-agent swarm orchestrator and PR review workbench.
- **Kelvra Security** (`http://localhost:8100`) — AI prompt guardrail and pre-commit secret leak microservice.

## Running Locally

```bash
uvicorn src.server:app --host 127.0.0.1 --port 8090
```

## Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```
