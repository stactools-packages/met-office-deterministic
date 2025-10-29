from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from stactools.met_office_deterministic.stac import (
    MetOfficeCollection,
    create_item,
    create_items_for_reference_time,
)
from tests.fixtures.obstore import pages


@pytest.mark.parametrize(  # type: ignore[misc]
    "collection",
    [
        "met-office-global-deterministic-10km-surface",
        "met-office-global-deterministic-10km-height",
        "met-office-global-deterministic-10km-pressure",
    ],
)
def test_create_item(collection: MetOfficeCollection) -> None:
    reference_time = datetime(2025, 10, 22, 0)

    with patch("stactools.met_office_deterministic.stac.obstore.list") as mock_list:
        mock_list.return_value = iter(pages)

        item = create_item(
            collection=collection,
            reference_time=reference_time,
            valid_time=reference_time + timedelta(hours=1),
        )

        item.validate()

        assert any("forecast" in extension for extension in item.stac_extensions)

        # Verify that items have the expected variables based on collection type
        if collection.endswith("-surface"):
            # Should not include pressure or height level variables
            assert "temperature_on_pressure_levels" not in item.assets
            assert "cloud_amount_on_height_levels" not in item.assets
            # Should include surface variables
            assert any(
                key.startswith(("CAPE_", "temperature_at_screen_level"))
                for key in item.assets.keys()
            )
        elif collection.endswith("-height"):
            # Should only include height level variables
            assert "cloud_amount_on_height_levels" in item.assets
            assert "temperature_on_pressure_levels" not in item.assets
        elif collection.endswith("-pressure"):
            # Should only include pressure level variables
            assert "temperature_on_pressure_levels" in item.assets
            assert "cloud_amount_on_height_levels" not in item.assets


@pytest.mark.parametrize(  # type: ignore[misc]
    "collection",
    [
        "met-office-global-deterministic-10km-surface",
        "met-office-global-deterministic-10km-height",
        "met-office-global-deterministic-10km-pressure",
    ],
)
def test_create_items_for_reference_time(collection: MetOfficeCollection) -> None:
    reference_time = datetime(2025, 10, 22, 0)

    with patch("stactools.met_office_deterministic.stac.obstore.list") as mock_list:
        mock_list.return_value = iter(pages)

        items = create_items_for_reference_time(
            collection=collection,
            reference_time=reference_time,
        )

        assert len(items) == len(pages)

        for i, item in enumerate(items):
            assert item.properties["forecast:horizon"] == f"PT000{i}H00M"
            item.validate()
            assert any("forecast" in extension for extension in item.stac_extensions)
