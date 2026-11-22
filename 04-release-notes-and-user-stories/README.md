# Release notes and user stories

> *Sample note:* This sample builds on the fictional [Print Queue API](../01-api-reference/README.md). Version 1.1 is imagined for this exercise.

This sample shows how I work in an Agile team. It has two parts: user stories with acceptance criteria that guide development, and the release notes that tell customers what changed.

# Part 1: User stories

## Story 1: Duplex printing

*As a* developer using the Print Queue API,
*I want to* request double-sided printing when I create a job,
*so that* my application can save paper for long documents.

*Acceptance criteria*

- The create job request accepts an optional `duplex` field with a value of `true` or `false`.
- If `duplex` is not provided, it defaults to `false`.
- The job object returned by every endpoint includes the `duplex` field.
- A value that is not `true` or `false` returns a `400 invalid_request` error with a clear message.
- The API reference documents the new field with an example.

## Story 2: Filter jobs by status

*As a* developer using the Print Queue API,
*I want to* list only jobs with a specific status,
*so that* I do not need to download and filter all jobs in my application.

*Acceptance criteria*

- `GET /jobs` accepts an optional `status` query parameter.
- Allowed values are `queued`, `printing`, `completed`, and `cancelled`.
- A value that is not allowed returns a `400 invalid_request` error that lists the allowed values.
- If `status` is omitted, all jobs are returned, as before.
- The API reference documents the parameter with an example.

## Documentation impact

| Page | Change needed |
|------|---------------|
| API reference: Create a print job | Add `duplex` to the request body table and examples. |
| API reference: The job object | Add `duplex` to the field table. |
| API reference: List print jobs | Add the `status` query parameter and an example. |
| Quickstart | Optional: mention `duplex` in Next steps. |
| Release notes | Add the entry below. |

# Part 2: Release notes

# Print Queue API 1.1 release notes

*Release date:* [Add date]

Version 1.1 adds double-sided printing and lets you filter the job list by status. It does not change any existing behavior. Applications built for version 1.0 continue to work without changes.

# New features

- *Double-sided printing.* When you create a job, you can now set `duplex` to `true` to print on both sides of the paper. The default is `false`. The `duplex` field also appears in every job object.
- *Filter jobs by status.* You can now add the `status` parameter to `GET /jobs` to return only jobs with that status. For example, `GET /jobs?status=queued` returns only queued jobs.

# Improvements

- Error messages for invalid requests now name the field that caused the error.

# Upgrade notes

No action is required. To use the new features, add `duplex` to your create job requests or `status` to your list requests. See the [API reference](../01-api-reference/README.md) for details.

---


