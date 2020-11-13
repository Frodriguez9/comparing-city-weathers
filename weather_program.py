'''
A program that compares weather values for two different
locations on earth.
'''

# TODO: - Refactor the program_dialog function. Make another function to assign
#         the weather data to its variables.
#       - make the variable 'answer' a parameter instead of a global variables
#       - Use .just() and . center() string methods to print consistent formats
#         in the table

import requests

API_ROOT = 'https://www.metaweather.com'
API_LOCATION = '/api/location/search/?query='
API_WEATHER = '/api/location/'  # + woeid


def fetch_location(query):
    return requests.get(API_ROOT + API_LOCATION + query).json()
    # returns a list
    # eg: [{'title': 'Caracas', 'location_type': 'City', 'woeid': 395269,
    #     'latt_long': '10.496050,-66.898277'}]

    # may have other cities if partical city names are given,
    # eg: new - New York, New England]


def fetch_weather(woeid):
    return requests.get(API_ROOT + API_WEATHER + woeid).json()
    # returns a dictionary
    # eg:    {'consolidated_weather': [{'id': 6584286904844288,
    #         'weather_state_name': 'Heavy Rain', 'weather_state_abbr': 'hr',
    #         'wind_direction_compass': 'ESE', '
    #          created': '2020-11-03T22:30:55.280414Z',
    #          'applicable_date': '2020-11-03',
    #          'min_temp': 19.555, 'max_temp':...}


def verify_location(location):
    if len(location) == 0:
        print(f"Hmm! We don't know where {answer.title()} is.")

    elif len(location) > 1:
        print("It looks like we have a few cities with similar names.\n"
              "Please select one:")
        for loc in location:
            print(f"\t - {loc['title']}")

    else:  # returns the name of the city if verified
        return location[0]['title']


def ask_for_query():
    return input('Give me a location: ')


def make_data_frame(locations):
    data_frame = []
    for loc in locations.values():
        data = []
        for value in loc.values():
            data.append(value)
        data_frame.append(data)
    return data_frame
    # returns a list with 2 lists.
    # eg: [[x.1, y.1, z.1],
    #     [a.2, b.2, c.2]]


def compute_averages(data_frame):
    columns = len(data_frame)
    # Number of culumns - represented by each city (2 cities in our case)

    lines = len(data_frame[0])
    # The number of values in the first list (city 1) should be equal to
    # the number of items of the second list (city 2). Therefore, we
    # arbitrarely take the first index as the number of lines of
    # the data frame.

    averages = []
    ave = 0

    for line in range(lines):
        for column in range(columns):
            try:
                value_location_1 = data_frame[column][line]
                value_location_2 = data_frame[column+1][line]
                ave = round((value_location_1 + value_location_2)/2, 2)
                averages.append(ave)
            except IndexError:
                continue
    return averages


def print_data_frame(data_frame, location_one, location_two):
    columns = len(data_frame)
    lines = len(data_frame[0])
    value_names = ['min temp',
                   'max temp',
                   'the temp',
                   'wind speed',
                   'air pressure',
                   'humidity']

    print('')
    print(f'{location_one.upper()} VS {location_two.upper()} '
          'WEATHER COMPARISON\n')
    print(f'ITEM \t\t{location_one.upper()} \t\t{location_two.upper()}'
          '\t\tAVERAGES')

    for column in range(lines):
        print(value_names[column], end='\t')
        for lines in range(columns):
            try:
                print(data_frame[lines][column], end='\t\t')
            except IndexError:
                continue
        print('')
    print('')


def program_dialog():
    print("\nPlease indicate what two cities you want to compare.")
    global answer
    comparable_weathers = {}
    location_one = ''
    location_two = ''

    try:
        while len(comparable_weathers) != 2:
            answer = ask_for_query()
            location = fetch_location(answer)
            verified_location = verify_location(location)

            if verified_location:
                if location_one == '':
                    location_one = verified_location

                else:
                    location_two = verified_location

                woeid = str(location[0]['woeid'])
                weather_data = fetch_weather(woeid)
                min_temp = round(weather_data['consolidated_weather'][0]
                                             ['min_temp'], 2)
                max_temp = round(weather_data['consolidated_weather'][0]
                                             ['max_temp'], 2)
                the_temp = round(weather_data['consolidated_weather'][0]
                                             ['the_temp'], 2)
                wind_speed = round(weather_data['consolidated_weather'][0]
                                               ['wind_speed'], 2)
                air_pressure = round(weather_data['consolidated_weather'][0]
                                                 ['air_pressure'], 2)
                humidity = round(weather_data['consolidated_weather'][0]
                                             ['humidity'], 2)

                comparable_weathers.setdefault(verified_location,
                                               {
                                                'min_temp': min_temp,
                                                'max_temp': max_temp,
                                                'the_temp': the_temp,
                                                'wind_speed': wind_speed,
                                                'air_pressure': air_pressure,
                                                'humidity': humidity,
                                                })

        data_table = make_data_frame(comparable_weathers)
        computed_values = compute_averages(data_table)
        data_table.append(computed_values)
        print_data_frame(data_table, location_one, location_two)

    # if requests.get(API_ROOT + API_LOCATION + query).status_code == 404
    except requests.exceptions.ConnectionError:
        print("\nERROR 404: Could not connect to server. "
              "Is your Internet Connection Okay? \n")

#Testing git commands


if __name__ == '__main__':
    program_dialog()
