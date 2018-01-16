import math

gravitational_constant = 6.67 * 10 ** -11
earth_radius = 6371000
earth_mass = 5.972 * 10 ** 24
earth_density = 5510
earth_escape_velocity = 11186
earth_temperature = 287.2
jupiter_radius = 69911000
star_temperature = {"O (35.000 K)": 35000, "B (15.000 K)": 15000, "A (9.000 K)": 9000, "F (7.000 K)": 7000, "G (5.500 K)": 5500, "K (4000 K)": 4000, "M (3000 K)": 3000, "SOL (5772 K)": 5772}
exo_albedo = {"Terra": 0.39, "Neptú": 0.35, "Júpiter": 0.52}


class ExoplanetDataWrapper:
    def __init__(self, ist, is_habitable, radius, density, escape_velocity, temperature, radius_relation, density_relation, escape_velocity_relation, temperature_relation):
        self.ist = ist
        self.is_habitable = is_habitable
        self.radius = radius
        self.density = density
        self.escape_velocity = escape_velocity
        self.temperature = temperature
        self.radius_relation = radius_relation
        self.density_relation = density_relation
        self.escape_velocity_relation = escape_velocity_relation
        self.temperature_relation = temperature_relation


def calculate_exoplanet_mass(exo_rad):
    exo_earth_radius = exo_rad * 10.97331659
    if exo_earth_radius < 6:
        return 0.9515 * exo_earth_radius ** 3.1 * earth_mass
    elif 6 < exo_earth_radius < 10:
        return 1.7013 * exo_earth_radius ** 2.0383 * earth_mass
    else:
        return 0.6631 * exo_earth_radius ** 2.4191 * earth_mass


def calculate_escape_velocity(exo_rad, exo_mass):
    return math.sqrt((2 * gravitational_constant * exo_mass) / (exo_rad * jupiter_radius))


def calculate_temperature(star_rad, star_type, exo_type, exo_orbit):
    return star_temperature[star_type] * (1 - exo_albedo[exo_type]) ** 0.25 * math.sqrt(star_rad / (2 * exo_orbit))


def calculate_exoplanet_density(exo_mass, exo_rad):
    return (3 * exo_mass) / (4 * math.pi * (exo_rad * jupiter_radius) ** 3)


def calculate_relation(exo_parameter, earth_parameter):
    exominusearth = exo_parameter - earth_parameter
    exoplusearth = exo_parameter + earth_parameter
    return 1 - abs(exominusearth / exoplusearth)


def calculate_IST(exoplanet_radius, exo_type, star_type, exo_orbit, star_rad):
    exo_mass = calculate_exoplanet_mass(exoplanet_radius)
    print(exo_mass)
    exo_density = calculate_exoplanet_density(exo_mass, exoplanet_radius)
    exo_escape_velocity = calculate_escape_velocity(exoplanet_radius, exo_mass)
    exo_temperature = calculate_temperature(star_rad, star_type, exo_type, exo_orbit)

    radius_relation = calculate_relation(exoplanet_radius * jupiter_radius, earth_radius)
    density_relation = calculate_relation(exo_density, earth_density)
    escape_velocity_relation = calculate_relation(exo_escape_velocity, earth_escape_velocity)
    temperature_relation = calculate_relation(exo_temperature, earth_temperature)

    ist = radius_relation ** (0.57 / 4) * density_relation ** (1.07 / 4) * escape_velocity_relation ** (
        0.7 / 4) * temperature_relation ** (5.58 / 4) * 100
    if 263 < exo_temperature < 383:
        is_habitable = True
    else:
        is_habitable = False
    return ExoplanetDataWrapper(ist, is_habitable, exoplanet_radius, exo_density, exo_escape_velocity, exo_temperature, radius_relation * 100, density_relation * 100, escape_velocity_relation * 100, temperature_relation * 100)
