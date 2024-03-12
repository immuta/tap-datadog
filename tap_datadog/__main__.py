"""datadog entry point."""

from __future__ import annotations

from tap_datadog.tap import Tapdatadog

Tapdatadog.cli()
