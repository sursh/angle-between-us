from math import radians, sin, cos, acos, sqrt, degrees, floor
import pandas as pd
import sys

LOCATIONS_FILE = 'data/simplemaps_worldcities_basicv1.75/worldcities.csv'


class City():

    def __init__(self, user_input):
        self.user_input = user_input

    def add_geo(self, latlong):
        self.lat, self.lng = latlong
        self.vector = self.compute_vector()

    def compute_vector(self):
        """ Express lat/long as a cartesian vector. """
        rho = 1  # Assuming spherical planet
        phi = radians(90 - self.lat)
        theta = radians(self.lng)

        x = rho * sin(phi) * cos(theta)
        y = rho * sin(phi) * sin(theta)
        z = rho * cos(phi)
        return x, y, z


def create_atlas():
    """ Get geo data and standardize it into a dict """
    atlas = {}
    df = pd.read_csv(LOCATIONS_FILE)

    # Filter to only the biggest cities to cut down on name collisions
    df = df[df.population > 1000000]

    for row in df.itertuples():
        atlas[row.city_ascii] = (row.lat, row.lng)

    return atlas


def get_user_inputs():
    # TODO: actually get user input
    input1 = 'Los Angeles'
    input2 = 'Mumbai'
    return input1, input2


def magnitude(x, y, z):
    return sqrt(x**2 + y**2 + z**2)


def compute_angle(cities):
    city1, city2 = cities
    x1, y1, z1 = city1.vector
    x2, y2, z2 = city2.vector
    mag1 = magnitude(x1, y1, z1)
    mag2 = magnitude(x2, y2, z2)
    angle = acos(x1*x2 + y1*y2 + z1*z2) / (mag1 * mag2)
    return floor(degrees(angle))


def main():
    atlas = create_atlas()
    cities = [City(inpt) for inpt in get_user_inputs()]

    for city in cities:
        try:
            atlas[city.user_input]
            city.name = city.user_input
            city.add_geo(atlas[city.name])
            print("Found {} in atlas with lat/long ({}, {})"
                  .format(city.name, city.lat, city.lng))
        except KeyError:
            print("ERROR: {} not found in city list".format(city.user_input))
            sys.exit(1)

    angle = compute_angle(cities)
    print("The angle between {} and {} is {} degrees"
          .format(cities[0].name, cities[1].name, angle))


if __name__ == '__main__':
    main()
