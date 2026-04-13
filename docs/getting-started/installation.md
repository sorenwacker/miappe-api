# Installation

## Requirements

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## Install from Source

```bash
git clone <repository-url>
cd metaseed
make install
```

## Development Installation

```bash
make dev
```

This installs dev dependencies (pytest, ruff, pre-commit) and docs dependencies (MkDocs).

## Verify Installation

```bash
uv run metaseed version
make test
```
