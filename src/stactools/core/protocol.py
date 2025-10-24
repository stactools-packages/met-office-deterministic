from typing import Any, Iterable, Protocol, runtime_checkable

from pystac import Collection, Item


@runtime_checkable
class STACProvider(Protocol):
    """
    Base protocol for STAC metadata providers.

    Implementations create STAC items and collections for specific datasets.
    Method signatures are intentionally flexible (*args, **kwargs) to accommodate
    different data sources and parameter requirements.
    """

    def create_item(self, *args: Any, **kwargs: Any) -> Item:
        """
        Create a single STAC item.

        Args and kwargs are implementation-specific, allowing flexibility
        for different data sources. Implementations should document their
        specific parameters using type hints and docstrings.

        Returns:
            pystac.Item: A valid STAC item
        """
        ...

    def create_items(self, *args: Any, **kwargs: Any) -> Iterable[Item]:
        """
        Create several STAC items.

        Args and kwargs are implementation-specific, allowing flexibility
        for different data sources. Implementations should document their
        specific parameters using type hints and docstrings.

        Returns:
            Iterable[Item]: An iterator of valid STAC items
        """
        ...

    def create_collection(self, *args: Any, **kwargs: Any) -> Collection:
        """
        Create a STAC collection.

        Args and kwargs are implementation-specific.

        Returns:
            pystac.Collection: A valid STAC collection
        """
        ...


@runtime_checkable
class AsyncSTACProvider(Protocol):
    """
    Async variant of STACProvider for I/O-heavy operations.

    Providers can implement either STACProvider, AsyncSTACProvider, or both.
    The ecosystem can provide adapters to convert between sync and async.
    """

    async def create_item(self, *args: Any, **kwargs: Any) -> Item:
        """Create a single STAC item asynchronously."""
        ...

    def create_items(self, *args: Any, **kwargs: Any) -> Iterable[Item]:
        """Create an iterator of STAC items asynchronously"""
        ...

    async def create_collection(self, *args: Any, **kwargs: Any) -> Collection:
        """Create a STAC collection asynchronously."""
        ...
