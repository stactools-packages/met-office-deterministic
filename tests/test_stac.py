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
    assert collection.title
    collection.validate()


def test_items(hrefs: list[str]) -> None:
    items = stac.create_items(hrefs)
    for item in items:
        datetime.datetime.strptime(
            item.properties["forecast:reference_datetime"], "%Y-%m-%dT%H:%M:%SZ"
        )

        for key, asset in item.assets.items():
            assert asset.roles == ["data"]
            assert asset.media_type == MediaType.NETCDF, "No media type: " + key
            assert asset.title

            # https://github.com/stactools-packages/met-office-deterministic/issues/13
            if item.properties["met_office_deterministic:model"] == Model.uk:
                assert key != "wet_bulb_potential_temperature_on_pressure_levels"

        item.validate()
