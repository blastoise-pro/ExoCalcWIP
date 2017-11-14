import math

gravitational_constant = 6.67 * 10 ** -11
earth_radius = 6371000
earth_mass = 5.972 * 10 ** 24
earth_density = 5510
earth_escape_velocity = 11186
earth_temperature = 287.2
jupiter_radius = 69911000
boltzmann_constant = 1.36 * 10 ** -23
star_temperature = {"O": 35000, "B": 15000, "A": 9000, "F": 7000, "G": 5500, "K": 4000, "M": 3000, "SOL": 5772}
exo_albedo = {"Terra": 0.39, "Neptú": 0.35, "Júpiter": 0.52}


class DoubleReturn:
    def __init__(self, ist, is_habitable):
        self.ist = ist
        self.is_habitable = is_habitable

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
    print("exo_rad ", exo_rad)
    return (3 * exo_mass) / (4 * math.pi * (exo_rad * jupiter_radius) ** 3)


def calculate_relation(x, y):
    xminusy = x - y
    xplusy = x + y
    return 1 - abs(xminusy / xplusy)


def calculate_IST(exoplanet_radius, exo_type, star_type, exo_orbit, star_rad, habitable_zone):
    exo_mass = calculate_exoplanet_mass(exoplanet_radius)
    print("mass ", exo_mass)
    exo_density = calculate_exoplanet_density(exo_mass, exoplanet_radius)
    exo_escape_velocity = calculate_escape_velocity(exoplanet_radius, exo_mass)
    print("exo escape velocity ", exo_escape_velocity)
    exo_temperature = calculate_temperature(star_rad, star_type, exo_type, exo_orbit)
    print("exo temp", exo_temperature)
    radius_relation = calculate_relation(exoplanet_radius * jupiter_radius, earth_radius)
    print("rad ", radius_relation)
    density_relation = calculate_relation(exo_density, earth_density)
    print("exo density", exo_density)
    print("density ", density_relation)
    escape_velocity_relation = calculate_relation(exo_escape_velocity, earth_escape_velocity)
    print("velocity ", escape_velocity_relation)
    temperature_relation = calculate_relation(exo_temperature, earth_temperature)
    print("temperature ", temperature_relation)
    ist = radius_relation ** (0.57 / 4) * density_relation ** (1.07 / 4) * escape_velocity_relation ** (
        0.7 / 4) * temperature_relation ** (5.58 / 4) * 100
    print(ist)
    if habitable_zone:
        if 263 < exo_temperature < 383:
            is_habitable = True
        else:
            is_habitable = False
    else:
        is_habitable = None
    combined_IST = DoubleReturn(ist, is_habitable)
    return combined_IST
