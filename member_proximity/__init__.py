import csv
import re
import time

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pandas
import requests


def clean_address(problem_address):
    """Format the address so it is usable by the geocoder.

    Parameters
    ----------
    problem_address: str
        The address that needs to be cleaned.

    Returns
    -------
    str: The cleaned address.

    """
    # clean the Apartment info out
    gg = re.search(
        r"(?:apt|apt\.|apartment|unit|bldg|building|#)([\s#]+)?\w+\s",
        problem_address,
        re.IGNORECASE,
    )
    if gg:
        gg = gg.group()
        problem_address = " ".join([piece.strip().strip(',') for piece in problem_address.split(gg)])

    # clean the extra zip code out
    city_info_results = re.search(r"\w+,\s+\w+(\s+\d+)?", problem_address)
    if not city_info_results:
        print("Error cleaning: {}".format(problem_address))
        return problem_address
    city_info = city_info_results.group()
    fixed_address = problem_address.split(city_info)[0].strip() + " " + city_info
    return fixed_address


def get_census_address(input_address):
    """
    Get the geocode location from census.gov

    Parameters
    ----------
    input_address: str
        The address to use to find the latlon location.

    Returns
    -------
    dict: Dictionary with latitude and longitude of address.

    """
    response = requests.get(
        "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?benchmark=4&format=json",
        params={"address": input_address},
    )
    try:
        geo_data = response.json()["result"]["addressMatches"][0]["coordinates"]
    except IndexError:
        return None
    return {"latitude": geo_data["y"], "longitude": geo_data["x"]}


def generate_address_latlon(ward_directory_export, address_latlon_file):
    """
    Generate a file with latitude and longitudes for the address.

    Parameters
    ----------
    ward_directory_export: str
        Path to the ward directory export csv file.
    address_latlon_file: str
        Output file to contain the member information
        along with the lat/lon info for the address.

    """
    geolocator = Nominatim(user_agent="find_closest_address")
    with open(ward_directory_export) as fileh, open(address_latlon_file, "w") as filew:
        reader = csv.reader(fileh)
        writer = csv.writer(filew)
        header = next(reader)
        writer.writerow(header[:5] + ["cleaned_address", "latitude", "longitude"])
        for household_row in reader:
            address = clean_address(household_row[4].strip())
            location = geolocator.geocode(address)
            latitude = None
            longitude = None
            if location is None:
                location = get_census_address(address)
                if location is None:
                    print(
                        "Location not found: {}".format(household_row[:5] + [address])
                    )
                else:
                    latitude = location["latitude"]
                    longitude = location["longitude"]
            else:
                latitude = location.latitude
                longitude = location.longitude
            writer.writerow(household_row[:5] + [address, latitude, longitude])
            time.sleep(0.5)


def generate_address_distance(input_address, address_latlon_file, output_distance_file):
    """
    Creates a file of distances to the input address sorted with the closest at the top.

    Parameters
    ----------
    input_address: str
        The address to use as a base to generate distances from.
    address_latlon_file: str
        Output file to contain the member information
        along with the lat/lon info for the address.
    output_distance_file:  str
        Path to output csv file with distances to the original input_address.

    """
    address = clean_address(input_address.strip())
    geolocator = Nominatim(user_agent="find_closest_address")
    location = geolocator.geocode(address)
    if not location:
        raise RuntimeError("Address location not found.")

    address_latlon_df = pandas.read_csv(address_latlon_file)

    def calc_distance(in_row):
        start = (location.latitude, location.longitude)
        end = (
            0 if pandas.isnull(in_row["latitude"]) else in_row["latitude"],
            0 if pandas.isnull(in_row["longitude"]) else in_row["longitude"],
        )
        return geodesic(start, end).miles

    address_latlon_df["distance"] = address_latlon_df.apply(calc_distance, axis=1)
    address_latlon_df = address_latlon_df.sort_values(by="distance")
    address_latlon_df.to_csv(output_distance_file, index=False)
    print(address_latlon_df.head(10))
