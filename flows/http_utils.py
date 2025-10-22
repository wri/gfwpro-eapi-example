"""HTTP helper utilities."""

from __future__ import annotations

from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

REDIRECT_STATUSES = {301, 302, 303, 307, 308}


def post_with_redirect(
  url: str,
  *,
  headers: Optional[Dict[str, str]] = None,
  data: Optional[Any] = None,
  json: Optional[Any] = None,
  max_redirects: int = 5,
  session: Optional[requests.Session] = None,
  **kwargs: Any,
) -> requests.Response:
  """Perform a POST request, manually following HTTP redirects.

  Some endpoints respond with a redirect (e.g., 302) that targets a signed URL.
  The default instrumentation here retries the POST at the redirected location
  while keeping the payload identical.
  """

  request_fn = session.post if session else requests.post

  response = request_fn(
    url,
    headers=headers,
    data=data,
    json=json,
    allow_redirects=False,
    **kwargs,
  )

  redirects = 0
  while response.status_code in REDIRECT_STATUSES:
    location = response.headers.get("Location")
    if not location:
      raise RuntimeError("Redirect response missing Location header")

    # Handle relative redirect targets.
    redirected_url = urljoin(response.url, location)

    redirects += 1
    if redirects > max_redirects:
      raise RuntimeError("Exceeded maximum redirects when POSTing")

    response = request_fn(
      redirected_url,
      headers=headers,
      data=data,
      json=json,
      allow_redirects=False,
      **kwargs,
    )

  return response


