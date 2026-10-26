import pytest
import pytest_asyncio
from umamusume import UmaMusumeAPI

@pytest_asyncio.fixture
async def client():
    async with UmaMusumeAPI() as c:
        yield c

@pytest.mark.asyncio
async def test_fetch_characters(client: UmaMusumeAPI):
    characters = await client.fetch_characters()
    assert characters
    assert len(characters) > 0
    assert characters[0].id

@pytest.mark.asyncio
async def test_fetch_character_detail(client: UmaMusumeAPI):
    characters = await client.fetch_characters()
    assert characters
    char_id = characters[0].id
    detail = await client.fetch_character_detail(char_id)
    assert detail
    assert detail.item_data.id == char_id

    # Test specific character with empty profileData & localized schema shifts (Special Week)
    special_week = await client.fetch_character_detail("100101-special-week")
    assert special_week
    assert special_week.item_data.id == "100101-special-week"
    assert special_week.char_data.name_en or special_week.char_data.en_name

@pytest.mark.asyncio
async def test_fetch_skills(client: UmaMusumeAPI):
    skills = await client.fetch_skills()
    assert skills
    assert len(skills) > 0

@pytest.mark.asyncio
async def test_fetch_support_effects(client: UmaMusumeAPI):
    effects = await client.fetch_support_effects()
    assert effects
    assert len(effects) > 0

@pytest.mark.asyncio
async def test_fetch_support_cards(client: UmaMusumeAPI):
    cards = await client.fetch_support_cards()
    assert cards
    assert len(cards) > 0

@pytest.mark.asyncio
async def test_fetch_support_card_detail(client: UmaMusumeAPI):
    cards = await client.fetch_support_cards()
    assert cards
    card_id = cards[0].id
    detail = await client.fetch_support_card_detail(card_id)
    assert detail
    assert detail.item_data.id == card_id

@pytest.mark.asyncio
async def test_fetch_races(client: UmaMusumeAPI):
    races = await client.fetch_races()
    assert races
    assert len(races) > 0

@pytest.mark.asyncio
async def test_fetch_racetracks(client: UmaMusumeAPI):
    racetracks = await client.fetch_racetracks()
    assert racetracks
    assert len(racetracks) > 0

@pytest.mark.asyncio
async def test_fetch_racetrack_detail(client: UmaMusumeAPI):
    detail = await client.fetch_racetrack_detail("chukyo")
    assert detail
    assert detail.racetrack_url_name == "chukyo"

@pytest.mark.asyncio
async def test_fetch_scenarios(client: UmaMusumeAPI):
    scenarios = await client.fetch_scenarios()
    assert scenarios
    assert len(scenarios) > 0

@pytest.mark.asyncio
async def test_fetch_status_effects(client: UmaMusumeAPI):
    effects = await client.fetch_status_effects()
    assert effects
    assert len(effects) > 0

@pytest.mark.asyncio
async def test_fetch_items(client: UmaMusumeAPI):
    items = await client.fetch_items()
    assert items
    assert len(items) > 0

@pytest.mark.asyncio
async def test_fetch_epithets(client: UmaMusumeAPI):
    epithets = await client.fetch_epithets()
    assert epithets
    assert len(epithets) > 0

@pytest.mark.asyncio
async def test_fetch_trainer_title(client: UmaMusumeAPI):
    titles = await client.fetch_trainer_title()
    assert titles
    assert len(titles) > 0
