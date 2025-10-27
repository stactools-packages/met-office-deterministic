import re
from collections import defaultdict
from datetime import datetime
from typing import Literal

import obstore
from obstore import store
from pystac import (
    Asset,
    Collection,
    Extent,
    Item,
    ItemAssetDefinition,
    Link,
    MediaType,
    Provider,
    ProviderRole,
    SpatialExtent,
    TemporalExtent,
)

from stactools.met_office_deterministic.constants import (
    GLOBAL_ABOUT_PDF,
    GLOBAL_BBOX,
    GLOBAL_DESCRIPTION,
    GLOBAL_GEOMETRY,
    HOST_PROVIDERS,
    UK_ABOUT_PDF,
    UK_BBOX,
    UK_DESCRIPTION,
    UK_GEOMETRY,
    UK_PROJECTED_BBOX,
    UK_PROJECTED_CRS_WKT2,
    UK_PROJECTED_GEOMETRY,
    global_height_variables,
    global_pressure_variables,
    global_surface_variables,
    uk_height_variables,
    uk_pressure_variables,
    uk_surface_variables,
)


def _format_multiline_string(string: str) -> str:
    """Format a multi-line string for use in metadata fields"""
    return re.sub(r" +", " ", re.sub(r"(?<!\n)\n(?!\n)", " ", string))


PROTOCOL = "s3"
BUCKET = "met-office-atmospheric-model-data"
REGION = "eu-west-2"

# TODO: set up configs for other datasets
PATH_PATTERN = r"^(?:(?P<protocol>[^:]+)://(?P<bucket>[^/]+)/)?(?P<collection>[^/]+)/(?P<reference_time>[^/]+)/(?P<valid_time>[^-]+)-(?P<forecast_horizon>[^-]+)-(?P<variable>.+?)(?:-(?P<duration>PT[\dHM]+))?\.nc$"

MetOfficeCollection = Literal[
    "met-office-global-deterministic-10km-surface",
    "met-office-global-deterministic-10km-height",
    "met-office-global-deterministic-10km-pressure",
    "met-office-uk-deterministic-2km-surface",
    "met-office-uk-deterministic-2km-height",
    "met-office-uk-deterministic-2km-pressure",
]


def _get_collection_variables(
    collection: MetOfficeCollection,
) -> dict[str, dict[str, str]]:
    """Get the list of valid variables for a given collection.

    Args:
        collection: The collection name

    Returns:
        List of valid variable names for the collection
    """
    if collection.startswith("met-office-global"):
        if collection.endswith("-pressure"):
            return global_pressure_variables
        elif collection.endswith("-height"):
            return global_height_variables
        elif collection.endswith("-surface"):
            return global_surface_variables
    elif collection.startswith("met-office-uk"):
        if collection.endswith("-pressure"):
            return uk_pressure_variables
        elif collection.endswith("-height"):
            return uk_height_variables
        elif collection.endswith("-surface"):
            return uk_surface_variables

    raise ValueError(f"Unknown collection: {collection}")


def _collect_assets(
    object_store: store.ObjectStore,
    key_prefix: str,
    variables: dict[str, dict[str, str]],
    protocol: str,
    bucket: str,
    valid_time: str | None = None,
) -> defaultdict[str, dict[str, Asset]]:
    """Collect assets grouped by item_id from object store.

    Args:
        object_store: The object store to query
        key_prefix: Prefix for filtering keys
        variables: List of valid variable names to include
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

            variable: str = parsed.group("variable")

            # Filter by collection-specific variables
            if variable not in variables:
                continue

            item_id = f"{parsed.group('reference_time')}-{parsed.group('valid_time')}"

            extra_fields = {
                "forecast:variable": variable,
                "updated": result["last_modified"].isoformat(),
            }

            if duration := parsed.group("duration"):
                extra_fields["forecast:duration"] = duration

            assets[item_id][variable] = Asset(
                href=f"{protocol}://{bucket}/{result['path']}",
                extra_fields=extra_fields,
                description=variables[variable]["description"],
                title=variable.replace("_", " "),
                roles=["data"],
                media_type=MediaType.NETCDF,
            )

    if not assets:
        msg = f"No assets found for prefix {key_prefix}"
        if valid_time:
            msg += f" with valid_time {valid_time}"

        raise ValueError(msg)

    return assets


def _create_item_from_assets(
    item_id: str,
    collection: MetOfficeCollection,
    assets: dict[str, Asset],
    reference_time: datetime,
    add_collection: bool = False,
) -> Item:
    """Create a STAC Item from a collection of assets."""
    example_asset_href = list(assets.values())[0].href
    parsed = re.match(PATH_PATTERN, example_asset_href)
    if not parsed:
        raise ValueError(f"could not parse {example_asset_href}")

    item = Item(
        id=item_id,
        datetime=datetime.strptime(parsed.group("valid_time"), "%Y%m%dT%H%MZ"),
        bbox=GLOBAL_BBOX if "global" in collection else UK_BBOX,
        geometry=GLOBAL_GEOMETRY if "global" in collection else UK_GEOMETRY,
        properties={
            "forecast:reference_datetime": reference_time.isoformat(),
            "forecast:horizon": parsed.group("forecast_horizon"),
        },
        stac_extensions=[
            "https://stac-extensions.github.io/forecast/v0.2.0/schema.json",
        ],
        assets=assets,
        collection=collection if add_collection else None,
    )

    if "uk" in collection:
        item.ext.add("proj")
        item.ext.proj.apply(
            geometry=UK_PROJECTED_GEOMETRY,
            bbox=UK_PROJECTED_BBOX,
            wkt2=UK_PROJECTED_CRS_WKT2,
        )

    return item


def create_item(
    collection: MetOfficeCollection,
    reference_time: datetime,
    valid_time: datetime,
    protocol: str = PROTOCOL,
    bucket: str = BUCKET,
    region: str = REGION,
    add_collection: bool = False,
) -> Item:
    """Create a single item"""
    object_store = store.from_url(
        f"{protocol}://{bucket}", region=region, skip_signature=True
    )

    base_collection = collection.replace("met-office-", "", 1)
    if base_collection.endswith(("-surface", "-height", "-pressure")):
        base_collection = base_collection.rsplit("-", 1)[0]

    key_prefix = "/".join(
        [
            base_collection,
            reference_time.strftime("%Y%m%dT%H%MZ"),
        ]
    )

    variables = _get_collection_variables(collection)
    valid_time_str = valid_time.strftime("%Y%m%dT%H%MZ")
    assets_by_item = _collect_assets(
        object_store, key_prefix, variables, protocol, bucket, valid_time=valid_time_str
    )

    if not assets_by_item:
        raise ValueError(f"No assets found for prefix {key_prefix}")

    if len(assets_by_item) > 1:
        raise ValueError(f"Expected single item but found {len(assets_by_item)}")

    item_id, assets = next(iter(assets_by_item.items()))
    return _create_item_from_assets(
        item_id, collection, assets, reference_time, add_collection
    )


def create_items_for_reference_time(
    collection: MetOfficeCollection,
    reference_time: datetime,
    protocol: str = PROTOCOL,
    bucket: str = BUCKET,
    region: str = REGION,
    add_collection: bool = False,
) -> list[Item]:
    """Create items for each forecasted timestep (valid_time) for a given reference
    time"""
    object_store = store.from_url(
        f"{protocol}://{bucket}", region=region, skip_signature=True
    )

    base_collection = collection.replace("met-office-", "", 1)
    if base_collection.endswith(("-surface", "-height", "-pressure")):
        base_collection = base_collection.rsplit("-", 1)[0]

    key_prefix = "/".join(
        [
            base_collection,
            reference_time.strftime("%Y%m%dT%H%MZ"),
        ]
    )

    variables = _get_collection_variables(collection)
    assets_by_item = _collect_assets(
        object_store, key_prefix, variables, protocol, bucket
    )

    return [
        _create_item_from_assets(
            item_id, collection, assets, reference_time, add_collection
        )
        for item_id, assets in assets_by_item.items()
    ]


def create_collection(id: MetOfficeCollection, protocol: str = PROTOCOL) -> Collection:
    collection = Collection(
        id=id,
        description=_format_multiline_string(
            UK_DESCRIPTION if "uk" in id else GLOBAL_DESCRIPTION
        ),
        extent=Extent(
            spatial=SpatialExtent(bboxes=[GLOBAL_BBOX if "global" in id else UK_BBOX]),
            temporal=TemporalExtent(intervals=[[None, None]]),
        ),
        license="CC-BY-SA-4.0",
        providers=[
            Provider(
                name="Met Office",
                url="https://www.metoffice.gov.uk/",
                roles=[
                    ProviderRole.LICENSOR,
                    ProviderRole.PROCESSOR,
                    ProviderRole.PRODUCER,
                ],
            ),
            HOST_PROVIDERS[protocol],  # this won't work for https links yet
        ],
        stac_extensions=[
            # "https://stac-extensions.github.io/datacube/v2.3.0/schema.json",
        ],
    )

    variables = _get_collection_variables(id)

    collection.item_assets = {
        asset_key: ItemAssetDefinition.create(
            title=asset_key.replace("_", " "),
            description=_format_multiline_string(asset_info["description"]),
            media_type=MediaType.NETCDF,
            roles=["data"],
        )
        for asset_key, asset_info in variables.items()
    }

    # todo: add datacube extension

    collection.add_link(
        Link(
            rel="about",
            media_type=MediaType.PDF,
            target=UK_ABOUT_PDF if "uk" in id else GLOBAL_ABOUT_PDF,
        )
    )
    return collection
