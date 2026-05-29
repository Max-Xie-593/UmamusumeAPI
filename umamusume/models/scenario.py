from __future__ import annotations

from typing import List, Optional
from .base import UmaMusumeModel, LocalizedNameMixin

class ScenarioLinkedCharacter(UmaMusumeModel, LocalizedNameMixin):
    char_id: int
    id: int
    url_name: str

class BasicScenario(UmaMusumeModel, LocalizedNameMixin):
    bg_color: str
    hard_caps: List[int]
    id: int
    order: int
    scenario_linked_characters: List[ScenarioLinkedCharacter]
    special_program: int
    start_ja: int
    stats: List[int]
    url_name: str
    name_en_old: Optional[str] = None
    name_en_full: Optional[str] = None
    start_en: Optional[int] = None
    start_ko: Optional[int] = None
    start_zh_tw: Optional[int] = None
