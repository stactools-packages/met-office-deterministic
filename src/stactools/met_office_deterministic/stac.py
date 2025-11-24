import datetime
from collections import defaultdict
from typing import Sequence

import shapely.geometry
from pystac import (
    Asset,
    Collection,
    Item,
    Link,
    Provider,
    ProviderRole,
)

from .constants import DESCRIPTIONS, ITEM_ASSETS, KEYWORDS, TITLES, Model, Theme
from .href import Href


def create_collection(model: Model, theme: Theme) -> Collection:
    """Create a STAC collection for a model and theme combination.

    Args:
        model: The Met Office model (global or UK).
        theme: The theme (height, pressure-level, near-surface, or whole-atmosphere).

    Returns:
        A STAC Collection object configured for the model and theme.
    """
    collection = Collection(
        id=model.get_collection_id(theme),
        description=DESCRIPTIONS[model][theme],
        title=TITLES[model][theme],
        license="CC-BY-SA-4.0",
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
        stac_extensions=[
            "https://stac-extensions.github.io/storage/v1.0.0/schema.json",
            "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
        ],
        extra_fields={
            "storage:schemes": {
                "aws": {
                    "type": "aws-s3",
                    "platform": "https://{bucket}.s3.{region}.amazonaws.com",
                    "bucket": "met-office-atmospheric-model-data",
                    "region": "eu-west-2",
                    "requester_pays": False,
                }
            },
            "auth:schemes": {"aws": {"type": "s3"}},
        },
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
    hrefs: defaultdict[str, defaultdict[str, list[Href]]] = defaultdict(
        lambda: defaultdict(list)
    )
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
    """Create a STAC item from a list of hrefs.

    Args:
        item_id: The ID for the item.
        hrefs: A list of Href objects to include as assets in the item.

    Returns:
        A STAC Item object with assets for each href.
    """
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
    if href.model == Model.uk:
        item.ext.add("proj")
        item.ext.proj.geometry = shapely.geometry.mapping(
            shapely.geometry.box(-1159000.0, -1037000.0, 925000.0, 903000.0)
        )
        item.ext.proj.wkt2 = 'PROJCS["unnamed",GEOGCS["unknown",DATUM["unnamed",SPHEROID["Spheroid",6378137,298.257222101004]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Lambert_Azimuthal_Equal_Area"],PARAMETER["latitude_of_center",54.9],PARAMETER["longitude_of_center",-2.5],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'  # noqa: E501
    return item


def _create_asset(href: Href) -> tuple[str, Asset]:
    """Create a STAC asset from an href.

    Args:
        href: The Href object to convert to an asset.

    Returns:
        A tuple of (asset_key, Asset) where the key is the parameter name.
    """
    extra_fields = {
        "forecast:variable": href.variable,
    }
    if href.duration:
        extra_fields["forecast:duration"] = href.duration
    asset = ITEM_ASSETS[href.model][href.theme][href.parameter].create_asset(
        href=href.href
    )
    asset.media_type = "application/netcdf"  # no idea why create asset drops this
    asset.extra_fields = extra_fields
    return (href.parameter, asset)
