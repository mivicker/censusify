from typing import AbstractSet

import asyncio

from .geography import FullGeography, Geography, build_call_tree
from .requestmanager import request_manager


class EmptyTable:
    """
    This is the empty table type that can be instantiated
    to then fill with value attributes.
    """


def filter_to_geo_attrs(dictionary):
    return {
        key.lower().replace(' ', '_'): value
        for key, value in dictionary.items()
        if key.lower().replace(' ', '_') in set(Geography.__match_args__)
    }


def build_full_geography(dictionary):
    result = FullGeography()

    for key, value in dictionary.items():
        try:
            table, variable = key.split("_")

            if not hasattr(result, table):
                result.__setattr__(table, EmptyTable())

            result.__getattribute__(table).__setattr__(
                "_" + variable, float(value)
            )  # The casting should probably be done elsewhere

        except ValueError:
            result.__setattr__(
                key, value
            )

    return result


def build_full_geos_from(
        response: list[list]
    ) -> dict[Geography, FullGeography]:
    
    labels, *data = response

    geographies = {
        Geography(
            **filter_to_geo_attrs(dict(zip(labels, column)))
        ): build_full_geography(dict(zip(labels, column)))
        for column in data
    }
    
    return geographies


def raw_look_up(
    geographies: list[Geography],
) - :
    call_tree = build_call_tree(geographies)
    geo_filters = call_tree.resolve()
    get_str = ",".join(closure_vars)

    calls = [
        f"{filled_base_url}get={get_str}{geo_filter}"
        for geo_filter in geo_filters
    ]

    responses = asyncio.run(request_manager(calls))
    # This should build the call tree and return the raw response.



def look_up(
    geographies: list[Geography],
    closure_vars: AbstractSet[str],
    filled_base_url: str,
) -> dict[Geography, FullGeography]:

    call_tree = build_call_tree(geographies)
    geo_filters = call_tree.resolve()
    get_str = ",".join(closure_vars)

    calls = [
        f"{filled_base_url}get={get_str}{geo_filter}"
        for geo_filter in geo_filters
    ]

    responses = asyncio.run(request_manager(calls))

    return {
        key: val for response in responses 
        for key, val in build_full_geos_from(response).items()
    }

