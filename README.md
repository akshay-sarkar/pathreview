# PathReview

**AI-powered portfolio review assistant** that helps early-career developers strengthen their professional portfolios.

PathReview analyzes GitHub profiles, resumes, and project repositories to generate structured, actionable feedback on portfolio completeness, project quality, skill gaps, and presentation improvements.

## Features

- **Profile Ingestion** — Upload a resume (PDF or Markdown), connect a GitHub profile, and link project repositories
- **RAG-Powered Feedback** — Retrieval-augmented generation produces specific, evidence-based feedback referencing your actual work
- **Multi-Tool Agent** — An AI agent orchestrates GitHub analysis, skill extraction, README scoring, and market comparison
- **Safety Guardrails** — Bias detection, content filtering, PII scrubbing, and prompt injection defense ensure feedback is constructive and safe
- **Web Dashboard** — View results, track improvement over time, and export shareable review summaries

## Quick Start

> **Windows users:** Use [Git Bash](https://git-scm.com/download/win) to run these commands, not PowerShell. See [docs/SETUP.md](docs/SETUP.md) for Windows-specific setup including installing `make`.

```bash
# Clone and enter the repo
git clone https://github.com/ascherj/pathreview.git
cd pathreview

# Configure environment (add your OPENROUTER_API_KEY to .env)
cp .env.example .env

# Start backing services — must be running before make setup
docker compose up -d

# Run first-time setup (installs deps, runs migrations, seeds DB, installs frontend)
make setup

# Start the application
make run
```

Then open http://localhost:5173 in your browser.

For detailed setup instructions including platform-specific notes, see [docs/SETUP.md](docs/SETUP.md).

## Architecture

PathReview is structured as a multi-service Python + React application with five major subsystems:

| Subsystem | Directory | Description |
|---|---|---|
| API Layer | `api/` | FastAPI REST API with authentication, validation, and rate limiting |
| Ingestion Pipeline | `ingestion/` | Document parsing, chunking, and embedding generation |
| RAG System | `rag/` | Hybrid retrieval, LLM-based review generation, and quality evaluation |
| Agent System | `agent/` | Multi-tool orchestration with planning, state management, and error handling |
| Safety Layer | `safety/` | Content filtering, bias detection, PII scrubbing, and prompt defense |
| Frontend | `frontend/` | React + TypeScript dashboard with Vite |

For a detailed architecture overview, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contributing

We welcome contributions! Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) before submitting a pull request.

## Development

```bash
make help          # Show all available commands
make test-unit     # Run unit tests (~30 seconds)
make check         # Run linter + formatter + type checker
make run           # Start the dev servers
```

## License

MIT


You have reusable internal components (filters, tables, storage, and other site-specific pieces). Those get composed and exposed cleanly through page objects. The pages then become the stable interface that test cases actually call.
With that structure in mind, here are the most useful skills to add, tuned specifically to your setup:
1.  Component Quality skill Reviews the internal building blocks (filters, tables, storage helpers, etc.) for consistency, proper typing, error handling, and reusability so the foundation stays solid.
2.  Page Composition skill Checks that pages correctly assemble and expose those components — correct method signatures, no leaking internal details, consistent patterns across all pages.
3.  Locator & Interaction skill Focuses on how components and pages interact with the DOM — prefers resilient locators and clean action methods that tests can rely on.
4.  Test Case Usage skill Looks at the generated Playwright tests and verifies they only talk to the page layer (not diving into components or raw locators), keeping the tests readable and maintainable.
5.  Cross-layer Consistency skill Makes sure naming, patterns, and contracts stay aligned from component → page → test case so the whole stack doesn’t drift over time.
These five sit nicely on top of the framework skill and TypeScript skill you already have. The Component Quality and Page Composition ones will probably give you the biggest leverage right now.