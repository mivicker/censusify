# d3geocoder

This geocoder uses the same core calculation as the IPDS parcel geocoder,
but makes it easily available for use with Pandas.

## Installing from github

```console
> pip install git+https://github.com/mikevatd3/d3geocoder
```

### Geopandas installation
*Installing geopandas with pip from a vanilla install of python is not very easy.*

I recommend using Anaconda for this, specifically [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Example use

```python
import pandas as pd
from d3geocoder import Geocoder


gc = Geocoder(
    user=<your username>,
    password=<your password>,
    host=<host>,
    dbname=<dbname>, # This can only be ipds because it has the necessary routines available
)

series = pd.Series([
    "2 Woodward Ave, Detroit, MI",
    "500 Temple Street, Detroit, MI",
    "4870 Cass Ave, Detroit, MI",
    "10 Woodward Ave, Detroit, MI", # Doesn't exist
])

df = gc.geocode(series)
```

This will return as a GeoDataFrame:

||id|d3_id|geom|
|-|-|----|--|
|0|0|15717717|POINT(...)|
|1|1|15637703|POINT(...)|
|2|2|15594487|POINT(...)|
|3|3|-1| None|

If the address is not found, a -1 will be returned for d3_id and None will be returned for geometry.

To get to x, y for this you can use geopandas x and y attributes on the geom column.

```python
df["x"] = df["geom"].x
df["y"] = df["geom"].y
```


TODO:
- This currently leaves the temp table behind and replaces it on the next run, but should instead clean up after itself.
- Optional kwarg to set precisely the CRS but I have questions
  - What CRS is used on the master table in ipds?
  - It says in the Map Product Review Quick Reference "NAD_1983_StatePlane_Michigan_South_FIPS_2113_I....' -- 'ESRI: 2113'
    - Does geopandas accept ESRI codes?
    - If not is there a comparable EPSG code? [link](https://spatialreference.org/ref/?search=michigan)
- Currently only returns centroid, but we have the full shape in the database, so add a optional flag to bring the whole shape over.
- Should probably not be used for larger datasets in its current form, say >10,000 rows.
  - Would like to build in a chunking mechanism to handle this (maybe with async too)
- Handle the upload process that is currently done by IPDS parcel geocoder, mostly to avoid awkward command line interface that I always mess up, lol.