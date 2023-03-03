#type: ignore
import pandas as pd

from d3census import censusify, Geography, Edition
from d3census.censusify import CensusifiedFunc
from d3census.geography import GeographyWildcard
from d3census.lookuper import look_up


@censusify
def total_pop(geo: Geography) -> float:
    return geo.B01001._001E


@censusify
def pct_over_65_living_alone(geo: Geography) -> float:
    try:
        living_alone = geo.B11010._012E + geo.B11010._005E
        not_living_alone = geo.B11010._015E + geo.B11010._008E

        return living_alone / (not_living_alone + living_alone)

    except ZeroDivisionError:
        return float('NaN')


wayne_tracts = Geography(
    state='26',
    county='163',
    tract='*'
)

acs2021 = Edition(
    key='',
    product='acs5',
    year=2021
)


def collect_lists(*functions: CensusifiedFunc) -> set[str]:
    return set().union(
            *(function.shopping_list for function in functions)
        )

def apply_multiple(
        geo: GeographyWildcard, 
        edition: Edition, 
        functions: list[CensusifiedFunc]
) -> pd.DataFrame:
    result = look_up([geo], collect_lists(*functions), edition.filled_base_url)
    fulls = result.values()
   
    df = pd.DataFrame(
        (full.tract,) + tuple(function.function(full) for function in functions)
        for full in fulls
    )

    df.columns = ['tract'] + [function.function.__name__ for function in functions]

    # Need to have a way to grab the most specific geo to order by,
    # or simply give a geoid (maybe this

    return  df

print(apply_multiple(
    wayne_tracts, 
    acs2021, 
    [total_pop, pct_over_65_living_alone]
)[:20])

# GeographySet = list[Geography] | GeographyWildcard
