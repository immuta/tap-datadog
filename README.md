# tap-datadog

`tap-datadog` is a Singer tap for datadog.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

Install from PyPi:

```bash
pipx install tap-datadog
```

Install from GitHub:

```bash
pipx install git+https://github.com/immuta/tap-datadog.git@main
```

## Configuration

### Accepted Config Options

## Settings

| Setting | Required | Default | Description |
|:--------|:--------:|:-------:|:------------|
| api_key | True     | None    | The API Key, generated in Datadog UI and stored in 1Password |
| application_key | True     | None    | The Application Key, generated in Datadog UI and stored in 1Password |
| slos | True     | None    | SLOs to replicate |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-datadog --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

An API Key and Application Key from Datadog must be provided in the `config.json`.

## Usage

You can easily run `tap-datadog` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-datadog --version
tap-datadog --help
tap-datadog --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-datadog` CLI interface directly using `poetry run`:

```bash
poetry run tap-datadog --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-datadog
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-datadog --version
# OR run a test `elt` pipeline:
meltano elt tap-datadog target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
