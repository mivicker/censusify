from dataclasses import dataclass

from typing import AbstractSet

from .geography import Geography, FullGeography
from .lookuper import look_up


@dataclass
class Edition:
    key: str  # This is annoying that we have to set the api key on this object
    product: str
    year: int
    base_url: str = "https://api.census.gov/data/{year}/acs/{product}?"

    def bind(
        self, geographies: list[Geography], closure_vars: AbstractSet[str]
    ) -> dict[Geography, FullGeography]:
        filled_base_url = self.base_url.format(
            year=str(self.year), product=self.product
        )

        return look_up(geographies, closure_vars, filled_base_url)

