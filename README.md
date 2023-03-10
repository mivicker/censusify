# censusify
An approach to managing calls to the US Census American Community Survey API.


## Installing from github

```console
> pip install git+https://github.com/data-driven-detroit/censusify
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

city_pct_of_state_pop(atlanta, georgia)(acs21)

# You can also use comprehensions and stars to use flexible
# numbers of arguments.

@censusify
def sum_several_geos(*geos: Tuple[Geography]) -> float:
    return sum([geo.B01001_001E for geo in geos])


@censusify
def some_percentage(*geos: Tuple[Geography]) -> float:
    
    sub_calcs = [(geo.B01001_026E + geo.B01001_034E) for geo in geos]

    return [(sub_calc / geo.B01001_001E) for sub_calc, geo in zip(sub_calcs, geos)]
```

## When using in a Jupyter notebook
Censusify makes mutiple calls to the Census API asynchronously, which currently breaks when running within a jupyter notebook. The solution currently is to use nest_asyncio.

```
pip install nest_asyncio
```

Then within your notebook before calling any censusified functions add:

```python
import nest_asyncio

nest_asyncio.apply()
```

TODO:

- Add a describe function to verify all variable names and geography names.
- Bring along MOE to have it handled reasonably.
