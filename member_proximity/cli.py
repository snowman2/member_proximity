"""
Command line interface for member proximity.
"""
import click

from member_proximity import generate_address_distance


@click.group(name="member-proximity")
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
def member_proximity(
    recalc, output_distance_file, ward_directory_export, input_address
):
    """ Creates a file of distances to the input address sorted with the closest at the top."""
    generate_address_distance(
        input_address, ward_directory_export, output_distance_file, recalc
    )
