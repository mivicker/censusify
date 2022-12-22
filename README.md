# d3censusify

A functional way to manage calls to the Census API.

## Installing from github

```console
> pip install git+https://github.com/mikevatd3/censusify
```

## Example use

```python
from censusify import Geography, Edition, censusify


# Define a funcion with the censusify decorator. You can use any valid table names
# as attributes to the geographies that you plan to pass.

@censusify
def city_pct_of_state_pop(city: Geography, state: Geography) -> float: # type hints are optional
  return city.B01001_001E / state.B01001_001E

# You then can define your target geographies

detroit = Geography(
  state='26',
  place='22000'
)

michigan = Geography(
  state='26'
)

# Then you specify the ACS edition that you'd like to use.

acs21 = Edition(
  key='<your census key>',
  product='acs5',
  year=2021,
)

# Then you can call the function on the given geographies, and 
# censusify does the rest of the work to pull in the correct tables.

# The call order is geographies, then edition

city_pct_of_state_pop(detroit, michigan)(acs21)

# ~0.06

atlanta = Geography(
  state='13',
  place='04000'
)

georgia = Geography(
  state='13'
)

city_pct_of_state_pop(detroit, michigan)(acs21)

```



TODO:

- Add a describe function to verify all variable names and geography names.
- Add async to the API calls
- Fuss with the interface so you can get more help defining functions earlier
- Add ability to group and nest functions
- Bring along MOE to have it handled reasonably