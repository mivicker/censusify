# type: ignore
from d3census import censusify, Geography, Edition

@censusify
def under_eighteen(geo: Geography) -> float:
    return sum([ 
        geo.B01001._003E, 
        geo.B01001._004E,
        geo.B01001._005E,
        geo.B01001._006E,
        geo.B01001._027E,
        geo.B01001._028E,
        geo.B01001._029E,
        geo.B01001._030E,
    ])


@censusify
def under_five(geo: Geography):
    return geo.B01001._003E + geo.B01001._027E


@censusify
def percent_children_under_5(geo: Geography) -> float:
    return under_five(geo) / under_eighteen(geo)


tract = Geography(state='26', county='163', tract='511400')
acs2021 = Edition("acs5", "acs5", "2021")

print(percent_children_under_5(tract)(acs2021))


@censusify
def pop_plus_ten(geo: Geography, ten) -> float:
    return geo.B01001._001E + ten

print(pop_plus_ten(tract, 11)(acs2021))

