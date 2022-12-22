import tomli
import pandas as pd
from d3geocoder import Geocoder


def test_one():
    with open("config.toml", "rb") as f:
        config = tomli.load(f)

    host, dbname, user, password = config["edw"].values()

    gc = Geocoder(
        user=user,
        password=password,
        host=host,
        dbname=dbname,
    )


    series = pd.Series([
        "2 Woodward Ave, Detroit, MI",
        "500 Temple Street, Detroit, MI",
        "4870 Cass Ave, Detroit, MI",
    ])


    print(gc.geocode(series))


if __name__ == "__main__":
    test_one()