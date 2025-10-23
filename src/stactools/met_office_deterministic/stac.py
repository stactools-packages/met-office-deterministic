import re
from collections import defaultdict
from datetime import datetime
from typing import Literal

import obstore
from geojson_pydantic import Polygon
from obstore import store
from pystac import Asset, Item

PROTOCOL = "s3"
BUCKET = "met-office-atmospheric-model-data"
REGION = "eu-west-2"

# TODO: set up configs for other datasets
PATH_PATTERN = r"^(?:(?P<protocol>[^:]+)://(?P<bucket>[^/]+)/)?(?P<collection>[^/]+)/(?P<reference_time>[^/]+)/(?P<valid_time>[^-]+)-(?P<forecast_horizon>[^-]+)-(?P<variable>.+?)(?:-(?P<duration>PT[\dHM]+))?\.nc$"

MetOfficeCollection = Literal["global-deterministic-10km", "uk-deterministic-2km"]


def _collect_assets(
    object_store: store.ObjectStore,
    key_prefix: str,
    protocol: str,
    bucket: str,
    valid_time: str | None = None,
) -> defaultdict[str, dict[str, Asset]]:
    """Collect assets grouped by item_id from object store.

    Args:
        object_store: The object store to query
        key_prefix: Prefix for filtering keys
        protocol: Storage protocol (e.g., 's3')
        bucket: Storage bucket name
        valid_time: Optional valid_time string to filter results
          (e.g., '20241022T0000Z')
    """
    print(f"checking for keys in {protocol}://{bucket}/{key_prefix}")

    assets: defaultdict[str, dict[str, Asset]] = defaultdict(dict[str, Asset])

    stream = obstore.list(
        object_store,
        prefix=key_prefix,
        chunk_size=100,
    )

    for list_result in stream:
        for result in list_result:
            parsed = re.match(PATH_PATTERN, result["path"])
            if not parsed:
                print(f"{result['path']} did not match the expected pattern")
                continue

            if valid_time and parsed.group("valid_time") != valid_time:
                continue

            item_id = f"{parsed.group('reference_time')}-{parsed.group('valid_time')}"
            variable: str = parsed.group("variable")

            extra_fields = {
                "forecast:variable": variable,
                "updated": result["last_modified"].isoformat(),
            }

            if duration := parsed.group("duration"):
                extra_fields["forecast:duration"] = duration

            assets[item_id][variable] = Asset(
                href=f"{protocol}://{bucket}/{result['path']}",
                extra_fields=extra_fields,
            )

    if not assets:
        msg = f"No assets found for prefix {key_prefix}"
        if valid_time:
            msg += f" with valid_time {valid_time}"

        raise ValueError(msg)

    return assets


def _create_item_from_assets(
    item_id: str,
    assets: dict[str, Asset],
    reference_time: datetime,
) -> Item:
    """Create a STAC Item from a collection of assets."""
    example_asset_href = list(assets.values())[0].href
    parsed = re.match(PATH_PATTERN, example_asset_href)
    if not parsed:
        raise ValueError(f"could not parse {example_asset_href}")

    item = Item(
        id=item_id,
        datetime=datetime.strptime(parsed.group("valid_time"), "%Y%m%dT%H%MZ"),
        bbox=[-180, -90, 180, 90],  # TODO: calculate extent for UK items
        geometry=Polygon.from_bounds(-180, -90, 180, 90).model_dump(exclude_none=True),
        properties={
            "forecast:reference_datetime": reference_time.isoformat(),
            "forecast:horizon": parsed.group("forecast_horizon"),
        },
        stac_extensions=[
            "https://stac-extensions.github.io/forecast/v0.2.0/schema.json",
        ],
        assets=assets,
    )

    return item


def create_item(
    collection: MetOfficeCollection,
    reference_time: datetime,
    valid_time: datetime,
    protocol: str = PROTOCOL,
    bucket: str = BUCKET,
    region: str = REGION,
) -> Item:
    """Create a single item"""
    object_store = store.from_url(
        f"{protocol}://{bucket}", region=region, skip_signature=True
    )

    key_prefix = "/".join(
        [
            collection,
            reference_time.strftime("%Y%m%dT%H%MZ"),
        ]
    )

    valid_time_str = valid_time.strftime("%Y%m%dT%H%MZ")
    assets_by_item = _collect_assets(
        object_store, key_prefix, protocol, bucket, valid_time=valid_time_str
    )

    if not assets_by_item:
        raise ValueError(f"No assets found for prefix {key_prefix}")

    if len(assets_by_item) > 1:
        raise ValueError(f"Expected single item but found {len(assets_by_item)}")

    item_id, assets = next(iter(assets_by_item.items()))
    return _create_item_from_assets(item_id, assets, reference_time)


def create_items_for_reference_time(
    collection: MetOfficeCollection,
    reference_time: datetime,
    protocol: str = PROTOCOL,
    bucket: str = BUCKET,
    region: str = REGION,
) -> list[Item]:
    """Create items for each forecasted timestep (valid_time) for a given reference
    time"""
    object_store = store.from_url(
        f"{protocol}://{bucket}", region=region, skip_signature=True
    )

    key_prefix = "/".join(
        [
            collection,
            reference_time.strftime("%Y%m%dT%H%MZ"),
        ]
    )

    assets_by_item = _collect_assets(object_store, key_prefix, protocol, bucket)

    return [
        _create_item_from_assets(item_id, assets, reference_time)
        for item_id, assets in assets_by_item.items()
    ]
