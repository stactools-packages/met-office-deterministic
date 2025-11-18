from pystac import Collection

from .constants import DESCRIPTIONS, Model, Theme


def create_collection(model: Model, theme: Theme) -> Collection:
    # Note: in the original spec document, each collection id had a "-data"
    # suffix. That's removed here, as it doesn't add any meaning.
    return Collection(
        id=f"met-office-{model}-deterministic-{theme}",
        description=DESCRIPTIONS[model][theme],
        extent=model.extent,
    )
