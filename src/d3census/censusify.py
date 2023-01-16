from abc import abstractproperty
from typing import Callable
import inspect
import textwrap
import ast

from ast import NodeVisitor, Attribute

from .geography import Geography
from .edition import Edition
from .lookuper import look_up



class AbstractCensusifiedFunction:
    @abstractproperty
    def shopping_list(self) -> set[str]:
        pass


def find_sub_funcs(function) -> list[Callable]:
    accessed_vars = inspect.getclosurevars(function)
    return [
        variable for variable in accessed_vars.globals.values() 
        if isinstance(variable, AbstractCensusifiedFunction)
    ]


def join_subshoppinglists(
    functions: list[AbstractCensusifiedFunction]
) -> set[str]:
    return {item for func in functions for item in func.shopping_list}


class GeoVisitor(NodeVisitor):
    def __init__(self) -> None:
        # Give local precidence
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
            case _:
                return


def write_variable_shopping_list(function) -> set[str]:
    tree = ast.parse(
        textwrap.dedent(inspect.getsource(function))
    )
    visitor = GeoVisitor()
    visitor.visit(tree)

    return visitor.target_variables


class CensusifiedFunc(AbstractCensusifiedFunction):
    def __init__(self, function):
        self.sub_funcs = find_sub_funcs(function)
        shopping_list = (
                write_variable_shopping_list(function) 
                | join_subshoppinglists(self.sub_funcs)
            )

        if not shopping_list:
            raise ValueError(
                "No Census variables to look up in censusified function."
            )

        self._shopping_list = shopping_list
        self.function = function

    @property
    def shopping_list(self) -> set[str]:
        return self._shopping_list

    def __call__(self, *geographies: Geography):

        frame = inspect.currentframe()
        callframe = inspect.getouterframes(frame, 2)
        # print(globals()[callframe[1].function])
        # print(isinstance(callframe[1].function, CensusifiedGeographyFunc))
        
        """
        if callframe[1].function == "__call__":
            return self.function(*geographies)
        """

        return CensusifiedGeographyFunc(self, *geographies)


class CensusifiedGeographyFunc(AbstractCensusifiedFunction):
    def __init__(self, censusified_func: CensusifiedFunc, *geographies: Geography):
        self.function = censusified_func
        self.geographies = geographies

    @property
    def shopping_list(self) -> set[str]:
        return self.function.shopping_list

    def bind_edition(self, edition: Edition):
        return look_up(
            self.geographies, 
            self.function.shopping_list, 
            edition.filled_base_url
        )

    def geo_call(self, edition: Edition):
        bound = self.bind_edition(edition)
        return self.function.function(*(bound[geo] for geo in self.geographies))

    def __call__(self, edition: Edition):
        return self.geo_call(edition)


def censusify(function):
    return CensusifiedFunc(function)
