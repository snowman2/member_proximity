"""
Command line interface for member proximity.
"""
import click

from member_proximity import generate_address_latlon, generate_address_distance


@click.group(name="member-proximity")
def member_proximity():
    """ Top-level command and entry point into the member proximity CLI"""
    pass


@click.command(name="generate-latlon")
@click.argument("ward_directory_export", type=click.Path(exists=True), required=True)
@click.argument("address_latlon_file", type=click.Path(), required=True)
def generate_latlon(address_latlon_file, ward_directory_export):
    """
    Generate a file with latitude and longitudes for the address.
    """
    generate_address_latlon(ward_directory_export, address_latlon_file)


@click.command(name="generate-distance")
@click.argument("input_address", required=True)
@click.argument("address_latlon_file", type=click.Path(exists=True), required=True)
@click.argument("output_distance_file", type=click.Path(), required=True)
def generate_distance(output_distance_file, address_latlon_file, input_address):
    """
    Creates a file of distances to the input address sorted with the closest at the top.
    """
    generate_address_distance(input_address, address_latlon_file, output_distance_file)


member_proximity.add_command(generate_latlon)
member_proximity.add_command(generate_distance)
