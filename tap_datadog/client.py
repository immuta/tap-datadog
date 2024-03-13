"""REST client handling, including datadogStream base class."""

from __future__ import annotations

import sys
from typing import Any, Callable, Iterable

import requests
from datetime import datetime, timedelta
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class DatadogStream(RESTStream):
    """datadog stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("url_base", "https://api.datadoghq.com/api/v1/")

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        headers["DD-API-KEY"] = self.config.get("api_key", "").strip()  # noqa: ERA001
        headers["DD-APPLICATION-KEY"] = self.config.get("application_key", "").strip()  # noqa: ERA001
        return headers

    def get_url(self, context: dict | None) -> str:
        url = super().get_url(context)
        return url.format(id = self.slo.get("id"))

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        to_ts = datetime.now()
        from_ts = datetime.now() - timedelta(days=1)
        params["from_ts"] = int(from_ts.timestamp())
        params["to_ts"] = int(to_ts.timestamp())
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """           
        data = response.json()["data"]
        yield from extract_jsonpath(self.records_jsonpath, input=data)
