from __future__ import annotations

from pydantic import Field
from typing import Optional, List, Dict, Any
from .base import UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin
from .enums import TypeElement

class SkillsEvo(UmaMusumeModel):
    new: int
    old: int

class SkillEffect(UmaMusumeModel):
    type_: int = Field(alias="type")
    value: int
    target: Optional[int] = None
    target_details: Optional[int] = None
    value_scale: Optional[int] = None
    max_procs: Optional[int] = None

class SkillConditionGroup(UmaMusumeModel):
    base_time: int
    condition: str
    effects: List[SkillEffect]
    precondition: Optional[str] = None
    cd: Optional[int] = None
    time_scale: Optional[int] = None

class Evo(UmaMusumeModel):
    evos: List[int]
    card_id: Optional[int] = None
    scenario_id: Optional[int] = None

class SkillGeneVersion(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    activation: int
    condition_groups: List[SkillConditionGroup]
    iconid: int
    id: int
    inherited: bool
    parent_skills: List[int]
    rarity: int
    tid: str
    cost: Optional[int] = None

class LocalizedGeneVersion(UmaMusumeModel):
    condition_groups: List[SkillConditionGroup]
    iconid: Optional[int] = None

class LocalizedSkill(UmaMusumeModel):
    char: Optional[List[int]] = None
    condition_groups: Optional[List[SkillConditionGroup]] = None
    gene_version: Optional[LocalizedGeneVersion] = None
    type_: Optional[List[TypeElement]] = Field(default=None, alias="type")
    char_e: Optional[List[int]] = None
    sup_e: Optional[List[List[int]]] = None
    sup_hint: Optional[List[List[int]]] = None
    iconid: Optional[int] = None

class SkillLOC(UmaMusumeModel):
    en: Optional[LocalizedSkill] = None
    ko: Optional[LocalizedSkill] = None
    zh_tw: Optional[LocalizedSkill] = None

class PreEvo(UmaMusumeModel):
    old: int
    card_id: Optional[int] = None
    scenario_id: Optional[int] = None

class BasicSkill(UmaMusumeModel, LocalizedNameMixin, LocalizedDescMixin):
    id: int
    tid: str
    rarity: int
    cost: Optional[int] = None
    type_: List[TypeElement] = Field(alias="type")
    iconid: int
    activation: int
    condition_groups: List[SkillConditionGroup]
    char: Optional[List[int]] = None
    gene_version: Optional[SkillGeneVersion] = None
    loc: Optional[SkillLOC] = None
    versions: Optional[List[int]] = None
    char_e: Optional[List[int]] = None
    sup_e: Optional[List[List[int]]] = None
    sup_hint: Optional[List[List[int]]] = None
    sce_e: Optional[List[int]] = None
    evo: Optional[List[Evo]] = None
    evo_cond: Optional[List[List[List[Any]]]] = None
    pre_evo: Optional[PreEvo] = None

class Skill(UmaMusumeModel):
    ja: List[List[str]]
    ko: Optional[List[List[str]]] = None
    zh_tw: Optional[List[List[str]]] = None

class EvoLOCData(UmaMusumeModel):
    card_id: int
    skills: Dict[str, Skill]
