from typing import Any, Callable
import inspect
import textwrap
from dataclasses import dataclass
import ast

from ast import NodeVisitor, Attribute

from .geography import Geography
from .edition import Edition
from lookuper import look_up


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
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    visitor = GeoVisitor()
    visitor.visit(tree)

    return visitor.target_variables


class CensusifiedGeographyFunc:
    def __init__(self, censusified_func, geography: Geography):
        self.function = censusified_func
        self.geography = geography

    def __call__(self, edition: Edition):
        bound = look_up(geographies, self.function.shopping_list, edition.filled_base_url) #type: ignore
        return self.function.function(*(bound[geo] for geo in geographies)) #type: ignore

    def return_un_calculated(self, edition: Edition):
        return look_up(geographies, self.function.shopping_list, edition.filled_base_url) #type: ignore


class CensusifiedFunc:
    def __init__(self, function):
        shopping_list = write_variable_shopping_list(function)

        if not shopping_list:
            raise ValueError("No Census variables to look up in censusified function.")
        self.shopping_list = shopping_list
        self.function = function

    def __call__(self, geography: Geography):
        return CensusifiedGeographyFunc(self, geography)


def censusify(function):
    return CensusifiedFunc(function)
