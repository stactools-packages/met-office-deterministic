"""Constants for Met Office Deterministic models.

### Sources:
- https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/uk-nwp-asdi-datasheet.pdf
- https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/uk-nwp-asdi-datasheet.pdf

This module defines variable metadata for Met Office Global and UK Deterministic models.
Variables are organized to eliminate duplication while maintaining clear model-specific
collections.

Structure:
    Shared Variables (common to both Global and UK models):
        - _shared_pressure_variables: 6 variables
        - _shared_height_variables: 1 variable (cloud_amount_on_height_levels)
        - _shared_surface_variables: 30 variables
          (including convection rainfall/snowfall rates)

    Global-only Variables:
        - _global_only_pressure_variables: 1 variable
          (wind_vertical_velocity_on_pressure_levels)
        - _global_only_surface_variables: 13 variables
          (CAPE_mixed_layer, CIN_mixed_layer, CAPE_most_unstable/surface,
          CIN_most_unstable/surface, convective cloud,
          latent heat flux, precipitation/rainfall accumulation, rainfall/snowfall
          rates, etc.)

    UK-only Variables:
        - _uk_only_height_variables: 3 variables (temperature, wind direction, wind
          speed on height levels)
        - _uk_only_surface_variables: 11 variables (hail, lightning, freezing levels,
          landseamask, pressure_at_surface, sensible heat flux, snowfall_accumulation,
          etc.)

Final Collections:
    Global Model Variables:
        - global_pressure_variables: 7 total (6 shared + 1 global-only)
        - global_height_variables: 1 total (1 shared)
        - global_surface_variables: 43 total (30 shared + 13 global-only)
        - TOTAL: 51 variables

    UK Model Variables:
        - uk_pressure_variables: 6 total (6 shared)
        - uk_height_variables: 4 total (1 shared + 3 UK-only)
        - uk_surface_variables: 41 total (30 shared + 11 UK-only)
        - TOTAL: 51 variables

Each variable dictionary contains:
    - description: Detailed explanation from Met Office documentation
    - unit: Measurement unit (e.g., "K", "m s-1", "Pa", "J kg-1")
"""

# Shared variable metadata (common to both Global and UK models)

_shared_pressure_variables = {
    "height_ASL_on_pressure_levels": {
        "description": """Height above mean sea level or altitude of the pressure 
        levels. This is considered approximately equivalent to geopotential height.
        Geopotential is the sum of the specific gravitational potential energy
        relative to the geoid and the specific centripetal potential energy.
        Geopotential height is the geopotential divided by the standard
        acceleration due to gravity.""",
        "unit": "m",
    },
    "relative_humidity_on_pressure_levels": {
        "description": """Fractional relative humidity (ratio of the partial pressure
        of water vapour to the equilibrium vapour pressure of water) on pressure
        levels.""",
        "unit": "1",
    },
    "temperature_on_pressure_levels": {
        "description": "Air temperature on pressure levels.",
        "unit": "K",
    },
    "wet_bulb_potential_temperature_on_pressure_levels": {
        "description": """Wet bulb potential temperature (temperature that a parcel
        of air at any level would have if starting at the wet bulb temperature,
        it was brought at a saturated adiabatic lapse rate, to the standard
        pressure of 1000hPa) on pressure levels.""",
        "unit": "K",
    },
    "wind_direction_on_pressure_levels": {
        "description": """Wind on a pressure level is defined as a two-dimensional
        (horizontal) air velocity vector with no vertical component. In
        meteorological reports the direction of the wind vector is given as
        the direction from which it is blowing.""",
        "unit": "degrees",
    },
    "wind_speed_on_pressure_levels": {
        "description": """Wind on a pressure level is defined as a two-dimensional
        (horizontal) air velocity with no vertical component. The speed is the
        magnitude of velocity.""",
        "unit": "m s-1",
    },
}

_shared_height_variables = {
    "cloud_amount_on_height_levels": {
        "description": """Fraction of horizontal grid square occupied by cloud on 
        height levels.""",
        "unit": "1",
    },
}

_shared_surface_variables = {
    "cloud_amount_below_1000ft_ASL": {
        "description": """Fraction of horizontal grid square occupied by cloud cover
        below 1,000 feet above sea level.""",
        "unit": "1",
    },
    "cloud_amount_of_high_cloud": {
        "description": """Fraction of horizontal grid square occupied by cloud in the
        high-level cloud height range; from 5,574m (~18,000ft) to 13,608m
        (~44,500ft).""",
        "unit": "1",
    },
    "cloud_amount_of_low_cloud": {
        "description": """Fraction on horizontal grid square occupied by cloud in the
        low-level cloud height range: from 111m (~350ft) to 1,949m (~6,500ft).""",
        "unit": "1",
    },
    "cloud_amount_of_medium_cloud": {
        "description": """A fraction of horizontal grid square occupied by cloud in
        the mid-level cloud height range; from 1,949m (~6,500ft) to 5,574m
        (~18,000ft).""",
        "unit": "1",
    },
    "cloud_amount_of_total_cloud": {
        "description": """Fraction of horizontal grid square occupied by cloud as
        diagnosed by the model cloud scheme. This is for the whole atmosphere
        column as seen from the surface or the top of the atmosphere.""",
        "unit": "1",
    },
    "fog_fraction_at_screen_level": {
        "description": """Fog means a visibility of 1000 m or lower. The reduction
        in visibility is caused by water droplets or minute ice crystals forming
        close to the surface. This quantity represents the fraction of horizontal
        grid square occupied by fog. An alternative interpretation is that this
        represents the fractional probability of fog being present at any location
        in the grid square.""",
        "unit": "1",
    },
    "precipitation_rate": {
        "description": """Instantaneous rate at which liquid water (as a depth) is
        being deposited on the surface.""",
        "unit": "m s-1",
    },
    "pressure_at_mean_sea_level": {
        "description": """Air pressure at mean sea level which is close to the geoid
        in sea areas. Air pressure at sea level is the quantity often abbreviated
        as MSLP or PMSL.""",
        "unit": "Pa",
    },
    "radiation_flux_in_longwave_downward_at_surface": {
        "description": """Longwave radiation at the surface from above directed at
        the ground. In accordance with common usage in geophysical disciplines
        "flux" implies per unit area called "flux density" in physics.""",
        "unit": "W m-2",
    },
    "radiation_flux_in_shortwave_direct_downward_at_surface": {
        "description": """Shortwave radiation at the surface from above directed at
        the ground. "Direct" means that the radiation has followed a direct path
        from the sun and is alternatively known as "direct insolation". In
        accordance with common usage in geophysical disciplines "flux" implies
        per unit area called "flux density" in physics.""",
        "unit": "W m-2",
    },
    "radiation_flux_in_uv_downward_at_surface": {
        "description": """Ultraviolet radiation at the surface from above directed
        at the ground. In accordance with common usage in geophysical disciplines
        flux implies per unit area called "flux density" in physics.""",
        "unit": "W m-2",
    },
    "relative_humidity_at_screen_level": {
        "description": """Fractional relative humidity (ratio of the partial pressure
        of water vapour to the equilibrium vapour pressure of water) at screen level
        (1.5m above the surface.)""",
        "unit": "1",
    },
    "snow_depth_water_equivalent": {
        "description": """Liquid water equivalent (LWE) depth of the snow lying on
        the surface (ground). Typically, water is 10 times as dense as snow so
        multiplying by 10 gives an approximate depth of the snow, although wet snow
        can be significantly denser and powder snow much less dense.""",
        "unit": "m",
    },
    "temperature_at_screen_level": {
        "description": "Air temperature at screen level (1.5m).",
        "unit": "K",
    },
    "temperature_at_screen_level_max": {
        "description": "Maximum instantaneous air temperature at screen level (1.5m).",
        "unit": "K",
    },
    "temperature_at_screen_level_min": {
        "description": "Minimum instantaneous air temperature at screen level (1.5m).",
        "unit": "K",
    },
    "temperature_at_surface": {
        "description": """Temperature at the surface interface between the air and the 
        ground.""",
        "unit": "K",
    },
    "temperature_of_dew_point_at_screen_level": {
        "description": """Dew point temperature (temperature at which a parcel of air
        reaches saturation upon being cooled at constant pressure and specific
        humidity) at screen level.""",
        "unit": "K",
    },
    "visibility_at_screen_level": {
        "description": """Distance at which a known object can be seen horizontally
        from screen level (1.5m).""",
        "unit": "m",
    },
    "wind_direction_at_10m": {
        "description": """Mean wind direction is equivalent to the mean direction
        observed over the 10 minutes preceding the validity time. In meteorological
        reports the direction of the wind vector is given as the direction from
        which it is blowing. 10m wind is the considered surface wind.""",
        "unit": "degrees",
    },
    "wind_gust_at_10m": {
        "description": """The gust speed is equivalent to the maximum 3 second mean
        wind speed observed over the 10 minutes preceding validity time. 10m wind
        is the considered surface wind.""",
        "unit": "m s-1",
    },
    "wind_gust_at_10m_max": {
        "description": """Maximum diagnosed instantaneous wind gust at 10m. This can
        be considered as the extreme wind speed that might be experienced in this
        period.""",
        "unit": "m s-1",
    },
    "wind_speed_at_10m": {
        "description": """Mean wind speed is equivalent to the mean speed observed
        over the 10 minutes preceding the validity time. 10m wind is the considered
        surface wind.""",
        "unit": "m s-1",
    },
    "pressure_at_tropopause": {
        "description": "Air pressure at tropopause.",
        "unit": "Pa",
    },
    "temperature_at_tropopause": {
        "description": "Temperature at tropopause.",
        "unit": "K",
    },
    "rainfall_rate_from_convection": {
        "description": """Instantaneous rate at which rain, produced by the model
        convection scheme, is being deposited on the surface.""",
        "unit": "m s-1",
    },
    "snowfall_rate_from_convection": {
        "description": """Rate at which liquid water equivalent (LWE) snow, produced
        by the model convection scheme, is being deposited on the surface.""",
        "unit": "m s-1",
    },
    "rainfall_rate_from_convection_max": {
        "description": """Maximum instantaneous rate at which rain, produced by the
        model convection scheme, is being deposited on the surface.""",
        "unit": "m s-1",
    },
    "snowfall_rate_from_convection_max": {
        "description": """Maximum instantaneous rate at which liquid water equivalent
        (LWE) snow, produced by the model convection scheme, is being deposited on
        the surface.""",
        "unit": "m s-1",
    },
    "snowfall_rate_from_convection_mean": {
        "description": """Mean rate at which liquid water equivalent (LWE) snow,
        produced by the model convection scheme, is being deposited on the
        surface.""",
        "unit": "m s-1",
    },
}

# Global-only variable metadata

_global_only_pressure_variables = {
    "wind_vertical_velocity_on_pressure_levels": {
        "description": """Speed of the vertical component of the air motion at a
        pressure level. Upwards is positive and downwards is negative.""",
        "unit": "m s-1",
    },
}

_global_only_surface_variables = {
    "CAPE_most_unstable_below_500hPa": {
        "description": """CAPE (Convective Available Potential Energy) calculated for
        the most unstable parcel where the most unstable parcel is defined as the
        parcel with the highest fixed level CAPE launched from any level (including
        screen-level = 1.5m) within 500hPa of the surface pressure.""",
        "unit": "J kg-1",
    },
    "CAPE_surface": {
        "description": """Value of CAPE (Convection Available Potential Energy)
        calculated for a surface based parcel, where a surface based parcel is
        defined as a parcel initiated with thermodynamic properties at screen level
        height (1.5m) i.e. the parcel is launched from screen level.""",
        "unit": "J kg-1",
    },
    "CAPE_mixed_layer_lowest_500m": {
        "description": """Convective Available Potential Energy (CAPE) calculated for
        a parcel with the thermodynamic properties of the density-weighted mean of
        the lowest 500 m above ground level.""",
        "unit": "J kg-1",
    },
    "CIN_most_unstable_below_500hPa": {
        "description": """Any additional energy required to lift the most unstable
        parcel to its level of free convection. Where most unstable parcel is
        defined as the parcel with the highest fixed-level CAPE launched from any
        level (including screen-level) within 500 hPa of the surface pressure.""",
        "unit": "J kg-1",
    },
    "CIN_surface": {
        "description": """Any additional energy required to lift a surface-based
        parcel (i.e. a parcel launched from screen-level (1.5m)) to its level of
        free convection.""",
        "unit": "J kg-1",
    },
    "CIN_mixed_layer_lowest_500m": {
        "description": """Any additional energy required to lift a mixed-layer parcel
        to its level of free convection. Where a mixed layer parcel is defined as a
        parcel with thermodynamic properties of the density weighted mean of the
        lowest 500 m above ground level (AGL).""",
        "unit": "J kg-1",
    },
    "cloud_amount_of_total_convective_cloud": {
        "description": """Fraction of horizontal grid squares occupied by convective
        cloud as diagnosed by the model convection scheme. This is for the whole
        atmosphere column as seen from the surface or the top of the atmosphere.""",
        "unit": "1",
    },
    "latent_heat_flux_at_surface_mean": {
        "description": """Exchange of heat between the surface and the air on account
        of evaporation (including sublimation). In accordance with common usage in
        geophysical disciplines "flux" implies per unit area called "flux density"
        in physics. Upwards is positive; negative is downward.""",
        "unit": "W m-2",
    },
    "precipitation_accumulation": {
        "description": """Implied depth of the layer of liquid water which has been
        deposited on the surface. This includes rain, snow and hail with the ice
        phase precipitation being considered as a liquid water equivalent (lwe)
        value. It includes the contribution from the model convection scheme if this
        is invoked (true for Global models but not the UK models) as well as that
        from the model precipitation scheme.""",
        "unit": "m",
    },
    "radiation_flux_in_shortwave_total_downward_at_surface": {
        "description": """Total shortwave radiation at the surface from above directed
        at the ground. In accordance with common usage in geophysical disciplines
        "flux" implies per unit area called "flux density" in physics.""",
        "unit": "W m-2",
    },
    "rainfall_accumulation": {
        "description": """Implied depth of the rain produced by the model precipitation
        scheme which has been deposited on the surface. For the Global models (which
        run a convection scheme) the "rainfall accumulation from convection" must be
        added to this to get the total rainfall accumulation.""",
        "unit": "m",
    },
    "rainfall_rate": {
        "description": """Instantaneous rate at which rain (as a depth) which has been
        produced by the model precipitation scheme is being deposited on the surface.
        For the Global models (which run a convection scheme) the "rainfall rate from
        convection" must be added to this to get the total rainfall rate.""",
        "unit": "m s-1",
    },
    "snowfall_rate": {
        "description": """Instantaneous rate at which liquid water equivalent (LWE)
        snow (as a depth) which has been produced by the model precipitation scheme
        is being deposited on the surface. For the Global models which run a
        convection scheme) the "snowfall rate from convection" must be added to this
        to get the total snowfall rate.""",
        "unit": "m s-1",
    },
}

# UK-only variable metadata

_uk_only_height_variables = {
    "temperature_on_height_levels": {
        "description": "Air temperature on height levels.",
        "unit": "K",
    },
    "wind_direction_on_height_levels": {
        "description": """Wind direction on height levels. In meteorological reports 
        the direction of the wind vector is given as the direction from which it is 
        blowing.""",
        "unit": "degrees",
    },
    "wind_speed_on_height_levels": {
        "description": """Wind speed on height levels. The speed is the magnitude of 
        velocity.""",
        "unit": "m s-1",
    },
}

_uk_only_surface_variables = {
    "hail_fall_accumulation": {
        "description": """Implied depth of hail (as liquid water equivalent) which has
        been deposited on the surface.""",
        "unit": "m",
    },
    "hail_fall_rate": {
        "description": """Instantaneous rate at which hail (as liquid water equivalent)
        is being deposited on the surface.""",
        "unit": "m s-1",
    },
    "height_AGL_at_cloud_base_where_cloud_cover_2p5_oktas": {
        "description": """Height above ground level at cloud base where cloud cover is
        2.5 oktas (approximately 31% coverage).""",
        "unit": "m",
    },
    "height_AGL_at_freezing_level": {
        "description": """Height above ground level at the 0°C isotherm (freezing
        level).""",
        "unit": "m",
    },
    "height_AGL_at_wet_bulb_freezing_level": {
        "description": """Height above ground level at the wet bulb freezing
        level.""",
        "unit": "m",
    },
    "landsea_mask": {
        "description": "Binary mask indicating land (1) or sea (0) surface type.",
        "unit": "1",
    },
    "lightning_flash_accumulation": {
        "description": "Accumulated count of lightning flashes in the grid square.",
        "unit": "1",
    },
    "pressure_at_surface": {
        "description": "Air pressure at the surface.",
        "unit": "Pa",
    },
    "radiation_flux_in_shortwave_diffuse_downward_at_surface": {
        "description": """Diffuse shortwave radiation at the surface from above
        directed at the ground. In accordance with common usage in geophysical
        disciplines "flux" implies per unit area called "flux density" in
        physics.""",
        "unit": "W m-2",
    },
    "sensible_heat_flux_at_surface": {
        "description": """Exchange of heat between the surface and the air by motion
        of air; also called "turbulent" heat flux. In accordance with common usage
        in geophysical disciplines "flux" implies per unit area called "flux density"
        in physics. Upwards is positive; negative is downward.""",
        "unit": "W m-2",
    },
    "snowfall_accumulation": {
        "description": """Implied depth of snow (as liquid water equivalent) which has
        been deposited on the surface.""",
        "unit": "m",
    },
}

# Global Deterministic Variables by Collection Type

global_pressure_variables = {
    **_shared_pressure_variables,
    **_global_only_pressure_variables,
}

global_height_variables = _shared_height_variables.copy()

global_surface_variables = {
    **_shared_surface_variables,
    **_global_only_surface_variables,
}

# UK Deterministic Variables by Collection Type

uk_pressure_variables = _shared_pressure_variables.copy()

uk_height_variables = {
    **_shared_height_variables,
    **_uk_only_height_variables,
}

uk_surface_variables = {
    **_shared_surface_variables,
    **_uk_only_surface_variables,
}

GLOBAL_BBOX = [-180.0, -90.0, 180.0, 90.0]
GLOBAL_GEOMETRY = {
    "type": "Polygon",
    "coordinates": [
        [
            [-180.0, -90.0],
            [180.0, -90.0],
            [180.0, 90.0],
            [-180.0, 90.0],
            [-180.0, -90.0],
        ]
    ],
}

UK_PROJECTED_BBOX = (-1159000.0, -1037000.0, 925000.0, 903000.0)

UK_PROJECTED_GEOMETRY = {
    "type": "Polygon",
    "coordinates": [
        [
            [-1159000.0, -1037000.0],
            [925000.0, -1037000.0],
            [925000.0, 903000.0],
            [-1159000.0, 903000.0],
            [-1159000.0, -1037000.0],
        ]
    ],
}
UK_BBOX = [-24.53378493833058, 44.50650694725796, 15.303254906837337, 63.01353038140843]
UK_GEOMETRY = {
    "type": "Polygon",
    "coordinates": [
        [
            [-24.53378493833058, 61.324488948957956],
            [-23.951373173315336, 60.493545743436769],
            [-23.390896432012816, 59.642901967655732],
            [-22.841332451643318, 58.755508388715391],
            [-22.31335960938301, 57.848390936796626],
            [-21.801567181007321, 56.912986826934201],
            [-21.305906343002128, 55.949248252727905],
            [-20.826259788283505, 54.957120844212596],
            [-20.358637436880535, 53.927882178398434],
            [-19.907071029893029, 52.870076921146051],
            [-19.47125743836736, 51.783621585087218],
            [-19.047676772929652, 50.659695923614777],
            [-18.636530266007984, 49.498124454681488],
            [-18.24076150704655, 48.307479067833967],
            [-17.85726509418285, 47.078823241490895],
            [-17.486059187992534, 45.811920231152506],
            [-17.127109019634418, 44.506506947257961],
            [-15.505827472321721, 44.731218368449781],
            [-13.885825860364733, 44.928314140866874],
            [-12.243428372623802, 45.100560386215285],
            [-10.605011280169697, 45.24509473459603],
            [-8.946742890035738, 45.36393890630027],
            [-7.295351722195853, 45.455113283820126],
            [-5.639648518520391, 45.519498986208873],
            [-3.981107744788353, 45.557004758650798],
            [-2.321224400757482, 45.567577173910777],
            [-0.661503245561277, 45.55120113548314],
            [0.996552142145287, 45.507900020207771],
            [2.65145028401201, 45.43773545751332],
            [4.301722517152545, 45.340806749681384],
            [5.945933326513551, 45.217249944602258],
            [7.582690128393277, 45.067236579159307],
            [9.223137694420183, 44.889515090803961],
            [9.516538867106773, 46.214340147390146],
            [9.82044599417415, 47.501001440503842],
            [10.132650886942383, 48.74091702446794],
            [10.457660860756802, 49.952037057383372],
            [10.79332144679133, 51.125708654880285],
            [11.13958576340595, 52.262120651749875],
            [11.499287378552452, 53.370228452045964],
            [11.869671426326294, 54.441366044050284],
            [12.253831966406114, 55.484426293773282],
            [12.648531526077839, 56.490743551039934],
            [13.05713338849257, 57.469156234231541],
            [13.475831953348639, 58.411006880996538],
            [13.912511851065867, 59.33378430533233],
            [14.35898320017346, 60.220118303314543],
            [14.824001969831695, 61.087422072202891],
            [15.303254906837337, 61.927027387435338],
            [12.871655946289337, 62.209277200563875],
            [10.400470016364583, 62.45057399884363],
            [7.914310140853996, 62.648572133129136],
            [5.400279783166546, 62.804447665893385],
            [2.864695576108446, 62.91753580170105],
            [0.333925859864863, 62.986973455823794],
            [-2.224322992711248, 63.01353038140843],
            [-4.763674234671517, 62.996681924309321],
            [-7.29679693171977, 62.936872788865081],
            [-9.836285590351739, 62.833403028602532],
            [-12.355687094751509, 62.687020652261616],
            [-14.848587701338502, 62.498353138924266],
            [-17.309046001669611, 62.268189153976081],
            [-19.750152039231516, 61.995224171054332],
            [-22.16609393016936, 61.679609773846522],
            [-24.53378493833058, 61.324488948957956],
        ]
    ],
}
