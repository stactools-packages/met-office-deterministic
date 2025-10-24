from datetime import datetime, timedelta
from unittest.mock import patch

from stactools.met_office_deterministic.provider import (
    STORAGE_BUCKET,
    STORAGE_PROTOCOL,
    STORAGE_REGION,
)
from stactools.met_office_deterministic.stac import (
    create_item,
    create_items_for_reference_time,
)
from tests.fixtures.obstore import pages


def test_create_item() -> None:
    reference_time = datetime(2025, 10, 22, 0)

    with patch("stactools.met_office_deterministic.stac.obstore.list") as mock_list:
        mock_list.return_value = iter(pages)

        item = create_item(
            collection="global-deterministic-10km",
            reference_time=reference_time,
            valid_time=reference_time + timedelta(hours=1),
            storage_protocol=STORAGE_PROTOCOL,
            storage_bucket=STORAGE_BUCKET,
            storage_region=STORAGE_REGION,
        )

        item.validate()

        assert any("forecast" in extension for extension in item.stac_extensions)


def test_create_items_for_reference_time() -> None:
    reference_time = datetime(2025, 10, 22, 0)

    with patch("stactools.met_office_deterministic.stac.obstore.list") as mock_list:
        mock_list.return_value = iter(pages)

        items = create_items_for_reference_time(
            collection="global-deterministic-10km",
            reference_time=reference_time,
            storage_protocol=STORAGE_PROTOCOL,
            storage_bucket=STORAGE_BUCKET,
            storage_region=STORAGE_REGION,
        )

        assert len(items) == len(pages)

        for i, item in enumerate(items):
            assert item.properties["forecast:horizon"] == f"PT000{i}H00M"
            item.validate()
            assert any("forecast" in extension for extension in item.stac_extensions)
