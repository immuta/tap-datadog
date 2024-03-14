"""Stream type classes for tap-datadog."""

from __future__ import annotations

import sys
import typing as t

from tap_datadog.client import DatadogStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources



SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"

class SLOStream(DatadogStream):
    """Define custom stream."""

    path = "slo/{id}/history"
    primary_keys: t.ClassVar[list[str]] = ["slo_id"]
    replication_key = "to_ts"
    is_sorted = True
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema_filepath = SCHEMAS_DIR / "slo_history.json"
