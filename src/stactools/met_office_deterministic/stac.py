from collections import defaultdict

from pystac import Asset, Collection, Item, MediaType

from .constants import DESCRIPTIONS, Model, Theme
from .href import Href


def create_collection(model: Model, theme: Theme) -> Collection:
    # Note: in the original spec document, each collection id had a "-data"
    # suffix. That's removed here, as it doesn't add any meaning.
    return Collection(
        id=f"met-office-{model}-deterministic-{theme}",
        description=DESCRIPTIONS[model][theme],
        extent=model.extent,
    )


def create_items(source_hrefs: list[str | Href]) -> list[Item]:
    """Creates one or more STAC items for the given hrefs."""
    hrefs = defaultdict(list)
    for source_href in source_hrefs:
        if isinstance(source_href, Href):
            href = source_href
        else:
            href = Href.parse(source_href)
        hrefs[href.item_id].append(href)
    return [_create_item(item_id, hrefs) for item_id, hrefs in hrefs.items()]


def _create_item(item_id: str, hrefs: list[Href]) -> Item:
    assert hrefs
    href = hrefs[0]
    item = Item(
        id=item_id,
        datetime=href.datetime,
        bbox=list(href.model.bbox),
        geometry=href.model.geometry,
        stac_extensions=[
            "https://stac-extensions.github.io/forecast/v0.2.0/schema.json",
        ],
        properties={
            "forecast:reference_datetime": href.reference_datetime,
            "forecast:horizon": href.forecast_horizon,
            "met_office_deterministic:model": href.model,
            "met_office_deterministic:theme": href.theme,
        },
        assets=dict(_create_asset(href) for href in hrefs),
    )
    return item


def _create_asset(href: Href) -> tuple[str, Asset]:
    extra_fields = {
        "forecast:variable": href.variable,
    }
    if href.duration:
        extra_fields["forecast:duration"] = href.duration
    return (
        href.parameter,
        Asset(
            href=href.href,
            media_type=MediaType.NETCDF,
            roles=["data"],
            extra_fields=extra_fields,
        ),
    )
