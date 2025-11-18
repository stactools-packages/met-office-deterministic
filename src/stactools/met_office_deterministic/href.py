from __future__ import annotations

import re
from dataclasses import dataclass

from .constants import Model, Theme

HREF_REGEX = re.compile(
    r"^(?:(?P<scheme>[^:]+)://(?P<bucket>[^/]+)/)?(?P<collection>[^/]+)/(?P<reference_time>[^/]+)/(?P<valid_time>[^-]+)-(?P<forecast_horizon>[^-]+)-(?P<parameter>.+)\.nc$"
)


@dataclass(frozen=True)
class Href:
    href: str
    model: Model
    theme: Theme
    parameter: str
    reference_time: str
    valid_time: str
    forecast_horizon: str

    @classmethod
    def parse(cls, href: str) -> Href:
        matched = HREF_REGEX.match(href)
        if not matched:
            raise ValueError(f"Invalid UK Met Office href: {href}")
        matched_dict = matched.groupdict()
        match collection := matched_dict["collection"]:
            case "global-deterministic-10km":
                model = Model.global_
            case "uk-deterministic-2km":
                model = Model.uk
            case _:
                raise ValueError(f"Invalid collection: {collection}")
        parameter = matched_dict["parameter"]
        theme = Theme.from_parameter(parameter)
        return Href(
            href=href,
            model=model,
            theme=theme,
            parameter=parameter,
            reference_time=matched_dict["reference_time"],
            valid_time=matched_dict["valid_time"],
            forecast_horizon=matched_dict["forecast_horizon"],
        )

    def __str__(self) -> str:
        return self.href
