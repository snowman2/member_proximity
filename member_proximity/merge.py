import warnings

import pandas

from member_proximity import clean_address


def merge_old_into_new(new_ward_directory, old_ward_directory):
    """
    This method is to copy the latitude and longitude from
    the old directory into the new directory.

    Parameters
    ----------
    new_ward_directory: str
        Path to the new ward directory.
    old_ward_directory: str
        Path to the old ward directory.

    """
    old_ward_directory_df = pandas.read_csv(old_ward_directory)
    location_columns = ("latitude", "longitude")
    for location_column in location_columns:
        if location_column not in old_ward_directory_df.columns:
            warnings.warn(
                "Old ward directory is missing required columns {}."
                " Noting done.".format(location_column)
            )
            return

    def add_cleaned_address(in_row):
        return clean_address(in_row["Family Address"])

    if "cleaned_address" not in old_ward_directory_df.columns:
        old_ward_directory_df["cleaned_address"] = old_ward_directory_df.apply(
            add_cleaned_address, axis=1
        )

    new_ward_directory_df = pandas.read_csv(new_ward_directory)
    if "cleaned_address" not in new_ward_directory_df.columns:
        new_ward_directory_df["cleaned_address"] = new_ward_directory_df.apply(
            add_cleaned_address, axis=1
        )

    merged_directories = pandas.merge(
        new_ward_directory_df,
        old_ward_directory_df[["cleaned_address", "latitude", "longitude"]],
        how="left",
        on=["cleaned_address"],
    )

    # if latitude and longitude were in both before, pick first value
    if (
        "latitude_x" in merged_directories.columns
        and "latitude_y" in merged_directories.columns
    ):
        merged_directories["latitude"] = merged_directories.latitude_x.combine_first(
            merged_directories.latitude_y
        )
        merged_directories = merged_directories.drop(
            columns=["latitude_x", "latitude_y"]
        )
    if (
        "longitude_x" in merged_directories.columns
        and "longitude_y" in merged_directories.columns
    ):
        merged_directories["longitude"] = merged_directories.longitude_x.combine_first(
            merged_directories.longitude_y
        )
        merged_directories = merged_directories.drop(
            columns=["longitude_x", "longitude_y"]
        )

    merged_directories.to_csv(new_ward_directory, index=False)
