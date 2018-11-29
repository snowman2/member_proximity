from collections import namedtuple
import re
import time
import warnings

from geopy.distance import geodesic
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
import pandas
import requests


Location = namedtuple("Location", ["latitude", "longitude"])


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
        r"\s(?:apt|apt\.|apartment|unit|unt|bldg\.|bldg|building|#)([\s#]+)?\w+\s",
        problem_address,
        re.IGNORECASE,
    )
    if gg:
        gg = gg.group()
        problem_address = " ".join(
            [piece.strip().strip(",") for piece in problem_address.split(gg)]
        )

    # clean the extra zip code out
    city_info_results = re.search(r"\w+,\s+\w+(\s+\d+)?", problem_address)
    if not city_info_results:
        warnings.warn("Error cleaning: {}".format(problem_address))
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
        "https://geocoding.geo.census.gov/geocoder/locations/"
        "onelineaddress?benchmark=4&format=json",
        params={"address": input_address},
    )
    try:
        geo_data = response.json()["result"]["addressMatches"][0]["coordinates"]
    except IndexError:
        return None
    return Location(latitude=geo_data["y"], longitude=geo_data["x"])


def get_location(address):
    """
    Return the location in latitude and longitude of the address.

    Parameters
    ----------
    address: str
        The address to find the location for.

    Returns
    -------
    tuple(:obj:`Location`, str): The location of the address.

    """
    location = get_census_address(address)
    try:
        if location is None:
            location = Nominatim(user_agent="member_proximity_py").geocode(address)
    except GeocoderUnavailable:
        pass
    # maximum of 1 request per second
    # https://operations.osmfoundation.org/policies/nominatim/
    time.sleep(1)
    return location


def generate_address_latlon(ward_directory_export, recalc=False):
    """
    Adds latitude and longitudes to the ward directory file.

    Parameters
    ----------
    ward_directory_export: str
        Path to the ward directory export csv file.
    recalc: bool
        If True, it will recalculate rows without locations.

    """
    ward_directory_df = pandas.read_csv(ward_directory_export)

    # make sure location columns added
    location_columns = ("cleaned_address", "latitude", "longitude")
    for location_column in location_columns:
        if location_column not in ward_directory_df.columns:
            ward_directory_df[location_column] = None
            recalc = True

    if not recalc:
        return

    def add_locations(in_row):
        if pandas.isnull(in_row["cleaned_address"]):
            in_row["cleaned_address"] = clean_address(in_row["Family Address"])

        if pandas.isnull(in_row["latitude"]) or pandas.isnull(in_row["longitude"]):
            location = get_location(in_row["cleaned_address"])
            if location is None:
                if location is None:
                    warnings.warn(
                        "Location not found: {}".format(
                            [in_row["cleaned_address"], in_row["Family Address"]]
                        )
                    )
            else:
                in_row["latitude"] = location.latitude
                in_row["longitude"] = location.longitude
        return in_row

    ward_directory_df = ward_directory_df.apply(add_locations, axis=1)
    ward_directory_df.to_csv(ward_directory_export, index=False)


def generate_address_distance(
    input_address, ward_directory_export, output_distance_file, recalc=False
):
    """
    Creates a file of distances to the input address sorted with the closest at the top.

    Parameters
    ----------
    input_address: str
        The address to use as a base to generate distances from.
    ward_directory_export: str
        Path to the ward directory export csv file.
    output_distance_file:  str
        Path to output csv file with distances to the original input_address.
    recalc: bool
        If True, it will recalculate rows without locations.

    """
    input_address = clean_address(input_address.strip())
    generate_address_latlon(ward_directory_export, recalc)
    address_latlon_df = pandas.read_csv(ward_directory_export)

    # use calculated location if address already calculated
    existing_addresses = address_latlon_df.loc[
        address_latlon_df.cleaned_address == input_address
    ]

    try:
        existing_address = existing_addresses.iloc[0]
        location = Location(
            latitude=existing_address["latitude"],
            longitude=existing_address["longitude"],
        )
    except IndexError:
        # look up location if not found in addresses
        location = get_location(input_address)

    if not location:
        raise RuntimeError("Address location not found.")

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
