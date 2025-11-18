import datetime
from collections import defaultdict
from typing import Sequence

from pystac import (
    Asset,
    Collection,
    Item,
    Link,
    MediaType,
    Provider,
    ProviderRole,
)

from .constants import DESCRIPTIONS, ITEM_ASSETS, KEYWORDS, TITLES, Model, Theme
from .href import Href


def create_collection(model: Model, theme: Theme) -> Collection:
    collection = Collection(
        id=model.get_collection_id(theme),
        description=DESCRIPTIONS[model][theme],
        title=TITLES[model][theme],
        keywords=["MetOffice"] + KEYWORDS[model][theme],
        providers=[
            Provider(
                url="https://www.metoffice.gov.uk/",
                name="Met Office",
                roles=[
                    ProviderRole.PRODUCER,
                    ProviderRole.LICENSOR,
                    ProviderRole.PROCESSOR,
                ],
            ),
        ],
        extent=model.extent,
    )
    collection.links = [
        Link(
            rel="license",
            target="https://creativecommons.org/licenses/by-sa/4.0/deed.en",
            media_type="text/html",
            title="Creative Commons Attribution-ShareAlike 4.0",
        ),
        # Link( rel="cite-as", target="", title="British Crown copyright
        # 2023-2025, the Met Office, is licensed under CC BY-SA", ),
        Link(
            rel="describedBy",
            target="https://www.metoffice.gov.uk/services/data/external-data-channels",
            title="Met Office Dataset Documentation",
        ),
    ]
    collection.item_assets = ITEM_ASSETS[model][theme]  # pyright: ignore[reportAttributeAccessIssue]
    return collection


def create_items(source_hrefs: Sequence[str | Href]) -> list[Item]:
    """Creates one or more STAC items for the given hrefs."""
    hrefs = defaultdict(lambda: defaultdict(list))
    for source_href in source_hrefs:
        if isinstance(source_href, Href):
            href = source_href
        else:
            href = Href.parse(source_href)
        hrefs[href.collection_id][href.item_id].append(href)
    items = list()
    for items_hrefs in hrefs.values():
        for item_id, item_hrefs in items_hrefs.items():
            items.append(_create_item(item_id, item_hrefs))
    return items


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
            "forecast:reference_datetime": datetime.datetime.strptime(
                href.reference_datetime, "%Y%m%dT%H%MZ"
            ).isoformat()
            + "Z",
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
    asset = ITEM_ASSETS[href.model][href.theme][href.parameter].create_asset(
        href=href.href
    )
    asset.media_type = MediaType.NETCDF  # no idea why create asset drops this
    asset.extra_fields = extra_fields
    return (href.parameter, asset)
