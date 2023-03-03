from typing import Optional
from dataclasses import dataclass, field
from collections import defaultdict

from .tablereference import BaseGeography


@dataclass
class GeographyWildcard(BaseGeography):
    """
    This is what you'd use anytime you want to pass a wildcard (*) for a
    geographic level.
    """


@dataclass
class GeographyLevel:
    code: str
    parents: list['GeographyLevel']


@dataclass(frozen=True)
class Geography(BaseGeography):
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
    def specificity(self) -> str:
        specificity_order = [
            "block",
            "block_group",
            "tract",
            "zcta",
            "subdivision",
            "county",
            "place",
            "state",
        ]

        for level in specificity_order:
            if getattr(self, level) != None:
                return level

        return "us"

    @property
    def geography_level(self):
        level_map = {
            "us": "010",
            "state": "040",
            "county": "050",
            "tract": "140",
            "congressional_district": "500",
            "state_senate_district": "610",
            "state_house_district": "620",
            "zcta": "860",
            # "950", # school_district primary
            # "960", # school_district secondary
            "school_district": "970", # school_district unified
        }

    def census_reporter_geoid(self):
        return f"{self.geography_level}00US{self.identifier}"

    @property
    def geoid(self):
        """
        This is kind of a hard function to write.
        """
        raise NotImplementedError("This would be nice to have, but Mike gave up before writing it.")
    
    identifier = geoid

    def __post_init__(self):
        required_parents = {
            "block_group": [],
        }


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


@dataclass
class HipCallTree:
    pass


