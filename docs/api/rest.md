# REST API Reference

MIAPPE-API provides a REST API built with [FastAPI](https://fastapi.tiangolo.com/).

## Starting the Server

```bash
# Development server with auto-reload
uv run uvicorn miappe_api.api:app --reload

# Production server
uv run uvicorn miappe_api.api:app --host 0.0.0.0 --port 8000
```

## API Documentation

When the server is running, interactive documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Endpoints

!!! note "Under Development"
    REST API endpoints are being implemented. This page will be updated as endpoints become available.

### Planned Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/schemas` | List available schemas |
| `GET` | `/schemas/{version}` | Get schema for version |
| `POST` | `/validate` | Validate metadata |
| `POST` | `/convert` | Convert between formats |

## Authentication

!!! note "Future Feature"
    Authentication is not yet implemented. The API currently runs without authentication.

## Error Responses

All errors follow a standard format:

```json
{
  "detail": "Error message describing the problem",
  "status_code": 400
}
```

## Rate Limiting

!!! note "Future Feature"
    Rate limiting is not yet implemented.
