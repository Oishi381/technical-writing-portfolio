# Print Queue API reference

> *Sample note:* The Print Queue API is fictional. This page is a documentation sample.
> The machine-readable specification is in [`openapi.yaml`](openapi.yaml). You can paste it into the [Swagger Editor](https://editor.swagger.io) to explore it.

*Audience:* Developers who want to submit and manage print jobs from their own applications.

The Print Queue API is a REST API that accepts and returns JSON. Use it to create print jobs, check their status, and cancel jobs that have not started printing.

# Base URL

```
http://localhost:5000/api/v1
```

# Authentication

Version 1.0 does not require authentication. It is intended for local development only.

# Errors

When a request fails, the API returns an HTTP status code and a JSON body in this format:

```json
{
  "error": {
    "code": "job_not_found",
    "message": "No job with ID job_99 exists."
  }
}
```

| HTTP status | Error code | Meaning |
|-------------|------------|---------|
| 400 | `invalid_request` | The request body is missing or contains an invalid value. |
| 404 | `job_not_found` | No job exists with the ID you specified. |
| 409 | `job_not_cancellable` | The job is no longer queued, so it cannot be cancelled. |

# The job object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique job ID, for example `job_1`. |
| `file_name` | string | Name of the file to print. |
| `copies` | integer | Number of copies, from 1 to 50. |
| `color` | boolean | `true` for color printing, `false` for black and white. |
| `status` | string | One of `queued`, `printing`, `completed`, or `cancelled`. |
| `created_at` | string | Time the job was created, in ISO 8601 format (UTC). |

# Endpoints

# Create a print job

`POST /jobs`

Creates a job and places it in the queue.

*Request body*

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `file_name` | string | Yes | None | Name of the file to print. Must not be empty. |
| `copies` | integer | No | `1` | Number of copies, from 1 to 50. |
| `color` | boolean | No | `false` | Set to `true` for color printing. |

*Example request*

```bash
curl -X POST http://localhost:5000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"file_name": "report.pdf", "copies": 2, "color": false}'
```

*Example response* (`201 Created`)

```json
{
  "color": false,
  "copies": 2,
  "created_at": "2026-01-15T09:30:00+00:00",
  "file_name": "report.pdf",
  "id": "job_1",
  "status": "queued"
}
```

*Possible errors:* `400 invalid_request`, for example when `file_name` is missing or `copies` is greater than 50.

# List print jobs

`GET /jobs`

Returns all jobs, oldest first.

*Example request*

```bash
curl http://localhost:5000/api/v1/jobs
```

*Example response* (`200 OK`)

```json
{
  "jobs": [
    {
      "color": false,
      "copies": 2,
      "created_at": "2026-01-15T09:30:00+00:00",
      "file_name": "report.pdf",
      "id": "job_1",
      "status": "queued"
    }
  ]
}
```

# Get a print job

`GET /jobs/{job_id}`

Returns one job.

| Parameter | Location | Description |
|-----------|----------|-------------|
| `job_id` | Path | The job ID, for example `job_1`. |

*Example request*

```bash
curl http://localhost:5000/api/v1/jobs/job_1
```

*Example response* (`200 OK`): the job object.

*Possible errors:* `404 job_not_found`.

# Cancel a print job

`DELETE /jobs/{job_id}`

Cancels a job that is still queued. The job is not removed. Its status changes to `cancelled`.

*Example request*

```bash
curl -X DELETE http://localhost:5000/api/v1/jobs/job_1
```

*Response:* `204 No Content`. The response has no body.

*Possible errors:* `404 job_not_found`, `409 job_not_cancellable`.


