from __future__ import annotations

import datetime
from enum import StrEnum
from typing import Any

import shapely.geometry
from pystac import Extent, ItemAssetDefinition, SpatialExtent, TemporalExtent
from shapely import Polygon


class Model(StrEnum):
    global_ = "global"
    uk = "uk"

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        """Get the bounding box for the model.

        Returns:
            A tuple of (min_lon, min_lat, max_lon, max_lat).

        Raises:
            ValueError: If the model is unexpected.
        """
        match self:
            case Model.global_:
                return (-180.0, -90, 180, 90)
            case Model.uk:
                return (-24.51, 44.52, 15.28, 61.93)
            case _:
                raise ValueError(f"Unexpected model: {self}")

    @property
    def geometry(self) -> dict[str, Any]:
        """Get the GeoJSON geometry for the model coverage area.

        Returns:
            A GeoJSON geometry dictionary.

        Raises:
            ValueError: If the model is unexpected.
        """
        match self:
            case Model.global_:
                return shapely.geometry.mapping(shapely.geometry.box(*self.bbox))
            case Model.uk:
                return shapely.geometry.mapping(
                    Polygon(
                        shell=[
                            (-17.12, 44.52),
                            (9.21, 44.90),
                            (15.28, 61.93),
                            (-24.51, 61.32),
                        ]
                    )
                )
            case _:
                raise ValueError(f"Unexpected model: {self}")

    @property
    def extent(self) -> Extent:
        """Get the STAC extent for the model.

        Returns:
            A STAC Extent object with spatial and temporal extents.
        """
        return Extent(
            spatial=SpatialExtent(bboxes=[list(self.bbox)]),
            temporal=TemporalExtent(intervals=[[datetime.datetime(2023, 1, 1), None]]),
        )

    def get_collection_id(self, theme: Theme) -> str:
        """Generate the collection ID for a model and theme combination.

        Args:
            theme: The theme to combine with this model.

        Returns:
            The collection ID string.
        """
        return f"met-office-{self}-deterministic-{theme}"


class Theme(StrEnum):
    height = "height"
    pressure_level = "pressure-level"
    near_surface = "near-surface"
    whole_atmosphere = "whole-atmosphere"

    @classmethod
    def from_parameter(cls, parameter: str) -> Theme:
        """Determine the theme from a parameter name.

        Args:
            parameter: The parameter name to classify.

        Returns:
            The Theme corresponding to the parameter.

        Raises:
            ValueError: If the parameter is unknown.
        """
        match parameter:
            case (
                "cloud_amount_on_height_levels"
                | "temperature_on_height_levels"
                | "wind_direction_on_height_levels"
                | "wind_speed_on_height_levels"
            ):
                return Theme.height
            case (
                "fog_fraction_at_screen_level"
                | "visibility_at_screen_level"
                | "pressure_at_mean_sea_level"
                | "pressure_at_surface"
                | "precipitation_rate"
                | "precipitation_accumulation-PT01H"
                | "precipitation_accumulation-PT03H"
                | "precipitation_accumulation-PT06H"
                | "rainfall_accumulation-PT01H"
                | "rainfall_accumulation-PT03H"
                | "rainfall_accumulation-PT06H"
                | "rainfall_rate"
                | "rainfall_rate_from_convection"
                | "rainfall_rate_from_convection_max-PT01H"
                | "rainfall_rate_from_convection_max-PT03H"
                | "rainfall_rate_from_convection_max-PT06H"
                | "radiation_flux_in_uv_downward_at_surface"
                | "radiation_flux_in_longwave_downward_at_surface"
                | "radiation_flux_in_shortwave_direct_downward_at_surface"
                | "radiation_flux_in_shortwave_total_downward_at_surface"
                | "radiation_flux_in_shortwave_diffuse_downward_at_surface"
                | "snow_depth_water_equivalent"
                | "snowfall_rate"
                | "snowfall_accumulation-PT01H"
                | "snowfall_accumulation-PT03H"
                | "snowfall_rate_from_convection"
                | "snowfall_rate_from_convection_mean-PT01H"
                | "snowfall_rate_from_convection_mean-PT03H"
                | "snowfall_rate_from_convection_mean-PT06H"
                | "snowfall_rate_from_convection_max-PT01H"
                | "snowfall_rate_from_convection_max-PT03H"
                | "snowfall_rate_from_convection_max-PT06H"
                | "hail_fall_rate"
                | "hail_fall_accumulation-PT01H"
                | "temperature_at_screen_level"
                | "temperature_at_surface"
                | "temperature_at_screen_level_max-PT01H"
                | "temperature_at_screen_level_max-PT03H"
                | "temperature_at_screen_level_max-PT06H"
                | "temperature_at_screen_level_min-PT01H"
                | "temperature_at_screen_level_min-PT03H"
                | "temperature_at_screen_level_min-PT06H"
                | "temperature_of_dew_point_at_screen_level"
                | "wind_direction_at_10m"
                | "wind_speed_at_10m"
                | "wind_gust_at_10m"
                | "wind_gust_at_10m_max-PT01H"
                | "wind_gust_at_10m_max-PT03H"
                | "wind_gust_at_10m_max-PT06H"
                | "sensible_heat_flux_at_surface"
                | "latent_heat_flux_at_surface_mean-PT01H"
                | "latent_heat_flux_at_surface_mean-PT03H"
                | "latent_heat_flux_at_surface_mean-PT06H"
                | "relative_humidity_at_screen_level"
                | "landsea_mask"
            ):
                return Theme.near_surface
            case (
                "height_ASL_on_pressure_levels"
                | "temperature_on_pressure_levels"
                | "wet_bulb_potential_temperature_on_pressure_levels"
                | "wind_speed_on_pressure_levels"
                | "wind_direction_on_pressure_levels"
                | "wind_vertical_velocity_on_pressure_levels"
                | "relative_humidity_on_pressure_levels"
            ):
                return Theme.pressure_level

            case (
                "cloud_amount_of_total_cloud"
                | "cloud_amount_of_high_cloud"
                | "cloud_amount_of_medium_cloud"
                | "cloud_amount_of_low_cloud"
                | "cloud_amount_below_1000ft_ASL"
                | "height_AGL_at_cloud_base_where_cloud_cover_2p5_oktas"
                | "cloud_amount_of_total_convective_cloud"
                | "pressure_at_tropopause"
                | "lightning_flash_accumulation-PT01H"
                | "temperature_at_tropopause"
                | "CAPE_most_unstable_below_500hPa"
                | "CAPE_surface"
                | "CAPE_mixed_layer_lowest_500m"
                | "CIN_surface"
                | "CIN_mixed_layer_lowest_500m"
                | "CIN_most_unstable_below_500hPa"
                | "height_AGL_at_wet_bulb_freezing_level"
                | "height_AGL_at_freezing_level"
            ):
                return Theme.whole_atmosphere
            case _:
                raise ValueError(f"Unknown parameter: {parameter}")


DESCRIPTIONS = {
    Model.global_: {
        Theme.height: "The Met Office Global Deterministic Height Level dataset provides a composite of weather parameters generated for specific atmospheric height levels.",  # noqa: E501
        Theme.pressure_level: "The Met Office Global Deterministic Pressure Level dataset provides a composite of weather parameters generated for specific atmospheric pressure levels.",  # noqa: E501
        Theme.near_surface: "The Met Office Global Deterministic Near Surface dataset provides a composite of weather parameters generated for the near-surface atmospheric layer.",  # noqa: E501
        Theme.whole_atmosphere: "The Met Office Global Deterministic Whole Atmosphere dataset provides a composite of weather parameters generated for the entire atmospheric column.",  # noqa: E501
    },
    Model.uk: {
        Theme.height: "The Met Office UK Deterministic Height Level dataset provides a composite of weather parameters generated for specific atmospheric height levels.",  # noqa: E501
        Theme.pressure_level: "The Met Office UK Deterministic Pressure Level dataset provides a composite of weather parameters generated for specific atmospheric pressure levels.",  # noqa: E501
        Theme.near_surface: "The Met Office UK Deterministic Near Surface dataset provides a composite of weather parameters generated for the near-surface atmospheric layer.",  # noqa: E501
        Theme.whole_atmosphere: "The Met Office UK Deterministic Whole Atmosphere dataset provides a composite of weather parameters generated for the entire atmospheric column.",  # noqa: E501
    },
}

TITLES = {
    Model.global_: {
        Theme.height: "Met Office Global Deterministic Height Level",
        Theme.pressure_level: "Met Office Global Deterministic Pressure Level",
        Theme.near_surface: "Met Office Global Deterministic Near Surface",
        Theme.whole_atmosphere: "Met Office Global Deterministic Whole Atmosphere",
    },
    Model.uk: {
        Theme.height: "Met Office UK Deterministic Height Level",
        Theme.pressure_level: "Met Office UK Deterministic Pressure Level",
        Theme.near_surface: "Met Office UK Deterministic Near Surface",
        Theme.whole_atmosphere: "Met Office UK Deterministic Whole Atmosphere",
    },
}

KEYWORDS = {
    Model.global_: {
        Theme.height: ["Global", "Cloud"],
        Theme.near_surface: ["Global", "Cloud"],
        Theme.pressure_level: ["Global", "Cloud"],
        Theme.whole_atmosphere: ["Global", "Cloud"],
    },
    Model.uk: {
        Theme.height: ["UK", "Cloud"],
        Theme.near_surface: ["UK", "Cloud"],
        Theme.pressure_level: ["UK", "Cloud"],
        Theme.whole_atmosphere: ["UK", "Cloud"],
    },
}

ITEM_ASSETS = {
    Model.global_: {
        Theme.height: {
            "cloud_amount_on_height_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount on height levels",
                    "roles": ["data"],
                }
            )
        },
        Theme.near_surface: {
            "fog_fraction_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Fog fraction at screen level",
                    "roles": ["data"],
                }
            ),
            "latent_heat_flux_at_surface_mean-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly latent heat flux at surface mean",
                    "roles": ["data"],
                }
            ),
            "latent_heat_flux_at_surface_mean-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly latent heat flux at surface mean",
                    "roles": ["data"],
                }
            ),
            "latent_heat_flux_at_surface_mean-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly latent heat flux at surface mean",
                    "roles": ["data"],
                }
            ),
            "precipitation_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly precipitation accumulation",
                    "roles": ["data"],
                }
            ),
            "precipitation_accumulation-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly precipitation accumulation",
                    "roles": ["data"],
                }
            ),
            "precipitation_accumulation-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly precipitation accumulation",
                    "roles": ["data"],
                }
            ),
            "precipitation_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Precipitation rate",
                    "roles": ["data"],
                }
            ),
            "pressure_at_mean_sea_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Pressure at mean sea level",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_longwave_downward_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in longwave downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_shortwave_direct_downward_at_surface": ItemAssetDefinition(  # noqa: E501
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in shortwave direct downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_shortwave_total_downward_at_surface": ItemAssetDefinition(  # noqa: E501
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in shortwave total downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_uv_downward_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in uv downward at surface",
                    "roles": ["data"],
                }
            ),
            "rainfall_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly rainfall accumulation",
                    "roles": ["data"],
                }
            ),
            "rainfall_accumulation-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly rainfall accumulation",
                    "roles": ["data"],
                }
            ),
            "rainfall_accumulation-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly rainfall accumulation",
                    "roles": ["data"],
                }
            ),
            "rainfall_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Rainfall rate",
                    "roles": ["data"],
                }
            ),
            "rainfall_rate_from_convection": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Rainfall rate from convection",
                    "roles": ["data"],
                }
            ),
            "rainfall_rate_from_convection_max-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly rainfall rate from convection max",
                    "roles": ["data"],
                }
            ),
            "rainfall_rate_from_convection_max-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly rainfall rate from convection max",
                    "roles": ["data"],
                }
            ),
            "rainfall_rate_from_convection_max-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly rainfall rate from convection max",
                    "roles": ["data"],
                }
            ),
            "relative_humidity_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Relative humidity at screen level",
                    "roles": ["data"],
                }
            ),
            "snow_depth_water_equivalent": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Snow depth water equivalent",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Snowfall rate",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Snowfall rate from convection",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection_max-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly snowfall rate from convection max",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection_max-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly snowfall rate from convection max",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection_max-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly snowfall rate from convection max",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection_mean-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly snowfall rate from convection mean",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection_mean-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly snowfall rate from convection mean",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate_from_convection_mean-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly snowfall rate from convection mean",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature at screen level",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_max-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly temperature at screen level max",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_max-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly temperature at screen level max",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_max-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly temperature at screen level max",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_min-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly temperature at screen level min",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_min-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly temperature at screen level min",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_min-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly temperature at screen level min",
                    "roles": ["data"],
                }
            ),
            "temperature_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature at surface",
                    "roles": ["data"],
                }
            ),
            "temperature_of_dew_point_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Dew point temperature at screen level",
                    "roles": ["data"],
                }
            ),
            "visibility_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Visibility at screen level",
                    "roles": ["data"],
                }
            ),
            "wind_direction_at_10m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind direction at 10m",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind gust at 10m",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m_max-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly wind gust at 10m max",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m_max-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly wind gust at 10m max",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m_max-PT06H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Six hourly wind gust at 10m max",
                    "roles": ["data"],
                }
            ),
            "wind_speed_at_10m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind speed at 10m",
                    "roles": ["data"],
                }
            ),
        },
        Theme.pressure_level: {
            "height_ASL_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Height above sea level on pressure levels",
                    "roles": ["data"],
                }
            ),
            "relative_humidity_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Relative humidity on pressure levels",
                    "roles": ["data"],
                }
            ),
            "temperature_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wet_bulb_potential_temperature_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wet bulb temperature on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wind_direction_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind direction on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wind_speed_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind speed on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wind_vertical_velocity_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind vertical velocity on pressure levels",
                    "roles": ["data"],
                }
            ),
        },
        Theme.whole_atmosphere: {
            "CAPE_mixed_layer_lowest_500m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Available Potential Energy mixed layer lowest 500m",  # noqa: E501
                    "roles": ["data"],
                }
            ),
            "CAPE_most_unstable_below_500hPa": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Available Potential Energy most unstable below 500hPa",  # noqa: E501
                    "roles": ["data"],
                }
            ),
            "CAPE_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Available Potential Energy with respect to surface",  # noqa: E501
                    "roles": ["data"],
                }
            ),
            "CIN_mixed_layer_lowest_500m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Inhibition mixed layer lowest 500m",
                    "roles": ["data"],
                }
            ),
            "CIN_most_unstable_below_500hPa": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Inhibition most unstable below 500hPa",
                    "roles": ["data"],
                }
            ),
            "CIN_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Inhibition with respect to surface",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_below_1000ft_ASL": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount below 1000ft Above Sea Level",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_high_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of high cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_low_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of low cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_medium_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of medium cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_total_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of total cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_total_convective_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of total convective cloud",
                    "roles": ["data"],
                }
            ),
            "pressure_at_tropopause": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Pressure at tropopause",
                    "roles": ["data"],
                }
            ),
            "temperature_at_tropopause": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature at tropopause",
                    "roles": ["data"],
                }
            ),
        },
    },
    Model.uk: {
        Theme.height: {
            "cloud_amount_on_height_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount on height levels",
                    "roles": ["data"],
                }
            ),
            "temperature_on_height_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature on height levels",
                    "roles": ["data"],
                }
            ),
            "wind_direction_on_height_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind direction on height levels",
                    "roles": ["data"],
                }
            ),
            "wind_speed_on_height_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind speed on height levels",
                    "roles": ["data"],
                }
            ),
        },
        Theme.near_surface: {
            "fog_fraction_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Fog fraction at screen level",
                    "roles": ["data"],
                }
            ),
            "hail_fall_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly hail fall accumulation",
                    "roles": ["data"],
                }
            ),
            "hail_fall_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hail fall rate",
                    "roles": ["data"],
                }
            ),
            "landsea_mask": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Land binary mask",
                    "roles": ["data"],
                }
            ),
            "precipitation_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly precipitation accumulation",
                    "roles": ["data"],
                }
            ),
            "precipitation_accumulation-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly precipitation accumulation",
                    "roles": ["data"],
                }
            ),
            "precipitation_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Precipitation rate",
                    "roles": ["data"],
                }
            ),
            "pressure_at_mean_sea_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Pressure at mean sea level",
                    "roles": ["data"],
                }
            ),
            "pressure_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Pressure at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_longwave_downward_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in longwave downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_shortwave_diffuse_downward_at_surface": ItemAssetDefinition(  # noqa: E501
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in shortwave diffuse downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_shortwave_direct_downward_at_surface": ItemAssetDefinition(  # noqa: E501
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in shortwave direct downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_shortwave_total_downward_at_surface": ItemAssetDefinition(  # noqa: E501
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in shortwave total downward at surface",
                    "roles": ["data"],
                }
            ),
            "radiation_flux_in_uv_downward_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Radiation flux in uv downward at surface",
                    "roles": ["data"],
                }
            ),
            "rainfall_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly rainfall accumulation",
                    "roles": ["data"],
                }
            ),
            "rainfall_accumulation-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly rainfall accumulation",
                    "roles": ["data"],
                }
            ),
            "rainfall_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Rainfall rate",
                    "roles": ["data"],
                }
            ),
            "relative_humidity_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Relative humidity at screen level",
                    "roles": ["data"],
                }
            ),
            "sensible_heat_flux_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Sensible heat flux at surface",
                    "roles": ["data"],
                }
            ),
            "snow_depth_water_equivalent": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Snow depth water equivalent",
                    "roles": ["data"],
                }
            ),
            "snowfall_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly snowfall accumulation",
                    "roles": ["data"],
                }
            ),
            "snowfall_accumulation-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly snowfall accumulation",
                    "roles": ["data"],
                }
            ),
            "snowfall_rate": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Snowfall rate",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature at screen level",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_max-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly temperature at screen level max",
                    "roles": ["data"],
                }
            ),
            "temperature_at_screen_level_min-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly temperature at screen level min",
                    "roles": ["data"],
                }
            ),
            "temperature_at_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature at surface",
                    "roles": ["data"],
                }
            ),
            "temperature_of_dew_point_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Dew point temperature at screen level",
                    "roles": ["data"],
                }
            ),
            "visibility_at_screen_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Visibility at screen level",
                    "roles": ["data"],
                }
            ),
            "wind_direction_at_10m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind direction at 10m",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind gust at 10m",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m_max-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly wind gust at 10m max",
                    "roles": ["data"],
                }
            ),
            "wind_gust_at_10m_max-PT03H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Three hourly wind gust at 10m max",
                    "roles": ["data"],
                }
            ),
            "wind_speed_at_10m": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind speed at 10m",
                    "roles": ["data"],
                }
            ),
        },
        Theme.pressure_level: {
            "height_ASL_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Height above sea level on pressure levels",
                    "roles": ["data"],
                }
            ),
            "relative_humidity_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Relative humidity on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wet_bulb_potential_temperature_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wet bulb temperature on pressure levels",
                    "roles": ["data"],
                }
            ),
            "temperature_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Temperature on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wind_direction_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind direction on pressure levels",
                    "roles": ["data"],
                }
            ),
            "wind_speed_on_pressure_levels": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Wind speed on pressure levels",
                    "roles": ["data"],
                }
            ),
        },
        Theme.whole_atmosphere: {
            "CAPE_most_unstable_below_500hPa": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Available Potential Energy most unstable below 500hPa",  # noqa: E501
                    "roles": ["data"],
                }
            ),
            "CAPE_surface": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Convective Available Potential Energy with respect to surface",  # noqa: E501
                    "roles": ["data"],
                }
            ),
            "cloud_amount_below_1000ft_ASL": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount below 1000ft Above Sea Level",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_high_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of high cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_low_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of low cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_medium_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of medium cloud",
                    "roles": ["data"],
                }
            ),
            "cloud_amount_of_total_cloud": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Cloud amount of total cloud",
                    "roles": ["data"],
                }
            ),
            "height_AGL_at_cloud_base_where_cloud_cover_2p5_oktas": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Height above ground level at cloud base where cloud cover 2p5 oktas",  # noqa: E501
                    "roles": ["data"],
                }
            ),
            "height_AGL_at_freezing_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Height above ground level at freezing level",
                    "roles": ["data"],
                }
            ),
            "height_AGL_at_wet_bulb_freezing_level": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Height above ground level at wet bulb freezing level",
                    "roles": ["data"],
                }
            ),
            "lightning_flash_accumulation-PT01H": ItemAssetDefinition(
                {
                    "media_type": "application/netcdf",
                    "title": "Hourly number of lightning flashes per unit area",
                    "roles": ["data"],
                }
            ),
        },
    },
}
