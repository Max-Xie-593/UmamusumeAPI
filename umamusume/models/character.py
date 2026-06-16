from __future__ import annotations

from typing import Optional, List, Union
from pydantic import Field, HttpUrl, TypeAdapter, field_validator
from datetime import datetime
from .base import UmaMusumeModel, LocalizedNameMixin, LocalizedTitleMixin, LocalizedReleaseMixin, PagePropsModel
from .enums import Aptitude, Obtained
from .skill import SkillsEvo, EvoLOCData
from .event import EventData
from .race import ObjectiveDatum

HttpUrlAdapter: TypeAdapter[HttpUrl] = TypeAdapter(HttpUrl)

class BasicCharacter(UmaMusumeModel, LocalizedNameMixin, LocalizedTitleMixin, LocalizedReleaseMixin):
    id: str = Field(alias="url_name") 
    tid: str 
    char_id: int 
    card_id: int 
    costume: int 
    rarity: int 
    version: str = Field(default="original", alias="version") 

    aptitude: List[Aptitude] = Field(alias="aptitude") 
    base_stats: List[int] = Field(alias="base_stats") 
    two_star_stats: Optional[List[int]] = Field(default=None, alias="two_star_stats") 
    three_star_stats: Optional[List[int]] = Field(default=None, alias="three_star_stats") 
    four_star_stats: List[int] = Field(alias="4_star_stats") 
    five_star_stats: List[int] = Field(alias="5_star_stats") 

    obtained: Obtained

    skills_event_en: Optional[List[int]] = None
    skills_awakening: List[int] = Field(alias="skills_awakening")
    skills_event: List[int] = Field(alias="skills_event")
    skills_evo: List[SkillsEvo] = Field(alias="skills_evo")
    skills_innate: List[int] = Field(alias="skills_innate")
    skills_unique: List[int] = Field(alias="skills_unique")
    stat_bonus: List[int] = Field(alias="stat_bonus")
    talent_group: int

class Rl(UmaMusumeModel):
    country: str
    races: int
    wins: int
    record: str
    earnings: int
    active: str
    death: Optional[datetime] = None
    earnings_other: Optional[List[List[Union[int, str]]]] = None

class ThreeSizes(UmaMusumeModel):
    b: int 
    w: int 
    h: int 

class CharData(UmaMusumeModel):
    url_name: str
    tid: str
    char_id: int
    jp_name: str
    en_name: str
    name_ko: str
    name_tw: str
    playable: bool
    active: bool
    active_ko: Optional[bool] = None
    active_zh_tw: Optional[bool] = None
    va_en: str
    va_ja: str
    va_ko: str
    va_zh_tw: str
    va_link: str
    three_sizes: ThreeSizes 
    birth_day: int
    birth_month: int
    birth_year: int
    height: int
    sex: int
    rl: Rl 
    playable_ko: Optional[bool] = None
    playable_zh_tw: Optional[bool] = None
    playable_en: Optional[bool] = None
    active_en: Optional[bool] = None
    race: Optional[Union[str, bool]] = None

    @field_validator('va_link')
    @classmethod
    def validate_va_link(cls, v: str) -> str:
        HttpUrlAdapter.validate_python(v)
        return v

class Images(UmaMusumeModel):
    uniform: bool
    racing: bool
    concept: Optional[bool] = None
    starting_future: Optional[bool] = None

class ProfileArtMeta(UmaMusumeModel):
    url_name: str
    images: Images

class ProfileEn(UmaMusumeModel):
    secrets: List[str]
    self_intro: Optional[str] = None
    tagline: Optional[str] = None
    weight: Optional[str] = None
    shoes: Optional[str] = None
    dorm: Optional[str] = None
    en_class: Optional[str] = Field(default=None, alias="class")
    ears: Optional[str] = None
    tail: Optional[str] = None
    strong: Optional[str] = None
    weak: Optional[str] = None
    family: Optional[str] = None

class ProfileData(UmaMusumeModel):
    char_id: int
    ja: ProfileEn
    ko: ProfileEn
    zh_tw: ProfileEn
    en: ProfileEn

class DetailedCharacter(PagePropsModel):
    item_data: BasicCharacter
    char_data: CharData
    profile_data: ProfileData
    profile_art_meta: ProfileArtMeta
    event_data: EventData
    objective_data: List[ObjectiveDatum]
    evo_loc_data: EvoLOCData
    is_char_card: bool
