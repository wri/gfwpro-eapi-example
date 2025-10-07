# GFW Pro External API – Plain Python Reference

This repository contains lightweight Python scripts that interact directly with the Global Forest Watch (GFW) Pro External API. Each script focuses on a specific workflow so partners can explore, test, and extend the API without any framework overhead. For the latest product documentation (including background, sample curl commands, release notes, and attribution requirements) visit the [GFW Pro API Confluence space](https://globalforestwatch.atlassian.net/wiki/spaces/GFWPRO/pages/123456789/GFW+Pro+API+Documentation).

## Endpoint Reference

All endpoints are rooted at `GFWPRO_BASE_URL` (default `https://pro.globalforestwatch.org/api/v1`).

| Method & Path | Description |
| --- | --- |
| `POST /prepare_upload` | Request a pre-signed S3 URL for uploading list data. Requires `userEmail` and `fileType` (`csv`, `xlsx`, `geojson`, `zip`, `kml`). |
| `PUT <signed-url>` | Upload the actual file directly to S3 using the signed URL returned above. |
| `POST /list/upload_new` | Create a new list and optionally trigger analyses (pass `analysisIDs` as a comma-separated string; commodity is required per 01/09/25 change). |
| `GET /list` | Paginated retrieval of lists for the organization (`pageSize`, `pageNum`). |
| `GET /list/{listId}` | Retrieve details/metadata for a single list. |
| `POST /list/{listId}/delete` | Delete a list; body must include `userEmail` for auditing. |
| `GET /list/{listId}/analysis/{analysisId}/status` | Check analysis progress. Possible values include `Pending`, `Running`, `Completed`, `Error`, `Active`, `Expired`. |
| `POST /list/{listId}/analysis/{analysisId}/analyze` | Add or re-run an analysis (e.g., GHG, FCD) for an existing list. Requires `userEmail`. |
| `POST /list/{listId}/analysis/{analysisId}/generate` | Generate downloadable results (or verifiable credentials for DefReport). |
| resultUrl (from status) | Download the ZIP bundle once analysis has completed/been generated. |

## Scripts

| Script | Endpoints Covered | Description |
| --- | --- | --- |
| `flows/upload_and_list.py` | `/prepare_upload`, signed URL `PUT`, `/list/upload_new`, `/list/{id}/analysis/{analysisId}/status`, `resultUrl` download | Full upload → analysis workflow with polling and automatic download; exits immediately if upstream reports `Error`. |
| `flows/alerts_analysis.py` | `/prepare_upload`, signed URL `PUT`, `/list/upload_new`, `/list/{id}/analysis/Alerts/generate` | Demonstrates triggering Alerts report generation with date filters. |
| `flows/ghg_analysis.py` | `/prepare_upload`, signed URL `PUT`, `/list/upload_new`, `/list/{id}/analysis/GHG/analyze` | Illustrates running a GHG analysis with commodity / yield settings. |
| `flows/list_management.py` | `/list`, `/list/{id}`, `/list/{id}/delete` | Enumerates lists, fetches details, and optionally deletes a list. |
| `flows/poll_analysis.py` | `/list/{id}/analysis/{analysisId}/status`, `resultUrl` download | Reusable polling helper that saves results once an analysis completes. |

The `sample_data/example.csv` file contains ready-to-use coordinates featuring the expected column headers.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the environment variables required for your workflow (see table below), then run the desired script, e.g.

```bash
python flows/upload_and_list.py
```

## Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `GFWPRO_BASE_URL` | API base URL | `https://pro.globalforestwatch.org/api/v1` |
| `GFWPRO_API_TOKEN` | API key sent as `x-api-key` | *(required)* |
| `USER_EMAIL` | Contact email used in upload / delete requests | `demo@example.com` |
| `CSV_PATH` | Path to upload file | `sample_data/example.csv` |
| `COMMODITY` | Commodity name (free form, required by API) | `Cocoa Generic` |
| `ANALYSIS` | Analysis ID (`FCD`, `Alerts`, `DefReport`, `GHG`) | `FCD` |
| `ALERT_START_DATE`, `ALERT_END_DATE` | Alerts date range | `2024-01-01`, `2024-12-31` |
| `GHG_YIELD` | Yield for GHG analysis (kg/ha) | `0.5` |
| `LIST_ID`, `ANALYSIS_ID` | Used by `poll_analysis.py` | *(none)* |
| `DELETE_LIST` | Set to `1` to delete the first list in `list_management.py` | `0` |

Scripts exit with a non-zero status if the upstream service reports a failure (e.g., analysis status `Error`). This makes them automation-friendly and easy to integrate with CI/CD or AI agents.

## Sample Data

`sample_data/example.csv` is a valid upload template:

```
Location Name,Latitude,Longitude,Analysis Radius,Analysis Area,Company,Contact
A1,-8.933,-52.138,0.5,,K,Jeff
A2,65.048,55.835,0.5,,L,James
A3,62.993,80.355,0.5,,M,Jessica
A4,50.81,116.9778,0.5,,N,Jarome
A5,35.743,-89.172,0.5,,O,Jake
A6,16.801,43.889,0.5,,P,Jack
```

Update or replace the file to test your own lists.

## Troubleshooting & Tips

- **401 Unauthorized** – ensure `GFWPRO_API_TOKEN` matches the environment (QA, staging, prod) and is passed as `x-api-key`.
- **4xx validation errors** – confirm required body fields such as `analysisIDs` (CSV string) and commodity spelling (per API release notes). Refer to the Confluence documentation for schema changes.
- **Analysis status `Error`** – indicates the upstream service encountered an issue (invalid geometry, data limits, etc.). Collect the `listId` and consult service logs or retry with a reduced dataset.
- **Protocol-relative URLs** (e.g., `//localhost:3335/...`) are normal in some environments; scripts normalize them to `http://` automatically.

## Security Guidance

- Rotate API tokens every 90 days.
- Restrict tokens to least-privilege roles and keep them in secure storage (env vars, secret managers).
- Always use HTTPS endpoints in production.

## AI Assistant Notes

- Each script already prints contextual messages; they can be chained or extended by AI agents without additional refactoring.
- Non-zero exit on error simplifies failure detection.
- For deeper background, release notes, and curl examples, see the [GFW Pro API Confluence space](https://globalforestwatch.atlassian.net/wiki/spaces/GFWPRO/pages/123456789/GFW+Pro+API+Documentation).
