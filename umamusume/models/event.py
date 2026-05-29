from __future__ import annotations

from pydantic import Field, Json, field_validator
from typing import Optional, List, Union, Dict, Any
from .base import UmaMusumeModel

class EventReward(UmaMusumeModel):
    type_: str = Field(alias="t")
    value: Optional[str] = Field(default=None, alias="v")
    details: Optional[Union[int, str]] = Field(default=None, alias="d")
    is_random: Optional[bool] = Field(default=None, alias="r")

class EventChoice(UmaMusumeModel):
    option: str = Field(alias="o")
    rewards: Optional[List[EventReward]] = Field(default=None, alias="r")

class EventItem(UmaMusumeModel):
    id: Optional[int] = Field(default=None, alias="i")
    name: Optional[str] = Field(default=None, alias="n")
    choices: Optional[List[EventChoice]] = Field(default=None, alias="c")
    conditions: Optional[List[List[Union[str, int]]]] = None
    did_not_exist: Optional[str] = None

class EventDetails(UmaMusumeModel):
    with_choice: Optional[List[EventItem]] = Field(default=None, alias="wchoice")
    no_choice: Optional[List[EventItem]] = Field(default=None, alias="nochoice")
    version: Optional[List[EventItem]] = None
    outings: Optional[List[EventItem]] = None
    secret: Optional[List[EventItem]] = None
    new_year: Optional[str] = Field(default=None, alias="nyear")
    dance: Optional[List[str]] = None
    random: Optional[List[EventItem]] = None
    arrows: Optional[List[EventItem]] = None

class EventData(UmaMusumeModel):
    ja: Optional[Json[EventDetails]] = None
    ko: Optional[Json[EventDetails]] = None
    zh_tw: Optional[Json[EventDetails]] = None
    en: Optional[Json[EventDetails]] = None

    @field_validator("ja", "ko", "zh_tw", "en", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any) -> Any:
        if v == "":
            return None
        return v
