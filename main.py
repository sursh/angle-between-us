import pandas as pd

LOCATIONS_FILE = 'data/simplemaps_worldcities_basicv1.75/worldcities.csv'


class City():

    def __init__(self, user_input):
        self.user_input = user_input


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
    input2 = 'London'
    return input1, input2


def main():
    atlas = create_atlas()
    cities = [City(inpt) for inpt in get_user_inputs()]

    for city in cities:
        try:
            atlas[city.user_input]
            city.name = city.user_input
            city.lat, city.lng = atlas[city.name]
            print("Found {} at ({}, {})".format(city.name, city.lat, city.lng))
        except KeyError:
            print("City {} not found in city list".format(city.user_input))

        # maybe do angle things


if __name__ == '__main__':
    main()
