from pydantic import BaseModel, ConfigDict, Field, AliasChoices, model_validator
from pydantic.alias_generators import to_camel
from datetime import datetime
from typing import Optional, Any, Union, List

class UmaMusumeModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True
    )

class PagePropsModel(UmaMusumeModel):
    n_ssg: bool = Field(alias="__N_SSG", default=False)

    @model_validator(mode='before')
    @classmethod
    def flatten_page_props(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'pageProps' in data:
            page_props = data.pop('pageProps')
            if isinstance(page_props, dict):
                data.update(page_props)
        return data

class LocalizedNameMixin(BaseModel):
    name_ja: Optional[str] = Field(default=None, validation_alias=AliasChoices('nameJa', 'name_ja', 'nameJp', 'name_jp', 'jpname', 'jp_name'))
    name_en: Optional[str] = Field(default=None, validation_alias=AliasChoices('nameEn', 'name_en', 'enname', 'en_name'))
    name_ko: Optional[str] = Field(default=None, validation_alias=AliasChoices('nameKo', 'name_ko'))
    name_tw: Optional[str] = Field(default=None, validation_alias=AliasChoices('nameTw', 'name_tw', 'nameZhTw', 'name_zh_tw'))

class LocalizedDescMixin(BaseModel):
    desc_ja: Optional[Union[List[str], str]] = Field(default=None, validation_alias=AliasChoices('descJa', 'desc_ja', 'descJp', 'desc_jp', 'jpdesc', 'jp_desc'))
    desc_en: Optional[Union[List[str], str]] = Field(default=None, validation_alias=AliasChoices('descEn', 'desc_en', 'endesc', 'en_desc', 'desc'))
    desc_ko: Optional[Union[List[str], str]] = Field(default=None, validation_alias=AliasChoices('descKo', 'desc_ko'))
    desc_tw: Optional[Union[List[str], str]] = Field(default=None, validation_alias=AliasChoices('descTw', 'desc_tw', 'descZhTw', 'desc_zh_tw'))

class LocalizedTitleMixin(BaseModel):
    title: Optional[str] = Field(default=None, description="Main title (often English fallback)")
    title_ja: Optional[str] = Field(default=None, validation_alias=AliasChoices('titleJa', 'title_ja', 'titleJp', 'title_jp'))
    title_en: Optional[str] = Field(default=None, validation_alias=AliasChoices('titleEn', 'title_en', 'titleEnGl', 'title_en_gl'))
    title_ko: Optional[str] = Field(default=None, validation_alias=AliasChoices('titleKo', 'title_ko'))
    title_tw: Optional[str] = Field(default=None, validation_alias=AliasChoices('titleTw', 'title_tw', 'titleZhTw', 'title_zh_tw'))

class LocalizedReleaseMixin(BaseModel):
    release_ja: Optional[datetime] = Field(default=None, validation_alias=AliasChoices('release', 'releaseJa', 'release_ja', 'releaseJp', 'release_jp'))
    release_en: Optional[datetime] = Field(default=None, validation_alias=AliasChoices('releaseEn', 'release_en'))
    release_ko: Optional[datetime] = Field(default=None, validation_alias=AliasChoices('releaseKo', 'release_ko'))
    release_tw: Optional[datetime] = Field(default=None, validation_alias=AliasChoices('releaseTw', 'release_tw', 'releaseZhTw', 'release_zh_tw'))
