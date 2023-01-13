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

    @property
    def filled_base_url(self) -> str:
        return self.base_url.format(
            year=str(self.year), product=self.product
        )
