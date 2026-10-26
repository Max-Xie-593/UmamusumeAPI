from __future__ import annotations

from typing import Optional, List, Union, Any
from pydantic import Field, HttpUrl, TypeAdapter, field_validator, AliasChoices
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
    country: Optional[str] = None
    races: Optional[int] = None
    wins: Optional[int] = None
    record: Optional[str] = None
    earnings: Optional[int] = None
    active: Optional[str] = None
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
    jp_name: Optional[str] = Field(default=None, validation_alias=AliasChoices('jp_name', 'jpName', 'name_ja', 'nameJa', 'name_jp', 'nameJp'))
    name_ja: Optional[str] = Field(default=None, validation_alias=AliasChoices('name_ja', 'nameJa', 'jp_name', 'jpName', 'name_jp', 'nameJp'))
    en_name: Optional[str] = Field(default=None, validation_alias=AliasChoices('en_name', 'enName', 'name_en', 'nameEn'))
    name_en: Optional[str] = Field(default=None, validation_alias=AliasChoices('name_en', 'nameEn', 'en_name', 'enName'))
    name_ko: Optional[str] = Field(default=None, validation_alias=AliasChoices('name_ko', 'nameKo'))
    name_tw: Optional[str] = Field(default=None, validation_alias=AliasChoices('name_tw', 'nameTw', 'name_zh_tw', 'nameZhTw'))
    name_zh_tw: Optional[str] = Field(default=None, validation_alias=AliasChoices('name_zh_tw', 'nameZhTw', 'name_tw', 'nameTw'))
    color_main: Optional[str] = None
    color_sub: Optional[str] = None
    playable: bool
    active: bool
    active_ko: Optional[bool] = None
    active_zh_tw: Optional[bool] = None
    va_en: Optional[str] = None
    va_ja: Optional[str] = None
    va_ko: Optional[str] = None
    va_zh_tw: Optional[str] = None
    va_link: Optional[str] = None
    three_sizes: Optional[ThreeSizes] = None 
    birth_day: Optional[int] = None
    birth_month: Optional[int] = None
    birth_year: Optional[int] = None
    height: Optional[int] = None
    sex: Optional[int] = None
    rl: Optional[Rl] = None 
    playable_ko: Optional[bool] = None
    playable_zh_tw: Optional[bool] = None
    playable_en: Optional[bool] = None
    active_en: Optional[bool] = None
    race: Optional[Union[str, bool]] = None

    @field_validator('va_link')
    @classmethod
    def validate_va_link(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
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
    secrets: Optional[List[str]] = None
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
    char_id: Optional[int] = None
    ja: Optional[ProfileEn] = None
    ko: Optional[ProfileEn] = None
    zh_tw: Optional[ProfileEn] = None
    en: Optional[ProfileEn] = None

class DetailedCharacter(PagePropsModel):
    item_data: BasicCharacter
    char_data: CharData
    profile_data: Optional[ProfileData] = None
    profile_art_meta: Optional[ProfileArtMeta] = None
    event_data: Optional[EventData] = None
    objective_data: Optional[List[ObjectiveDatum]] = None
    evo_loc_data: Optional[EvoLOCData] = None
    is_char_card: bool

    @field_validator('profile_data', mode='before')
    @classmethod
    def validate_profile_data(cls, v: Any) -> Any:
        if v == {} or v == []:
            return None
        return v
