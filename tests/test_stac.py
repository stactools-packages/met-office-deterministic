import datetime

import pytest

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
    assert len(collection.links) == 2

    license_link = next(link for link in collection.links if link.rel == "license")
    assert license_link.href == "https://creativecommons.org/licenses/by-sa/4.0/deed.en"
    assert license_link.media_type == "text/html"

    describedy_link = next(
        link for link in collection.links if link.rel == "describedby"
    )
    assert (
        describedy_link.href
        == "https://www.metoffice.gov.uk/services/data/external-data-channels"
    )

    collection.validate()


def test_items(hrefs: list[str]) -> None:
    items = stac.create_items(hrefs)
    for item in items:
        datetime.datetime.strptime(
            item.properties["forecast:reference_datetime"], "%Y-%m-%dT%H:%M:%SZ"
        )

        for key, asset in item.assets.items():
            assert asset.roles == ["data"]
            assert asset.media_type == "application/netcdf", "No media type: " + key
            assert asset.title

        item.validate()
