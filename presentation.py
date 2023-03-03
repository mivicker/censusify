from d3census import censusify, Geography, Edition


@censusify
def under_18(geo: Geography) -> tuple[float, float]:
    return ((geo.B01001._002E, geo.B01001._002M), 
            (geo.B01001._001E, geo.B01001._001M))


@censusify
def ten_to_fourteen_by_race(geo: Geography) -> dict[str, float]:
    return {
        'white': geo.B01001H._005E + geo.B01001H._020E, 
        'black': geo.B01001B._005E + geo.B01001B._020E,
    }


@censusify
def ten_to_fourteen_total(geo: Geography) -> float:
    return geo.B01001._005E + geo.B01001._029E


print(under_18(Geography("Detroit", "26", "22000"))(Edition("","acs5", "2021")))