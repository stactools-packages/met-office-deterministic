import inspect
import json
import logging
import sys
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any, cast

import typer
from pystac import Item

from stactools.core.protocol import STACProvider


class OutputFormat(StrEnum):
    """Output format for create-items command."""

    NDJSON = "ndjson"
    GEOJSON = "geojson"


OutputOption = Annotated[
    Path | None,
    typer.Option(help="Write output to file instead of stdout"),
]
VerboseOption = Annotated[
    bool,
    typer.Option("--verbose", "-v", help="Enable verbose logging"),
]
QuietOption = Annotated[
    bool,
    typer.Option("--quiet", "-q", help="Suppress all logging"),
]
LogFileOption = Annotated[
    Path | None,
    typer.Option(help="Write logs to file instead of stderr"),
]
FormatOption = Annotated[
    OutputFormat,
    typer.Option(
        help="Output format: ndjson (one item per line) or geojson (FeatureCollection)"
    ),
]


def _setup_logging(verbose: bool, quiet: bool, log_file: Path | None) -> None:
    """Configure logging based on CLI options."""
    if quiet:
        level = logging.CRITICAL + 1  # Suppress all logs
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    handlers: list[logging.Handler] = []

    if log_file:
        handlers.append(logging.FileHandler(log_file))
    else:
        handlers.append(logging.StreamHandler(sys.stderr))

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        handlers=handlers,
        force=True,
    )


def _write_output(content: str, output_file: Path | None) -> None:
    """Write content to stdout or file."""
    if output_file:
        output_file.write_text(content)
        logging.info(f"Output written to {output_file}")
    else:
        print(content)


def _format_items_as_geojson(items: list[Item]) -> str:
    """Format items as GeoJSON FeatureCollection."""
    features = [item.to_dict() for item in items]
    feature_collection = {"type": "FeatureCollection", "features": features}
    return json.dumps(feature_collection)


def create_cli_app(provider: STACProvider, name: str, help_text: str) -> typer.Typer:
    """Generate Typer CLI app from a STACProvider implementation."""
    app = typer.Typer(name=name, help=help_text)
    cli_params = [
        inspect.Parameter(
            "output",
            inspect.Parameter.KEYWORD_ONLY,
            default=None,
            annotation=OutputOption,
        ),
        inspect.Parameter(
            "verbose",
            inspect.Parameter.KEYWORD_ONLY,
            default=False,
            annotation=VerboseOption,
        ),
        inspect.Parameter(
            "quiet",
            inspect.Parameter.KEYWORD_ONLY,
            default=False,
            annotation=QuietOption,
        ),
        inspect.Parameter(
            "log_file",
            inspect.Parameter.KEYWORD_ONLY,
            default=None,
            annotation=LogFileOption,
        ),
    ]

    # create-collection
    provider_sig = inspect.signature(provider.create_collection)
    provider_params = list(provider_sig.parameters.values())

    def create_collection_wrapper(
        output: OutputOption = None,
        verbose: VerboseOption = False,
        quiet: QuietOption = False,
        log_file: LogFileOption = None,
        **kwargs: dict[str, Any],
    ) -> None:
        _setup_logging(verbose, quiet, log_file)
        logging.debug(f"Creating collection with parameters: {kwargs}")

        collection = provider.create_collection(**kwargs)
        content = json.dumps(collection.to_dict())
        _write_output(content, output)

    new_sig = provider_sig.replace(parameters=provider_params + cli_params)
    cast(Any, create_collection_wrapper).__signature__ = new_sig

    app.command(name="create-collection")(create_collection_wrapper)

    # create-item
    provider_sig = inspect.signature(provider.create_item)
    provider_params = list(provider_sig.parameters.values())

    def create_item_wrapper(
        output: OutputOption = None,
        verbose: VerboseOption = False,
        quiet: QuietOption = False,
        log_file: LogFileOption = None,
        **kwargs: dict[str, Any],
    ) -> None:
        _setup_logging(verbose, quiet, log_file)
        logging.debug(f"Creating item with parameters: {kwargs}")

        item = provider.create_item(**kwargs)
        content = json.dumps(item.to_dict())
        _write_output(content, output)

    new_sig = provider_sig.replace(parameters=provider_params + cli_params)
    cast(Any, create_item_wrapper).__signature__ = new_sig

    app.command(name="create-item")(create_item_wrapper)

    # create-items
    provider_sig = inspect.signature(provider.create_items)
    provider_params = list(provider_sig.parameters.values())

    def create_items_wrapper(
        output: OutputOption = None,
        format: FormatOption = OutputFormat.NDJSON,
        verbose: VerboseOption = False,
        quiet: QuietOption = False,
        log_file: LogFileOption = None,
        **kwargs: dict[str, Any],
    ) -> None:
        _setup_logging(verbose, quiet, log_file)
        logging.debug(f"Creating items with parameters: {kwargs}")

        items = list(provider.create_items(**kwargs))
        logging.info(f"Generated {len(items)} items")

        if format == OutputFormat.GEOJSON:
            content = _format_items_as_geojson(items)
            _write_output(content, output)
        else:  # NDJSON
            if output:
                lines = [json.dumps(item.to_dict()) for item in items]
                content = "\n".join(lines)
                _write_output(content, output)
            else:
                for item in items:
                    print(json.dumps(item.to_dict()))

    format_param = inspect.Parameter(
        "format",
        inspect.Parameter.KEYWORD_ONLY,
        default=OutputFormat.NDJSON,
        annotation=FormatOption,
    )
    cli_params.insert(1, format_param)

    new_sig = provider_sig.replace(parameters=provider_params + cli_params)
    cast(Any, create_items_wrapper).__signature__ = new_sig

    app.command(name="create-items")(create_items_wrapper)

    return app
