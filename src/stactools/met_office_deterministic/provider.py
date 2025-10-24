from datetime import datetime
from typing import Iterable

from pystac import Collection, Item

from stactools.met_office_deterministic.stac import (
    MetOfficeCollection,
    create_item,
    create_items_for_reference_time,
)

STORAGE_PROTOCOL = "s3"
STORAGE_BUCKET = "met-office-atmospheric-model-data"
STORAGE_REGION = "eu-west-2"


class MetOfficeSTACProvider:
    """Implements STACProvider and BatchSTACProvider protocols."""

    def create_item(
        self,
        collection: MetOfficeCollection,
        reference_time: datetime,
        valid_time: datetime,
        storage_protocol: str = STORAGE_PROTOCOL,
        storage_bucket: str = STORAGE_BUCKET,
        storage_region: str = STORAGE_REGION,
    ) -> Item:
        return create_item(
            collection,
            reference_time,
            valid_time,
            storage_protocol,
            storage_bucket,
            storage_region,
        )

    def create_items(
        self,
        collection: MetOfficeCollection,
        reference_time: datetime,
        storage_protocol: str = STORAGE_PROTOCOL,
        storage_bucket: str = STORAGE_BUCKET,
        storage_region: str = STORAGE_REGION,
    ) -> Iterable[Item]:
        for item in create_items_for_reference_time(
            collection,
            reference_time,
            storage_protocol,
            storage_bucket,
            storage_region,
        ):
            yield item

    def create_collection(self, collection: MetOfficeCollection) -> Collection:
        raise NotImplementedError("collection creation is not yet implemented")
