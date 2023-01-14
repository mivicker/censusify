from abc import abstractproperty
from typing import Any, Callable
import inspect
import textwrap
from dataclasses import dataclass
import ast

from ast import NodeVisitor, Attribute, Name, Call

from .geography import Geography
from .edition import Edition
from .lookuper import look_up


class AbstractCensusifiedFunction:
    @abstractproperty
    def shopping_list(self) -> list[str]:
        pass



class GeoVisitor(NodeVisitor):
    def __init__(self) -> None:
        # Give local precidence
        self.variables_in_scope = {**globals(), **locals()}
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

    def visit_Call(self, node: Call) -> Any:
        function_id = node.func.id # type: ignore
        function = self.variables_in_scope[function_id]

        match function:
            case AbstractCensusifiedFunction():
                self.target_variables.add(function.shopping_list)


def write_variable_shopping_list(function) -> set[str]:
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    visitor = GeoVisitor()
    visitor.visit(tree)

    return visitor.target_variables


class CensusifiedGeographyFunc(AbstractCensusifiedFunction):
    def __init__(self, censusified_func, *geographies: Geography):
        self.function = censusified_func
        self.geographies = geographies

    @property
    def shopping_list(self) -> list[str]:
        return self.function.shopping_list

    def bind_edition(self, edition: Edition):
        return look_up(
            self.geographies, 
            self.function.shopping_list, 
            edition.filled_base_url
        )
    
    def __call__(self, edition: Edition):
        bound = self.bind_edition(edition)
        return self.function.function(*(bound[geo] for geo in self.geographies))


class CensusifiedFunc(AbstractCensusifiedFunction):
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
