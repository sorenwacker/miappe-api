# CLI Reference

Metaseed provides a command-line interface built with [Typer](https://typer.tiangolo.com/).

## Installation

The CLI is available after installing the package:

```bash
uv sync
uv run metaseed --help
```

## Commands

### version

Show the package version:

```bash
metaseed version
```

### entities

List available MIAPPE entities for a version:

```bash
metaseed entities --version 1.1
```

### validate

Validate a MIAPPE metadata file:

```bash
metaseed validate <file> --entity investigation --version 1.1
```

### template

Generate an empty template for an entity:

```bash
metaseed template investigation --output my_investigation.yaml --format yaml
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
metaseed convert input.yaml output.json --entity investigation
```

The format is determined by file extension (`.yaml`, `.yml`, or `.json`).

### ui

Launch the web interface:

```bash
metaseed ui --host 127.0.0.1 --port 8080
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
2. Environment variables (prefixed with `METASEED_`)
3. Configuration file (`metaseed.yaml` in current directory)
