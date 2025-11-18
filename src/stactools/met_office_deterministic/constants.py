from __future__ import annotations

import datetime
from enum import StrEnum

from pystac import Extent, SpatialExtent, TemporalExtent


class Model(StrEnum):
    global_ = "global"
    uk = "uk"

    @property
    def extent(self) -> Extent:
        match self:
            case Model.global_:
                bbox = [-180.0, -90, 180, 90]
            case Model.uk:
                bbox = [-24.53378, 44.50651, 15.30325, 63.01353]
            case _:
                raise ValueError(f"Unexpected model: {self}")
        return Extent(
            spatial=SpatialExtent(bboxes=[bbox]),
            temporal=TemporalExtent(intervals=[[datetime.datetime(2023, 1, 1), None]]),
        )


class Theme(StrEnum):
    height = "height"
    pressure_level = "pressure-level"
    near_surface = "near-surface"
    whole_atmosphere = "whole-atmosphere"

    @classmethod
    def from_parameter(cls, parameter: str) -> Theme:
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
