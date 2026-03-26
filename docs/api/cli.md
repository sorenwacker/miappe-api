# CLI Reference

MIAPPE-API provides a command-line interface built with [Typer](https://typer.tiangolo.com/).

## Installation

The CLI is available after installing the package:

```bash
uv sync
uv run miappe --help
```

## Commands

!!! note "Under Development"
    CLI commands are being implemented. This page will be updated as commands become available.

### Planned Commands

```bash
# Validate a metadata file
miappe validate <file>

# Convert between formats
miappe convert <input> <output>

# Generate empty template
miappe template <entity-type> --version 1.1

# Start REST API server
miappe serve
```

## Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help message and exit |

## Configuration

The CLI reads configuration from:

1. Command-line arguments
2. Environment variables (prefixed with `MIAPPE_`)
3. Configuration file (`miappe.yaml` in current directory)
