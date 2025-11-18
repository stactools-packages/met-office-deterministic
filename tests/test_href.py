from stactools.met_office_deterministic.href import Href


def test_global_hrefs(global_hrefs: list[str]) -> None:
    for raw_href in global_hrefs:
        href = Href.parse(raw_href)
        href.item_id.startswith("20250614T")


def test_uk_hrefs(uk_hrefs: list[str]) -> None:
    for raw_href in uk_hrefs:
        href = Href.parse(raw_href)
        href.item_id.startswith("20250614T")
