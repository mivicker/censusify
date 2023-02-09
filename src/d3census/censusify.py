import inspect
import textwrap
import ast

from ast import NodeVisitor, Attribute

from .geography import Geography, FullGeography
from .edition import Edition
from .lookuper import look_up
from .censusified_in_abstract import AbstractCensusifiedFunction


def find_sub_funcs(function) -> list[AbstractCensusifiedFunction]:
    accessed_vars = inspect.getclosurevars(function)
    
    to_check = {
        *accessed_vars.nonlocals.values(),
        *accessed_vars.globals.values()
    }

    return [
        variable for variable in to_check
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
        sub_funcs = find_sub_funcs(function)

        shopping_list = (
                write_variable_shopping_list(function) 
                | join_subshoppinglists(sub_funcs)
            )

        if not shopping_list:
            raise ValueError(
                "No Census variables to look up in censusified function."
            )
    
        self.sub_funcs = sub_funcs
        self._shopping_list = shopping_list
        self.function = function

    @property
    def shopping_list(self) -> set[str]:
        return self._shopping_list

    def __call__(self, *geographies: Geography):
        if all(isinstance(geo, FullGeography) for geo in geographies):
            return self.function(*geographies)

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
