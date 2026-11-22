"""Minimal Flask server for the sample Print Queue API v1.0.

Jobs are stored in memory and are lost when the server stops.
"""
from datetime import datetime, timezone
from itertools import count

from flask import Flask, jsonify, request

app = Flask(__name__)
jobs = {}
job_ids = count(1)


def error(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status


@app.post("/api/v1/jobs")
def create_job():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error("invalid_request", "The request body must be a JSON object.", 400)

    file_name = data.get("file_name")
    if not isinstance(file_name, str) or not file_name.strip():
        return error("invalid_request", "file_name is required and must be a non-empty string.", 400)

    copies = data.get("copies", 1)
    if isinstance(copies, bool) or not isinstance(copies, int) or not 1 <= copies <= 50:
        return error("invalid_request", "copies must be an integer from 1 to 50.", 400)

    color = data.get("color", False)
    if not isinstance(color, bool):
        return error("invalid_request", "color must be true or false.", 400)

    job_id = f"job_{next(job_ids)}"
    jobs[job_id] = {
        "id": job_id,
        "file_name": file_name,
        "copies": copies,
        "color": color,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return jsonify(jobs[job_id]), 201


@app.get("/api/v1/jobs")
def list_jobs():
    return jsonify({"jobs": list(jobs.values())})


@app.get("/api/v1/jobs/<job_id>")
def get_job(job_id):
    job = jobs.get(job_id)
    if job is None:
        return error("job_not_found", f"No job with ID {job_id} exists.", 404)
    return jsonify(job)


@app.delete("/api/v1/jobs/<job_id>")
def cancel_job(job_id):
    job = jobs.get(job_id)
    if job is None:
        return error("job_not_found", f"No job with ID {job_id} exists.", 404)
    if job["status"] != "queued":
        return error("job_not_cancellable",
                     f"Job {job_id} has status '{job['status']}' and cannot be cancelled.", 409)
    job["status"] = "cancelled"
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
