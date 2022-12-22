from dataclasses import dataclass

import json
import requests

from .geography import Geography, FullGeography, build_call_tree


def filter_to_geo_attrs(dictionary):
    return {
        key.lower(): value
        for key, value in dictionary.items()
        if key.lower() in set(Geography.__match_args__)
    }


def build_full_geography(dictionary):
    result = FullGeography()

    for key, value in dictionary.items():
        result.__setattr__(
            key, float(value)
        )  # The casting should probably be done elsewhere

    return result


def build_full_geos_from(response: list[list]) -> list[FullGeography]:
    labels, *data = response

    return {
        Geography(**filter_to_geo_attrs(dict(zip(labels, column)))): build_full_geography(
            dict(zip(labels, column))
        )
        for column in data
    }


@dataclass
class Edition:
    key: str  # This is annoying that we have to set the api key on this object
    product: str
    year: int
    base_url: str = "https://api.census.gov/data/{year}/acs/{product}?"

    def bind(
        self, geographies: list[Geography], closure_vars: list[str]
    ) -> list[FullGeography]:

        call_tree = build_call_tree(geographies)
        geo_filters = call_tree.resolve()
        get_str = ",".join(closure_vars)
        filled_base_url = self.base_url.format(
            year=str(self.year), product=self.product
        )

        responses = [
            json.loads(
                requests.get(f"{filled_base_url}get={get_str}{geo_filter}").content
            )
            for geo_filter in geo_filters
        ]
        
        return {
            key: val for response in responses 
            for key, val in build_full_geos_from(response).items()
        }

acs_groups = json.loads(requests.get("https://api.census.gov/data/2020/acs/acs5/groups.json").content)