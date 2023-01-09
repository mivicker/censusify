from typing import Any, Callable, no_type_check
import inspect
from inspect import getclosurevars
from dataclasses import dataclass
import ast

from ast import NodeVisitor, Attribute

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


class GeoVisitor(NodeVisitor):
    def __init__(self) -> None:
        self.target_variables = set()
        super().__init__()

    def visit_Attribute(self, node: Attribute) -> None:
        match node:
            case Attribute(
                value=Attribute(attr=attr),
                attr=sub_attr
            ):
                if hasattr(Geography, attr):
                    self.target_variables.add(attr+sub_attr)
                return

            case _:
                return


def write_variable_shopping_list(function) -> set[str]:
    tree = ast.parse(inspect.getsource(function))
    visitor = GeoVisitor()
    visitor.visit(tree)

    return visitor.target_variables


def censusify(function):
    shopping_list = write_variable_shopping_list(function)

    if not shopping_list:
        raise ValueError("No Census variables to look up in censusified function.")

    def add_geography(*geographies: tuple[Geography, ...]):
        def add_edition(edition: Edition):

            bound = edition.bind(geographies, look_up_vars) #type: ignore
            return function(*(bound[geo] for geo in geographies)) #type: ignore

        return add_edition

    return add_geography
