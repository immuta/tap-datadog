"""datadog tap class."""

from __future__ import annotations
from re import sub

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_datadog import streams


class Tapdatadog(Tap):
    """datadog tap class."""

    name = "tap-datadog"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The API Key, generated in Datadog UI and stored in 1Password",
        ),
        th.Property(
            "application_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The Application Key, generated in Datadog UI and stored in 1Password",
        ),
        th.Property(
            "slos",
            th.ArrayType(th.ObjectType(
                th.Property("name", th.StringType, description="The name of the SLO"),
                th.Property("id", th.StringType, description="The id of the SLO"),
            )),
            required=True,
            description="SLOs to replicate",
        ),
        th.Property(
            "from_ts",
            th.NumberType,
            required=False,
            description="The Unix timestamp to start the extract from, by default now - 1 day",
        ),
        th.Property(
            "to_ts",
            th.NumberType,
            required=False,
            description="The Unix timestamp to start the extract to, by default now",
        ),
        th.Property(
            "slos",
            th.ArrayType(th.ObjectType(
                th.Property("name", th.StringType, description="The name of the SLO"),
                th.Property("id", th.StringType, description="The id of the SLO"),
            )),
            required=True,
            description="SLOs to replicate",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.datadogStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """

        def snake_case(s):
            # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
            # and add an underscore between words, finally convert the result to lowercase
            return '_'.join(
                sub('([A-Z][a-z]+)', r' \1',
                sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()

        result = []
        for slo in self.config.get("slos"):
            stream_name = "slo_{name}".format(name = snake_case(slo.get("name")))
            stream = streams.SLOStream(tap=self, name=stream_name)
            stream.slo = slo
            result.append(stream)
        return result


if __name__ == "__main__":
    Tapdatadog.cli()
