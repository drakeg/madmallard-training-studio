# Mad Mallard Training Studio
[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://python.org/) [![Flask](https://img.shields.io/badge/Flask-web-black?logo=flask)](https://flask.palletsprojects.com/) [![SQLite](https://img.shields.io/badge/SQLite-storage-blue?logo=sqlite)](https://sqlite.org/) [![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docs.docker.com/compose/)

[![CI](https://github.com/drakeg/madmallard-training-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/drakeg/madmallard-training-studio/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/drakeg/madmallard-training-studio)](LICENSE) [![Issues](https://img.shields.io/github/issues/drakeg/madmallard-training-studio)](https://github.com/drakeg/madmallard-training-studio/issues) [![PRs](https://img.shields.io/github/issues-pr/drakeg/madmallard-training-studio)](https://github.com/drakeg/madmallard-training-studio/pulls)

Local-first walkthrough to approved staff training packages. Initial buyer: independent RV parks. Pilot price hypothesis: $549; demand not yet validated.

## Prototype
Manual entry of up to 15 steps, immutable saved step content, approval and text checklist/Mermaid source exports from the same revision. Recording upload, whisper.cpp, AI drafting, rendered diagrams, video and current-revision tracking are planned, not implemented.

Run `docker compose up --build -d` and open http://localhost:8098. Data persists in a named volume. Loopback only by default: this prototype has no authentication or CSRF protection and must not be exposed to customers or untrusted networks. Use fictional data only.

Try a fictional late arrival: check reservation, confirm assigned site, place welcome packet in lockbox, record handoff. Approve before exporting.

Tests: `python -m unittest -v` after installing requirements. See SPRINTS.md, BACKLOG.md and THIRD_PARTY.md. MIT original code.
