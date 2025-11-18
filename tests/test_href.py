from pathlib import Path

import pytest

from stactools.met_office_deterministic.href import Href


@pytest.fixture
def global_hrefs(fixtures: Path) -> list[str]:
    hrefs = list()
    with open(fixtures / "s3-ls-global-20250614T0000Z.txt") as f:
        for line in f:
            hrefs.append(
                "s3://met-office-atmospheric-model-data/global-deterministic-10km/20250614T0000Z/"
                + line.split()[3]
            )
    return hrefs


@pytest.fixture
def uk_hrefs(fixtures: Path) -> list[str]:
    hrefs = list()
    with open(fixtures / "s3-ls-uk-20250614T0000Z.txt") as f:
        for line in f:
            hrefs.append(
                "s3://met-office-atmospheric-model-data/uk-deterministic-2km/20250614T0000Z/"
                + line.split()[3]
            )
    return hrefs


def test_global_hrefs(global_hrefs: list[str]) -> None:
    for href in global_hrefs:
        _ = Href.parse(href)


def test_uk_hrefs(uk_hrefs: list[str]) -> None:
    for href in uk_hrefs:
        _ = Href.parse(href)
