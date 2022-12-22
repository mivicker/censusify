from typing import Any, Callable
from inspect import getclosurevars
from dataclasses import dataclass

from .geography import Geography
from .edition import Edition


def describe(callable: Callable[[Geography, ...], Any]) -> Callable[[Edition], str]:
    """
    Pass a censusified function and get a docstring on of the geographies and tables
    that are accessed.
    """


@dataclass
class TableGroup:
    pass


@dataclass
class Table:
    pass


@dataclass
class CensusAPIFunction:
    function: Callable[[Geography, ...], Any]
    geographies: list[Geography]
    tables: list[Table]

    def __call__(self):
        return 


def censusify(function):
    closure_vars = getclosurevars(function).unbound

    def add_geography(*geographies: tuple[Geography, ...]):
        def add_edition(edition: Edition):
            
            bound = edition.bind(geographies, closure_vars) 

            return function(*(bound[geo] for geo in geographies))

        return add_edition

    return add_geography


if __name__ == "__main__":

    # This makes sense for one geography
    @censusify
    def under_eighteen(geo: Geography) -> float:
        return sum(
            [
                geo.B01001_003E,
                geo.B01001_004E,
                geo.B01001_005E,
                geo.B01001_006E,
                geo.B01001_027E,
                geo.B01001_028E,
                geo.B01001_029E,
                geo.B01001_030E,
            ]
        )

    acs2020 = Edition("acs5", "acs5", "2020")

    mi = Geography(state=26)
    result = under_eighteen(mi)(acs2020)
    print(result)

    assert result == 2_177_878

    oh = Geography(state=39)
    result = under_eighteen(oh)(acs2020)
    print(result)

    # What should this look like for multiple geographies

    mi_total_pop = censusify(lambda mi: [mi.B01001_001E])(mi)(acs2020)

    print(mi_total_pop)


# Variables (codes in acs)
#   'get=' function specifies the required and selected variables you are requesting the API to give you.
# Predicate
#   how the variables should be limited and filtered
#   &for restricts the variables by geography at various levels
#   &in (delimited by %20)


# What we want to avoid, though currently unsure how to do it.
# Too many lookups
# Too large of lookups
