from typing import Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class GeoTemplate:
    """
    This the template that is used to define functions.
    This may not even be necessary.
    """
    pass


@dataclass
class GeographySet:
    """
    This is what you'd use anytime you want to pass a wildcard (*) for a
    geographic level.
    """
    pass



@dataclass(frozen=True)
class Geography:
    # An optimization on this could be to store everything as geoid
    # and step through the string to step back out to the tree.
    # Then we could use the geoid to hash back to the geography.
    # we could have a special factory for a set.
    """
    This is the geography that is passed to a censusified function that
    specifies the geography to filter to from the API.
    """
    name: str = field(compare=False, default='')
    # >
    # aianhh: Optional[str] = None # American Indian/Alaska Native Area/Hawaiian Home Land
    # ->
    # urban_areas: Optional[str] = None
    # core_based_statistical_areas: Optional[str] = None
    # zcta: Optional[str] = None # Zip code tabulation area
    state: Optional[str] = None
    # -->
    # congressional_district: Optional[str] = None
    # school_district: Optional[str] = None
    place: Optional[str] = None
    # puma: Optional[str] = None # Public Use Microdata Areas
    # anrc: Optional[str] = None # Alaska Native Regional Corporation
    # sld: Optional[str] = None # State legislative district
    # uga: Optional[str] = None # Oregon urban growth area
    county: Optional[str] = None
    # --->
    # taz: Optional[str] = None # Traffic Analysis Zones
    tract: Optional[str] = None
    # ---->
    block_group: Optional[str] = None
    # --->
    subdivision: Optional[str] = None    
    # ---->
    # subbarrio: Optional[str] = None
    # subminor_civil_divisions: = None
    block: Optional[str] = None

    @property
    def geoid(self):
        """
        This is kind of a hard function to write.
        """
        pass


    def __post_init__(self):
        layers = [
            [self.state],
            [self.county, self.place],
            [self.tract, self.subdivision],
            [self.block_group],
            [self.block],
        ] #There are many breaking cases for this approach, you have to check the tree is valid

        for layer in layers:
            if sum([geo != None for geo in layer]) > 1:
                raise ValueError("Invalid combination of geographies. See geography documentation for details.")


class FullGeography:
    """
    The placeholder class for distinguishing if a geography is full.
    """


@dataclass
class CallTree:
    """
    The call tree is where the coupling to the API is strongest.
    Maybe should be grouped with Edition to represent fully that coupling.
    """
    states: list = field(default_factory=list)
    counties: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    places: defaultdict[list] = field(default_factory=lambda: defaultdict(list))   
    subdivisions: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    tracts: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    block_groups: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    blocks: defaultdict[list] = field(default_factory=lambda: defaultdict(list))

    def resolve_states(self) -> list[str]:
        return [f"&for=state:{state}" for state in self.states]

    def resolve_counties(self) -> list[str]:
        return [
            f"&for=county:{','.join(counties)}&in=state:{state}" 
            for state, counties in self.counties.items()
        ]

    def resolve_places(self) -> list[str]:
        return [
            f"&for=place:{','.join(place for place in places)}&in=state:{state}" 
            for state, places in self.places.items()
        ]

    def resolve_subdivisions(self) -> list[str]:
        return [
            f"&for=county%20subdivision:{subdivision}&in=state:{state}%20county:{county}"
            for (state, county), subdivision in self.subdivisions.items()
        ]

    def resolve_tracts(self) -> list[str]:
        result = []
        for (state, county), tracts in self.tracts.items():
            tract_str = ",".join(tract for tract in tracts)
            result.append(
                f"&for=tract:{tract_str}&in=state:{state}%20county:{county}"
            )

        return result

    def resolve_block_groups(self) -> list[str]:
        result = []
        for (state, county, tract), bgroups in self.block_groups.items():
            bg_string = ",".join(bgroups)

            result.append(
                f"&for=block%20group:{bg_string}&in=tract:{tract}%20state:{state}%20county:{county}"
            )

        return result


    def resolve_blocks(self) -> list[str]:
        raise ValueError("Block geographies are not supported on ACS.")


    def resolve(self) -> list[str]:
        return [
            *self.resolve_places(),
            *self.resolve_states(),
            *self.resolve_counties(),
            *self.resolve_tracts(),
            *self.resolve_block_groups(),
        ]


def build_call_tree(geographies: list[Geography]) -> CallTree:
    """
    Build a call tree object given a list of geographies.
    """
    call_tree  = CallTree()
    for geography in geographies:
        match geography:
            case Geography(
                state=state,
                county=None,
                place=None,
                subdivision=None,
                tract=None,
                block_group=None,
                block=None,
            ): 
                call_tree.states.append(state)

            case Geography(
                state=state,
                county=county,
                place=None,
                tract=None,
                block=None,
            ):
                call_tree.counties[state].append(county)

            case Geography(
                state=state,
                county=None,
                place=place,
                tract=None,
                block=None,
            ):
                call_tree.places[state].append(place)

            case Geography(
                state=state,
                county=county,
                place=None,
                subdivision=subdivision,
                tract=None,
                block=None,
            ):
                call_tree.subdivisions[(state, county)].append(subdivision)

            case Geography(
                state=state,
                county=county,
                place=None,
                subdivision=None,
                tract=tract,
                block_group=None,
                block=None,
            ):
                call_tree.tracts[(state, county)].append(tract)

            case Geography(
                state=state,
                county=county,
                subdivision=None,
                tract=tract,
                block_group=block_group,
                block=None,
            ):
                call_tree.block_groups[(state, county, tract)].append(block_group)

            case Geography(
                state=state,
                county=county,
                subdivision=None,
                tract=tract,
                block_group=block_group,
                block=block,
            ):
                call_tree.blocks[(state, county, tract, block_group)].append(block)

    return call_tree





