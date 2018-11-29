"""
Command line interface for member proximity.
"""
import click

from member_proximity import generate_address_distance
from member_proximity.merge import merge_old_into_new


@click.group(name="member-proximity")
def member_proximity():
    """ Member proximity CLI interface."""
    pass


@member_proximity.command(name="distance")
@click.argument("input_address", required=True)
@click.argument("ward_directory_export", type=click.Path(exists=True), required=True)
@click.argument("output_distance_file", type=click.Path(), required=True)
@click.option(
    "-r",
    "--recalc",
    is_flag=True,
    required=False,
    help="Recalculate the missing longitude and latitude in the file.",
)
def distance(recalc, output_distance_file, ward_directory_export, input_address):
    """ Creates a file of distances to the input address sorted with the closest at the top."""
    generate_address_distance(
        input_address, ward_directory_export, output_distance_file, recalc
    )


@member_proximity.command(name="merge")
@click.argument(
    "new_ward_directory_export", type=click.Path(exists=True), required=True
)
@click.argument(
    "old_ward_directory_export", type=click.Path(exists=True), required=True
)
def merge(old_ward_directory_export, new_ward_directory_export):
    """ Merge data from an old version of a ward directory into a new version of the ward directory.
        Keep a backup of the new version before running this command.
    """
    merge_old_into_new(new_ward_directory_export, old_ward_directory_export)
