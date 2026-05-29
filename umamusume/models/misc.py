from __future__ import annotations

from typing import List, Optional
from .base import UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin
from .enums import TEnum

class BasicStatusEffect(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    id: int
    name_en_eon: Optional[str] = None
    desc_en_eon: Optional[str] = None

class BasicItem(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    id: int
    limit: int
    type: int
    desc: Optional[str] = None
    name_en_gl: Optional[str] = None
    desc_en_gl: Optional[str] = None
    obtain: Optional[List[str]] = None
    uses: Optional[List[str]] = None
    inactive: Optional[bool] = None

class Reward(UmaMusumeModel):
    d: int
    t: TEnum
    v: str

class BasicEpithet(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    disp_order: int
    id: int
    rank: int
    name_en_gl: Optional[str] = None
    desc_en_gl: Optional[str] = None
    char: Optional[int] = None
    scenario: Optional[int] = None
    rewards: Optional[List[Reward]] = None

class BasicTrainerTitle(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    id: int
    name_zh_tw: Optional[str] = None
