import datetime

import pytest
from pystac import MediaType

from stactools.met_office_deterministic import stac
from stactools.met_office_deterministic.constants import Model, Theme


@pytest.mark.parametrize(
    "theme",
    (Theme.height, Theme.pressure_level, Theme.near_surface, Theme.whole_atmosphere),
)
@pytest.mark.parametrize("model", (Model.global_, Model.uk))
def test_collection(model: Model, theme: Theme) -> None:
    collection = stac.create_collection(model, theme)
    collection.validate()


def test_items(hrefs: list[str]) -> None:
    items = stac.create_items(hrefs)
    for item in items:
        datetime.datetime.strptime(
            item.properties["forecast:reference_datetime"], "%Y-%m-%dT%H:%M:%SZ"
        )
        item.validate()

        for asset in item.assets.values():
            assert asset.roles == ["data"]
            assert asset.media_type == MediaType.NETCDF
