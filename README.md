# member_proximity
Find members of the church who are closest to an address based on ward directory.

Before using this tool, you may want to check out Ward Maps: https://www.lds.org/maps/directory/.


This uses the Nomatim geocoder credit “© OpenStreetMap contributors”.
https://www.openstreetmap.org/copyright

## CLI Interface

### Generate distance file to the address of interest.

The first run may take a few minutes to run as it is looking up addresses.
The next runs should be faster as the results are cached in the file.


```bash
member-proximity distance "1234 Abc Dr City, Iowa 12345" 123456.csv 123456_distance.csv
```

### Merge old ward directory file cache data into the new ward directory version.

```bash
member-proximity merge 123456_new.csv 123456_old.csv
```


## Python Interface

### Generate distance file to the address of interest.

The first run may take a few minutes to run as it is looking up addresses.
The next runs should be faster as the results are cached in the file.

```python
from member_proximity import generate_address_distance

input_address = "1234 Abc Dr City, Iowa 12345"
ward_directory_export = "123456.csv"
output_distance_file = "123456_distance.csv"

generate_address_distance(input_address, ward_directory_export, output_distance_file)
```

### Merge old ward directory file cache data into the new ward directory version.

```python
from member_proximity.merge import merge_old_into_new

merge_old_into_new("123456_new.csv", "123456_old.csv")

```
