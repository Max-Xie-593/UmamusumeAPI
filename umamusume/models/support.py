from __future__ import annotations

from typing import Optional, List, Union
from pydantic import Field
from .base import UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin, LocalizedTitleMixin, LocalizedReleaseMixin, PagePropsModel
from .enums import SupportCardType, Obtained, Symbol
from .event import EventData

class HintOtherClass(UmaMusumeModel):
    hint_type: int
    hint_value: int

class HintOtherLevelStats(UmaMusumeModel):
    level: int
    stats: List[HintOtherClass]

class Hints(UmaMusumeModel):
    hint_others: List[Union[HintOtherClass, HintOtherLevelStats, List[HintOtherClass]]]
    hint_skills: List[int]

class SupportCardEffect(UmaMusumeModel):
    type_: int = Field(alias="type")
    value: int
    value_1: Optional[int] = None
    value_2: Optional[int] = None
    value_3: Optional[int] = None
    value_4: Optional[int] = None

class UniqueEffect(UmaMusumeModel):
    effects: List[SupportCardEffect]
    level: int

class BasicSupportCard(UmaMusumeModel, LocalizedNameMixin, LocalizedTitleMixin, LocalizedReleaseMixin):
    id: str = Field(alias="url_name")
    char_id: int
    char_name: str
    effects: List[List[int]]
    event_skills: List[int]
    hints: Hints
    obtained: Obtained
    rarity: int
    support_id: int
    tid: str
    type_: SupportCardType = Field(alias="type")
    event_skills_en: Optional[List[int]] = None
    unique: Optional[UniqueEffect] = None
    unique_desc: Optional[str] = None

class BasicSupportEffect(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    id: int
    calc: Optional[str] = None
    name_en_eon: Optional[str] = None
    desc_en_eon: Optional[str] = None
    symbol: Optional[Symbol] = None
    inactive: Optional[bool] = None
    note: Optional[str] = None

class DetailedSupportCard(PagePropsModel):
    item_data: BasicSupportCard = Field(alias="itemData")
    event_data: EventData = Field(alias="eventData")
    profile_url_name: str = Field(alias="profileUrlName")
    is_level_dependent: bool = Field(alias="isLevelDependent")
