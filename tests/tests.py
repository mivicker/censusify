# type: ignore
from pprint import pprint

from d3census import censusify, Geography, Edition
from d3census.censusify import find_subobjects
from d3census.geography import build_call_tree
    # This makes sense for one geography

"""Integration Tests"""

def test_single_geo_single_val():
    mi = Geography(state='26')
    acs2021 = Edition("acs5", "acs1", "2021")
    mi_total_pop = censusify(lambda state: state.B01001_001E)(mi)(acs2021)
    
    assert mi_total_pop == 10_050_811 # I wonder if these ever change?


def test_single_geo_multiple_vals():
    mi = Geography(state='26')
    acs2019 = Edition("acs5", "acs5", "2019")

    @censusify
    def under_eighteen(geo: Geography) -> float:
        return sum( 
            [ 
                geo.B01001_003E, 
                geo.B01001_004E,
                geo.B01001_005E,
                geo.B01001_006E,
                geo.B01001_027E,
                geo.B01001_028E,
                geo.B01001_029E,
                geo.B01001_030E,
            ]
        )
    
    zero_to_seventeen = under_eighteen(mi)(acs2019)
    
    assert  zero_to_seventeen == 2_177_878


def test_multi_geo_single_parent():
    detroit = Geography(state='26', place='22000')
    grand_rapids = Geography(state='26', place='34000')
    acs2021 = Edition("acs5", "acs5", "2021")

    @censusify
    def geo_difference(first: Geography, second: Geography) -> float:
        return first.B01001_001E - second.B01001_001E

    difference = geo_difference(detroit, grand_rapids)(acs2021)

    assert  difference == 447_800


def test_multi_geo_multi_parent_single_level():
    detroit = Geography(state='26', place='22000')
    cincinnati = Geography(state='39', place='15000')
    atlanta = Geography(state='13', place='04000')

    acs2019 = Edition("acs5", "acs5", "2019")

    @censusify
    def list_of_pops(geo_one, geo_two, geo_three) -> list[float]:
        # This fails
        return [
            geo_one.B01001_001E,
            geo_two.B01001_001E,
            geo_three.B01001_001E,
        ]

    assert len(list_of_pops(
        detroit,
        cincinnati,
        atlanta
    )(acs2019)) == 3


def test_multi_geo_star_func():
    detroit = Geography(state='26', place='22000')
    grand_rapids = Geography(state='26', place='34000')
    cinncinnati = Geography(state='39', place='15000')
    dayton = Geography(state='39', place='21000')
    atlanta = Geography(state='13', place='04000')

    acs2019 = Edition("acs5", "acs5", "2019")

    @censusify
    def list_of_pops(*geos) -> list[float]:
        # This fails because of the comprehension
        return [
            (
                sum([geo.B01001_004E, geo.B01001_005E]) 
                / geo.B01001_001E
            ) for geo in geos
        ]

    assert len(list_of_pops(
        detroit,
        grand_rapids,
        cinncinnati,
        dayton,
        atlanta,
    )(acs2019)) == 5


def test_calltree_same_parent():
    detroit = Geography(state='26', place='22000')
    grand_rapids = Geography(state='26', place='34000')
    cinncinnati = Geography(state='39', place='15000')
    dayton = Geography(state='39', place='21000')
    atlanta = Geography(state='13', place='04000')

    call_tree = build_call_tree([
        detroit, grand_rapids, dayton, cinncinnati, atlanta
    ])

    assert len(call_tree.resolve()) == 3


def test_multi_geo_multi_parent_multi_level():
    wayne = Geography(state='26', county='163')
    tract = Geography(state='26', county='163', tract='511400')
    bg_5 = Geography(state='26', county='163', tract='511400', block_group='5')
    livingston = Geography(state='26', county='093')
    grand_rapids = Geography(state='26', place='34000')
    cincinnati = Geography(state='39', place='15000')
    dayton = Geography(state='39', place='21000')
    atlanta = Geography(state='13', place='04000')

    acs2019 = Edition("acs5", "acs5", "2019")


    @censusify
    def sum_weird_things(*geos):
        return sum(geo.B01001_028E for geo in geos)
    
    print(Geography.__match_args__)

    print(sum_weird_things(
        wayne,
        tract,
        bg_5,
        livingston,
        grand_rapids,
        cincinnati,
        dayton,
        atlanta
    )(acs2019))

# Geography 

# Call tree

# Edition


# Variables (codes in acs)
#   'get=' function specifies the required and selected variables you are requesting the API to give you.
# Predica
#   how the variables should be limited and filtered
#   &for restricts the variables by geography at various levels
#   &in (delimited by %20)


# What we want to avoid, though currently unsure how to do it.
# Too many lookups
# Too large of lookups


if __name__ == "__main__":
    # test_single_geo_single_val()
    # test_single_geo_multiple_vals()
    # test_calltree_same_parent()
    # test_multi_geo_single_parent()
    # test_multi_geo_multi_parent_single_level()
    # test_multi_geo_star_func()
    test_multi_geo_multi_parent_multi_level()
