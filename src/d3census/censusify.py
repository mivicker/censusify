from typing import Any, Callable, no_type_check
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
    geographies: list[Geography] # This is going to be more complicated...
    tables: list[Table]

    def __call__(self):
        return 


@dataclass
class CensusAPIFunctionGroup:
    function: Callable
    sub_functions: list[CensusAPIFunction]


@no_type_check
def censusify(function):
    closure_vars = getclosurevars(function).unbound

    def add_geography(*geographies: tuple[Geography, ...]):
        def add_edition(edition: Edition):
            
            bound = edition.bind(geographies, closure_vars) 

            return function(*(bound[geo] for geo in geographies))

        return add_edition

    return add_geography

