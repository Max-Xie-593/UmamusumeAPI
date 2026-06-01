from __future__ import annotations

from aiohttp_client_cache import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger

import asyncio
import json
import re
from collections.abc import Sequence
from typing import Final, Any, Optional, Self, TYPE_CHECKING

from .exceptions import *
from .constants import *

if TYPE_CHECKING:
    import aiohttp

from .models import *

class UmaMusumeAPI:
    """Asynchronous client for interacting with the Uma Musume Gametora Website.

    Provides methods to fetch various Uma Musume game data.

    Raises:
        RuntimeError: Runtime errors (e.g., calling endpoints before starting session)
        DataNotFoundError: Data not found errors
        ConnectionTimeoutError: Connection timeout errors
        UmaMusumeAPIError: Catch-all for other errors
    """
    
    # Replace with the actual base URL of the Uma Musume API you intend to use
    BASE_URL: Final[str] = "https://gametora.com"

    def __init__(self, *, cache_ttl: int = 3600, headers: Optional[dict[str,Any]] = None, session: Optional[aiohttp.ClientSession] = None):
        """Initializes Asynchronous client for the Uma Musume API.

        Args:
            cache_ttl (int, optional): Time-to-live for cached responses in seconds. Defaults to 3600.
            headers (Optional[dict[str,Any]], optional): Optional custom headers for HTTP requests. Defaults to None.
            session (Optional[aiohttp.ClientSession], optional): Optional existing aiohttp.ClientSession to use. Defaults to None.
        """
        self._cache_ttl = cache_ttl
        self._session = session
        self._headers = headers or {"User-Agent": "umamusume-api-py"}
        self.info: Optional[str] = None
        self.manifest: Optional[dict[str, Any]] = None
    
    async def __aenter__(self) -> Self:
        """Async context manager entry point. Starts the API session."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Async context manager exit point. Closes the API session."""
        await self.close()

    async def _request(self, endpoint: str, *, static: bool = False, use_cache: bool = True) -> dict[str,Any]:
        """Internal REST method to retrieve JSON information from the API.

        Args:
            endpoint (str): The specific API endpoint to call.
            use_cache (bool): Whether to use cached data. Defaults to True.

        Raises:
            RuntimeError: If session is not started.
            UmaMusumeAPIError: Specific API-related errors based on HTTP status codes.

        Returns:
            dict[str, Any]: Parsed JSON response.
        """
        if self._session is None:
            msg = f"Call `{self.__class__.__name__}.start()` before making requests."
            raise RuntimeError(msg)

        if endpoint == UMAMUSUME_STATIC_DIR:
            url = f"{self.BASE_URL}/{UMAMUSUME_STATIC_DIR}"
        elif static:
            if endpoint == MANIFEST_PATH:
                url = f"{self.BASE_URL}/data/{MANIFEST_PATH}/{UMAMUSUME_STATIC_DIR}.json"
            else:
                endpoint_hash = self.manifest[endpoint]
                url = f"{self.BASE_URL}/data/{UMAMUSUME_STATIC_DIR}/{endpoint}.{endpoint_hash}.json"
        else:
            if not self.info:
                raise RuntimeError("Build ID is not available. Ensure client has started.")
            # Extract the query ID from the end of the endpoint (e.g. 'characters/102202')
            query_id = endpoint.split("/")[-1]
            url = f"{self.BASE_URL}/_next/data/{self.info}/{UMAMUSUME_STATIC_DIR}/{endpoint}.json?id={query_id}"

        logger.debug(f"Requesting {url}")

        if endpoint == UMAMUSUME_STATIC_DIR:
            async with self._session.get(url) as resp:
                html = await resp.text()
                match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
                raise RuntimeError("Coud not find __NEXT_DATA__ script tag.")
        else:
            if not use_cache and isinstance(self._session, CachedSession):
                async with self._session.disabled(), self._session.get(url) as resp:
                    if resp.status != 200:
                        self._handle_error(resp.status)
                    data = await resp.json()
            else:
                async with self._session.get(url) as resp:
                    if resp.status != 200:
                        self._handle_error(resp.status)
                    data = await resp.json()

        return data

    def _handle_error(self, code: int) -> None:
        """Error handling logic for API requests.

        Args:
            code (int): HTTP Error code.

        Raises:
            DataNotFoundError: For 404 Not Found.
            ConnectionTimeoutError: For 522/524 connection timeouts.
            UmaMusumeAPIError: Catch-all for other status codes.
        """
        match code:
            case 404:
                raise DataNotFoundError
            case 522 | 524:
                raise ConnectionTimeoutError
            case _:
                raise UmaMusumeAPIError(code)

    async def start(self) -> None:
        """Initializes the internal aiohttp client session.

        Must be called before making any API requests if not using the client
        as an async context manager. Creates a CachedSession if no
        session was provided during initialization.
        """
        self._session = self._session or CachedSession(
            headers=self._headers,
            cache=SQLiteBackend(str(CACHE_PATH / "aiohttp-cache.db"), expire_after=self._cache_ttl),
        )
        # Note: You can add logic here to fetch the latest API version or data hash
        # similar to the FGO API's `fetch_latest_version()` method.
        await self.fetch_latest_version()
        await self.fetch_latest_manifest()

    async def close(self) -> None:
        """Closes the internal aiohttp client session.

        Should be called to gracefully shut down the session if not using
        the client as an async context manager.
        """
        if self._session is not None:
            await self._session.close()
    
    async def fetch_manifest(self, use_cache: bool = True) -> dict[str, str]:
        """Fetches manifest information for the current website build.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            dict[str, str]: A dictionary mapping endpoint hashes to their corresponding file names.
        """
        data = await self._request(MANIFEST_PATH,static=True,use_cache=use_cache)
        return data

    async def fetch_characters(self, use_cache: bool = True) -> Sequence[BasicCharacter]:
        """Fetches summary information for all characters.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicCharacter]: A list of BasicCharacter Objects.
        """
        data = await self._request("character-cards",static=True,use_cache=use_cache)
        # Assumes the API returns a list of character dictionaries
        return [BasicCharacter(**char) for char in data]
    
    async def fetch_character_detail(self, id: str, use_cache: bool = True) -> DetailedCharacter:
        """Fetches detailed information for a specific character by their ID.

        Args:
            id (int): The ID of the character to fetch.
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            DetailedCharacter: A DetailedCharacter object.
        """
        data = await self._request(f"characters/{id}", use_cache=use_cache)
        # Assumes the API returns a single dictionary representing the detailed character
        return DetailedCharacter(**data)

    async def fetch_skills(self, use_cache: bool = True) -> Sequence[BasicSkill]:
        """Fetches summary information for all skills.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicSkill]: A list of BasicSkill Objects.
        """
        data = await self._request("skills",static=True,use_cache=use_cache)
        return [BasicSkill(**skill) for skill in data]

    async def fetch_support_effects(self, use_cache: bool = True) -> Sequence[BasicSupportEffect]:
        """Fetches summary information for all support effects.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[SupportEffect]: A list of SupportEffect Objects.
        """
        data = await self._request("support_effects",static=True,use_cache=use_cache)
        return [BasicSupportEffect(**effect) for effect in data]

    async def fetch_support_cards(self, use_cache: bool = True) -> Sequence[BasicSupportCard]:
        """Fetches summary information for all support cards.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicSupportCard]: A list of BasicSupportCard Objects.
        """
        data = await self._request("support-cards",static=True,use_cache=use_cache)
        return [BasicSupportCard(**card) for card in data]

    async def fetch_support_card_detail(self, id: str, use_cache: bool = True) -> DetailedSupportCard:
        """Fetches detailed information for a specific support card by its ID.

        Args:
            id (str): The ID of the support card to fetch.
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            DetailedSupportCard: A DetailedSupportCard object.
        """
        data = await self._request(f"supports/{id}", use_cache=use_cache)
        # Assumes the API returns a single dictionary representing the detailed support card
        return DetailedSupportCard(**data)
    
    async def fetch_races(self, use_cache: bool = True) -> Sequence[BasicRace]:
        """Fetches summary information for all races.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicRace]: A list of BasicRace Objects.
        """
        data = await self._request("races",static=True,use_cache=use_cache)
        return [BasicRace(**race) for race in data]
    
    async def fetch_racetracks(self, use_cache: bool = True) -> Sequence[DetailedRacetrack]:
        """Fetches detailed information for all racetracks.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[DetailedRacetrack]: A list of DetailedRacetrack objects.
        """
        data = await self._request(f"racetracks",static=True,use_cache=use_cache)
        return [DetailedRacetrack(**track) for track in data]
    
    async def fetch_racetrack_detail(self, id: str, use_cache: bool = True) -> DetailedRacetrack:
        """Fetches detailed information for a specific racetrack by its ID.

        Args:
            id (str): The ID of the racetrack to fetch.
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            DetailedTrackName: A DetailedTrackName object.
        """
        data = await self._request(f"racetracks/{id}", use_cache=use_cache)
        return DetailedTrackName(**data)

    async def fetch_scenarios(self, use_cache: bool = True) -> Sequence[BasicScenario]:
        """Fetches summary information for all scenarios.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicScenario]: A list of BasicScenario Objects.
        """
        data = await self._request("scenarios",static=True,use_cache=use_cache)
        return [BasicScenario(**scenario) for scenario in data]
    
    async def fetch_status_effects(self, use_cache: bool = True) -> Sequence[BasicStatusEffect]:
        """Fetches summary information for all status effects.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicStatusEffect]: A list of BasicStatusEffect Objects.
        """
        data = await self._request("status-effects",static=True,use_cache=use_cache)
        return [BasicStatusEffect(**effect) for effect in data]

    async def fetch_items(self, use_cache: bool = True) -> Sequence[BasicItem]:
        """Fetches summary information for all items.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicItem]: A list of BasicItem Objects.
        """
        data = await self._request("items",static=True,use_cache=use_cache)
        return [BasicItem(**item) for item in data]

    async def fetch_epithets(self, use_cache: bool = True) -> Sequence[BasicEpithet]:
        """Fetches summary information for all epithets.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicEpithet]: A list of BasicEpithet Objects.
        """
        data = await self._request("nicknames",static=True,use_cache=use_cache)
        return [BasicEpithet(**epithet) for epithet in data]

    async def fetch_trainer_title(self, use_cache: bool = True) -> Sequence[BasicTrainerTitle]:
        """Fetches summary information for all trainer titles.

        Args:
            use_cache (bool, optional): Whether to use cached data if available. Defaults to True.

        Returns:
            Sequence[BasicTrainerTitle]: A list of BasicTrainerTitle Objects.
        """
        data = await self._request("trainer-titles",static=True,use_cache=use_cache)
        return [BasicTrainerTitle(**title) for title in data]

    async def _save_version(self, info: Any, output_filename: str = "info") -> None:
        """saves the version information to the cache.

        Args:
            info (Any): JSON information for the website build
        """
        CACHE_PATH.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(json.dump,info,open(f"{CACHE_PATH}/{output_filename}.json","w"),indent=4)
    
    async def _get_version(self) -> Optional[str]:
        """saves the version information to the cache.

        Returns:
            Optional[str]: build ID for the current website
        """
        try:
            data = await asyncio.to_thread(json.load,open(f"{CACHE_PATH}/info.json","r"))
            return data["buildId"]
        except (FileNotFoundError, ValueError):
            return None
        
    async def _get_manifest(self) -> Optional[dict[str,str]]:
        """saves the version information to the cache.

        Returns:
            Optional[str]: build ID for the current website
        """
        try:
            data = await asyncio.to_thread(json.load,open(f"{CACHE_PATH}/manifest.json","r"))
            return data
        except (FileNotFoundError, ValueError):
            return None

    async def fetch_latest_version(self) -> None:
        """Fetches the latest build ID hash from the website

        Returns:
            The latest build ID from the website
        """
        currentVersion = await self._get_version()
        version = await self._request(UMAMUSUME_STATIC_DIR, use_cache=False)
        hash = version["buildId"]
        self.info = hash
        if currentVersion is None or currentVersion != hash:
            logger.debug("Version not found or outdated, updating to latest version.")
            await self._save_version({ "buildId" : hash })
            currentVersion = hash
        logger.debug(f"Current build for Umamusume site: {currentVersion}")
    
    async def fetch_latest_manifest(self) -> None:
        """saves the version information to the cache.

        Args:
            info (Any): JSON information for the website build
        """
        currentVersion = await self._get_manifest()
        version = await self.fetch_manifest()
        self.manifest = version
        if currentVersion is None or currentVersion != version:
            logger.debug("Manifest not found or outdated, updating to latest version.")
            await self._save_version(version,output_filename="manifest")
        logger.debug(f"Current manifest for Umamusume site saved")
