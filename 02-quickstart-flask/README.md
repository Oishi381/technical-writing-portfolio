# Quickstart: Run the Print Queue API with Flask

> **Sample note:** The Print Queue API is fictional. This tutorial is a documentation sample. All code in this folder was run and tested.

**Audience:** Developers who know basic Python and want to try the API on their own computer.
**Time:** About 10 minutes.

In this quickstart, you start a local Flask server that implements the [Print Queue API](../01-api-reference/README.md), then create, check, and cancel a print job.

## Before you begin

You need:

- Python 3.9 or later. To check your version, run `python3 --version`.
- `pip`, the Python package installer.
- `curl`, or another tool for sending HTTP requests.

## Step 1: Set up the project

1. Open a terminal and go to this folder:

   ```bash
   cd 02-quickstart-flask
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows, run `venv\Scripts\activate` instead.

3. Install Flask:

   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Start the server

Run the application:

```bash
python app.py
```

The terminal shows that the server is running at `http://127.0.0.1:5000`. Leave this terminal open and use a second terminal for the remaining steps.

## Step 3: Create a print job

Send a `POST` request to create a job:

```bash
curl -X POST http://localhost:5000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"file_name": "report.pdf", "copies": 2}'
```

The server responds with the new job. Its status is `queued`:

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

Your `created_at` value will be different. Note the `id`. You use it in the next steps.

## Step 4: Check the job

Replace `job_1` with your job ID if it is different:

```bash
curl http://localhost:5000/api/v1/jobs/job_1
```

The server returns the same job object.

## Step 5: Cancel the job

```bash
curl -i -X DELETE http://localhost:5000/api/v1/jobs/job_1
```

The `-i` option shows the response headers. The first line is `HTTP/1.1 204 NO CONTENT`. A `204` response has no body.

Check the job again. Its status is now `cancelled`:

```bash
curl http://localhost:5000/api/v1/jobs/job_1
```

## Step 6: See an error response

Try to create a job with an invalid number of copies:

```bash
curl -X POST http://localhost:5000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"file_name": "report.pdf", "copies": 99}'
```

The server returns a `400` error:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "copies must be an integer from 1 to 50."
  }
}
```

## Troubleshooting

| Problem | Cause and solution |
|---------|--------------------|
| `Address already in use` | Another program is using port 5000. Stop that program, or change the port: `app.run(debug=True, port=5001)`. |
| `command not found: python3` | Python is not installed or is not on your PATH. On Windows, try `python` instead of `python3`. |
| `404 job_not_found` | The job ID does not exist. Jobs are stored in memory and are lost when you stop the server. |

## Next steps

- Read the full [API reference](../01-api-reference/README.md).
- Open [`app.py`](app.py) and read how each endpoint validates input.
- Add a new field, such as `duplex`, and update the reference to match.

---

*Authoring note: [Add your own note here. For example: "I ran every command on my own computer and corrected the expected output. An AI assistant helped draft the first version."]*
