# CLI Reference

MIAPPE-API provides a command-line interface built with [Typer](https://typer.tiangolo.com/).

## Installation

The CLI is available after installing the package:

```bash
uv sync
uv run miappe --help
```

## Commands

### version

Show the package version:

```bash
miappe version
```

### entities

List available MIAPPE entities for a version:

```bash
miappe entities --version 1.1
```

### validate

Validate a MIAPPE metadata file:

```bash
miappe validate <file> --entity investigation --version 1.1
```

### template

Generate an empty template for an entity:

```bash
miappe template investigation --output my_investigation.yaml --format yaml
```

Options:

| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output file path (prints to stdout if not specified) |
| `--format`, `-f` | Output format: `yaml` (default) or `json` |
| `--version`, `-v` | MIAPPE version (default: 1.1) |

### convert

Convert between YAML and JSON formats:

```bash
miappe convert input.yaml output.json --entity investigation
```

The format is determined by file extension (`.yaml`, `.yml`, or `.json`).

### ui

Launch the NiceGUI web interface:

```bash
miappe ui --host 127.0.0.1 --port 8080
```

Options:

| Option | Description |
|--------|-------------|
| `--host`, `-h` | Host to bind to (default: 127.0.0.1) |
| `--port`, `-p` | Port to bind to (default: 8080) |

The web interface provides:

- Visual entity browser organized by hierarchy
- Dynamic forms generated from YAML specifications
- Nested entity creation (e.g., add Studies to an Investigation)
- Validation feedback
- Support for both MIAPPE and ISA profiles

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
