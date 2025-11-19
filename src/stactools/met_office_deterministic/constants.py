from __future__ import annotations

import datetime
from enum import StrEnum
from typing import Any

import shapely.geometry
from pystac import Extent, ItemAssetDefinition, SpatialExtent, TemporalExtent


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
                # Where box is the projected corners:
                # shapely.geometry.mapping(raster_footprint.reproject_geometry(Polygon(raster_footprint.densify_by_distance(list(box.exterior.coords), 50000)), source_crs, "EPSG:4326"))  # noqa: E501
                return {
                    "type": "Polygon",
                    "coordinates": (
                        (
                            (9.2231377, 44.8895151),
                            (9.3195613, 45.3343933),
                            (9.4180189, 45.7789614),
                            (9.5185708, 46.2232224),
                            (9.6212802, 46.6671789),
                            (9.7262126, 47.1108334),
                            (9.8334361, 47.5541883),
                            (9.9430221, 47.9972456),
                            (10.0550445, 48.4400072),
                            (10.1695809, 48.8824747),
                            (10.2867117, 49.3246496),
                            (10.4065211, 49.7665328),
                            (10.5290971, 50.2081254),
                            (10.6545313, 50.6494277),
                            (10.7829198, 51.0904402),
                            (10.9143626, 51.5311627),
                            (11.0489647, 51.9715948),
                            (11.1868357, 52.4117359),
                            (11.3280904, 52.8515847),
                            (11.4728491, 53.2911399),
                            (11.6212377, 53.7303993),
                            (11.7733883, 54.1693608),
                            (11.9294394, 54.6080214),
                            (12.0895365, 55.0463779),
                            (12.253832, 55.4844263),
                            (12.4224863, 55.9221622),
                            (12.5956679, 56.3595807),
                            (12.7735541, 56.7966761),
                            (12.9563313, 57.2334421),
                            (13.1441959, 57.6698715),
                            (13.3373546, 58.1059567),
                            (13.5360254, 58.541689),
                            (13.7404385, 58.9770588),
                            (13.9508365, 59.4120557),
                            (14.1674756, 59.8466684),
                            (14.3906269, 60.2808841),
                            (14.6205768, 60.7146893),
                            (14.8576285, 61.148069),
                            (15.102103, 61.581007),
                            (15.3032549, 61.9270274),
                            (14.3801505, 62.0395207),
                            (13.4508349, 62.1461448),
                            (12.5155738, 62.2468383),
                            (11.5746469, 62.3415426),
                            (10.6283475, 62.4302014),
                            (9.6769822, 62.5127616),
                            (8.7208703, 62.5891729),
                            (7.7603431, 62.6593884),
                            (6.7957434, 62.7233643),
                            (5.8274248, 62.7810604),
                            (4.8557508, 62.8324401),
                            (3.8810938, 62.8774706),
                            (2.9038346, 62.9161227),
                            (1.9243611, 62.9483716),
                            (0.9430673, 62.9741961),
                            (-0.0396477, 62.9935794),
                            (-1.0233806, 63.0065087),
                            (-2.0077255, 63.0129755),
                            (-2.9922745, 63.0129755),
                            (-3.9766194, 63.0065087),
                            (-4.9603523, 62.9935794),
                            (-5.9430673, 62.9741961),
                            (-6.9243611, 62.9483716),
                            (-7.9038346, 62.9161227),
                            (-8.8810938, 62.8774706),
                            (-9.8557508, 62.8324401),
                            (-10.8274248, 62.7810604),
                            (-11.7957434, 62.7233643),
                            (-12.7603431, 62.6593884),
                            (-13.7208703, 62.5891729),
                            (-14.6769822, 62.5127616),
                            (-15.6283475, 62.4302014),
                            (-16.5746469, 62.3415426),
                            (-17.5155738, 62.2468383),
                            (-18.4508349, 62.1461448),
                            (-19.3801505, 62.0395207),
                            (-20.3032549, 61.9270274),
                            (-21.2198966, 61.8087285),
                            (-22.1298388, 61.6846898),
                            (-23.0328592, 61.554979),
                            (-23.9287502, 61.4196658),
                            (-24.5337849, 61.3244889),
                            (-24.2323643, 60.9008838),
                            (-23.9398382, 60.4765593),
                            (-23.6558386, 60.0515435),
                            (-23.3800163, 59.6258623),
                            (-23.1120407, 59.1995398),
                            (-22.8515978, 58.7725986),
                            (-22.5983897, 58.3450596),
                            (-22.3521336, 57.9169422),
                            (-22.1125608, 57.4882644),
                            (-21.8794157, 57.0590431),
                            (-21.6524556, 56.6292938),
                            (-21.4314492, 56.1990308),
                            (-21.2161765, 55.7682676),
                            (-21.0064279, 55.3370164),
                            (-20.8020036, 54.9052887),
                            (-20.6027134, 54.473095),
                            (-20.4083756, 54.0404449),
                            (-20.218817, 53.6073472),
                            (-20.0338721, 53.1738102),
                            (-19.8533831, 52.7398413),
                            (-19.6771988, 52.3054472),
                            (-19.5051752, 51.870634),
                            (-19.3371741, 51.4354073),
                            (-19.1730636, 50.9997721),
                            (-19.0127173, 50.5637328),
                            (-18.8560144, 50.1272934),
                            (-18.7028388, 49.6904572),
                            (-18.5530796, 49.2532274),
                            (-18.4066304, 48.8156065),
                            (-18.263389, 48.3775966),
                            (-18.1232576, 47.9391996),
                            (-17.9861422, 47.5004167),
                            (-17.8519526, 47.0612492),
                            (-17.7206021, 46.6216976),
                            (-17.5920075, 46.1817623),
                            (-17.4660888, 45.7414434),
                            (-17.3427692, 45.3007408),
                            (-17.2219746, 44.8596538),
                            (-17.127109, 44.5065069),
                            (-16.5097002, 44.595348),
                            (-15.8905483, 44.6803982),
                            (-15.2697191, 44.7616412),
                            (-14.6472803, 44.8390611),
                            (-14.023301, 44.9126427),
                            (-13.3978521, 44.9823716),
                            (-12.7710056, 45.0482339),
                            (-12.1428352, 45.1102163),
                            (-11.5134158, 45.1683065),
                            (-10.8828235, 45.2224925),
                            (-10.2511358, 45.2727635),
                            (-9.6184313, 45.319109),
                            (-8.9847895, 45.3615196),
                            (-8.3502909, 45.3999864),
                            (-7.7150171, 45.4345016),
                            (-7.0790504, 45.4650578),
                            (-6.4424739, 45.4916487),
                            (-5.8053711, 45.5142688),
                            (-5.1678263, 45.5329133),
                            (-4.5299243, 45.5475782),
                            (-3.8917502, 45.5582604),
                            (-3.2533893, 45.5649578),
                            (-2.6149273, 45.5676689),
                            (-1.9764498, 45.5663931),
                            (-1.3380427, 45.5611306),
                            (-0.6997915, 45.5518827),
                            (-0.0617817, 45.5386512),
                            (0.5759014, 45.521439),
                            (1.2131731, 45.5002497),
                            (1.8499488, 45.4750876),
                            (2.4861446, 45.4459582),
                            (3.1216774, 45.4128675),
                            (3.7564644, 45.3758224),
                            (4.390424, 45.3348306),
                            (5.0234752, 45.2899006),
                            (5.6555381, 45.2410417),
                            (6.2865337, 45.1882638),
                            (6.9163841, 45.1315778),
                            (7.5450129, 45.0709952),
                            (8.1723445, 45.0065282),
                            (8.798305, 44.9381897),
                            (9.2231377, 44.8895151),
                        ),
                    ),
                }
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
