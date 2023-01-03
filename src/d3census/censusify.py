from typing import Any, Callable, no_type_check
from keyword import iskeyword
import builtins
from inspect import getclosurevars, iscode
from dataclasses import dataclass

from .geography import Geography
from .edition import Edition


def describe(callable: Callable[[Geography, ...], Any]) -> Callable[[Edition], str]:  # type: ignore
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
    function: Callable[[Geography, ...], Any] # type: ignore
    geographies: list[Geography]  # This is going to be more complicated...
    tables: list[Table]

    def __call__(self):
        return


@dataclass
class CensusAPIFunctionGroup:
    function: Callable
    sub_functions: list[CensusAPIFunction]


def find_subobjects(function):
    """
    This needs to be improved.
    """
    to_check = list(function.__code__.co_consts)
    result = set()

    while to_check:
        subobject = to_check.pop()
        if iscode(subobject):
            for unbound in subobject.co_names:
                if (
                    iskeyword(unbound) # check against keywords
                    or (unbound in set(dir(builtins))) # check against builtins
                    or (unbound in ['bind']) # check against called module methodnames
                ):
                    continue
                result.add(unbound)
            to_check.extend(subobject.co_consts)

    return result


@no_type_check
def censusify(function):
    closure_vars = set(getclosurevars(function).unbound)
    sub_clousure_vars = find_subobjects(function)

    look_up_vars = closure_vars | sub_clousure_vars
    # This looks through comprehensions

    if not look_up_vars:
        raise ValueError("No variables to look up.")

    def add_geography(*geographies: tuple[Geography, ...]):
        def add_edition(edition: Edition):

            bound = edition.bind(geographies, look_up_vars) #type: ignore
            return function(*(bound[geo] for geo in geographies)) #type: ignore

        return add_edition

    return add_geography
