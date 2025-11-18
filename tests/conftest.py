from pathlib import Path

import pytest


@pytest.fixture
def fixtures() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture(params=["global", "uk"])
def hrefs(fixtures: Path, request: pytest.FixtureRequest) -> list[str]:
    hrefs = list()
    match request.param:
        case "global":
            file_name = "s3-ls-global-20250614T0000Z.txt"
            prefix = "s3://met-office-atmospheric-model-data/global-deterministic-10km/20250614T0000Z/"
        case "uk":
            file_name = "s3-ls-uk-20250614T0000Z.txt"
            prefix = "s3://met-office-atmospheric-model-data/uk-deterministic-2km/20250614T0000Z/"
        case _:
            raise NotImplementedError
    with open(fixtures / file_name) as f:
        for line in f:
            hrefs.append(prefix + line.split()[3])
    return hrefs
