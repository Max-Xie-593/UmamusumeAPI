from __future__ import annotations

from typing import Optional, List
from .base import UmaMusumeModel, LocalizedNameMixin, PagePropsModel
from .enums import DidNotExist, UnreleasedServer, Location

class Alt(UmaMusumeModel):
    course_id: int
    did_not_exist: DidNotExist
    direction: int
    id: int
    race_id: int
    tid: str
    track: int
    unreleased_servers: List[UnreleasedServer]
    distance: Optional[int] = None
    entries: Optional[int] = None

class Factor(UmaMusumeModel):
    effect_1: str
    effect_2: str

class BasicRace(UmaMusumeModel, LocalizedNameMixin):
    banner_id: int
    course: int
    course_id: int
    direction: int
    distance: int
    entries: int
    grade: int
    group: int
    id: int
    list_ura: List[str]
    race_id: int
    season: int
    terrain: int
    tid: str
    time: int
    track: int
    url_name: str
    factor: Optional[Factor] = None
    unreleased_servers: Optional[List[UnreleasedServer]] = None
    alts: Optional[List[Alt]] = None
    did_not_exist: Optional[DidNotExist] = None

class Corner(UmaMusumeModel):
    end: int
    number: int
    start: int

class Lap(UmaMusumeModel):
    end: int
    lap: int
    start: int

class NoMansLand(UmaMusumeModel):
    end: int
    start: int

class Phase(UmaMusumeModel):
    end: int
    id: int
    start: int

class Slope(UmaMusumeModel):
    end: int
    slope: int
    start: int

class SpurtStart(UmaMusumeModel):
    lap: int
    location: List[Location]
    meters: int

class Straight(UmaMusumeModel):
    end: float
    front_type: int
    start: int

class TerrainChange(UmaMusumeModel):
    start: int
    terrain: int

class Course(UmaMusumeModel):
    corners: List[Corner]
    distance: int
    id: int
    inout: int
    laps: List[Lap]
    length: int
    no_mans_land: List[NoMansLand]
    overlaps: List[str]
    phases: List[Phase]
    position_keep_end: int
    slopes: List[Slope]
    spurt_start: SpurtStart
    stat_thresholds: List[int]
    straights: List[Straight]
    terrain: int
    terrain_changes: List[TerrainChange]
    turn: int

class DetailedRacetrack(UmaMusumeModel):
    courses: List[Course]
    id: int

class DetailedTrackName(PagePropsModel):
    racetrack_id: int
    racetrack_url_name: str

class Race(UmaMusumeModel):
    id: int
    name_en: Optional[str] = None
    name_jp: str
    name_ko: Optional[str] = None
    name_tw: Optional[str] = None
    group: int
    grade: int
    track: int
    distance: int
    terrain: int
    fans_needed: int
    fans_gained: int
    icon_id: int
    url_name: Optional[str] = None
    unreleased_servers: Optional[List[str]] = None

class Alternative(UmaMusumeModel):
    order: int
    turn: int
    cond_type: int
    cond_id: int
    cond_value: int
    cond_value_2: int
    race_type: int
    target_type: int
    race_choice: int
    race_choice_details: int
    races: List[Race]
    turns_break: int

class ObjectiveDatum(UmaMusumeModel):
    order: int
    turn: int
    cond_type: int
    cond_id: int
    cond_value: int
    cond_value_2: int
    race_type: int
    target_type: int
    race_choice: int
    race_choice_details: int
    races: Optional[List[Race]] = None
    turns_break: Optional[int] = None
    alternatives: Optional[List[Alternative]] = None
