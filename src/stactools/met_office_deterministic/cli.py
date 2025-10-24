from importlib.metadata import metadata

from stactools.core.cli import create_cli_app
from stactools.met_office_deterministic.provider import MetOfficeSTACProvider

_metadata = metadata("stactools-met-office-deterministic")

app = create_cli_app(
    MetOfficeSTACProvider(),
    name="met-office-stac",
    help_text=_metadata["Summary"],
)
