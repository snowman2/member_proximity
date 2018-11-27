# member_proximity
Find members of the church who are closest to an address based on ward directory.


## Step 1: Generate file with latitude and longitude for each address 

You only need to do this once for step 2.

```python
from member_proximity import generate_address_latlon

ward_directory_export = "123456.csv"
address_latlon_file = "123456_latlon.csv"

generate_address_latlon(ward_directory_export, address_latlon_file)
```

## Step 2: Generate distance file to the address of interest

You can repeat this step as many times as you need to to generate a distance file for an address.

```python
from member_proximity import generate_address_distance

input_address = "1234 Abc Dr City, Iowa 12345"
address_latlon_file = "123456_latlon.csv"
output_distance_file = "123456_distance.csv"

generate_address_distance(input_address, address_latlon_file, output_distance_file)
```